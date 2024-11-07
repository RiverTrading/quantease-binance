import quantease_binance as qb
from quantease_binance import SymbolType



def main():
    symbols = qb.fetch_all_symbols(asset_type="futures/um")
    for s, i in symbols.items():
        if i.type == SymbolType.PERP:
            _df = qb.fetch_data(
                symbol=s,
                data_type="klines",
                asset_type="futures/um",
                start=i.availableSince,
                end=i.availableTo,
                timeframe="1h",
                use_async=True,
                save_local=True,
            )

if __name__ == "__main__":
    main()
