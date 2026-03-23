"""
模型封装层
提供统一的模型接口
"""
import os
import subprocess
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
from utils.logger import get_logger
from config import get_config, paths

logger = get_logger(__name__)


class BaseModel(ABC):
    """模型基类"""

    def __init__(self, run_name: str, run_date: str):
        self.run_name = run_name
        self.run_date = run_date
        self.run_dir = paths.get_run_dir(run_date, run_name)
        self.input_dir = paths.get_input_dir(run_date, run_name)
        self.output_dir = paths.get_output_dir(run_date, run_name)
        self.model_dir = paths.get_model_dir(run_date, run_name)

    @abstractmethod
    def initialize(self, **kwargs):
        """初始化模型"""
        pass

    @abstractmethod
    def run(self):
        """运行模型"""
        pass

    @abstractmethod
    def post_process(self):
        """后处理"""
        pass

    @abstractmethod
    def cleanup(self):
        """清理临时文件"""
        pass

    def execute(self, **kwargs):
        """执行完整流程"""
        logger.info(f"Starting model execution: {self.run_name}")
        self.initialize(**kwargs)
        self.run()
        self.post_process()
        logger.info(f"Model execution completed: {self.run_name}")


class SingleModel(BaseModel):
    """单一模型"""

    def __init__(self, run_name: str, run_date: str):
        super().__init__(run_name, run_date)
        self.base_model_path = get_config('paths.base_model_single', '2008_2_Events_Hack')

    def initialize(self, rainfall_file: str = None, init_state: bool = False, **kwargs):
        """初始化单一模型"""
        logger.info(f"Initializing single model: {self.run_name}")

        # 创建目录
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.input_dir, exist_ok=True)

        # 复制基础模型文件
        if os.path.exists(self.base_model_path):
            self._copy_tree(self.base_model_path, self.model_dir)

        # 复制降雨文件
        if rainfall_file and os.path.exists(rainfall_file):
            import shutil
            dest = os.path.join(self.input_dir, 'DailyRain.csv')
            shutil.copy2(rainfall_file, dest)

    def run(self):
        """运行HEC-HMS模型"""
        logger.info(f"Running HEC-HMS model: {self.run_name}")
        dssvue_cmd = get_config('paths.dssvue_cmd', 'dssvue/hec-dssvue.sh')

        # CSV转DSS
        csv_to_dss_cmd = f"{dssvue_cmd} csv_to_dss_util.py --date {self.run_date} --run_name {self.run_name} --model_dir {self.model_dir}"
        subprocess.call([csv_to_dss_cmd], shell=True)

        # 运行模型
        run_cmd = f"{dssvue_cmd} --run {self.model_dir}/2008_2_Events.script"
        subprocess.call([run_cmd], shell=True)

    def post_process(self):
        """后处理"""
        logger.info(f"Post-processing: {self.run_name}")
        dssvue_cmd = get_config('paths.dssvue_cmd', 'dssvue/hec-dssvue.sh')

        # DSS转CSV
        dss_to_csv_cmd = f"{dssvue_cmd} dss_to_csv_util.py --date {self.run_date} --run_name {self.run_name} --model_dir {self.model_dir}"
        subprocess.call([dss_to_csv_cmd], shell=True)

    def cleanup(self):
        """清理临时文件"""
        logger.info(f"Cleaning up: {self.run_name}")

    def _copy_tree(self, src: str, dst: str):
        """复制目录树"""
        import shutil
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


class DistributedModel(BaseModel):
    """分布式模型"""

    def __init__(self, run_name: str, run_date: str):
        super().__init__(run_name, run_date)
        self.base_model_path = get_config('paths.base_model_distributed', '2008_2_Events_Distributed')

    def initialize(self, rainfall_files: List[str] = None, init_state: bool = False, **kwargs):
        """初始化分布式模型"""
        logger.info(f"Initializing distributed model: {self.run_name}")

        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.input_dir, exist_ok=True)

        if os.path.exists(self.base_model_path):
            self._copy_tree(self.base_model_path, self.model_dir)

        if rainfall_files:
            import shutil
            for f in rainfall_files:
                if os.path.exists(f):
                    dest = os.path.join(self.input_dir, os.path.basename(f))
                    shutil.copy2(f, dest)

    def run(self):
        """运行分布式模型"""
        logger.info(f"Running distributed model: {self.run_name}")
        # 类似SingleModel的run方法
        dssvue_cmd = get_config('paths.dssvue_cmd', 'dssvue/hec-dssvue.sh')
        run_cmd = f"{dssvue_cmd} --run {self.model_dir}/2008_2_Events.script"
        subprocess.call([run_cmd], shell=True)

    def post_process(self):
        """后处理"""
        logger.info(f"Post-processing distributed model: {self.run_name}")
        dssvue_cmd = get_config('paths.dssvue_cmd', 'dssvue/hec-dssvue.sh')
        dss_to_csv_cmd = f"{dssvue_cmd} dss_to_csv_util.py --date {self.run_date} --run_name {self.run_name} --model_dir {self.model_dir}"
        subprocess.call([dss_to_csv_cmd], shell=True)

    def cleanup(self):
        """清理"""
        logger.info(f"Cleaning up: {self.run_name}")

    def _copy_tree(self, src: str, dst: str):
        """复制目录树"""
        import shutil
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)


class ModelFactory:
    """模型工厂"""

    @staticmethod
    def create(model_type: str, run_name: str, run_date: str) -> BaseModel:
        """
        创建模型实例

        Args:
            model_type: 模型类型 ('single' or 'distributed')
            run_name: 运行名称
            run_date: 运行日期

        Returns:
            模型实例
        """
        if model_type == 'single':
            return SingleModel(run_name, run_date)
        elif model_type == 'distributed':
            return DistributedModel(run_name, run_date)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
