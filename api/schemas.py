"""
API层 - 请求/响应模式定义
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class InitRequest:
    """初始化请求"""
    run_name: str
    run_datetime: str
    model_type: str = 'single'
    init_state: bool = False
    rainfall_file: Optional[str] = None


@dataclass
class RunRequest:
    """运行请求"""
    run_id: str


@dataclass
class UploadRequest:
    """上传请求"""
    run_id: str
    zip_file_name: str


@dataclass
class ModelResponse:
    """模型响应"""
    status: int
    run_id: Optional[str] = None
    description: str = ''
    data: Optional[Dict[str, Any]] = None


@dataclass
class ErrorResponse:
    """错误响应"""
    status: int
    description: str
    error_code: Optional[str] = None
