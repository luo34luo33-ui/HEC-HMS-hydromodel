"""
IO工具模块
提供文件读写相关的工具函数
"""
import os
import json
import csv
from typing import Any, Dict, List, Optional
from utils.logger import get_logger

logger = get_logger(__name__)


def ensure_dir(directory: str) -> str:
    """确保目录存在，不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")
    return directory


def read_json(file_path: str) -> Dict[str, Any]:
    """读取JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: str, data: Dict[str, Any], indent: int = 2):
    """写入JSON文件"""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    logger.info(f"Wrote JSON to {file_path}")


def read_csv(file_path: str) -> List[List[str]]:
    """读取CSV文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        return list(reader)


def write_csv(file_path: str, data: List[List[Any]], header: Optional[List[str]] = None):
    """写入CSV文件"""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(data)
    logger.info(f"Wrote CSV to {file_path}")


def file_exists(file_path: str) -> bool:
    """检查文件是否存在"""
    return os.path.isfile(file_path)


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(file_path)[1].lower()
