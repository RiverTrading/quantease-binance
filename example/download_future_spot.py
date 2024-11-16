import quantease_binance as qb
from quantease_binance import SymbolType
import pandas as pd

qb.config.set_cache_dir(
    "./.cache"
)  # Set the custome cache directory, the default is `./.cache`


def main():
    spots = qb.fetch_all_symbols(asset_type="spot")
    futures = qb.fetch_all_symbols(asset_type="futures/um")
    
    spots = {s: i for s, i in spots.items() if i.active}
    futures = {s: i for s, i in futures.items() if i.active}
    
    symbols = list(set(spots.keys()) & set(futures.keys()))
    
    dfs_spot = []
    dfs_future = []
    
    for s in symbols:
            try:
                df_spot = qb.fetch_data(
                    symbol=s,
                    data_type="klines",
                    asset_type="spot",
                    start=max(pd.Timestamp("2024-08-24", tz="UTC"), spots[s].availableSince),
                    end=spots[s].availableTo,
                    timeframe="1m",
                    use_async=True,
                    save_local=True,
                    limit_rate=None,  # 2 request per second, if set to None, no limit
                )
                df_spot["symbol"] = s
                dfs_spot.append(df_spot)
                
                df_future = qb.fetch_data(
                    symbol=s,
                    data_type="klines",
                    asset_type="futures/um",
                    start=max(pd.Timestamp("2024-08-24", tz="UTC"), futures[s].availableSince),
                    end=futures[s].availableTo,
                    timeframe="1m",
                    use_async=True,
                    save_local=True,
                    limit_rate=None,  # 2 request per second, if set to None, no limit
                )
                df_future["symbol"] = s
                dfs_future.append(df_future)
                
            except Exception as e:
                print(f"Error: {e}")
    
    df_spot = pd.concat(dfs_spot)
    df_future = pd.concat(dfs_future)
    
    df_spot = pd.pivot_table(df_spot, index="datetime", columns="symbol", values="close")
    df_future = pd.pivot_table(df_future, index="datetime", columns="symbol", values="close")
    
    df_spot.to_parquet("spot.parquet")
    df_future.to_parquet("future.parquet")


if __name__ == "__main__":
    main()
