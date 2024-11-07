from datetime import datetime
from typing import Dict

import pandas as pd
from pandas import DataFrame
from dateutil import tz
import asynciolimiter

from .utils import Symbol
from .utils import gen_dates, get_data, get_data_async, unify_datetime
from . import config
from typing import Optional, Union, List, Literal
import asyncio
import platform
import aiohttp
#import uvloop

from tqdm import tqdm
from tqdm.asyncio import tqdm 
from tardis_dev import get_exchange_details
from enum import Enum

class SymbolType(Enum):
    SPOT = "spot"
    PERP = "perpetual"
    FUTURE = "future"


def fetch_klines(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    timeframe: str = "1m",
    asset_type: Literal["spot", "futures/um", "futures/cm"] = "spot",
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="klines",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        timeframe=timeframe,
        tz=tz,
    )

def fetch_trades(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    asset_type: Literal["spot", "futures/um", "futures/cm"] = "spot",
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="trades",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        tz=tz,
    )

def fetch_agg_trades(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    asset_type: Literal["spot", "futures/um", "futures/cm"] = "spot",
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="aggTrades",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        tz=tz,
    )

def fetch_book_ticker(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    asset_type: Literal["spot", "futures/um", "futures/cm"] = "spot",
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="bookTicker",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        tz=tz,
    )

def fetch_funding_rate(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    asset_type: Literal["spot", "futures/um", "futures/cm"],
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="fundingRate",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        tz=tz,
    )

def fetch_metrics(
    symbol: str,
    start: Union[str, datetime],
    end: Union[str, datetime],
    asset_type: Literal["spot", "futures/um", "futures/cm"],
    tz: Optional[str] = None,
) -> DataFrame:
    """convinience function by calling ``fetch_data``"""

    return fetch_data(
        data_type="metrics",
        asset_type=asset_type,
        symbol=symbol,
        start=start,
        end=end,
        tz=tz,
    )

def fetch_data(
    symbol: str,
    asset_type: Literal["spot", "futures/um", "futures/cm"],
    data_type: Literal["klines", "aggTrades", "bookTicker", "fundingRate", "trades", "metrics"],
    start: datetime,
    end: datetime,
    tz: Optional[str] = "UTC",
    timeframe: Optional[str] = None,
    use_async: Optional[bool] = False,
    save_local: Optional[bool] = False,
    limit_rate: Optional[float] = 3 / 1, # 3 requests per second
) -> DataFrame:
    """
    :param symbol: The binance market pair name. e.g. ``'BTCUSDT'``.
    :param start:  The start datetime of requested data. If it's an instance of ``datetime.datetime``,
    :param asset_type: The asset type of requested data. It must be one of ``'spot'``, ``'futures/um'``, ``'futures/cm'``.
    :param data_type: The type of requested data. It must be one of ``'klines'``, ``'aggTrades'``, ``'bookTicker'``.
        it's timezone is ignored. If it's a ``str``, it should be parsed by
        `dateutil <https://github.com/dateutil/dateutil>`_, e.g. ``"2022-1-1 8:10"``.
    :param end:  The end datetime of requested data. If it's an instance of ``datetime.datetime``,
        it's timezone is ignored. If it's a ``str``, it should be parsed by
        `dateutil <https://github.com/dateutil/dateutil>`_, e.g. ``"2022-1-2 8:10"``.
    :param tz: Timezone of ``start``, ``end``, and the open/close datetime of the returned dataframe.
        It should be a time zone name of `tz database <https://en.wikipedia.org/wiki/Tz_database>`_, e.g. "Asia/Shanghai".
        Your can find a full list of available time zone names in
        `List of tz database time zones <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List>`_.
    :param timeframe: The kline interval. e.g. "1m". see ``binance_history.constants.TIMEFRAMES``
        to see the full list of available intervals.
    :return: A pandas dataframe with columns `open`, `high`, `low`, `close`, `volume`, `trades`, `close_datetime`.
        the dataframe's index is the open datetime of klines, the timezone of the datetime is set by ``tz``,
        if it is None, your local timezone will be used.
    """
    if tz is None:
        tz = tz.tzlocal().tzname(None)

    start, end = unify_datetime(start), unify_datetime(end)

    start, end = pd.Timestamp(start, tz=tz), pd.Timestamp(end, tz=tz)

    symbol = symbol.upper().replace("/", "")

    months, days = gen_dates(
        data_type,
        asset_type,
        symbol,
        start.tz_convert(None),
        end.tz_convert(None),
        timeframe=timeframe,
    )
    if use_async:
        if platform.system() == "linux" or platform.system() == "Darwin":
            import uvloop
            uvloop.install()
        elif platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        df = asyncio.run(_gather(symbol=symbol, asset_type=asset_type, data_type=data_type, tz=tz, timeframe=timeframe, months=months, days=days, save_local=save_local, limit_rate=limit_rate))
    else:
        monthly_dfs = [
            get_data(data_type, asset_type, "monthly", symbol, dt, tz, timeframe, save_local)
            for dt in tqdm(months, desc="Downloading data", unit="month")
        ]
        if data_type != "fundingRate":
            daily_dfs = [
                get_data(data_type, asset_type, "daily", symbol, dt, tz, timeframe, save_local)
                for dt in tqdm(days, desc="Downloading data", unit="day")
            ]
        else:
            daily_dfs = []
        df = pd.concat(monthly_dfs + daily_dfs)
    return df[(start <= df.index) & (df.index < end)]

async def _gather(
    symbol: str,
    asset_type: Literal["spot", "futures/um", "futures/cm"],
    data_type: str,
    tz: Optional[str] = None,
    timeframe: Optional[str] = None,
    months: List[datetime] = [],
    days: List[datetime] = [],
    limit_rate: float = 3 / 1, # 3 requests per second
    save_local: Optional[bool] = False,
):

    limiter = asynciolimiter.Limiter(rate=limit_rate)
    session = aiohttp.ClientSession()
    try:
        monthly_dfs = [
            get_data_async(data_type, asset_type, "monthly", symbol, dt, tz, timeframe, save_local, session, limiter)
            for dt in months
        ]
        if data_type != "fundingRate":
            daily_dfs = [
                get_data_async(data_type, asset_type, "daily", symbol, dt, tz, timeframe, save_local, session, limiter)
                for dt in days
            ]
        else:
            daily_dfs = []
        dfs = await tqdm.gather(*monthly_dfs, *daily_dfs)
        df = pd.concat(dfs)
        return df
    except asyncio.CancelledError:
        print("Cancelled")
    finally:
        await session.close()

def fetch_all_symbols(asset_type: Literal["spot", "futures/um", "futures/cm"] = "spot") -> Dict[str, Symbol]:
    
    exchange_map = {
        "spot": "binance",
        "futures/um": "binance-futures",
        "futures/cm": "binance-delivery",
        
    }
    
    info = {}
    
    res = get_exchange_details(exchange = exchange_map[asset_type])
    symbols = res['datasets']['symbols']
    
    for s in symbols:
        if s["id"] not in ["FUTURES", "PERPETUALS", "SPOT"]:
            info[s['id']] = Symbol(
                id = s['id'],
                type = SymbolType(s['type']),
                availableSince=pd.to_datetime(s['availableSince'], utc=True),
                availableTo=pd.to_datetime(s['availableTo'], utc=True),
            )
    
    return info
    
    # exchange.load_markets()
    # spot, futures_um, futures_cm = [], [], []
    # for symbol, data in exchange.markets.items():
    #     if data['active']:
    #         id = data['id']
    #         symbol = data['symbol']
    #         typ = data['type']
    #         if typ == 'spot':
    #             spot.append({'id': id, 'symbol': symbol, 'asset_type': "spot"})
    #         elif typ == 'swap':
    #             if data['subType'] == 'linear':
    #                 futures_um.append({'id': id, 'symbol': symbol, 'asset_type': "futures/um"})
    #             elif data['subType'] == 'inverse':
    #                 futures_cm.append({'id': id, 'symbol': symbol, 'asset_type': "futures/cm"})
    # if asset_type == 'spot':
    #     return spot
    # elif asset_type == 'futures/um':
    #     return futures_um
    # elif asset_type == 'futures/cm':
    #     return futures_cm
    

