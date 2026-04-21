# Bitvavo Exchange Plugin for bt_api

## English | [中文](#中文)

---

## Overview

**Bitvavo** is a leading European cryptocurrency exchange based in Amsterdam, Netherlands. Founded in 2017, it provides a secure and user-friendly platform for trading over 200 cryptocurrencies with EUR trading pairs. Bitvavo is known for its low fees, fast processing times, and strong regulatory compliance within the EU.

This package provides the **Bitvavo exchange plugin for bt_api**, offering a unified interface for interacting with Bitvavo exchange through the [bt_api](https://github.com/cloudQuant/bt_api_py) framework.

### Key Features

- **REST API Integration**: Full access to Bitvavo's REST endpoints for market data and trading
- **Synchronous & Asynchronous**: Supports both sync and async request patterns
- **Unified Interface**: Integrates seamlessly with bt_api's `BtApi` class
- **Comprehensive Coverage**: Ticker, OrderBook, Klines, Trading, Balance, Account operations
- **HMAC-SHA256 Authentication**: Secure API key authentication following Bitvavo's signature scheme

### Authentication

Bitvavo uses **HMAC-SHA256** signature authentication. The signature is computed as:

```
signature = HMAC-SHA256(secret, timestamp + method + url_path + body)
```

Where:
- `timestamp`: Unix timestamp in milliseconds
- `method`: HTTP method (GET, POST, DELETE, etc.)
- `url_path`: The API path (e.g., `/v2/order`)
- `body`: Request body (empty string for GET requests)

### API Endpoint

| Environment | REST URL | WebSocket URL |
|------------|----------|---------------|
| Production | `https://api.bitvavo.com/v2` | `wss://ws.bitvavo.com/v2/` |

### Supported Operations

| Category | Operations | Status |
|----------|------------|--------|
| **Market Data** | Ticker, OrderBook, Trades, Klines/Candles | ✅ Supported |
| **Trading** | Place Order, Cancel Order, Query Order | ✅ Supported |
| **Account** | Balance, Account Info, Open Orders | ✅ Supported |
| **Exchange Info** | Markets, Symbols | ✅ Supported |

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bitvavo
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitvavo
cd bt_api_bitvavo
pip install -e .
```

### Requirements

- Python 3.9 or higher
- bt_api_base >= 0.15
- Valid Bitvavo API key and secret

---

## Quick Start

### Initialize with BtApi

```python
from bt_api_py import BtApi

# Initialize with Bitvavo exchange
exchange_config = {
    "BITVAVO___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# Get ticker data
ticker = api.get_tick("BITVAVO___SPOT", "BTC-EUR")
print(ticker)
```

### Direct Usage

```python
from bt_api_bitvavo import BitvavoRequestDataSpot

# Initialize the feed directly
feed = BitvavoRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# Get ticker
ticker = feed.get_tick("BTC-EUR")
print(ticker)

# Get order book
depth = feed.get_depth("BTC-EUR", count=20)
print(depth)

# Place an order
order = feed.make_order(
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",
    offset="buy"  # buy or sell
)
print(order)
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

    # Async ticker request
    ticker = await api.async_get_tick("BITVAVO___SPOT", "BTC-EUR")
    print(ticker)

asyncio.run(main())
```

---

## API Reference

### Market Data

#### Get Ticker (24h)

```python
ticker = feed.get_tick("BTC-EUR")
```

#### Get Order Book

```python
depth = feed.get_depth("BTC-EUR", count=20)
```

#### Get Klines/Candles

```python
# Supported periods: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
klines = feed.get_kline("BTC-EUR", period="1h", count=100)
```

### Trading

#### Place Order

```python
order = feed.make_order(
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",  # limit, market
    offset="buy"         # buy, sell
)
```

#### Cancel Order

```python
result = feed.cancel_order("BTC-EUR", order_id="your_order_id")
```

#### Query Order

```python
order_info = feed.query_order("BTC-EUR", order_id="your_order_id")
```

### Account

#### Get Balance

```python
balance = feed.get_balance()  # All balances
balance = feed.get_balance(symbol="BTC")  # Specific asset balance
```

#### Get Account Info

```python
account = feed.get_account()
```

---

## Supported Symbols

Bitvavo supports trading with EUR as the quote currency for most pairs. Common trading pairs include:

| Symbol | Description |
|--------|-------------|
| BTC-EUR | Bitcoin / Euro |
| ETH-EUR | Ethereum / Euro |
| USDT-EUR | Tether / Euro |
| SOL-EUR | Solana / Euro |
| XRP-EUR | Ripple / Euro |

For a complete list of supported markets, use:

```python
markets = feed.get_exchange_info()
```

---

## Architecture

```
bt_api_bitvavo/
├── src/bt_api_bitvavo/          # Source code
│   ├── exchange_data/           # Exchange configuration and metadata
│   │   └── __init__.py        # BitvavoExchangeData, BitvavoExchangeDataSpot
│   ├── feeds/                  # API feeds
│   │   └── live_bitvavo/      # Live trading feed
│   │       ├── request_base.py # Base class with HMAC auth
│   │       └── spot.py        # Spot trading implementation
│   ├── tickers/               # Ticker utilities
│   ├── errors/               # Error definitions
│   └── plugin.py             # Plugin registration
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── pyproject.toml            # Package configuration
└── README.md                 # This file
```

---

## Error Handling

Bitvavo API errors are translated to standard bt_api exceptions. Common error codes:

| Error Code | Description |
|------------|-------------|
| 100-199 | Authentication errors |
| 200-299 | Permission errors |
| 300-399 | Resource errors |
| 400-499 | Parameter errors |
| 500-599 | Rate limit errors |

---

## Rate Limits

Bitvavo implements rate limiting:
- **Public endpoints**: 60 requests per second
- **Authenticated endpoints**: 60 requests per second
- **Trading endpoints**: 10 requests per second (order placement)

The plugin includes built-in rate limiting to stay within these bounds.

---

## Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitvavo.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitvavo |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitvavo/issues |
| Bitvavo API Docs | https://docs.bitvavo.com/ |

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_bitvavo/issues)
- Email: yunjinqi@gmail.com

---

## Changelog

### v0.1.0

- Initial release
- REST API support for spot trading
- HMAC-SHA256 authentication
- Support for ticker, depth, klines, trading, balance operations

---

# 中文

---

## 概述

**Bitvavo** 是一家位于荷兰阿姆斯特丹的欧洲领先的加密货币交易所，成立于2017年。它提供一个安全、用户友好的平台，可交易超过200种加密货币，主要以EUR交易对为主。Bitvavo 以其低手续费、快速处理时间和强大的欧盟监管合规性而闻名。

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **Bitvavo 交易所插件**，通过统一接口与 Bitvavo 交易所进行交互。

### 核心功能

- **REST API 集成**：全面访问 Bitvavo 的市场数据和交易 REST 端点
- **同步与异步**：支持同步和异步请求模式
- **统一接口**：与 bt_api 的 `BtApi` 类无缝集成
- **全面覆盖**：行情、订单簿、K线、交易、余额、账户操作
- **HMAC-SHA256 认证**：遵循 Bitvavo 签名方案的安全 API 密钥认证

### 认证方式

Bitvavo 使用 **HMAC-SHA256** 签名认证。签名计算方式：

```
signature = HMAC-SHA256(secret, timestamp + method + url_path + body)
```

其中：
- `timestamp`：Unix 时间戳（毫秒）
- `method`：HTTP 方法（GET、POST、DELETE 等）
- `url_path`：API 路径（如 `/v2/order`）
- `body`：请求体（GET 请求为空字符串）

### API 端点

| 环境 | REST URL | WebSocket URL |
|------|----------|---------------|
| 生产环境 | `https://api.bitvavo.com/v2` | `wss://ws.bitvavo.com/v2/` |

### 支持的操作

| 类别 | 操作 | 状态 |
|------|------|------|
| **市场数据** | 行情、订单簿、成交、K线 | ✅ 已支持 |
| **交易** | 下单、撤单、查询订单 | ✅ 已支持 |
| **账户** | 余额、账户信息、开放订单 | ✅ 已支持 |
| **交易所信息** | 市场、交易对 | ✅ 已支持 |

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitvavo
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitvavo
cd bt_api_bitvavo
pip install -e .
```

### 系统要求

- Python 3.9 或更高版本
- bt_api_base >= 0.15
- 有效的 Bitvavo API 密钥和密钥

---

## 快速开始

### 使用 BtApi 初始化

```python
from bt_api_py import BtApi

# 使用 Bitvavo 交易所初始化
exchange_config = {
    "BITVAVO___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# 获取行情数据
ticker = api.get_tick("BITVAVO___SPOT", "BTC-EUR")
print(ticker)
```

### 直接使用

```python
from bt_api_bitvavo import BitvavoRequestDataSpot

# 直接初始化 feed
feed = BitvavoRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# 获取行情
ticker = feed.get_tick("BTC-EUR")
print(ticker)

# 获取订单簿
depth = feed.get_depth("BTC-EUR", count=20)
print(depth)

# 下单
order = feed.make_order(
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",
    offset="buy"  # buy 或 sell
)
print(order)
```

### 异步使用

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

    # 异步获取行情
    ticker = await api.async_get_tick("BITVAVO___SPOT", "BTC-EUR")
    print(ticker)

asyncio.run(main())
```

---

## API 参考

### 市场数据

#### 获取 24 小时行情

```python
ticker = feed.get_tick("BTC-EUR")
```

#### 获取订单簿

```python
depth = feed.get_depth("BTC-EUR", count=20)
```

#### 获取 K 线

```python
# 支持的周期：1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
klines = feed.get_kline("BTC-EUR", period="1h", count=100)
```

### 交易

#### 下单

```python
order = feed.make_order(
    symbol="BTC-EUR",
    volume=0.01,
    price=50000,
    order_type="limit",  # limit, market
    offset="buy"         # buy, sell
)
```

#### 撤单

```python
result = feed.cancel_order("BTC-EUR", order_id="your_order_id")
```

#### 查询订单

```python
order_info = feed.query_order("BTC-EUR", order_id="your_order_id")
```

### 账户

#### 获取余额

```python
balance = feed.get_balance()  # 所有余额
balance = feed.get_balance(symbol="BTC")  # 指定资产余额
```

#### 获取账户信息

```python
account = feed.get_account()
```

---

## 支持的交易对

Bitvavo 支持以 EUR 作为大多数交易对的报价货币。常见交易对包括：

| 交易对 | 描述 |
|--------|------|
| BTC-EUR | 比特币 / 欧元 |
| ETH-EUR | 以太坊 / 欧元 |
| USDT-EUR | 泰达币 / 欧元 |
| SOL-EUR | Solana / 欧元 |
| XRP-EUR | Ripple / 欧元 |

获取完整的支持市场列表：

```python
markets = feed.get_exchange_info()
```

---

## 架构

```
bt_api_bitvavo/
├── src/bt_api_bitvavo/          # 源代码
│   ├── exchange_data/           # 交易所配置和元数据
│   │   └── __init__.py        # BitvavoExchangeData, BitvavoExchangeDataSpot
│   ├── feeds/                  # API feeds
│   │   └── live_bitvavo/      # 实时交易 feed
│   │       ├── request_base.py # 带有 HMAC 认证的基类
│   │       └── spot.py        # 现货交易实现
│   ├── tickers/               # 行情工具
│   ├── errors/               # 错误定义
│   └── plugin.py             # 插件注册
├── tests/                     # 单元测试
├── docs/                      # 文档
├── pyproject.toml            # 包配置
└── README.md                 # 本文件
```

---

## 错误处理

Bitvavo API 错误会转换为标准的 bt_api 异常。常见错误代码：

| 错误代码 | 描述 |
|----------|------|
| 100-199 | 认证错误 |
| 200-299 | 权限错误 |
| 300-399 | 资源错误 |
| 400-499 | 参数错误 |
| 500-599 | 频率限制错误 |

---

## 频率限制

Bitvavo 实施了频率限制：
- **公共端点**：每秒 60 个请求
- **认证端点**：每秒 60 个请求
- **交易端点**：每秒 10 个请求（下单）

插件内置了频率限制以保持在这些范围内。

---

## 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitvavo.readthedocs.io/ |
| 中文文档 | https://bt-api-bitvavo.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_bitvavo |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitvavo/issues |
| Bitvavo API 文档 | https://docs.bitvavo.com/ |

---

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

---

## 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_bitvavo/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com

---

## 更新日志

### v0.1.0

- 初始版本发布
- 支持现货交易的 REST API
- HMAC-SHA256 认证
- 支持行情、订单簿、K线、交易、余额操作