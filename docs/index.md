---
title: Home | bt_api_bitvavo
---

<!-- English -->
# bt_api_bitvavo Documentation

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitvavo.svg)](https://pypi.org/project/bt_api_bitvavo/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitvavo.svg)](https://pypi.org/project/bt_api_bitvavo/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitvavo/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitvavo/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitvavo/badge/?version=latest)](https://bt-api-bitvavo.readthedocs.io/)

## Overview

`bt_api_bitvavo` is the **Bitvavo exchange plugin** for the [bt_api](https://github.com/cloudQuant/bt_api_py) plugin ecosystem. Bitvavo is a leading European cryptocurrency exchange based in Amsterdam, Netherlands, founded in 2017, offering trading for 200+ cryptocurrencies with EUR pairs.

This package provides unified REST interfaces for **Spot** trading on Bitvavo, integrating seamlessly with the bt_api `BtApi` class via `ExchangeRegistry`.

## Key Benefits

- **HMAC-SHA256 Authentication**: Full request signing following Bitvavo's signature scheme
- **Synchronous & Asynchronous**: Supports both sync and async request patterns
- **Plugin Architecture**: Auto-registers at import time via `ExchangeRegistry`
- **Unified Interface**: Works with `BtApi` for multi-exchange portfolio management
- **EUR-First**: Bitvavo's EUR trading pairs provide excellent liquidity for European users
- **Comprehensive Coverage**: Ticker, OrderBook, K-lines, Trading, Balance, Account operations

## Architecture Overview

```
bt_api_bitvavo/
├── plugin.py                     # register_plugin() — bt_api plugin entry point
├── registry_registration.py       # register_bitvavo() — feeds/exchange_data registration
├── exchange_data/
│   └── __init__.py              # BitvavoExchangeData, BitvavoExchangeDataSpot
├── feeds/
│   └── live_bitvavo/
│       ├── request_base.py       # BitvavoRequestData — base with HMAC auth
│       └── spot.py              # BitvavoRequestDataSpot — spot trading implementation
├── errors/
│   └── __init__.py              # BitvavoErrorTranslator — error code mapping
├── tickers/
│   └── ticker_utils.py           # Ticker utilities
├── configs/
│   └── bitvavo.yaml            # Exchange configuration
└── __init__.py                  # BitvavoRequestDataSpot export
```

## Supported Exchange Code

| Exchange Code | Asset Type | REST Base | WSS Base |
|---|---|---|---|
| `BITVAVO___SPOT` | Spot | `https://api.bitvavo.com/v2` | `wss://ws.bitvavo.com/v2/` |

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_tick` | 24h rolling ticker |
| | `get_depth` | Order book depth (5/10/20/50/100) |
| | `get_kline` | Intervals: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d |
| | `get_exchange_info` | Available markets |
| **Account** | `get_balance` | All asset balances or specific symbol |
| | `get_account` | Full account info |
| **Trading** | `make_order` | LIMIT/MARKET orders |
| | `cancel_order` | Cancel by order ID |
| | `query_order` | Query order by ID |
| | `get_open_orders` | All open orders |

## Quick Start

### Installation

```bash
pip install bt_api_bitvavo
```

Or from source:

```bash
git clone https://github.com/cloudQuant/bt_api_bitvavo
cd bt_api_bitvavo
pip install -e .
```

### bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "BITVAVO___SPOT": {
            "api_key": "your_api_key",
            "secret": "your_api_secret",
        }
    }
)

# Market data (no auth required)
ticker = api.get_tick("BITVAVO___SPOT", "BTC-EUR")
depth = api.get_depth("BITVAVO___SPOT", "BTC-EUR", count=20)

# Authenticated requests
balance = api.get_balance("BITVAVO___SPOT")
order = api.make_order(
    exchange_name="BITVAVO___SPOT",
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",
)
```

### Direct Usage

```python
from bt_api_bitvavo import BitvavoRequestDataSpot

feed = BitvavoRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret",
)

# Market data
ticker = feed.get_tick("BTC-EUR")
depth = feed.get_depth("BTC-EUR", count=20)
klines = feed.get_kline("BTC-EUR", period="1h", count=100)

# Trading
order = feed.make_order(
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",
)
balance = feed.get_balance()
```

### Asynchronous Usage

```python
import asyncio
from bt_api_py import BtApi

async def main():
    api = BtApi(
        exchange_kwargs={
            "BITVAVO___SPOT": {
                "api_key": "your_api_key",
                "secret": "your_api_secret",
            }
        }
    )

    ticker = await api.async_get_tick("BITVAVO___SPOT", "BTC-EUR")
    print(ticker)

asyncio.run(main())
```

## Authentication

Bitvavo uses **HMAC-SHA256** signature authentication. The signature is computed as:

```
signature = HMAC-SHA256(secret, timestamp + method + url_path + body)
```

Where:
- `timestamp`: Unix timestamp in milliseconds
- `method`: HTTP method (GET, POST, DELETE)
- `url_path`: The API path (e.g., `/v2/order`)
- `body`: Request body (empty string for GET requests)

## Error Handling

All Bitvavo API errors are translated to bt_api_base `ApiError` subclasses:

| Error Code | Error | Description |
|---|---|---|
| `100` | `INVALID_API_KEY` | Invalid API key |
| `101` | `PERMISSION_DENIED` | No permission for this endpoint |
| `200` | `INSUFFICIENT_BALANCE` | Insufficient balance |
| `201` | `INVALID_VOLUME` | Order volume too small |
| `202` | `INVALID_PRICE` | Price is invalid |
| `203` | `MIN_NOTIONAL` | Order value below minimum |
| `204` | `INVALID_ORDER_TYPE` | Invalid order type |
| `205` | `INVALID_SIDE` | Invalid order side |
| `300` | `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `301` | `IP_BANNED` | IP banned |
| `400` | `INVALID_SYMBOL` | Market does not exist |
| `401` | `ORDER_NOT_FOUND` | Order not found |
| `402` | `ORDER_ALREADY_FILLED` | Order already filled |
| `403` | `MARKET_CLOSED` | Market is closed |
| `500` | `INTERNAL_ERROR` | Internal server error |
| `501` | `EXCHANGE_OVERLOADED` | Service temporarily unavailable |

## Rate Limits

| Endpoint Type | Limit |
|---|---|
| Public endpoints | 60 req/sec |
| Authenticated endpoints | 60 req/sec |
| Trading endpoints | 10 req/sec |

## Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitvavo.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitvavo |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitvavo/issues |
| PyPI Package | https://pypi.org/project/bt_api_bitvavo/ |
| Bitvavo API Docs | https://docs.bitvavo.com/ |
| bt_api_base Docs | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## 中文

### 概述

`bt_api_bitvavo` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 插件生态系统的 **Bitvavo 交易所插件**。Bitvavo 是荷兰阿姆斯特丹的欧洲领先加密货币交易所，成立于2017年，提供 200+ 种加密货币的 EUR 交易对。

本包为 Bitvavo 现货交易提供统一的 REST 接口，通过 `ExchangeRegistry` 与 bt_api 的 `BtApi` 类无缝集成。

### 核心优势

- **HMAC-SHA256 认证**：遵循 Bitvavo 签名方案的完整请求签名
- **同步与异步**：支持同步和异步请求模式
- **插件架构**：通过 `ExchangeRegistry` 导入时自动注册
- **统一接口**：与 `BtApi` 配合实现多交易所投资组合管理
- **EUR 优先**：Bitvavo 的 EUR 交易对为欧洲用户提供良好流动性
- **全面覆盖**：行情、订单簿、K线、交易、余额、账户操作

### 架构

```
bt_api_bitvavo/
├── plugin.py                     # register_plugin() — bt_api 插件入口
├── registry_registration.py       # register_bitvavo() — feeds/exchange_data 注册
├── exchange_data/
│   └── __init__.py              # BitvavoExchangeData, BitvavoExchangeDataSpot
├── feeds/
│   └── live_bitvavo/
│       ├── request_base.py       # BitvavoRequestData — 带 HMAC 认证的基类
│       └── spot.py              # BitvavoRequestDataSpot — 现货交易实现
├── errors/
│   └── __init__.py              # BitvavoErrorTranslator — 错误代码映射
├── tickers/
│   └── ticker_utils.py          # 行情工具
├── configs/
│   └── bitvavo.yaml            # 交易所配置
└── __init__.py                  # BitvavoRequestDataSpot 导出
```

### 支持的交易所代码

| 交易所代码 | 资产类型 | REST 基础地址 | WSS 基础地址 |
|---|---|---|---|
| `BITVAVO___SPOT` | 现货 | `https://api.bitvavo.com/v2` | `wss://ws.bitvavo.com/v2/` |

### 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **市场数据** | `get_tick` | 24小时滚动行情 |
| | `get_depth` | 订单簿深度（5/10/20/50/100） |
| | `get_kline` | 周期：1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d |
| | `get_exchange_info` | 可用市场 |
| **账户** | `get_balance` | 所有资产余额或指定 symbol |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 限价/市价单 |
| | `cancel_order` | 按订单 ID 撤单 |
| | `query_order` | 按 ID 查询订单 |
| | `get_open_orders` | 所有挂单 |

### 快速开始

```bash
pip install bt_api_bitvavo
```

bt_api 插件集成：

```python
from bt_api_py import BtApi

api = BtApi(
    exchange_kwargs={
        "BITVAVO___SPOT": {
            "api_key": "your_api_key",
            "secret": "your_api_secret",
        }
    }
)

ticker = api.get_tick("BITVAVO___SPOT", "BTC-EUR")
balance = api.get_balance("BITVAVO___SPOT")
```

### 认证方式

Bitvavo 使用 **HMAC-SHA256** 签名认证。签名计算方式：

```
signature = HMAC-SHA256(secret, timestamp + method + url_path + body)
```

其中：
- `timestamp`：Unix 时间戳（毫秒）
- `method`：HTTP 方法（GET、POST、DELETE）
- `url_path`：API 路径（如 `/v2/order`）
- `body`：请求体（GET 请求为空字符串）

### 错误处理

所有 Bitvavo API 错误翻译为 bt_api_base `ApiError` 子类，映射见上方英文版错误表。

### 限流配置

| 端点类型 | 限制 |
|---|---|
| 公共端点 | 60 请求/秒 |
| 认证端点 | 60 请求/秒 |
| 交易端点 | 10 请求/秒 |

### 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitvavo.readthedocs.io/ |
| 中文文档 | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitvavo |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitvavo/issues |
| PyPI 包 | https://pypi.org/project/bt_api_bitvavo/ |
| Bitvavo API 文档 | https://docs.bitvavo.com/ |
| bt_api_base 文档 | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |
