"""
服务层 - 模型运行服务
封装模型运行的业务逻辑
"""
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from models import ModelFactory, BaseModel
from data.loader import HecDataLoader
from config import paths, get_config
from utils.logger import get_logger

logger = get_logger(__name__)


class ModelService:
    """模型服务"""

    def __init__(self):
        self.data_loader = HecDataLoader(paths.get_upload_dir())

    def init_model(
        self,
        model_type: str,
        run_name: str,
        run_datetime: str,
        rainfall_file: Optional[str] = None,
        init_state: bool = False
    ) -> Dict[str, Any]:
        """
        初始化模型

        Args:
            model_type: 模型类型 ('single' or 'distributed')
            run_name: 运行名称
            run_datetime: 运行时间
            rainfall_file: 降雨文件路径
            init_state: 是否使用初始状态

        Returns:
            运行信息字典
        """
        run_date = datetime.strptime(run_datetime, '%Y-%m-%d %H:%M:%S')
        run_date_str = run_date.strftime('%Y-%m-%d')

        # 检查运行目录是否已存在
        run_dir = paths.get_run_dir(run_date_str, run_name)
        if os.path.exists(run_dir):
            raise ValueError(f"Run {run_name} already exists for date {run_date_str}")

        # 创建模型实例
        model = ModelFactory.create(model_type, run_name, run_date_str)

        # 初始化模型
        model.initialize(rainfall_file=rainfall_file, init_state=init_state)

        # 生成运行ID
        run_id = f"HECHMS:{model_type}:{run_date_str}:{run_name}"

        logger.info(f"Model initialized: {run_id}")
        return {
            'run_id': run_id,
            'run_name': run_name,
            'run_date': run_date_str,
            'model_type': model_type
        }

    def run_model(self, run_id: str) -> Dict[str, Any]:
        """
        运行模型

        Args:
            run_id: 运行ID

        Returns:
            运行结果
        """
        # 解析run_id
        parts = self._parse_run_id(run_id)
        model_type = parts['type']
        run_date = parts['date']
        run_name = parts['name']

        # 创建并运行模型
        model = ModelFactory.create(model_type, run_name, run_date)
        model.run()
        model.post_process()

        logger.info(f"Model run completed: {run_id}")
        return {
            'run_id': run_id,
            'status': 'completed',
            'output_dir': paths.get_output_dir(run_date, run_name)
        }

    def get_run_status(self, run_id: str) -> Dict[str, Any]:
        """
        获取运行状态

        Args:
            run_id: 运行ID

        Returns:
            状态信息
        """
        parts = self._parse_run_id(run_id)
        run_date = parts['date']
        run_name = parts['name']

        output_dir = paths.get_output_dir(run_date, run_name)
        discharge_file = os.path.join(output_dir, 'DailyDischarge.csv')

        return {
            'run_id': run_id,
            'exists': os.path.exists(output_dir),
            'has_output': os.path.exists(discharge_file)
        }

    def _parse_run_id(self, run_id: str) -> Dict[str, str]:
        """解析运行ID"""
        parts = run_id.split(':')
        if len(parts) != 4:
            raise ValueError(f"Invalid run_id format: {run_id}")

        return {
            'prefix': parts[0],
            'type': parts[1],
            'date': parts[2],
            'name': parts[3]
        }


class DataService:
    """数据服务"""

    def __init__(self):
        self.data_loader = HecDataLoader(paths.get_upload_dir())

    def load_rainfall(self, run_date: str, run_name: str):
        """加载降雨数据"""
        return self.data_loader.load_rainfall(run_date, run_name)

    def load_discharge(self, run_date: str, run_name: str):
        """加载流量数据"""
        return self.data_loader.load_discharge(run_date, run_name)

    def get_available_runs(self, run_date: str) -> List[str]:
        """获取可用的运行列表"""
        date_dir = os.path.join(paths.get_upload_dir(), run_date)
        if not os.path.exists(date_dir):
            return []
        return [d for d in os.listdir(date_dir) if os.path.isdir(os.path.join(date_dir, d))]


class TaskService:
    """任务调度服务"""

    def __init__(self):
        self.model_service = ModelService()

    def execute_workflow(
        self,
        model_type: str,
        run_name: str,
        run_datetime: str,
        rainfall_file: str = None
    ) -> Dict[str, Any]:
        """
        执行完整工作流

        Args:
            model_type: 模型类型
            run_name: 运行名称
            run_datetime: 运行时间
            rainfall_file: 降雨文件

        Returns:
            执行结果
        """
        try:
            # 初始化
            init_result = self.model_service.init_model(
                model_type, run_name, run_datetime, rainfall_file
            )
            run_id = init_result['run_id']

            # 运行
            run_result = self.model_service.run_model(run_id)

            return {
                'success': True,
                'run_id': run_id,
                'result': run_result
            }
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
