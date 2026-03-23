"""
深度学习模块 - 数据适配器
为深度学习模型准备数据
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple, List
from utils.logger import get_logger

logger = get_logger(__name__)


class MLDataAdapter:
    """深度学习数据适配器"""

    def __init__(self):
        self.normalization_params = {}

    def prepare_training_data(
        self,
        precip: np.ndarray,
        pet: np.ndarray,
        discharge: np.ndarray,
        sequence_length: int = 24,
        forecast_horizon: int = 1,
        train_ratio: float = 0.8
    ) -> Dict[str, np.ndarray]:
        """
        准备训练数据

        Args:
            precip: 降水数据
            pet: 潜在蒸散发数据
            discharge: 流量数据
            sequence_length: 输入序列长度
            forecast_horizon: 预测步长
            train_ratio: 训练集比例

        Returns:
            数据字典
        """
        # 合并输入特征
        inputs = np.column_stack([precip, pet])
        targets = discharge.reshape(-1, 1)

        # 归一化
        inputs_norm, input_params = self._normalize(inputs, 'minmax')
        targets_norm, target_params = self._normalize(targets, 'minmax')

        self.normalization_params = {
            'inputs': input_params,
            'targets': target_params
        }

        # 创建序列
        X, y = self._create_sequences(inputs_norm, targets_norm, sequence_length, forecast_horizon)

        # 划分训练集和验证集
        n_train = int(len(X) * train_ratio)

        return {
            'X_train': X[:n_train],
            'y_train': y[:n_train],
            'X_val': X[n_train:],
            'y_val': y[n_train:]
        }

    def prepare_prediction_data(
        self,
        precip: np.ndarray,
        pet: np.ndarray,
        sequence_length: int = 24
    ) -> np.ndarray:
        """准备预测数据"""
        inputs = np.column_stack([precip, pet])
        inputs_norm, _ = self._normalize(inputs, 'minmax')
        return inputs_norm[-sequence_length:].reshape(1, sequence_length, -1)

    def inverse_transform_predictions(
        self,
        predictions: np.ndarray
    ) -> np.ndarray:
        """反归一化预测结果"""
        params = self.normalization_params.get('targets', {})
        if not params:
            return predictions

        min_val = params.get('min', 0)
        max_val = params.get('max', 1)
        return predictions * (max_val - min_val) + min_val

    def _normalize(
        self,
        data: np.ndarray,
        method: str = 'minmax'
    ) -> Tuple[np.ndarray, Dict[str, float]]:
        """归一化"""
        if method == 'minmax':
            min_val = np.min(data, axis=0)
            max_val = np.max(data, axis=0)
            range_val = max_val - min_val
            range_val[range_val == 0] = 1  # 避免除零
            normalized = (data - min_val) / range_val
            params = {'min': min_val, 'max': max_val}
        elif method == 'zscore':
            mean = np.mean(data, axis=0)
            std = np.std(data, axis=0)
            std[std == 0] = 1  # 避免除零
            normalized = (data - mean) / std
            params = {'mean': mean, 'std': std}
        else:
            raise ValueError(f"Unknown method: {method}")

        return normalized, params

    def _create_sequences(
        self,
        inputs: np.ndarray,
        targets: np.ndarray,
        sequence_length: int,
        forecast_horizon: int
    ) -> Tuple[np.ndarray, np.ndarray]:
        """创建序列"""
        n_samples = len(inputs) - sequence_length - forecast_horizon + 1

        X = np.zeros((n_samples, sequence_length, inputs.shape[1]))
        y = np.zeros((n_samples, forecast_horizon, targets.shape[1]))

        for i in range(n_samples):
            X[i] = inputs[i:i + sequence_length]
            y[i] = targets[i + sequence_length:i + sequence_length + forecast_horizon]

        return X, y


class FeatureExtractor:
    """特征提取器"""

    @staticmethod
    def extract_temporal_features(data: np.ndarray) -> Dict[str, np.ndarray]:
        """提取时间特征"""
        return {
            'mean': np.mean(data),
            'std': np.std(data),
            'min': np.min(data),
            'max': np.max(data),
            'range': np.max(data) - np.min(data)
        }

    @staticmethod
    def extract_hydrological_features(
        precip: np.ndarray,
        discharge: np.ndarray
    ) -> Dict[str, float]:
        """提取水文特征"""
        return {
            'total_precip': np.sum(precip),
            'total_discharge': np.sum(discharge),
            'peak_discharge': np.max(discharge),
            'runoff_coefficient': np.sum(discharge) / np.sum(precip) if np.sum(precip) > 0 else 0,
            'precip_days': np.sum(precip > 0),
            'zero_flow_days': np.sum(discharge == 0)
        }
