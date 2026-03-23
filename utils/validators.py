"""
数据验证工具模块
提供数据验证相关的工具函数
"""
import numpy as np
from typing import Optional, List, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """数据验证异常"""
    pass


def validate_non_negative(data: np.ndarray, name: str = "data") -> bool:
    """验证数据非负"""
    if np.any(data < 0):
        logger.warning(f"{name} contains negative values")
        return False
    return True


def validate_no_nan(data: np.ndarray, name: str = "data") -> bool:
    """验证数据无NaN值"""
    if np.any(np.isnan(data)):
        logger.warning(f"{name} contains NaN values")
        return False
    return True


def validate_no_inf(data: np.ndarray, name: str = "data") -> bool:
    """验证数据无Inf值"""
    if np.any(np.isinf(data)):
        logger.warning(f"{name} contains Inf values")
        return False
    return True


def validate_range(
    data: np.ndarray,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
    name: str = "data"
) -> bool:
    """验证数据范围"""
    if min_val is not None and np.any(data < min_val):
        logger.warning(f"{name} contains values below {min_val}")
        return False
    if max_val is not None and np.any(data > max_val):
        logger.warning(f"{name} contains values above {max_val}")
        return False
    return True


def validate_precipitation(precip: np.ndarray) -> bool:
    """验证降水数据"""
    valid = True
    if not validate_non_negative(precip, "precipitation"):
        valid = False
    if not validate_no_nan(precip, "precipitation"):
        valid = False
    return valid


def validate_discharge(discharge: np.ndarray) -> bool:
    """验证流量数据"""
    valid = True
    if not validate_non_negative(discharge, "discharge"):
        valid = False
    if not validate_no_nan(discharge, "discharge"):
        valid = False
    return valid


def validate_time_series_continuity(times: List) -> bool:
    """验证时间序列连续性"""
    if len(times) < 2:
        return True
    
    diffs = [times[i+1] - times[i] for i in range(len(times)-1)]
    if len(set(diffs)) > 1:
        logger.warning("Time series has inconsistent intervals")
        return False
    return True
