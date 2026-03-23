"""
数学工具模块
提供常用的数学计算函数
"""
import numpy as np
from typing import Union, Tuple


ArrayLike = Union[np.ndarray, float, int]


def safe_divide(a: ArrayLike, b: ArrayLike, epsilon: float = 1e-10) -> ArrayLike:
    """安全除法，避免除零错误"""
    return a / np.maximum(b, epsilon)


def clip_value(value: ArrayLike, min_val: float = None, max_val: float = None) -> ArrayLike:
    """裁剪值到指定范围"""
    return np.clip(value, min_val, max_val)


def ensure_non_negative(value: ArrayLike) -> ArrayLike:
    """确保非负"""
    return np.maximum(value, 0)


def calculate_nse(observed: np.ndarray, simulated: np.ndarray) -> float:
    """计算纳什效率系数 (Nash-Sutcliffe Efficiency)"""
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)
    
    mean_observed = np.mean(observed)
    numerator = np.sum((observed - simulated) ** 2)
    denominator = np.sum((observed - mean_observed) ** 2)
    
    if denominator == 0:
        return 0.0
    return 1 - (numerator / denominator)


def calculate_rmse(observed: np.ndarray, simulated: np.ndarray) -> float:
    """计算均方根误差 (Root Mean Square Error)"""
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)
    return np.sqrt(np.mean((observed - simulated) ** 2))


def calculate_mae(observed: np.ndarray, simulated: np.ndarray) -> float:
    """计算平均绝对误差 (Mean Absolute Error)"""
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)
    return np.mean(np.abs(observed - simulated))


def calculate_bias(observed: np.ndarray, simulated: np.ndarray) -> float:
    """计算偏差"""
    return np.mean(simulated - observed)


def calculate_r_squared(observed: np.ndarray, simulated: np.ndarray) -> float:
    """计算决定系数 R²"""
    observed = np.asarray(observed)
    simulated = np.asarray(simulated)
    
    correlation_matrix = np.corrcoef(observed, simulated)
    correlation = correlation_matrix[0, 1]
    return correlation ** 2


def water_balance_check(
    precip: np.ndarray,
    evap: np.ndarray,
    runoff: np.ndarray,
    delta_storage: float
) -> Tuple[float, bool]:
    """水量平衡检查"""
    precip_sum = np.sum(precip)
    evap_sum = np.sum(evap)
    runoff_sum = np.sum(runoff)
    
    balance = precip_sum - evap_sum - runoff_sum - delta_storage
    is_balanced = abs(balance) < 1e-6
    
    return balance, is_balanced
