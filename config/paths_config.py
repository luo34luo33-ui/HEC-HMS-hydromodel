"""
路径配置模块
统一管理项目中使用的各种路径
"""
import os
from config.model_config import PROJECT_ROOT, get_config


class PathsConfig:
    """路径配置管理"""

    # 项目目录
    PROJECT_ROOT = PROJECT_ROOT

    # 数据目录
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

    # 模型目录
    CORE_DIR = os.path.join(PROJECT_ROOT, 'core')

    # 测试目录
    TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')

    # 示例数据目录
    EXAMPLE_DATA_DIR = os.path.join(PROJECT_ROOT, 'example_data')

    # 文档目录
    DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

    # 原始代码备份目录
    LEGACY_DIR = os.path.join(PROJECT_ROOT, 'legacy')

    @staticmethod
    def get_upload_dir() -> str:
        """获取上传目录"""
        return get_config('paths.upload_dir', '/home/uwcc-admin/udp_150/hec-hms')

    @staticmethod
    def get_base_model_single() -> str:
        """获取单一模型基础目录"""
        return get_config('paths.base_model_single', '2008_2_Events_Hack')

    @staticmethod
    def get_base_model_distributed() -> str:
        """获取分布式模型基础目录"""
        return get_config('paths.base_model_distributed', '2008_2_Events_Distributed')

    @staticmethod
    def get_run_dir(run_date: str, run_name: str) -> str:
        """获取运行目录"""
        upload_dir = PathsConfig.get_upload_dir()
        return os.path.join(upload_dir, run_date, run_name)

    @staticmethod
    def get_input_dir(run_date: str, run_name: str) -> str:
        """获取输入目录"""
        return os.path.join(PathsConfig.get_run_dir(run_date, run_name), 'input')

    @staticmethod
    def get_output_dir(run_date: str, run_name: str) -> str:
        """获取输出目录"""
        return os.path.join(PathsConfig.get_run_dir(run_date, run_name), 'output')

    @staticmethod
    def get_model_dir(run_date: str, run_name: str) -> str:
        """获取模型运行目录"""
        return os.path.join(PathsConfig.get_run_dir(run_date, run_name), '2008_2_Events')


# 全局路径实例
paths = PathsConfig()
