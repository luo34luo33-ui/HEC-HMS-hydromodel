"""
CSV格式处理器
处理CSV格式的数据读写
"""
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from utils.logger import get_logger
from utils.io_utils import ensure_dir

logger = get_logger(__name__)


class CsvFormatter:
    """CSV格式处理器"""

    @staticmethod
    def read_precipitation(
        file_path: str,
        locations: List[str] = None
    ) -> pd.DataFrame:
        """
        读取降水CSV文件

        Args:
            file_path: 文件路径
            locations: 站点名称列表

        Returns:
            降水数据DataFrame
        """
        if locations is None:
            locations = ['Awissawella', 'Colombo']

        df = pd.read_csv(
            file_path,
            header=None,
            names=['time'] + [f'value_{loc.lower()}' for loc in locations],
            parse_dates=['time']
        )
        df = df.set_index('time')
        logger.info(f"Read precipitation: {len(df)} records from {file_path}")
        return df

    @staticmethod
    def write_precipitation(
        data: pd.DataFrame,
        file_path: str,
        columns: List[str] = None
    ):
        """
        写入降水CSV文件

        Args:
            data: 降水数据
            file_path: 输出路径
            columns: 输出列名
        """
        ensure_dir(os.path.dirname(file_path))

        if columns:
            data = data[columns]

        data.to_csv(
            file_path,
            encoding='utf-8',
            header=False,
            index=True
        )
        logger.info(f"Wrote precipitation: {len(data)} records to {file_path}")

    @staticmethod
    def read_discharge(file_path: str) -> pd.DataFrame:
        """读取流量CSV文件"""
        df = pd.read_csv(
            file_path,
            header=None,
            names=['time', 'discharge'],
            parse_dates=['time']
        )
        df = df.set_index('time')
        logger.info(f"Read discharge: {len(df)} records from {file_path}")
        return df

    @staticmethod
    def write_discharge(data: pd.DataFrame, file_path: str):
        """写入流量CSV文件"""
        ensure_dir(os.path.dirname(file_path))
        data.to_csv(
            file_path,
            encoding='utf-8',
            header=False,
            index=True
        )
        logger.info(f"Wrote discharge: {len(data)} records to {file_path}")

    @staticmethod
    def create_hourly_rainfall(
        start_time: str,
        values: List[float],
        location_id: str = 'Location'
    ) -> pd.DataFrame:
        """创建小时降雨数据"""
        times = pd.date_range(start=start_time, periods=len(values), freq='H')
        df = pd.DataFrame({location_id: values}, index=times)
        return df

    @staticmethod
    def to_model_format(
        df: pd.DataFrame,
        value_columns: List[str]
    ) -> np.ndarray:
        """转换为模型输入格式"""
        return df[value_columns].values

    @staticmethod
    def from_model_format(
        times: pd.DatetimeIndex,
        values: np.ndarray,
        column_names: List[str]
    ) -> pd.DataFrame:
        """从模型输出格式转换"""
        if values.ndim == 1:
            return pd.DataFrame({column_names[0]: values}, index=times)
        return pd.DataFrame(values, index=times, columns=column_names)
