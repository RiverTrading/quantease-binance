import datetime
import io
import asyncio
import asynciolimiter
import os
import os.path
import zipfile
import warnings
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse
from dataclasses import dataclass
from dateutil import parser

import httpx
import aiohttp
import pandas as pd

# import pendulum
from pandas import Timestamp, DataFrame

from . import config
from .exceptions import NetworkError, DataNotFound


@dataclass
class Symbol:
    id: str
    type: str
    availableSince: pd.DatetimeIndex
    availableTo: pd.DatetimeIndex


def gen_data_url(
    data_type: str,
    asset_type: str,
    freq: str,
    symbol: str,
    dt: Timestamp,
    timeframe: Optional[str] = None,
):
    """
    https://data.binance.vision/data/futures/cm/monthly/bookTicker/AAVEUSD_PERP/AAVEUSD_PERP-bookTicker-2024-01.zip
    https://data.binance.vision/data/futures/um/monthly/fundingRate/1000BONKUSDT/1000BONKUSDT-fundingRate-2024-01.zip
    https://data.binance.vision/data/spot/monthly/trades/1INCHBTC/1INCHBTC-trades-2024-04.zip
    https://data.binance.vision/data/futures/um/daily/metrics/1000BONKUSDC/1000BONKUSDC-metrics-2024-07-01.zip
    """

    url: str
    date_str: str

    if freq == "monthly":
        date_str = dt.strftime("%Y-%m")
    elif freq == "daily":
        date_str = dt.strftime("%Y-%m-%d")
    else:
        raise ValueError(f"freq must be 'monthly' or 'daily', but got '{freq}'")

    if data_type == "klines":
        if timeframe is None:
            raise ValueError("'timeframe' must not be None when data_type is 'klines'")
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}/{timeframe}"
            f"/{symbol}-{timeframe}-{date_str}.zip"
        )
    elif data_type == "trades":
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}"
            f"/{symbol}-{data_type}-{date_str}.zip"
        )
    elif data_type == "aggTrades":
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}"
            f"/{symbol}-{data_type}-{date_str}.zip"
        )
    elif data_type == "bookTicker":
        if asset_type != "futures/cm":
            raise ValueError(f"asset_type must be 'futures/cm', but got '{asset_type}'")
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}"
            f"/{symbol}-{data_type}-{date_str}.zip"
        )
    elif data_type == "fundingRate":
        if asset_type == "spot":
            raise ValueError(
                f"asset_type must be 'futures/cm' or 'future/um', but got '{asset_type}'"
            )
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}"
            f"/{symbol}-{data_type}-{date_str}.zip"
        )
    elif data_type == "metrics":
        if asset_type == "spot":
            raise ValueError(
                f"asset_type must be 'futures/cm' or 'future/um', but got '{asset_type}'"
            )
        url = (
            f"https://data.binance.vision/data/{asset_type}/{freq}/{data_type}/{symbol}"
            f"/{symbol}-{data_type}-{date_str}.zip"
        )
    else:
        raise ValueError(
            f"data_type must in 'klines', 'aggTrades', 'bookTicker', 'fundingRate', but got '{data_type}'"
        )
    return url


# def unify_datetime(input: Union[str, datetime.datetime]) -> datetime.datetime:
#     if isinstance(input, str):
#         return pendulum.parse(input, strict=False).replace(tzinfo=None)
#     elif isinstance(input, datetime.datetime):
#         return input.replace(tzinfo=None)
#     else:
#         raise TypeError(input)


def unify_datetime(input: Union[str, datetime.datetime]) -> datetime.datetime:
    if isinstance(input, str):
        return parser.parse(input, fuzzy=True).replace(tzinfo=None)
    elif isinstance(input, datetime.datetime):
        return input.replace(tzinfo=None)
    else:
        raise TypeError(f"Unsupported input type: {type(input)}")


def exists_month(month_url):
    try:
        resp = httpx.head(month_url)
    except (httpx.TimeoutException, httpx.NetworkError) as e:
        raise NetworkError(e)

    if resp.status_code == 200:
        return True
    elif resp.status_code == 404:
        return False
    else:
        raise NetworkError(resp.status_code)


def gen_dates(
    data_type: str,
    asset_type: str,
    symbol: str,
    start: Timestamp,
    end: Timestamp,
    timeframe: Optional[str] = None,
):
    assert start.tz is None and end.tz is None

    if start > end:
        raise ValueError("start cannot be greater than end")

    months = pd.date_range(
        Timestamp(start.year, start.month, 1),
        end,
        freq="MS",
    ).to_list()

    assert len(months) > 0

    # if not exists_month(last_month_url):
    #     daily_month = months.pop()
    #     if len(months) > 1:
    #         second_last_month_url = gen_data_url(
    #             data_type,
    #             asset_type,
    #             "monthly",
    #             symbol,
    #             months[-1],
    #             timeframe=timeframe,
    #         )
    #         if not exists_month(second_last_month_url):
    #             daily_month = months.pop()

    #     days = pd.date_range(
    #         Timestamp(daily_month.year, daily_month.month, 1),
    #         end,
    #         freq="D",
    #     ).to_list()
    # else:
    #     days = []
    start_year = None
    start_month = None
    while months:
        month = months[-1]
        month_url = gen_data_url(
            data_type, asset_type, "monthly", symbol, month, timeframe=timeframe
        )

        if exists_month(month_url):
            break

        months.pop()
        start_year = month.year
        start_month = month.month

    st = Timestamp(start_year, start_month, 1)
    if start_year and start_month and st != end:
        days = pd.date_range(
            st,
            end,
            freq="D",
            inclusive="left",
        ).to_list()
    else:
        days = []

    non_existent_start = None
    while months and not exists_month(
        gen_data_url(
            data_type, asset_type, "monthly", symbol, months[0], timeframe=timeframe
        )
    ):
        if non_existent_start is None:
            non_existent_start = months[0]
        months.pop(0)

    if non_existent_start:
        non_existent_end = months[0] - pd.Timedelta(days=1) if months else end
        warning_message = f"Data does not exist for the period: {non_existent_start.strftime('%Y-%m')} to {non_existent_end.strftime('%Y-%m')}"
        warnings.warn(warning_message)

    return months, days


def get_data(
    data_type: str,
    asset_type: str,
    freq: str,
    symbol: str,
    dt: Timestamp,
    data_tz: str,
    timeframe: Optional[str] = None,
    save_local: bool = False,
) -> DataFrame:
    if data_type == "klines":
        assert timeframe is not None

    url = gen_data_url(data_type, asset_type, freq, symbol, dt, timeframe)

    df = load_data_from_disk(url)
    if df is None:
        try:
            df = download_data(data_type, data_tz, url)
            save_data_to_disk(url, df, save_local)
        except DataNotFound:
            warn = f"Data not found: {url}"
            warnings.warn(warn)
            return None
    return df


async def get_data_async(
    data_type: str,
    asset_type: str,
    freq: str,
    symbol: str,
    dt: Timestamp,
    data_tz: str,
    timeframe: Optional[str] = None,
    save_local: bool = False,
    session: aiohttp.ClientSession = None,
    limiter: asynciolimiter.Limiter = None,
) -> DataFrame:
    if data_type == "klines":
        assert timeframe is not None

    url = gen_data_url(data_type, asset_type, freq, symbol, dt, timeframe)

    df = load_data_from_disk(url)
    if df is None:
        try:
            df = await download_data_async(
                data_type, data_tz, url, session=session, limiter=limiter
            )
            save_data_to_disk(url, df, save_local)
        except DataNotFound:
            warn = f"Data not found: {url}"
            warnings.warn(warn)
            return None
    return df


def download_data(data_type: str, data_tz: str, url: str) -> DataFrame:
    assert data_type in [
        "klines",
        "aggTrades",
        "bookTicker",
        "fundingRate",
        "trades",
        "metrics",
    ]

    try:
        resp = httpx.get(url)
    except (httpx.TimeoutException, httpx.NetworkError) as e:
        raise NetworkError(e)

    if resp.status_code == 200:
        pass
    elif resp.status_code == 404:
        raise DataNotFound(url)
    else:
        raise NetworkError(url)

    if data_type == "klines":
        return load_klines(data_tz, resp.content)
    elif data_type == "aggTrades":
        return load_agg_trades(data_tz, resp.content)
    elif data_type == "bookTicker":
        return load_book_ticker(data_tz, resp.content)
    elif data_type == "fundingRate":
        return load_funding_rate(data_tz, resp.content)
    elif data_type == "trades":
        return load_trades(data_tz, resp.content)
    elif data_type == "metrics":
        return load_metrics(data_tz, resp.content)


async def download_data_async(
    data_type: str,
    data_tz: str,
    url: str,
    max_retries: int = 3,
    session: aiohttp.ClientSession = None,
    limiter: asynciolimiter.Limiter = None,
) -> DataFrame:
    assert data_type in [
        "klines",
        "aggTrades",
        "bookTicker",
        "fundingRate",
        "trades",
        "metrics",
    ]
    await limiter.wait()
    async def attempt_download():
        try:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    return content
                elif resp.status == 404:
                    raise DataNotFound(url)
                else:
                    raise NetworkError(f"HTTP {resp.status}: {url}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            raise NetworkError(str(e))

    for attempt in range(max_retries):
        try:
            content = await attempt_download()
            break
        except NetworkError as e:
            if attempt == max_retries - 1:  # Last attempt
                raise
            await asyncio.sleep(2**attempt)  # Exponential backoff

    if data_type == "klines":
        return load_klines(data_tz, content)
    elif data_type == "aggTrades":
        return load_agg_trades(data_tz, content)
    elif data_type == "bookTicker":
        return load_book_ticker(data_tz, content)
    elif data_type == "fundingRate":
        return load_funding_rate(data_tz, content)
    elif data_type == "trades":
        return load_trades(data_tz, content)
    elif data_type == "metrics":
        return load_metrics(data_tz, content)


def load_klines(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                usecols=range(12),
                header=0,
                names=[
                    "open_time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "quote_volume",
                    "count",
                    "taker_buy_volume",
                    "taker_buy_quote_volume",
                    "ignore",
                ],
            )
            df["datetime"] = pd.to_datetime(
                df.open_time, unit="ms", utc=True
            ).dt.tz_convert(data_tz)
            df.set_index("datetime", inplace=True)
    return df


def load_agg_trades(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                header=0,
                usecols=[0, 1, 2, 3, 4, 5, 6],
                names=[
                    "agg_trade_id",
                    "price",
                    "quantity",
                    "first_trade_id",
                    "last_trade_id",
                    "transact_time",
                    "is_buyer_maker",
                ],
            )
            df["datetime"] = pd.to_datetime(
                df.transact_time, unit="ms", utc=True
            ).dt.tz_convert(data_tz)
            df.set_index("datetime", inplace=True)
    return df


def load_book_ticker(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                header=0,
                usecols=[0, 1, 2, 3, 4, 5, 6],
                names=[
                    "update_id",
                    "bid_price",
                    "bid_quantity",
                    "ask_price",
                    "ask_quantity",
                    "transaction_time",
                    "event_time",
                ],
            )
            df["datetime"] = pd.to_datetime(
                df.event_time, unit="ms", utc=True
            ).dt.tz_convert(data_tz)
            df.set_index("datetime", inplace=True)
    return df


def load_funding_rate(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                header=0,
                usecols=[0, 1, 2],
                names=["calc_time", "funding_interval_hours", "last_funding_rate"],
            )
            df["datetime"] = pd.to_datetime(
                df.calc_time, unit="ms", utc=True
            ).dt.tz_convert(data_tz)
            df.set_index("datetime", inplace=True)
    return df


def load_trades(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                header=0,
                usecols=[0, 1, 2, 3, 4, 5],
                names=["id", "price", "qty", "base_qty", "time", "is_buyer_maker"],
            )
            df["datetime"] = pd.to_datetime(df.time, unit="ms", utc=True).dt.tz_convert(
                data_tz
            )
            df.set_index("datetime", inplace=True)
    return df


def load_metrics(data_tz: str, content: bytes) -> DataFrame:
    with zipfile.ZipFile(io.BytesIO(content)) as zipf:
        csv_name = zipf.namelist()[0]
        with zipf.open(csv_name, "r") as csvfile:
            df = pd.read_csv(
                csvfile,
                header=0,
                usecols=range(8),
                names=[
                    "create_time",
                    "symbol",
                    "sum_open_interest",
                    "sum_open_interest_value",
                    "count_toptrader_long_short_ratio",
                    "sum_toptrader_long_short_ratio",
                    "count_long_short_ratio",
                    "sum_taker_long_short_vol_ratio",
                ],
            )
            df["datetime"] = pd.to_datetime(df.create_time, utc=True).dt.tz_convert(
                data_tz
            )
            df.set_index("datetime", inplace=True)
    return df


def get_local_data_path(url: str) -> Path:
    path = urlparse(url).path
    path = path.replace("zip", "parquet")
    return config.CACHE_DIR / path[1:]


def save_data_to_disk(url: str, df: DataFrame, save_local: bool = False) -> None:
    path = get_local_data_path(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    # df.to_pickle(path)
    if save_local:
        df.to_parquet(path)


def load_data_from_disk(url: str) -> Union[DataFrame, None]:
    path = get_local_data_path(url)
    if os.path.exists(path):
        # return pd.read_pickle(path)
        return pd.read_parquet(path)
    else:
        return None
