## Project Description

This project provides a Python API for fetching historical data from the Binance exchange. It includes functions for fetching klines, trades, aggregated trades, book ticker data, funding rates, and metrics.

### Usage

To use the functions in `binance_history/api.py`, you need to import the necessary modules and call the desired function with the appropriate parameters. Here's an example:

```python
from datetime import datetime
from binance_history.api import fetch_klines

# Fetch klines data for BTCUSDT from 2022-01-01 to 2022-01-02
symbol = "BTCUSDT"
start = datetime(2022, 1, 1)
end = datetime(2022, 1, 2)
klines = fetch_klines(symbol, start, end)

# Print the fetched klines data
print(klines)
```

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

### Note

The functions in this API require the `binance_history.utils` module and the `gen_dates`, `get_data`, `unify_datetime`, and `get_data_async` functions from it. Make sure to import them as well.
