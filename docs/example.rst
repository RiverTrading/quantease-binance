Examples
========

This section provides detailed examples of how to use the Quantease Binance package for different types of data collection.

Download Perpetual Futures Data
-----------------------------

This example shows how to download historical data for perpetual futures contracts:

.. code-block:: python

    import os
    import quantease_binance as qb
    from quantease_binance import SymbolType

    output_path = os.path.join(os.getcwd(), "perp_data")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/um")
        for s, i in symbols.items():
            if i.type == SymbolType.PERP:  # Filter for perpetual futures contracts
                try:
                    output_file = os.path.join(output_path, f"{s}.parquet")
                    if not os.path.exists(output_file):
                        df = qb.fetch_data(
                            symbol=s,
                            data_type="klines",
                            asset_type="futures/um",
                            start=i.availableSince,
                            end=i.availableTo,
                            timeframe="1h",
                            use_async=True,
                            save_local=False,
                            limit_rate=2 / 1,  # 2 request per second
                        )
                        df.to_parquet(output_file)
                except Exception as e:
                    print(f"Error: {e}")

Download Spot Data
----------------

Example for downloading spot market historical data:

.. code-block:: python

    import os
    import quantease_binance as qb
    from quantease_binance import SymbolType

    output_path = os.path.join(os.getcwd(), "spot_data")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def main():
        symbols = qb.fetch_all_symbols(asset_type="spot")
        for s, i in symbols.items():
            if i.type == SymbolType.SPOT:
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
                            limit_rate=2 / 1
                        )
                        df.to_parquet(output_file)
                except Exception as e:
                    print(f"Error: {e}")

Download Futures Data
-------------------

Example for downloading futures market data:

.. code-block:: python

    import os
    import quantease_binance as qb
    from quantease_binance import SymbolType

    output_path = os.path.join(os.getcwd(), "future_data")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/cm")
        for s, i in symbols.items():
            if i.type == SymbolType.FUTURE:
                try:
                    output_file = os.path.join(output_path, f"{s}.parquet")
                    if not os.path.exists(output_file):
                        df = qb.fetch_data(
                            symbol=s,
                            data_type="klines",
                            asset_type="futures/cm",
                            start=i.availableSince,
                            end=i.availableTo,
                            timeframe="1h",
                            use_async=True,
                            save_local=False,
                            limit_rate=2 / 1
                        )
                        df.to_parquet(output_file)
                except Exception as e:
                    print(f"Error: {e}") 

Download Funding Rate Data
------------------------

Example for downloading funding rate data for perpetual futures contracts:

.. code-block:: python

    import os
    import quantease_binance as qb
    from quantease_binance import SymbolType

    output_path = os.path.join(os.getcwd(), "funding_data")
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/um")
        for s, i in symbols.items():
            if i.type == SymbolType.PERP:  # Only PERP contracts have funding data
                try:
                    output_file = os.path.join(output_path, f"{s}.parquet")
                    if not os.path.exists(output_file):
                        df = qb.fetch_data(
                            symbol=s,
                            data_type="fundingRate",
                            asset_type="futures/um",
                            start=i.availableSince,
                            end=i.availableTo,
                            use_async=True,
                            save_local=True,
                            limit_rate=1 / 1  # 1 request per second
                        )
                        df.to_parquet(output_file)
                    else:
                        print(f"File {output_file} already exists")
                except Exception as e:
                    print(f"Error: {e}")
