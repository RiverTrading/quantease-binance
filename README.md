## Project Description

This project provides a Python API for fetching historical data from the Binance exchange. It includes functions for fetching klines, trades, aggregated trades, book ticker data, funding rates, and metrics.

### Usage

To use the functions in `binance_history`, you need to import the necessary modules and call the desired function with the appropriate parameters. Here are some examples:

#### Fetch all the symbols

To fetch all symbols from the Binance exchange, you can use the `fetch_all_symbols` function. Here's an example of how to use it:

```python
import binance_history as bh

symbols = bh.fetch_all_symbols()
print(symbols)
```

This will return a list of symbols based on the specified `asset_type`. By default, the `asset_type` is set to "spot". If you want to fetch symbols for perp futures contracts, you can specify the `asset_type` as "futures/um" for linear contracts or "futures/cm" for inverse contracts.

#### Fetch Aggregated Trades Data

```python
import binace_history as bh

agg_trades = bh.fetch_agg_trades(
    symbol='BTCUSDT',
    start='2024-01-01',
    end='2024-05-01',
    asset_type='spot',
    tz='UTC'
)
print(agg_trades)
```

#### Fetch Book Ticker Data

```python
book_ticker = bh.fetch_book_ticker(
    symbol='AAVEUSD_PERP',
    start='2024-01-01',
    end='2024-02-01',
    asset_type='futures/cm',
    tz='UTC'
)
print(book_ticker)
```

#### Fetch Funding Rate Data

```python
funding_rate = bh.fetch_funding_rate(
    symbol='ETHUSDT',
    start='2019-01-01',
    end='2024-07-01',
    asset_type='futures/um',
    tz='UTC'
)
print(funding_rate)
```

#### Fetch Trades Data

```python
trade = bh.fetch_trades(
    symbol='ETHUSDT',
    start='2024-05-01',
    end='2024-07-10',
    asset_type='spot',
    tz='UTC'
)
print(trade)
```

#### Fetch Klines Data

```python
klines = bh.fetch_klines(
    symbol='BTCUSDT',
    start='2018-01-01',
    end='2024-07-12',
    timeframe='1m',
    asset_type='spot',
    tz='UTC'
)
print(klines)
```

#### Fetch Metrics Data

```python
metrics = bh.fetch_metrics(
    symbol='BTCUSDT',
    start='2024-01-01',
    end='2024-04-01',
    asset_type='futures/um',
    tz='UTC'
)
print(metrics)
```

Make sure to replace the placeholders with the actual values for `symbol`, `start`, `end`, and other parameters as needed.

Make sure you have the required dependencies installed (`pandas`, `pendulum`, `asyncio`, `uvloop`, `tqdm`) before running the code.

### Function Documentation

#### `fetch_klines`

Convenience function for fetching klines data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `timeframe` (str, optional): The kline interval. Default is "1m".
- `asset_type` (str, optional): The asset type of the requested data. Default is "spot".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `open`, `high`, `low`, `close`, `volume`, `trades`, `close_datetime`.

#### `fetch_trades`

Convenience function for fetching trades data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `asset_type` (str, optional): The asset type of the requested data. Default is "spot".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `id`, `price`, `qty`, `quoteQty`, `time`, `isBuyerMaker`, `isBestMatch`.

#### `fetch_agg_trades`

Convenience function for fetching aggregated trades data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `asset_type` (str, optional): The asset type of the requested data. Default is "spot".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `id`, `price`, `qty`, `firstTradeId`, `lastTradeId`, `time`, `isBuyerMaker`, `isBestMatch`.

#### `fetch_book_ticker`

Convenience function for fetching book ticker data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `asset_type` (str, optional): The asset type of the requested data. Default is "spot".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `symbol`, `bidPrice`, `bidQty`, `askPrice`, `askQty`, `time`.

#### `fetch_funding_rate`

Convenience function for fetching funding rate data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `asset_type` (str): The asset type of the requested data. Must be one of "spot", "futures/um", "futures/cm".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `symbol`, `fundingRate`, `fundingTime`.

#### `fetch_metrics`

Convenience function for fetching metrics data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `start` (str or datetime): The start datetime of the requested data.
- `end` (str or datetime): The end datetime of the requested data.
- `asset_type` (str): The asset type of the requested data. Must be one of "spot", "futures/um", "futures/cm".
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with columns `symbol`, `openInterest`, `numberOfTrades`, `volume`, `quoteVolume`, `takerBuyBaseAssetVolume`, `takerBuyQuoteAssetVolume`, `openTime`, `closeTime`.

#### `fetch_data`

Main function for fetching data.

Parameters:
- `symbol` (str): The Binance market pair name, e.g., "BTCUSDT".
- `asset_type` (str): The asset type of the requested data. Must be one of "spot", "futures/um", "futures/cm".
- `data_type` (str): The type of requested data. Must be one of "klines", "aggTrades", "bookTicker", "fundingRate", "metrics".
- `start` (datetime): The start datetime of the requested data.
- `end` (datetime): The end datetime of the requested data.
- `tz` (str, optional): Timezone of the datetime parameters and the returned dataframe. Default is "UTC".
- `timeframe` (str, optional): The kline interval. Default is None.

Returns:
- `DataFrame`: A pandas dataframe with the requested data.

#### `fetch_all_symbols`

Function to fetch all symbols from the Binance exchange.

Parameters:
- `exchange` (object): The exchange object initialized with ccxt library. Default is `config.EXCHANGE`.
- `asset_type` (str, optional): The asset type for which symbols are fetched. Must be one of "spot", "futures/um", "futures/cm". Default is "spot".

Returns:
- `List[str]`: A list of symbol IDs based on the specified `asset_type`.

### Note

The functions in this API require the `binance_history.utils` module and the `gen_dates`, `get_data`, `unify_datetime`, and `get_data_async` functions from it. Make sure to import them as well.
