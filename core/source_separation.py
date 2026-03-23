"""
水源划分模块
将总径流划分为地表径流、壤中流、地下径流
"""
import numpy as np
from typing import Dict, Any, Tuple


def source_separation(
    pe: np.ndarray,
    r: np.ndarray,
    sm: np.ndarray,
    ex: np.ndarray,
    ki: float,
    kg: float,
    s0: float = 0.0,
    fr0: float = 0.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    水源划分

    Args:
        pe: 有效降雨量 (mm)
        r: 总产流量 (mm)
        sm: 流域平均自由水蓄量 (mm)
        ex: 自由水蓄水容量曲线指数
        ki: 壤中流出流系数
        kg: 地下水出流系数
        s0: 初始自由水蓄量 (mm)
        fr0: 初始产流面积比

    Returns:
        rs: 地表径流 (mm)
        ri: 壤中流 (mm)
        rg: 地下径流 (mm)
        s: 自由水蓄量过程
        fr: 产流面积比过程
    """
    n = len(r)
    rs = np.zeros(n)
    ri = np.zeros(n)
    rg = np.zeros(n)
    s = np.zeros(n)
    fr = np.zeros(n)

    # 自由水蓄水容量
    s_max = np.max(sm) if len(sm) > 0 else 50.0

    s[0] = s0
    fr[0] = fr0

    for i in range(n):
        if r[i] > 0:
            # 产流面积比
            if ex > 0:
                fr[i] = 1 - (1 - min(s[i] / s_max, 1)) ** ex
            else:
                fr[i] = 1 if s[i] >= s_max else 0

            # 地表径流
            if fr[i] > 0:
                rs[i] = (r[i] / fr[i]) * fr[i]

            # 自由水蓄量更新
            ds = r[i] - rs[i]
            s[i] = s[i] + ds

            # 壤中流和地下径流
            ri[i] = ki * s[i]
            rg[i] = kg * s[i]

            # 蓄量更新
            s[i] = s[i] - ri[i] - rg[i]
            s[i] = max(0, s[i])

        if i < n - 1:
            s[i+1] = s[i]
            fr[i+1] = fr[i]

    return rs, ri, rg, s, fr


class SourceSeparationModel:
    """水源划分模型类"""

    def __init__(self, ki: float, kg: float, ex: float = 1.5, s_max: float = 50.0):
        self.ki = ki
        self.kg = kg
        self.ex = ex
        self.s_max = s_max

    def separate(
        self,
        pe: np.ndarray,
        r: np.ndarray,
        initial_s: float = 0.0
    ) -> Dict[str, np.ndarray]:
        """
        执行水源划分

        Args:
            pe: 有效降雨量
            r: 总产流量
            initial_s: 初始自由水蓄量

        Returns:
            dict: 包含各水源分量的字典
        """
        rs, ri, rg, s, fr = source_separation(
            pe, r,
            sm=np.array([self.s_max]),
            ex=self.ex,
            ki=self.ki,
            kg=self.kg,
            s0=initial_s
        )

        return {
            'surface_runoff': rs,
            'interflow': ri,
            'baseflow': rg,
            'storage': s,
            'contributing_area_ratio': fr
        }

    def get_parameters(self) -> Dict[str, float]:
        """获取模型参数"""
        return {
            'ki': self.ki,
            'kg': self.kg,
            'ex': self.ex,
            's_max': self.s_max
        }

    def set_parameters(self, **kwargs):
        """设置模型参数"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
