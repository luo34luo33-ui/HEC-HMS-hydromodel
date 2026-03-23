"""
核心模块接口
定义水文模型的抽象接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List
import numpy as np


class HydroModelInterface(ABC):
    """水文模型接口基类"""

    @abstractmethod
    def run(
        self,
        inputs: Dict[str, np.ndarray],
        params: Dict[str, Any],
        initial_states: Optional[Dict[str, Any]] = None
    ) -> Dict[str, np.ndarray]:
        """
        运行模型

        Args:
            inputs: 输入数据字典
                - precip: 降水量
                - pet: 潜在蒸散发
            params: 模型参数
            initial_states: 初始状态

        Returns:
            outputs: 输出数据字典
                - runoff: 径流量
                - discharge: 流量
        """
        pass

    @abstractmethod
    def calibrate(
        self,
        observed: np.ndarray,
        inputs: Dict[str, np.ndarray],
        param_ranges: Dict[str, Tuple[float, float]],
        algorithm: str = 'SCE-UA',
        **kwargs
    ) -> Dict[str, Any]:
        """
        参数率定

        Args:
            observed: 观测数据
            inputs: 输入数据
            param_ranges: 参数范围
            algorithm: 优化算法

        Returns:
            result: 率定结果
        """
        pass

    @abstractmethod
    def get_params_info(self) -> Dict[str, Dict[str, Any]]:
        """获取参数信息"""
        pass

    @abstractmethod
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数有效性"""
        pass


class DataAdapterInterface(ABC):
    """数据适配器接口"""

    @abstractmethod
    def load(self, path: str) -> Dict[str, Any]:
        """加载数据"""
        pass

    @abstractmethod
    def save(self, data: Dict[str, Any], path: str):
        """保存数据"""
        pass

    @abstractmethod
    def to_model_format(self, raw_data: Any) -> Dict[str, np.ndarray]:
        """转换为模型格式"""
        pass

    @abstractmethod
    def from_model_format(self, model_output: Dict[str, np.ndarray]) -> Any:
        """从模型格式转换"""
        pass


class EvaluatorInterface(ABC):
    """模型评估接口"""

    @abstractmethod
    def calculate_metrics(
        self,
        observed: np.ndarray,
        simulated: np.ndarray
    ) -> Dict[str, float]:
        """计算评估指标"""
        pass

    @abstractmethod
    def generate_report(
        self,
        observed: np.ndarray,
        simulated: np.ndarray,
        output_path: Optional[str] = None
    ) -> str:
        """生成评估报告"""
        pass


class MLModelInterface(ABC):
    """深度学习模型接口（预留）"""

    @abstractmethod
    def build_model(self, input_shape: Tuple, **kwargs):
        """构建模型"""
        pass

    @abstractmethod
    def train(
        self,
        train_data: Dict[str, np.ndarray],
        val_data: Optional[Dict[str, np.ndarray]] = None,
        **kwargs
    ):
        """训练模型"""
        pass

    @abstractmethod
    def predict(self, inputs: np.ndarray) -> np.ndarray:
        """预测"""
        pass

    @abstractmethod
    def save_model(self, path: str):
        """保存模型"""
        pass

    @abstractmethod
    def load_model(self, path: str):
        """加载模型"""
        pass
