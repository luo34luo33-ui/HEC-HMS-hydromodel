"""
配置模块
提供统一的配置管理接口
"""
from config.model_config import ModelConfig, config, get_config, get_param_range
from config.paths_config import PathsConfig, paths

__all__ = [
    'ModelConfig',
    'config',
    'get_config',
    'get_param_range',
    'PathsConfig',
    'paths'
]
