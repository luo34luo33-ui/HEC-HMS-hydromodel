# HEC-HMS 水文模型自动化系统

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

本项目提供 HEC-HMS（Hydrologic Engineering Center - Hydrologic Modeling System）水文模型的自动化运行和管理接口，支持单一模型和分布式模型的配置、运行及结果处理。

## 特性

- **模块化架构**: 清晰的模块划分，易于维护和扩展
- **配置外部化**: 参数配置与代码分离，便于调整
- **REST API**: 基于 Flask 的 Web 服务接口
- **深度学习预留**: 标准化数据接口，便于耦合深度学习模型
- **完整测试**: 单元测试和集成测试框架

## 项目结构

```
HEC-HMS-hydromodel/
│
├── config/                    # 配置模块
│   ├── model_config.py       # 模型参数配置
│   ├── paths_config.py       # 路径配置
│   ├── default_params.json   # 默认参数
│   └── param_ranges.json     # 参数范围
│
├── core/                      # 核心算法模块
│   ├── generation.py         # 产流计算
│   ├── routing.py            # 汇流计算
│   ├── source_separation.py  # 水源划分
│   └── interfaces.py         # 模型接口抽象
│
├── data/                      # 数据处理模块
│   ├── loader.py             # 数据加载
│   ├── preprocessor.py       # 数据预处理
│   ├── validator.py          # 数据验证
│   └── formatters/           # 格式转换(CSV/DSS)
│
├── models/                    # 模型封装层
│   └── base_model.py         # 单一/分布式模型
│
├── api/                       # API层
│   ├── routes.py             # Flask路由
│   └── schemas.py            # 请求/响应模式
│
├── services/                  # 服务层
│   ├── model_service.py      # 模型运行服务
│   └── data_service.py       # 数据处理服务
│
├── db/                        # 数据库模块
│   ├── adapter.py            # 数据库适配器
│   └── repositories.py       # 数据仓库
│
├── ml/                        # 深度学习模块（预留）
│   ├── interfaces.py         # DL接口
│   └── data_adapter.py       # 数据适配器
│
├── utils/                     # 工具模块
│   ├── logger.py             # 日志系统
│   ├── io_utils.py           # IO工具
│   ├── math_utils.py         # 数学工具
│   └── validators.py         # 数据验证
│
├── visualization/             # 可视化模块
│   └── hydrograph.py         # 水文过程线
│
├── tests/                     # 测试模块
│   ├── base.py               # 测试基类
│   └── unit/                 # 单元测试
│
├── legacy/                    # 原代码备份
├── main.py                    # 主程序入口
├── requirements.txt           # 依赖清单
├── setup.py                   # 安装脚本
└── ARCHITECTURE_GUIDE.md      # 架构规范
```

## 模型结构

### 单一模型（Single Basin Model）
单一模型结构基于 Kelani Upper Basin（Kelani 上游流域），包含以下组件：
- **Control 文件** (`Control_1.control`): 定义模型时间步长、控制间隔等运行参数
- **Run 文件** (`2008_2_Events.run`): 配置模型运行序列、状态保存/读取设置
- **Gage 文件** (`2008_2_Events.gage`): 雨量站数据配置
- **Basin States**: 流域初始状态文件

### 分布式模型（Distributed Basin Model）
分布式模型支持多个子流域的并行计算，基于 Kelani Basin 整体流域：
- **上游流域 (KUB)**: Kelani Upper Basin
- **下游流域 (KLB)**: Kelani Lower Basin

## 核心模块说明

### 配置模块 (`config/`)
- `model_config.py`: 统一的参数配置管理，支持嵌套配置
- `paths_config.py`: 项目路径管理
- `default_params.json`: 默认参数值

### 核心算法 (`core/`)
- `generation.py`: 产流计算（新安江模型等）
- `routing.py`: 汇流计算（Muskingum、线性水库）
- `source_separation.py`: 水源划分（地表径流、壤中流、地下径流）
- `interfaces.py`: 标准化模型接口定义

### 数据处理 (`data/`)
- `loader.py`: CSV、JSON 等格式数据加载
- `preprocessor.py`: 缺失值填充、异常值处理、数据归一化
- `validator.py`: 数据有效性验证

### API 服务 (`api/`)
基于 Flask 框架的 REST API 服务，提供以下端点：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/hec_hms/` | GET | 服务状态检查 |
| `/hec_hms/init-start-single` | POST | 初始化单一模型运行 |
| `/hec_hms/init-start-distributed` | POST | 初始化分布式模型运行 |
| `/hec_hms/init-run` | POST | 执行模型计算 |
| `/hec_hms/upload_data` | POST | 上传结果数据到数据库 |
| `/hec_hms/upload` | POST | 打包输出文件 |

### 深度学习模块 (`ml/`)
为深度学习耦合预留的标准接口：
- `DeepLearningInterface`: 深度学习模型接口
- `MLDataAdapter`: 数据适配器（序列创建、归一化）
- 标准化数据格式: `[n_timesteps, n_basins, n_features]`

## 安装使用

### 环境要求

- Python 3.6+
- HEC-DSSVue（需要单独安装）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/your-username/HEC-HMS-hydromodel.git
cd HEC-HMS-hydromodel
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置数据库连接：
在 `config/default_params.json` 中配置数据库参数

5. 运行 Web 服务器：
```bash
python main.py
```

## API 使用示例

### 初始化单一模型
```bash
curl -X POST "http://localhost:8080/hec_hms/init-start-single?run-name=test_run&datetime=2024-01-01%2000:00:00" \
  -F "rainfall=@DailyRain.csv"
```

### 执行模型
```bash
curl -X POST "http://localhost:8080/hec_hms/init-run?run-name=test_run&datetime=2024-01-01%2000:00:00"
```

### 上传结果
```bash
curl -X POST "http://localhost:8080/hec_hms/upload_data?run-name=test_run&datetime=2024-01-01%2000:00:00&force-insert=False"
```

## 数据流程

```
1. 初始化阶段
   ├── 复制基础模型文件
   ├── 生成/获取降雨数据
   ├── 更新模型配置文件
   └── CSV 转换为 DSS 格式

2. 模型运行
   └── 执行 HEC-HMS 脚本

3. 后处理阶段
   ├── DSS 输出转换为 CSV
   ├── 保存模型状态
   └── 打包输出文件

4. 数据上传（可选）
   └── 流量数据导入数据库
```

## 输出文件结构

```
<run-date>/
└── <run-name>/
    ├── input/
    │   └── DailyRain.csv           # 输入降雨数据
    ├── 2008_2_Events/
    │   ├── Control_1.control       # 控制文件
    │   ├── 2008_2_Events.run       # 运行文件
    │   ├── 2008_2_Events.gage      # 雨量站配置
    │   ├── 2008_2_Events.dss       # 模型数据文件
    │   └── 2008_2_Events.script    # 执行脚本
    └── output/
        ├── DailyDischarge.csv      # 输出流量数据
        └── <run-name>.zip          # 完整输出打包
```

## 测试

运行单元测试：
```bash
python tests/unit/test_generation.py
python tests/unit/test_routing.py
```

运行所有测试：
```bash
python -m pytest tests/
```

## 深度学习耦合

本项目预留了深度学习耦合接口，可以方便地集成 LSTM、Transformer 等深度学习模型：

```python
from ml.interfaces import DeepLearningInterface
from ml.data_adapter import MLDataAdapter

# 准备数据
adapter = MLDataAdapter()
data = adapter.prepare_training_data(precip, pet, discharge, sequence_length=24)

# 实现自定义深度学习模型
class MyLSTMModel(DeepLearningInterface):
    def build_model(self, input_shape, output_shape, **kwargs):
        # 实现模型构建
        pass
    
    def train(self, train_inputs, train_targets, **kwargs):
        # 实现训练逻辑
        pass
    
    def predict(self, inputs):
        # 实现预测逻辑
        pass
```

## 开发指南

### 添加新的产流模型
1. 在 `core/generation.py` 中继承 `RunoffGenerationBase`
2. 实现 `calculate()` 和 `get_required_params()` 方法
3. 在 `tests/unit/test_generation.py` 中添加测试

### 添加新的汇流方法
1. 在 `core/routing.py` 中继承 `RoutingBase`
2. 实现 `route()` 方法
3. 添加对应的单元测试

## 注意事项

1. 默认上传目录可通过 `config/default_params.json` 配置
2. 分布式模型需要配置多个雨量站数据文件
3. 建议使用虚拟环境隔离项目依赖
4. HEC-DSSVue 需要单独安装并配置路径
5. 原代码备份在 `legacy/` 目录

## 版本历史

- **v2.0.0** (2024): 重构为模块化架构
  - 新增配置外部化
  - 新增深度学习接口预留
  - 新增单元测试框架
  - 优化代码结构
- **v1.0.0**: 初始版本

## 许可证

MIT License

## 联系方式

- 项目主页: https://github.com/your-username/HEC-HMS-hydromodel
- 问题反馈: https://github.com/your-username/HEC-HMS-hydromodel/issues
