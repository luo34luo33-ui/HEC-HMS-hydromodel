"""
可视化模块
提供水文过程线、对比图等可视化功能
"""
from visualization.hydrograph import (
    plot_hydrograph,
    plot_comparison,
    plot_residuals,
    plot_precipitation_discharge
)

__all__ = [
    'plot_hydrograph',
    'plot_comparison',
    'plot_residuals',
    'plot_precipitation_discharge'
]
