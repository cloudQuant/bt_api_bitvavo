# BITVAVO Documentation

## English

Welcome to the BITVAVO documentation for bt_api.

### Quick Start

```bash
pip install bt_api_bitvavo
```

```python
from bt_api_bitvavo import BitvavoApi
feed = BitvavoApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## 中文

欢迎使用 bt_api 的 BITVAVO 文档。

### 快速开始

```bash
pip install bt_api_bitvavo
```

```python
from bt_api_bitvavo import BitvavoApi
feed = BitvavoApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## API Reference

See source code in `src/bt_api_bitvavo/` for detailed API documentation.
