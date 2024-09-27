import quantease_binance as qb



def main():
    symbols = qb.fetch_all_symbols(asset_type = "futures/cm")
    for s, i in symbols.items():
        if i.type == "future":
            qb.fetch_data(
                symbol = s,
                data_type="klines",
                asset_type="futures/cm",
                start=i.availableSince,
                end=i.availableTo,
                timeframe="1m",
                use_async=True,
                save_local=True,
            )
    
    
    
if __name__ == '__main__':
    main()
