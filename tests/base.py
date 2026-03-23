"""
测试框架
提供单元测试和集成测试基础
"""
import os
import sys
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


class TestBase:
    """测试基类"""

    @staticmethod
    def create_test_precipitation(n: int = 100) -> np.ndarray:
        """创建测试降水数据"""
        np.random.seed(42)
        return np.random.exponential(scale=5.0, size=n)

    @staticmethod
    def create_test_discharge(n: int = 100) -> np.ndarray:
        """创建测试流量数据"""
        np.random.seed(42)
        return np.random.exponential(scale=50.0, size=n)

    @staticmethod
    def create_test_pet(n: int = 100) -> np.ndarray:
        """创建测试潜在蒸散发数据"""
        np.random.seed(42)
        return np.random.uniform(1.0, 5.0, size=n)

    @staticmethod
    def create_test_dataframe(n: int = 100) -> pd.DataFrame:
        """创建测试DataFrame"""
        np.random.seed(42)
        times = pd.date_range('2020-01-01', periods=n, freq='H')
        return pd.DataFrame({
            'precip': np.random.exponential(5.0, n),
            'pet': np.random.uniform(1.0, 5.0, n),
            'discharge': np.random.exponential(50.0, n)
        }, index=times)

    @staticmethod
    def assert_arrays_close(
        a: np.ndarray,
        b: np.ndarray,
        rtol: float = 1e-5,
        atol: float = 1e-8
    ):
        """断言数组近似相等"""
        np.testing.assert_allclose(a, b, rtol=rtol, atol=atol)

    @staticmethod
    def assert_no_nan(data: np.ndarray):
        """断言无NaN值"""
        assert not np.any(np.isnan(data)), "Array contains NaN values"

    @staticmethod
    def assert_non_negative(data: np.ndarray):
        """断言非负"""
        assert np.all(data >= 0), "Array contains negative values"


class MockDataLoader:
    """模拟数据加载器"""

    @staticmethod
    def load_precipitation(file_path: str) -> pd.DataFrame:
        """模拟加载降水数据"""
        n = 100
        times = pd.date_range('2020-01-01', periods=n, freq='H')
        np.random.seed(42)
        return pd.DataFrame({
            'value_kub': np.random.exponential(5.0, n),
            'value_klb': np.random.exponential(5.0, n)
        }, index=times)

    @staticmethod
    def load_discharge(file_path: str) -> pd.DataFrame:
        """模拟加载流量数据"""
        n = 100
        times = pd.date_range('2020-01-01', periods=n, freq='H')
        np.random.seed(42)
        return pd.DataFrame({
            'discharge': np.random.exponential(50.0, n)
        }, index=times)
