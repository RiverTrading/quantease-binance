import os
import quantease_binance as qb
from quantease_binance import SymbolType


output_path = os.path.join(os.getcwd(), "spot_data")

if not os.path.exists(output_path):
    os.makedirs(output_path)


def main():
    symbols = qb.fetch_all_symbols(asset_type="spot")
    for s, i in symbols.items():
        # In `futures/um`, there are `SymbolType.PERP` and `SymbolType.FUTURE`
        if i.type == SymbolType.SPOT:  # Filter for perpetual futures contracts
            try:
                output_file = os.path.join(output_path, f"{s}.parquet")
                if not os.path.exists(output_file):
                    df = qb.fetch_data(
                        symbol=s,
                        data_type="klines",
                        asset_type="spot",
                        start=i.availableSince,
                        end=i.availableTo,
                        timeframe="1h",
                        use_async=True,
                        save_local=False,
                        limit_rate=2 / 1,  # 2 request per second
                    )
                    df.to_parquet(output_file)
                else:
                    print(f"File {output_file} already exists")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
