"""
工具模块
提供日志、IO、数学、验证等通用工具
"""
from utils.logger import Logger, get_logger
from utils.io_utils import (
    ensure_dir, read_json, write_json,
    read_csv, write_csv, file_exists, get_file_extension
)
from utils.math_utils import (
    safe_divide, clip_value, ensure_non_negative,
    calculate_nse, calculate_rmse, calculate_mae,
    calculate_bias, calculate_r_squared, water_balance_check
)
from utils.validators import (
    ValidationError, validate_non_negative, validate_no_nan,
    validate_no_inf, validate_range, validate_precipitation,
    validate_discharge, validate_time_series_continuity
)

__all__ = [
    # Logger
    'Logger', 'get_logger',
    # IO
    'ensure_dir', 'read_json', 'write_json',
    'read_csv', 'write_csv', 'file_exists', 'get_file_extension',
    # Math
    'safe_divide', 'clip_value', 'ensure_non_negative',
    'calculate_nse', 'calculate_rmse', 'calculate_mae',
    'calculate_bias', 'calculate_r_squared', 'water_balance_check',
    # Validators
    'ValidationError', 'validate_non_negative', 'validate_no_nan',
    'validate_no_inf', 'validate_range', 'validate_precipitation',
    'validate_discharge', 'validate_time_series_continuity'
]
