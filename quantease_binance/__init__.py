from .api import fetch_klines, fetch_agg_trades, fetch_data, fetch_book_ticker, fetch_funding_rate, fetch_trades, fetch_metrics, fetch_all_symbols, SymbolType

from importlib import metadata

try:
    __version__ = metadata.version("quantease-binance")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"


__all__ = ["fetch_klines", "fetch_agg_trades", "fetch_data", "fetch_book_ticker", "fetch_funding_rate", "fetch_trades", "fetch_metrics", "fetch_all_symbols", "SymbolType"]
