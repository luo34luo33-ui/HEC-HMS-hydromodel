"""
核心计算模块
包含产流、汇流、水源划分等核心算法
"""
from core.generation import RunoffGenerationBase, XinAnJiangRunoff, SimpleRunoff
from core.routing import (
    RoutingBase, MuskingumRouting, LinearReservoirRouting,
    muskingum_routing, linear_reservoir
)
from core.source_separation import source_separation, SourceSeparationModel
from core.interfaces import (
    HydroModelInterface, DataAdapterInterface,
    EvaluatorInterface, MLModelInterface
)

__all__ = [
    # Generation
    'RunoffGenerationBase', 'XinAnJiangRunoff', 'SimpleRunoff',
    # Routing
    'RoutingBase', 'MuskingumRouting', 'LinearReservoirRouting',
    'muskingum_routing', 'linear_reservoir',
    # Source Separation
    'source_separation', 'SourceSeparationModel',
    # Interfaces
    'HydroModelInterface', 'DataAdapterInterface',
    'EvaluatorInterface', 'MLModelInterface'
]
