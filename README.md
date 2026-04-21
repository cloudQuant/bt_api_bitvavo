# BITVAVO

Exchange plugin for bt_api framework.

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitvavo.svg)](https://pypi.org/project/bt_api_bitvavo/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitvavo.svg)](https://pypi.org/project/bt_api_bitvavo/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitvavo/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitvavo/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitvavo/badge/?version=latest)](https://bt-api-bitvavo.readthedocs.io/)

---

## English | [中文](#中文)

### Overview

This package provides **Bitvavo exchange plugin for bt_api** for the [bt_api](https://github.com/cloudQuant/bt_api_py) framework. It offers a unified interface for interacting with **BITVAVO** exchange.

### Features

- Exchange integration with bt_api
- REST API support
- Market data access
- Basic trading operations

### Installation

```bash
pip install bt_api_bitvavo
```

Or install from source:

```bash
git clone https://github.com/cloudQuant/bt_api_bitvavo
cd bt_api_bitvavo
pip install -e .
```

### Quick Start

```python
from bt_api_bitvavo import BitvavoApi

# Initialize
feed = BitvavoApi(api_key="your_key", secret="your_secret")

# Get ticker data
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### Supported Operations

| Operation | Status |
|-----------|--------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitvavo.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitvavo |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitvavo/issues |

### Requirements

- Python 3.9+
- bt_api_base >= 0.15

### Architecture

```
bt_api_bitvavo/
├── src/bt_api_bitvavo/     # Source code
│   ├── containers/     # Data containers
│   ├── feeds/          # API feeds
│   ├── gateway/       # Gateway adapter
│   └── plugin.py      # Plugin registration
├── tests/             # Unit tests
└── docs/             # Documentation
```

### License

MIT License - see [LICENSE](LICENSE) for details.

### Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitvavo/issues)
- Email: yunjinqi@gmail.com

---

## 中文

### 概述

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitvavo exchange plugin for bt_api**。它提供了与 **BITVAVO** 交易所交互的统一接口。

### 功能特点

- bt_api交易所集成
- REST API支持
- 市场数据访问
- 基本交易操作

### 安装

```bash
pip install bt_api_bitvavo
```

或从源码安装：

```bash
git clone https://github.com/cloudQuant/bt_api_bitvavo
cd bt_api_bitvavo
pip install -e .
```

### 快速开始

```python
from bt_api_bitvavo import BitvavoApi

# 初始化
feed = BitvavoApi(api_key="your_key", secret="your_secret")

# 获取行情数据
ticker = feed.get_ticker("BTCUSDT")
print(ticker)
```

### 支持的操作

| 操作 | 状态 |
|------|------|
| Ticker | ✅ |
| OrderBook | ✅ |
| Trades | ✅ |
| Bars/Klines | ✅ |
| Orders | ✅ |
| Balances | ✅ |
| Positions | ✅ |

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitvavo.readthedocs.io/ |
| 中文文档 | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitvavo |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitvavo/issues |

### 系统要求

- Python 3.9+
- bt_api_base >= 0.15

### 架构

```
bt_api_bitvavo/
├── src/bt_api_bitvavo/     # 源代码
│   ├── containers/     # 数据容器
│   ├── feeds/          # API 源
│   ├── gateway/        # 网关适配器
│   └── plugin.py       # 插件注册
├── tests/             # 单元测试
└── docs/             # 文档
```

### 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

### 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitvavo/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com
