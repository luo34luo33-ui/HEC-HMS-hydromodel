"""
产流计算模块
为未来深度学习耦合预留的产流计算接口
"""
import numpy as np
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod


class RunoffGenerationBase(ABC):
    """产流计算基类"""

    @abstractmethod
    def calculate(
        self,
        precip: np.ndarray,
        pet: np.ndarray,
        params: Dict[str, Any],
        initial_states: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        计算产流

        Args:
            precip: 降水量数组
            pet: 潜在蒸散发数组
            params: 模型参数
            initial_states: 初始状态

        Returns:
            runoff: 产流量数组
            final_states: 最终状态
        """
        pass

    @abstractmethod
    def get_required_params(self) -> list:
        """获取所需参数列表"""
        pass


class XinAnJiangRunoff(RunoffGenerationBase):
    """新安江产流模型（示例）"""

    def calculate(
        self,
        precip: np.ndarray,
        pet: np.ndarray,
        params: Dict[str, Any],
        initial_states: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        新安江模型产流计算
        
        Args:
            precip: 降水量 (mm)
            pet: 潜在蒸散发 (mm)
            params: 模型参数
                - wm: 张力水容量 (mm)
                - b: 蓄水容量曲线指数
                - imp: 不透水面积比例
                - c: 深层蒸散发系数
            initial_states: 初始状态
                - w: 初始土壤含水量 (mm)

        Returns:
            runoff: 产流量 (mm)
            final_states: 最终状态
        """
        wm = params.get('wm', 120.0)
        b = params.get('b', 0.3)
        imp = params.get('imp', 0.01)
        c = params.get('c', 0.15)

        if initial_states:
            w = initial_states.get('w', wm * 0.5)
        else:
            w = wm * 0.5

        n = len(precip)
        runoff = np.zeros(n)

        for i in range(n):
            p = precip[i]
            e = pet[i]

            # 简化的产流计算（占位实现）
            pe = max(0, p - e)
            runoff[i] = pe * (1 - imp) if pe > 0 else 0
            w = min(wm, max(0, w + p - e - runoff[i]))

        final_states = {'w': w}
        return runoff, final_states

    def get_required_params(self) -> list:
        return ['wm', 'b', 'imp', 'c']


class SimpleRunoff(RunoffGenerationBase):
    """简单产流模型（降雨-径流系数法）"""

    def calculate(
        self,
        precip: np.ndarray,
        pet: np.ndarray,
        params: Dict[str, Any],
        initial_states: Optional[Dict[str, float]] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """简单产流计算"""
        runoff_coef = params.get('runoff_coef', 0.5)
        runoff = precip * runoff_coef
        return runoff, {}

    def get_required_params(self) -> list:
        return ['runoff_coef']
