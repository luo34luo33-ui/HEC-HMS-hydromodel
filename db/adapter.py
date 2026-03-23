"""
数据库模块 - 适配器
提供数据库连接和操作接口
"""
import json
import hashlib
import traceback
from typing import Dict, Any, Optional, List
import pandas as pd
from sqlalchemy import create_engine
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseAdapter:
    """数据库适配器基类"""

    def __init__(self):
        self.engine = None

    def connect(self, connection_string: str):
        """建立数据库连接"""
        self.engine = create_engine(connection_string)
        logger.info("Database connected")

    def disconnect(self):
        """断开数据库连接"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database disconnected")


class MySqlAdapter(DatabaseAdapter):
    """MySQL数据库适配器"""

    def __init__(self, config_file: str = None):
        super().__init__()
        self.config_file = config_file
        self.meta_struct = {
            'station': '',
            'variable': '',
            'unit': '',
            'type': '',
            'source': '',
            'name': ''
        }
        self.meta_struct_keys = sorted(self.meta_struct.keys())

    def load_config(self, config_file: str = None):
        """加载配置文件"""
        file_path = config_file or self.config_file
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                connection_string = 'mysql://{}:{}@{}/{}'.format(
                    config.get('MYSQL_USER', ''),
                    config.get('MYSQL_PASSWORD', ''),
                    config.get('MYSQL_HOST', 'localhost'),
                    config.get('MYSQL_DB', '')
                )
                self.connect(connection_string)
            except Exception as e:
                logger.error(f"Failed to load config: {e}")

    def get_time_series_values(
        self,
        event_id: str,
        data_from: str,
        data_to: str
    ) -> pd.DataFrame:
        """获取时间序列数据"""
        try:
            sql = "SELECT `time`,`value` FROM `data` WHERE `id`=%s AND `time`>=%s AND `time`<=%s"
            return pd.read_sql_query(sql, self.engine, params=[event_id, data_from, data_to])
        except Exception as e:
            logger.error(f"Failed to get time series: {e}")
            return pd.DataFrame()

    def save_time_series_values(self, data_frame: pd.DataFrame):
        """保存时间序列数据"""
        try:
            data_frame.to_sql(name='data', con=self.engine, if_exists='append', index=False)
        except Exception as e:
            logger.error(f"Failed to save time series: {e}")
            traceback.print_exc()

    def get_event_id(self, meta_data: Dict[str, str]) -> Optional[str]:
        """获取事件ID"""
        hash_data = {k: meta_data.get(k, '') for k in self.meta_struct_keys}
        m = hashlib.sha256()
        m.update(json.dumps(hash_data, sort_keys=True).encode("ascii"))
        possible_id = m.hexdigest()

        try:
            connection = self.engine.connect()
            result = connection.execute(
                "SELECT 1 FROM `run` WHERE `id`=%s", possible_id
            )
            if result.fetchone() is not None:
                return possible_id
        except Exception as e:
            logger.error(f"Failed to get event ID: {e}")
        return None

    def create_event_id(self, meta_data: Dict[str, str]) -> str:
        """创建事件ID"""
        hash_data = {k: meta_data.get(k, '') for k in self.meta_struct_keys}
        m = hashlib.sha256()
        m.update(json.dumps(hash_data, sort_keys=True).encode("ascii"))
        event_id = m.hexdigest()
        return event_id

    def save_init_state(self, date: str, init_data: Any):
        """保存初始状态"""
        try:
            sql = "UPDATE tbl_hec_init SET file=%s WHERE date=%s"
            self.engine.connect().execute(sql, (init_data, date))
        except Exception as e:
            logger.error(f"Failed to save init state: {e}")

    def get_init_state(self, date: str) -> Optional[Any]:
        """获取初始状态"""
        try:
            sql = "SELECT file FROM tbl_hec_init WHERE date=%s"
            result = self.engine.connect().execute(sql, (date,))
            row = result.fetchone()
            return row[0] if row else None
        except Exception as e:
            logger.error(f"Failed to get init state: {e}")
            return None
