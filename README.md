# Project Documentation

## Project Description

This project provides a Python API for fetching historical data from the Binance exchange. It includes functionalities for retrieving Klines, trades, aggregate trades, book ticker data, funding rates, and metrics.

## Quick Start Guide

[View Full Documentation](https://quantease-binance-history.readthedocs.io/en/latest/index.html#)  

To use the functions in `quantease_binance`, you need to import the necessary modules and call the desired functions with appropriate parameters. Here are some examples:

### Installation

`quantease-binance` can be installed using `pip`:

```bash
pip install quantease-binance
```

### Fetch All Trading Pairs

To fetch all trading pairs from the Binance exchange, you can use the `fetch_all_symbols` function. Here’s how to use it:

```python
import quantease_binance as qb

symbols = qb.fetch_all_symbols()
print(symbols)
```

This will return a list of trading pairs based on the specified `asset_type`. By default, `asset_type` is set to "spot". If you want to get trading pairs for perpetual contracts, specify `asset_type` as "futures/um" or "futures/cm".

### Fetch Aggregate Trade Data

```python
import quantease_binance as qb

agg_trades = qb.fetch_agg_trades(
    symbol='BTCUSDT',
    start='2024-01-01',
    end='2024-05-01',
    asset_type='spot',
    tz='UTC'
)
print(agg_trades)
```

### Fetch Book Ticker Data

```python
book_ticker = qb.fetch_book_ticker(
    symbol='AAVEUSD_PERP',
    start='2024-01-01',
    end='2024-02-01',
    asset_type='futures/cm',
    tz='UTC'
)
print(book_ticker)
```

### Fetch Funding Rate Data

```python
funding_rate = qb.fetch_funding_rate(
    symbol='ETHUSDT',
    start='2019-01-01',
    end='2024-07-01',
    asset_type='futures/um',
    tz='UTC'
)
print(funding_rate)
```

### Fetch Trade Data

```python
trade = qb.fetch_trades(
    symbol='ETHUSDT',
    start='2024-05-01',
    end='2024-07-10',
    asset_type='spot',
    tz='UTC'
)
print(trade)
```

### Fetch Kline Data

```python
klines = qb.fetch_klines(
    symbol='BTCUSDT',
    start='2018-01-01',
    end='2024-07-12',
    timeframe='1m',
    asset_type='spot',
    tz='UTC'
)
print(klines)
```

### Fetch Metrics Data

```python
metrics = qb.fetch_metrics(
    symbol='BTCUSDT',
    start='2024-01-01',
    end='2024-04-01',
    asset_type='futures/um',
    tz='UTC'
)
print(metrics)
```

Make sure to replace the placeholders for `symbol`, `start`, `end`, and other parameters as needed.

## API Documentation

### `fetch_klines`

Convenience function to fetch Kline data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `timeframe` (str, optional): Kline interval. Default is "1m".
- `asset_type` (str, optional): Asset type for the data request. Default is "spot".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `open`, `high`, `low`, `close`, `volume`, `trades`, `close_datetime` columns.

### `fetch_trades`

Convenience function to fetch trade data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `asset_type` (str, optional): Asset type for the data request. Default is "spot".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `id`, `price`, `qty`, `quoteQty`, `time`, `isBuyerMaker`, `isBestMatch` columns.

### `fetch_agg_trades`

Convenience function to fetch aggregate trade data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `asset_type` (str, optional): Asset type for the data request. Default is "spot".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `id`, `price`, `qty`, `firstTradeId`, `lastTradeId`, `time`, `isBuyerMaker`, `isBestMatch` columns.

### `fetch_book_ticker`

Convenience function to fetch book ticker data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `asset_type` (str, optional): Asset type for the data request. Default is "spot".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `symbol`, `bidPrice`, `bidQty`, `askPrice`, `askQty`, `time` columns.

### `fetch_funding_rate`

Convenience function to fetch funding rate data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `asset_type` (str): Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `symbol`, `fundingRate`, `fundingTime` columns.

### `fetch_metrics`

Convenience function to fetch metrics data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): Start time for the data request.
- `end` (str or datetime): End time for the data request.
- `asset_type` (str): Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing `symbol`, `openInterest`, `numberOfTrades`, `volume`, `quoteVolume`, `takerBuyBaseAssetVolume`, `takerBuyQuoteAssetVolume`, `openTime`, `closeTime` columns.

### `fetch_data`

Main function to fetch data.

**Parameters:**

- `symbol` (str): Binance market pair name, e.g., "BTCUSDT".
- `asset_type` (str): Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
- `data_type` (str): Type of data to request. Must be one of "klines", "aggTrades", "bookTicker", "fundingRate", "metrics".
- `start` (datetime): Start time for the data request.
- `end` (datetime): End time for the data request.
- `tz` (str, optional): Timezone for the returned DataFrame's datetime parameters. Default is "UTC".
- `timeframe` (str, optional): Kline interval. Default is None.

**Returns:**

- `DataFrame`: A pandas DataFrame containing the requested data.

### `fetch_all_symbols`

Function to fetch all trading pairs from the Binance exchange.

**Parameters:**

- `exchange` (object): Exchange object initialized using the ccxt library. Default is `config.EXCHANGE`.
- `asset_type` (str, optional): Asset type for the trading pairs to fetch. Must be one of "spot", "futures/um", or "futures/cm". Default is "spot".

**Returns:**

- `List[str]`: List of trading pair IDs based on the specified `asset_type`.

### Notes

Functions in this API require the `quantease_binance.utils` module and its `gen_dates`, `get_data`, `unify_datetime`, and `get_data_async` functions. Ensure to import them as well.
