"""
数据库模块 - 数据仓库
提供数据访问的高层接口
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import pandas as pd
from db.adapter import MySqlAdapter
from utils.logger import get_logger

logger = get_logger(__name__)


class TimeSeriesRepository:
    """时间序列数据仓库"""

    def __init__(self, adapter: MySqlAdapter):
        self.adapter = adapter

    def get_precipitation(
        self,
        station_id: str,
        start_time: str,
        end_time: str
    ) -> pd.DataFrame:
        """获取降水数据"""
        return self.adapter.get_time_series_values(station_id, start_time, end_time)

    def get_discharge(
        self,
        station_id: str,
        start_time: str,
        end_time: str
    ) -> pd.DataFrame:
        """获取流量数据"""
        return self.adapter.get_time_series_values(station_id, start_time, end_time)

    def save_results(
        self,
        run_id: str,
        data: pd.DataFrame
    ):
        """保存模型结果"""
        self.adapter.save_time_series_values(data)


class ModelStateRepository:
    """模型状态仓库"""

    def __init__(self, adapter: MySqlAdapter):
        self.adapter = adapter

    def save_state(self, date: str, state: Any):
        """保存模型状态"""
        self.adapter.save_init_state(date, state)

    def get_state(self, date: str) -> Optional[Any]:
        """获取模型状态"""
        return self.adapter.get_init_state(date)


class RunRepository:
    """运行记录仓库"""

    def __init__(self, adapter: MySqlAdapter):
        self.adapter = adapter

    def create_run(self, meta_data: Dict[str, str]) -> str:
        """创建运行记录"""
        return self.adapter.create_event_id(meta_data)

    def get_run(self, meta_data: Dict[str, str]) -> Optional[str]:
        """获取运行记录"""
        return self.adapter.get_event_id(meta_data)
