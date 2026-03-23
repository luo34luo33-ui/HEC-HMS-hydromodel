"""
数据加载模块
提供统一的数据加载接口
"""
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from utils.logger import get_logger
from utils.io_utils import read_csv, read_json

logger = get_logger(__name__)


class DataLoader:
    """数据加载器"""

    @staticmethod
    def load_csv(
        file_path: str,
        datetime_col: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        加载CSV文件

        Args:
            file_path: 文件路径
            datetime_col: 日期时间列名
            **kwargs: pandas.read_csv参数

        Returns:
            DataFrame
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path, **kwargs)

        if datetime_col and datetime_col in df.columns:
            df[datetime_col] = pd.to_datetime(df[datetime_col])
            df = df.set_index(datetime_col)

        logger.info(f"Loaded CSV: {file_path}, shape: {df.shape}")
        return df

    @staticmethod
    def load_precipitation(file_path: str) -> pd.DataFrame:
        """加载降水数据"""
        df = pd.read_csv(
            file_path,
            header=None,
            names=['time', 'value_kub', 'value_klb'],
            parse_dates=['time']
        )
        df = df.set_index('time')
        logger.info(f"Loaded precipitation: {len(df)} records")
        return df

    @staticmethod
    def load_discharge(file_path: str) -> pd.DataFrame:
        """加载流量数据"""
        df = pd.read_csv(
            file_path,
            header=None,
            names=['time', 'discharge'],
            parse_dates=['time']
        )
        df = df.set_index('time')
        logger.info(f"Loaded discharge: {len(df)} records")
        return df

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """加载JSON文件"""
        return read_json(file_path)

    @staticmethod
    def to_numpy(
        df: pd.DataFrame,
        columns: Optional[List[str]] = None
    ) -> np.ndarray:
        """DataFrame转numpy数组"""
        if columns:
            return df[columns].values
        return df.values

    @staticmethod
    def create_timeseries(
        start: str,
        end: str,
        freq: str = 'H'
    ) -> pd.DatetimeIndex:
        """创建时间序列索引"""
        return pd.date_range(start=start, end=end, freq=freq)


class HecDataLoader:
    """HEC-HMS专用数据加载器"""

    def __init__(self, base_path: str):
        self.base_path = base_path

    def load_rainfall(self, run_date: str, run_name: str) -> pd.DataFrame:
        """加载降雨数据"""
        file_path = os.path.join(
            self.base_path, run_date, run_name, 'input/DailyRain.csv'
        )
        return DataLoader.load_precipitation(file_path)

    def load_discharge(self, run_date: str, run_name: str) -> pd.DataFrame:
        """加载流量数据"""
        file_path = os.path.join(
            self.base_path, run_date, run_name, 'output/DailyDischarge.csv'
        )
        return DataLoader.load_discharge(file_path)

    def load_model_config(self, run_date: str, run_name: str) -> Dict[str, Any]:
        """加载模型配置"""
        control_file = os.path.join(
            self.base_path, run_date, run_name, '2008_2_Events/Control_1.control'
        )
        run_file = os.path.join(
            self.base_path, run_date, run_name, '2008_2_Events/2008_2_Events.run'
        )

        config = {
            'control_file': control_file,
            'run_file': run_file
        }
        return config
