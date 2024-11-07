import quantease_binance as qb
from quantease_binance import SymbolType

def main():
    symbols = qb.fetch_all_symbols(asset_type="futures/um")
    for s, i in symbols.items():
        # In `futures/um`, there are `SymbolType.PERP` and `SymbolType.FUTURE`
        if i.type == SymbolType.PERP:  # Filter for perpetual futures contracts
            try:
                _df = qb.fetch_data(
                    symbol=s,
                    data_type="klines",
                    asset_type="futures/um",
                    start=i.availableSince,
                    end=i.availableTo,
                    timeframe="1h",
                    use_async=True,
                    save_local=True,
                    limit_rate=2 / 1,  # 2 request per second
                )
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
