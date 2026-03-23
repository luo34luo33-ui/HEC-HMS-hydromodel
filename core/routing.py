"""
汇流计算模块
提供各种汇流计算方法
"""
import numpy as np
from typing import Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod


class RoutingBase(ABC):
    """汇流计算基类"""

    @abstractmethod
    def route(
        self,
        inflow: np.ndarray,
        params: Dict[str, Any],
        initial_state: Optional[float] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        汇流计算

        Args:
            inflow: 入流数组
            params: 模型参数
            initial_state: 初始状态

        Returns:
            outflow: 出流数组
            final_state: 最终状态
        """
        pass


class MuskingumRouting(RoutingBase):
    """Muskingum河道演算法"""

    def route(
        self,
        inflow: np.ndarray,
        params: Dict[str, Any],
        initial_state: Optional[float] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Muskingum河道演算

        Args:
            inflow: 入流数组 (m³/s)
            params: 模型参数
                - k: 蓄量常数 (hours)
                - x: 权重因子 (0-0.5)
                - dt: 时间步长 (hours)
            initial_state: 初始出流量

        Returns:
            outflow: 出流数组
            final_state: 最终出流量
        """
        k = params.get('k', 12.0)  # 蓄量常数
        x = params.get('x', 0.2)   # 权重因子
        dt = params.get('dt', 1.0) # 时间步长

        # 计算Muskingum系数
        denominator = 2 * k * (1 - x) + dt
        c1 = (dt - 2 * k * x) / denominator
        c2 = (dt + 2 * k * x) / denominator
        c3 = (2 * k * (1 - x) - dt) / denominator

        n = len(inflow)
        outflow = np.zeros(n)

        # 初始条件
        if initial_state is not None:
            outflow[0] = initial_state
        else:
            outflow[0] = inflow[0]

        # Muskingum递推计算
        for i in range(1, n):
            outflow[i] = c1 * inflow[i] + c2 * inflow[i-1] + c3 * outflow[i-1]
            outflow[i] = max(0, outflow[i])  # 确保非负

        return outflow, {'final_outflow': outflow[-1]}


class LinearReservoirRouting(RoutingBase):
    """线性水库调蓄法"""

    def route(
        self,
        inflow: np.ndarray,
        params: Dict[str, Any],
        initial_state: Optional[float] = None
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        线性水库调蓄

        Args:
            inflow: 入流数组
            params: 模型参数
                - k: 水库蓄量常数
                - dt: 时间步长
            initial_state: 初始蓄水量

        Returns:
            outflow: 出流数组
            final_state: 最终蓄水量
        """
        k = params.get('k', 24.0)
        dt = params.get('dt', 1.0)

        if initial_state is not None:
            s = initial_state
        else:
            s = inflow[0] * k

        n = len(inflow)
        outflow = np.zeros(n)

        for i in range(n):
            # 蓄量方程: dS/dt = I - O, O = S/k
            s = s + (inflow[i] - s/k) * dt
            outflow[i] = s / k
            outflow[i] = max(0, outflow[i])

        return outflow, {'final_storage': s}


def muskingum_routing(inflow: np.ndarray, k: float, x: float, dt: float) -> np.ndarray:
    """
    Muskingum河道演算（便捷函数）

    Args:
        inflow: 入流数组
        k: 蓄量常数
        x: 权重因子
        dt: 时间步长

    Returns:
        outflow: 出流数组
    """
    router = MuskingumRouting()
    outflow, _ = router.route(inflow, {'k': k, 'x': x, 'dt': dt})
    return outflow


def linear_reservoir(x: float, weight: float, last_y: float) -> float:
    """
    线性水库单步计算

    Args:
        x: 当前入流
        weight: 权重系数
        last_y: 上一步出流

    Returns:
        y: 当前出流
    """
    return weight * x + (1 - weight) * last_y
