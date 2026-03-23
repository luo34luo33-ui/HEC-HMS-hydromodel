"""
可视化模块
提供水文过程线、对比图等可视化功能
"""
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Optional, List
from utils.logger import get_logger

logger = get_logger(__name__)


def plot_hydrograph(
    times: np.ndarray,
    observed: np.ndarray,
    simulated: np.ndarray,
    title: str = "Hydrograph",
    save_path: Optional[str] = None
):
    """
    绘制水文过程线

    Args:
        times: 时间数组
        observed: 观测流量
        simulated: 模拟流量
        title: 图标题
        save_path: 保存路径
    """
    plt.figure(figsize=(12, 6))
    plt.plot(times, observed, 'b-', label='Observed', linewidth=1.5)
    plt.plot(times, simulated, 'r--', label='Simulated', linewidth=1.5)
    plt.xlabel('Time')
    plt.ylabel('Discharge (m³/s)')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved hydrograph to {save_path}")

    plt.close()


def plot_comparison(
    observed: np.ndarray,
    simulated: np.ndarray,
    title: str = "Observed vs Simulated",
    save_path: Optional[str] = None
):
    """
    绘制观测-模拟对比图

    Args:
        observed: 观测值
        simulated: 模拟值
        title: 图标题
        save_path: 保存路径
    """
    plt.figure(figsize=(8, 8))
    plt.scatter(observed, simulated, alpha=0.5, s=10)

    # 添加1:1线
    max_val = max(np.max(observed), np.max(simulated))
    min_val = min(np.min(observed), np.min(simulated))
    plt.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=1.5)

    plt.xlabel('Observed (m³/s)')
    plt.ylabel('Simulated (m³/s)')
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved comparison plot to {save_path}")

    plt.close()


def plot_residuals(
    times: np.ndarray,
    residuals: np.ndarray,
    title: str = "Residuals",
    save_path: Optional[str] = None
):
    """
    绘制残差图

    Args:
        times: 时间数组
        residuals: 残差
        title: 图标题
        save_path: 保存路径
    """
    plt.figure(figsize=(12, 4))
    plt.plot(times, residuals, 'g-', linewidth=1)
    plt.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    plt.xlabel('Time')
    plt.ylabel('Residual (m³/s)')
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved residual plot to {save_path}")

    plt.close()


def plot_precipitation_discharge(
    times: np.ndarray,
    precip: np.ndarray,
    discharge: np.ndarray,
    title: str = "Precipitation and Discharge",
    save_path: Optional[str] = None
):
    """
    绘制降雨-径流图

    Args:
        times: 时间数组
        precip: 降水
        discharge: 流量
        title: 图标题
        save_path: 保存路径
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # 降雨图
    ax1.bar(times, precip, color='blue', alpha=0.7)
    ax1.set_ylabel('Precipitation (mm)')
    ax1.invert_yaxis()  # 降雨向下
    ax1.grid(True, alpha=0.3)

    # 流量图
    ax2.plot(times, discharge, 'r-', linewidth=1.5)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Discharge (m³/s)')
    ax2.grid(True, alpha=0.3)

    plt.suptitle(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Saved precipitation-discharge plot to {save_path}")

    plt.close()
