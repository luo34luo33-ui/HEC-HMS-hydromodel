"""
模型参数配置模块
从JSON文件加载配置，并提供配置访问接口
"""
import os
import json
from typing import Dict, Any, Optional


# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件路径
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PARAMS_PATH = os.path.join(CONFIG_DIR, 'default_params.json')
PARAM_RANGES_PATH = os.path.join(CONFIG_DIR, 'param_ranges.json')


class ModelConfig:
    """模型配置管理类"""

    _instance = None
    _params: Dict[str, Any] = {}
    _ranges: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(DEFAULT_PARAMS_PATH):
            with open(DEFAULT_PARAMS_PATH, 'r', encoding='utf-8') as f:
                self._params = json.load(f)

        if os.path.exists(PARAM_RANGES_PATH):
            with open(PARAM_RANGES_PATH, 'r', encoding='utf-8') as f:
                self._ranges = json.load(f)

    def get_param(self, key: str, default: Any = None) -> Any:
        """获取参数值，支持点号分隔的嵌套key"""
        keys = key.split('.')
        value = self._params
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_range(self, param_name: str) -> Optional[Dict[str, float]]:
        """获取参数取值范围"""
        return self._ranges.get(param_name)

    @property
    def params(self) -> Dict[str, Any]:
        return self._params

    @property
    def ranges(self) -> Dict[str, Any]:
        return self._ranges


# 全局配置实例
config = ModelConfig()


# 便捷函数
def get_config(key: str, default: Any = None) -> Any:
    """获取配置值"""
    return config.get_param(key, default)


def get_param_range(param_name: str) -> Optional[Dict[str, float]]:
    """获取参数取值范围"""
    return config.get_range(param_name)
