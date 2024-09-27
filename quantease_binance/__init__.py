import sys

from .api import fetch_klines, fetch_agg_trades, fetch_data, fetch_book_ticker, fetch_funding_rate, fetch_trades, fetch_metrics, fetch_all_symbols

from importlib import metadata
import platform

if platform.system() == "Windows":
    __version__ = "1.0.0"
else:
    __version__ = "1.0.0"


del metadata, sys, platform

__all__ = ["fetch_klines", "fetch_agg_trades", "fetch_data", "fetch_book_ticker", "fetch_funding_rate", "fetch_trades", "fetch_metrics", "fetch_all_symbols"]
