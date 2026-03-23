"""
HEC-HMS 水文模型自动化系统
主程序入口
"""
import sys
import os

# 添加项目根目录到路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from api.routes import create_app
from utils.logger import get_logger
from config import get_config

logger = get_logger(__name__)


def main():
    """主函数"""
    app = create_app()

    host = get_config('server.host', 'localhost')
    port = get_config('server.port', 8080)

    logger.info(f"Starting HEC-HMS API server on {host}:{port}")
    app.run(host, port)


if __name__ == '__main__':
    main()
