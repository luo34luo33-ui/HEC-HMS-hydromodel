"""
数据预处理模块
提供数据清洗、转换等预处理功能
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List
from utils.logger import get_logger

logger = get_logger(__name__)


class DataPreprocessor:
    """数据预处理器"""

    @staticmethod
    def fill_missing(
        data: pd.DataFrame,
        method: str = 'linear',
        limit: Optional[int] = None
    ) -> pd.DataFrame:
        """
        填充缺失值

        Args:
            data: 输入数据
            method: 填充方法 ('linear', 'ffill', 'bfill', 'mean', 'zero')
            limit: 填充限制

        Returns:
            填充后的数据
        """
        df = data.copy()

        if method == 'linear':
            df = df.interpolate(method='linear', limit=limit)
        elif method == 'ffill':
            df = df.fillna(method='ffill', limit=limit)
        elif method == 'bfill':
            df = df.fillna(method='bfill', limit=limit)
        elif method == 'mean':
            df = df.fillna(df.mean())
        elif method == 'zero':
            df = df.fillna(0)

        logger.info(f"Filled missing values using method: {method}")
        return df

    @staticmethod
    def remove_outliers(
        data: np.ndarray,
        n_std: float = 3.0
    ) -> np.ndarray:
        """
        移除异常值

        Args:
            data: 输入数据
            n_std: 标准差倍数阈值

        Returns:
            处理后的数据
        """
        mean = np.mean(data)
        std = np.std(data)
        lower = mean - n_std * std
        upper = mean + n_std * std

        result = np.clip(data, lower, upper)
        n_outliers = np.sum((data < lower) | (data > upper))
        logger.info(f"Removed {n_outliers} outliers")
        return result

    @staticmethod
    def resample(
        data: pd.DataFrame,
        target_freq: str,
        aggregation: str = 'sum'
    ) -> pd.DataFrame:
        """
        重采样时间序列数据

        Args:
            data: 输入数据
            target_freq: 目标频率 ('H', 'D', '6H', etc.)
            aggregation: 聚合方法 ('sum', 'mean', 'max', 'min')

        Returns:
            重采样后的数据
        """
        if aggregation == 'sum':
            return data.resample(target_freq).sum()
        elif aggregation == 'mean':
            return data.resample(target_freq).mean()
        elif aggregation == 'max':
            return data.resample(target_freq).max()
        elif aggregation == 'min':
            return data.resample(target_freq).min()
        else:
            raise ValueError(f"Unknown aggregation method: {aggregation}")

    @staticmethod
    def normalize(data: np.ndarray, method: str = 'minmax') -> np.ndarray:
        """
        数据归一化

        Args:
            data: 输入数据
            method: 归一化方法 ('minmax', 'zscore')

        Returns:
            归一化后的数据
        """
        if method == 'minmax':
            min_val = np.min(data)
            max_val = np.max(data)
            if max_val == min_val:
                return np.zeros_like(data)
            return (data - min_val) / (max_val - min_val)
        elif method == 'zscore':
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                return np.zeros_like(data)
            return (data - mean) / std
        else:
            raise ValueError(f"Unknown normalization method: {method}")

    @staticmethod
    def cumulative_to_incremental(cumulative: np.ndarray) -> np.ndarray:
        """累积量转增量"""
        result = np.zeros_like(cumulative)
        result[0] = cumulative[0]
        result[1:] = np.diff(cumulative)
        return np.maximum(result, 0)

    @staticmethod
    def incremental_to_cumulative(incremental: np.ndarray) -> np.ndarray:
        """增量转累积量"""
        return np.cumsum(incremental)


def prepare_model_input(
    precip: np.ndarray,
    pet: np.ndarray,
    datetime_index: Optional[pd.DatetimeIndex] = None
) -> Dict[str, Any]:
    """
    准备模型输入数据

    Args:
        precip: 降水量数组
        pet: 潜在蒸散发数组
        datetime_index: 时间索引

    Returns:
        模型输入字典
    """
    inputs = {
        'precip': np.asarray(precip, dtype=np.float64),
        'pet': np.asarray(pet, dtype=np.float64)
    }

    if datetime_index is not None:
        inputs['datetime'] = datetime_index

    return inputs


def split_train_val(
    data: Dict[str, np.ndarray],
    train_ratio: float = 0.8
) -> Tuple[Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    """
    划分训练集和验证集

    Args:
        data: 数据字典
        train_ratio: 训练集比例

    Returns:
        (train_data, val_data)
    """
    n_samples = len(next(iter(data.values())))
    n_train = int(n_samples * train_ratio)

    train_data = {k: v[:n_train] for k, v in data.items()}
    val_data = {k: v[n_train:] for k, v in data.items()}

    return train_data, val_data
