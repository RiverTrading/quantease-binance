import quantease_binance as qb
from quantease_binance import SymbolType

qb.config.set_cache_dir(
    "./.cache"
)  # Set the custome cache directory, the default is `./.cache`


def main():
    symbols = qb.fetch_all_symbols(asset_type="spot")
    for s, i in symbols.items():
        # In `futures/um`, there are `SymbolType.PERP` and `SymbolType.FUTURE`
        if i.type == SymbolType.SPOT:  # Filter for perpetual futures contracts
            try:
                _df = qb.fetch_data(
                    symbol=s,
                    data_type="klines",
                    asset_type="spot",
                    start=i.availableSince,
                    end=i.availableTo,
                    timeframe="1h",
                    use_async=True,
                    save_local=True,
                    limit_rate=2 / 1,  # 2 request per second, if set to None, no limit
                )
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
