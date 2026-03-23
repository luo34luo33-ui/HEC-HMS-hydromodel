"""
数据验证模块
提供数据完整性、有效性验证
"""
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    statistics: Dict[str, Any]

    def __str__(self):
        status = "PASS" if self.is_valid else "FAIL"
        msg = f"Validation: {status}"
        if self.errors:
            msg += f"\n  Errors: {len(self.errors)}"
            for e in self.errors[:5]:
                msg += f"\n    - {e}"
        if self.warnings:
            msg += f"\n  Warnings: {len(self.warnings)}"
            for w in self.warnings[:5]:
                msg += f"\n    - {w}"
        return msg


class DataValidator:
    """数据验证器"""

    def validate_precipitation(
        self,
        data: np.ndarray,
        min_val: float = 0,
        max_val: float = 500
    ) -> ValidationResult:
        """验证降水数据"""
        errors = []
        warnings = []
        statistics = {}

        # 检查NaN
        nan_count = np.sum(np.isnan(data))
        if nan_count > 0:
            errors.append(f"Contains {nan_count} NaN values")

        # 检查负值
        neg_count = np.sum(data < 0)
        if neg_count > 0:
            errors.append(f"Contains {neg_count} negative values")

        # 检查异常高值
        high_count = np.sum(data > max_val)
        if high_count > 0:
            warnings.append(f"Contains {high_count} values > {max_val}")

        # 统计信息
        statistics = {
            'count': len(data),
            'mean': np.nanmean(data),
            'std': np.nanstd(data),
            'min': np.nanmin(data),
            'max': np.nanmax(data),
            'zero_count': np.sum(data == 0)
        }

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, statistics)

    def validate_discharge(
        self,
        data: np.ndarray,
        min_val: float = 0,
        max_val: float = 10000
    ) -> ValidationResult:
        """验证流量数据"""
        errors = []
        warnings = []
        statistics = {}

        nan_count = np.sum(np.isnan(data))
        if nan_count > 0:
            errors.append(f"Contains {nan_count} NaN values")

        neg_count = np.sum(data < 0)
        if neg_count > 0:
            errors.append(f"Contains {neg_count} negative values")

        high_count = np.sum(data > max_val)
        if high_count > 0:
            warnings.append(f"Contains {high_count} values > {max_val}")

        statistics = {
            'count': len(data),
            'mean': np.nanmean(data),
            'std': np.nanstd(data),
            'min': np.nanmin(data),
            'max': np.nanmax(data),
            'zero_count': np.sum(data == 0)
        }

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, statistics)

    def validate_time_series(
        self,
        df: pd.DataFrame,
        expected_freq: str = 'H'
    ) -> ValidationResult:
        """验证时间序列"""
        errors = []
        warnings = []
        statistics = {}

        if df.empty:
            errors.append("DataFrame is empty")
            return ValidationResult(False, errors, warnings, statistics)

        # 检查时间索引
        if not isinstance(df.index, pd.DatetimeIndex):
            errors.append("Index is not DatetimeIndex")
        else:
            # 检查时间间隔
            time_diffs = df.index.to_series().diff().dropna()
            if len(time_diffs.unique()) > 1:
                warnings.append("Inconsistent time intervals")

            statistics['start'] = df.index.min()
            statistics['end'] = df.index.max()
            statistics['duration'] = df.index.max() - df.index.min()

        statistics['rows'] = len(df)
        statistics['columns'] = len(df.columns)

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, statistics)

    def validate_model_inputs(
        self,
        inputs: Dict[str, np.ndarray]
    ) -> ValidationResult:
        """验证模型输入"""
        errors = []
        warnings = []
        statistics = {}

        required_keys = ['precip', 'pet']
        for key in required_keys:
            if key not in inputs:
                errors.append(f"Missing required input: {key}")

        if 'precip' in inputs and 'pet' in inputs:
            if len(inputs['precip']) != len(inputs['pet']):
                errors.append("precip and pet have different lengths")

        for key, data in inputs.items():
            if isinstance(data, np.ndarray):
                if np.any(np.isnan(data)):
                    warnings.append(f"{key} contains NaN values")
                if np.any(np.isinf(data)):
                    warnings.append(f"{key} contains Inf values")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, statistics)


class WaterBalanceValidator:
    """水量平衡验证器"""

    def validate(
        self,
        precip: np.ndarray,
        evap: np.ndarray,
        runoff: np.ndarray,
        delta_storage: float = 0,
        tolerance: float = 0.01
    ) -> ValidationResult:
        """
        验证水量平衡

        Args:
            precip: 降水量
            evap: 蒸散发量
            runoff: 径流量
            delta_storage: 蓄量变化
            tolerance: 容许误差比例

        Returns:
            验证结果
        """
        errors = []
        warnings = []
        statistics = {}

        p_sum = np.sum(precip)
        e_sum = np.sum(evap)
        r_sum = np.sum(runoff)

        balance = p_sum - e_sum - r_sum - delta_storage
        balance_error = abs(balance) / p_sum if p_sum > 0 else 0

        statistics = {
            'precip_sum': p_sum,
            'evap_sum': e_sum,
            'runoff_sum': r_sum,
            'delta_storage': delta_storage,
            'balance': balance,
            'balance_error': balance_error,
            'runoff_coefficient': r_sum / p_sum if p_sum > 0 else 0
        }

        if balance_error > tolerance:
            errors.append(
                f"Water balance error: {balance_error:.4f} > {tolerance}"
            )

        # 检查径流系数
        runoff_coef = r_sum / p_sum if p_sum > 0 else 0
        if runoff_coef > 1.0:
            errors.append(f"Runoff coefficient > 1.0: {runoff_coef:.4f}")
        elif runoff_coef > 0.8:
            warnings.append(f"High runoff coefficient: {runoff_coef:.4f}")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors, warnings, statistics)
