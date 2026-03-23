"""
产流模块测试
"""
import sys
import os
import numpy as np

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.base import TestBase
from core.generation import XinAnJiangRunoff, SimpleRunoff


class TestXinAnJiangRunoff(TestBase):
    """新安江产流模型测试"""

    def test_basic_calculation(self):
        """测试基本计算"""
        n = 100
        precip = self.create_test_precipitation(n)
        pet = self.create_test_pet(n)

        model = XinAnJiangRunoff()
        params = {'wm': 120.0, 'b': 0.3, 'imp': 0.01, 'c': 0.15}

        runoff, states = model.calculate(precip, pet, params)

        assert len(runoff) == n
        self.assert_no_nan(runoff)
        self.assert_non_negative(runoff)

    def test_with_initial_states(self):
        """测试带初始状态的计算"""
        n = 50
        precip = self.create_test_precipitation(n)
        pet = self.create_test_pet(n)

        model = XinAnJiangRunoff()
        params = {'wm': 120.0, 'b': 0.3, 'imp': 0.01, 'c': 0.15}
        initial_states = {'w': 60.0}

        runoff, states = model.calculate(precip, pet, params, initial_states)

        assert len(runoff) == n
        assert 'w' in states


class TestSimpleRunoff(TestBase):
    """简单产流模型测试"""

    def test_basic_calculation(self):
        """测试基本计算"""
        n = 100
        precip = self.create_test_precipitation(n)
        pet = self.create_test_pet(n)

        model = SimpleRunoff()
        params = {'runoff_coef': 0.5}

        runoff, states = model.calculate(precip, pet, params)

        assert len(runoff) == n
        self.assert_no_nan(runoff)
        self.assert_non_negative(runoff)

    def test_runoff_coefficient(self):
        """测试径流系数"""
        precip = np.array([10.0, 20.0, 30.0])
        pet = np.array([2.0, 3.0, 4.0])

        model = SimpleRunoff()
        params = {'runoff_coef': 0.6}

        runoff, _ = model.calculate(precip, pet, params)

        expected = precip * 0.6
        self.assert_arrays_close(runoff, expected)


def run_tests():
    """运行所有测试"""
    print("Running generation tests...")

    # TestXinAnJiangRunoff
    test_xaj = TestXinAnJiangRunoff()
    test_xaj.test_basic_calculation()
    print("  - test_basic_calculation: PASSED")

    test_xaj.test_with_initial_states()
    print("  - test_with_initial_states: PASSED")

    # TestSimpleRunoff
    test_simple = TestSimpleRunoff()
    test_simple.test_basic_calculation()
    print("  - test_basic_calculation: PASSED")

    test_simple.test_runoff_coefficient()
    print("  - test_runoff_coefficient: PASSED")

    print("All generation tests passed!")


if __name__ == '__main__':
    run_tests()
