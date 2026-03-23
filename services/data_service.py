"""
服务层 - 数据服务
封装数据访问的业务逻辑
"""
import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from data.loader import DataLoader, HecDataLoader
from data.preprocessor import DataPreprocessor
from data.validator import DataValidator
from config import paths
from utils.logger import get_logger

logger = get_logger(__name__)


class DataService:
    """数据服务"""

    def __init__(self):
        self.data_loader = HecDataLoader(paths.get_upload_dir())
        self.preprocessor = DataPreprocessor()
        self.validator = DataValidator()

    def load_and_validate_precipitation(
        self,
        run_date: str,
        run_name: str
    ) -> Dict[str, Any]:
        """加载并验证降水数据"""
        try:
            df = self.data_loader.load_rainfall(run_date, run_name)
            result = self.validator.validate_precipitation(df.values.flatten())
            return {
                'success': True,
                'data': df,
                'validation': result
            }
        except Exception as e:
            logger.error(f"Failed to load precipitation: {e}")
            return {'success': False, 'error': str(e)}

    def load_and_validate_discharge(
        self,
        run_date: str,
        run_name: str
    ) -> Dict[str, Any]:
        """加载并验证流量数据"""
        try:
            df = self.data_loader.load_discharge(run_date, run_name)
            result = self.validator.validate_discharge(df.values.flatten())
            return {
                'success': True,
                'data': df,
                'validation': result
            }
        except Exception as e:
            logger.error(f"Failed to load discharge: {e}")
            return {'success': False, 'error': str(e)}

    def prepare_training_data(
        self,
        precip: np.ndarray,
        discharge: np.ndarray,
        sequence_length: int = 24,
        train_ratio: float = 0.8
    ) -> Dict[str, np.ndarray]:
        """
        准备训练数据（为深度学习预留）

        Args:
            precip: 降水数据
            discharge: 流量数据
            sequence_length: 序列长度
            train_ratio: 训练集比例

        Returns:
            训练数据字典
        """
        n_samples = len(precip)
        n_train = int(n_samples * train_ratio)

        return {
            'train_precip': precip[:n_train],
            'train_discharge': discharge[:n_train],
            'val_precip': precip[n_train:],
            'val_discharge': discharge[n_train:],
            'sequence_length': sequence_length
        }

    def get_available_dates(self) -> List[str]:
        """获取可用的数据日期"""
        upload_dir = paths.get_upload_dir()
        if not os.path.exists(upload_dir):
            return []

        dates = []
        for item in os.listdir(upload_dir):
            if os.path.isdir(os.path.join(upload_dir, item)):
                try:
                    pd.to_datetime(item)
                    dates.append(item)
                except:
                    pass

        return sorted(dates)
