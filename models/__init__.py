"""
模型封装层
提供统一的模型运行接口
"""
from models.base_model import BaseModel, SingleModel, DistributedModel, ModelFactory

__all__ = [
    'BaseModel',
    'SingleModel',
    'DistributedModel',
    'ModelFactory'
]
