"""
深度学习模块 - 接口
为深度学习耦合预留的接口
"""
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List
from utils.logger import get_logger

logger = get_logger(__name__)


class DeepLearningInterface(ABC):
    """深度学习模型接口"""

    @abstractmethod
    def build_model(self, input_shape: Tuple, output_shape: Tuple, **kwargs):
        """
        构建模型

        Args:
            input_shape: 输入形状 (n_timesteps, n_features)
            output_shape: 输出形状 (n_timesteps, n_outputs)
            **kwargs: 其他参数
        """
        pass

    @abstractmethod
    def train(
        self,
        train_inputs: np.ndarray,
        train_targets: np.ndarray,
        val_inputs: Optional[np.ndarray] = None,
        val_targets: Optional[np.ndarray] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        训练模型

        Args:
            train_inputs: 训练输入
            train_targets: 训练目标
            val_inputs: 验证输入
            val_targets: 验证目标
            **kwargs: 训练参数

        Returns:
            训练历史
        """
        pass

    @abstractmethod
    def predict(self, inputs: np.ndarray) -> np.ndarray:
        """
        预测

        Args:
            inputs: 输入数据

        Returns:
            预测结果
        """
        pass

    @abstractmethod
    def save_model(self, path: str):
        """保存模型"""
        pass

    @abstractmethod
    def load_model(self, path: str):
        """加载模型"""
        pass


class HydroDataTransformer:
    """水文数据转换器（为深度学习准备数据）"""

    @staticmethod
    def create_sequences(
        data: np.ndarray,
        sequence_length: int,
        forecast_horizon: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        创建序列数据

        Args:
            data: 原始数据
            sequence_length: 输入序列长度
            forecast_horizon: 预测步长

        Returns:
            (inputs, targets)
        """
        n_samples = len(data) - sequence_length - forecast_horizon + 1
        if n_samples <= 0:
            raise ValueError("Data too short for given sequence_length and forecast_horizon")

        inputs = np.zeros((n_samples, sequence_length, data.shape[1] if data.ndim > 1 else 1))
        targets = np.zeros((n_samples, forecast_horizon))

        for i in range(n_samples):
            if data.ndim > 1:
                inputs[i] = data[i:i + sequence_length]
                targets[i] = data[i + sequence_length:i + sequence_length + forecast_horizon, 0]
            else:
                inputs[i, :, 0] = data[i:i + sequence_length]
                targets[i] = data[i + sequence_length:i + sequence_length + forecast_horizon]

        return inputs, targets

    @staticmethod
    def normalize_data(
        data: np.ndarray,
        method: str = 'minmax'
    ) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        归一化数据

        Args:
            data: 原始数据
            method: 归一化方法

        Returns:
            (normalized_data, normalization_params)
        """
        if method == 'minmax':
            min_val = np.min(data)
            max_val = np.max(data)
            if max_val == min_val:
                normalized = np.zeros_like(data)
            else:
                normalized = (data - min_val) / (max_val - min_val)
            params = {'min': min_val, 'max': max_val}
        elif method == 'zscore':
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                normalized = np.zeros_like(data)
            else:
                normalized = (data - mean) / std
            params = {'mean': mean, 'std': std}
        else:
            raise ValueError(f"Unknown method: {method}")

        return normalized, params

    @staticmethod
    def denormalize_data(
        data: np.ndarray,
        params: Dict[str, float],
        method: str = 'minmax'
    ) -> np.ndarray:
        """反归一化"""
        if method == 'minmax':
            min_val = params['min']
            max_val = params['max']
            return data * (max_val - min_val) + min_val
        elif method == 'zscore':
            mean = params['mean']
            std = params['std']
            return data * std + mean
        else:
            raise ValueError(f"Unknown method: {method}")


class ModelEnsemble:
    """模型集成（预留）"""

    def __init__(self):
        self.models = []
        self.weights = []

    def add_model(self, model: DeepLearningInterface, weight: float = 1.0):
        """添加模型"""
        self.models.append(model)
        self.weights.append(weight)

    def predict(self, inputs: np.ndarray) -> np.ndarray:
        """集成预测"""
        if not self.models:
            raise ValueError("No models in ensemble")

        predictions = []
        for model in self.models:
            pred = model.predict(inputs)
            predictions.append(pred)

        # 加权平均
        weights = np.array(self.weights) / np.sum(self.weights)
        result = np.zeros_like(predictions[0])
        for pred, w in zip(predictions, weights):
            result += pred * w

        return result
