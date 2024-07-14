from pathlib import Path
import ccxt
# CACHE_DIR = Path.home() / ".binance-history"
CACHE_DIR = Path.cwd() / ".cache"
EXCHANGE = ccxt.binance()