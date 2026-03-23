"""
汇流模块测试
"""
import sys
import os
import numpy as np

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.base import TestBase
from core.routing import (
    MuskingumRouting, LinearReservoirRouting,
    muskingum_routing, linear_reservoir
)


class TestMuskingumRouting(TestBase):
    """Muskingum汇流测试"""

    def test_basic_routing(self):
        """测试基本汇流"""
        n = 100
        inflow = self.create_test_discharge(n)

        router = MuskingumRouting()
        params = {'k': 12.0, 'x': 0.2, 'dt': 1.0}

        outflow, state = router.route(inflow, params)

        assert len(outflow) == n
        self.assert_no_nan(outflow)
        self.assert_non_negative(outflow)

    def test_with_initial_state(self):
        """测试带初始状态的汇流"""
        inflow = np.array([10.0, 20.0, 30.0, 40.0, 50.0])

        router = MuskingumRouting()
        params = {'k': 12.0, 'x': 0.2, 'dt': 1.0}

        outflow, state = router.route(inflow, params, initial_state=15.0)

        assert len(outflow) == 5
        assert outflow[0] == 15.0

    def test_conservation(self):
        """测试质量守恒（近似）"""
        inflow = np.ones(100) * 10.0

        router = MuskingumRouting()
        params = {'k': 12.0, 'x': 0.2, 'dt': 1.0}

        outflow, _ = router.route(inflow, params)

        # 稳态下入流应等于出流
        self.assert_arrays_close(outflow[-1], 10.0, rtol=0.1)


class TestLinearReservoirRouting(TestBase):
    """线性水库汇流测试"""

    def test_basic_routing(self):
        """测试基本汇流"""
        n = 100
        inflow = self.create_test_discharge(n)

        router = LinearReservoirRouting()
        params = {'k': 24.0, 'dt': 1.0}

        outflow, state = router.route(inflow, params)

        assert len(outflow) == n
        self.assert_no_nan(outflow)
        self.assert_non_negative(outflow)


class TestConvenienceFunctions(TestBase):
    """便捷函数测试"""

    def test_muskingum_function(self):
        """测试Muskingum便捷函数"""
        inflow = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
        outflow = muskingum_routing(inflow, k=12.0, x=0.2, dt=1.0)

        assert len(outflow) == 5
        self.assert_no_nan(outflow)

    def test_linear_reservoir_function(self):
        """测试线性水库便捷函数"""
        y = linear_reservoir(x=10.0, weight=0.5, last_y=8.0)
        expected = 0.5 * 10.0 + 0.5 * 8.0
        assert abs(y - expected) < 1e-10


def run_tests():
    """运行所有测试"""
    print("Running routing tests...")

    # TestMuskingumRouting
    test_musk = TestMuskingumRouting()
    test_musk.test_basic_routing()
    print("  - test_basic_routing: PASSED")

    test_musk.test_with_initial_state()
    print("  - test_with_initial_state: PASSED")

    test_musk.test_conservation()
    print("  - test_conservation: PASSED")

    # TestLinearReservoirRouting
    test_lr = TestLinearReservoirRouting()
    test_lr.test_basic_routing()
    print("  - test_basic_routing: PASSED")

    # TestConvenienceFunctions
    test_conv = TestConvenienceFunctions()
    test_conv.test_muskingum_function()
    print("  - test_muskingum_function: PASSED")

    test_conv.test_linear_reservoir_function()
    print("  - test_linear_reservoir_function: PASSED")

    print("All routing tests passed!")


if __name__ == '__main__':
    run_tests()
