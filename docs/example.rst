Examples
========

This section provides detailed examples of how to use the Quantease Binance package for different types of data collection.

Download Perpetual Futures Data
-----------------------------

This example shows how to download historical data for perpetual futures contracts:

.. code-block:: python

    import quantease_binance as qb
    from quantease_binance import SymbolType

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/um")
        for s, i in symbols.items():
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

Download Spot Data
----------------

Example for downloading spot market historical data:

.. code-block:: python

    import quantease_binance as qb
    from quantease_binance import SymbolType

    qb.config.set_cache_dir("./.cache")  # Set the custom cache directory

    def main():
        symbols = qb.fetch_all_symbols(asset_type="spot")
        for s, i in symbols.items():
            if i.type == SymbolType.SPOT:
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
                        limit_rate=2 / 1
                    )
                except Exception as e:
                    print(f"Error: {e}")

Download Futures Data
-------------------

Example for downloading futures market data:

.. code-block:: python

    import quantease_binance as qb
    from quantease_binance import SymbolType

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/cm")
        for s, i in symbols.items():
            if i.type == SymbolType.FUTURE:
                try:
                    _df = qb.fetch_data(
                        symbol=s,
                        data_type="klines",
                        asset_type="futures/cm",
                        start=i.availableSince,
                        end=i.availableTo,
                        timeframe="1h",
                        use_async=True,
                        save_local=True,
                        limit_rate=2 / 1
                    )
                except Exception as e:
                    print(f"Error: {e}")

Download Funding Rate Data
------------------------

Example for downloading funding rate data for perpetual futures contracts:

.. code-block:: python

    import quantease_binance as qb
    from quantease_binance import SymbolType

    def main():
        symbols = qb.fetch_all_symbols(asset_type="futures/um")
        for s, i in symbols.items():
            if i.type == SymbolType.PERP:  # Only PERP contracts have funding data
                try:
                    _df = qb.fetch_data(
                        symbol=s,
                        data_type="fundingRate",
                        asset_type="futures/um",
                        start=i.availableSince,
                        end=i.availableTo,
                        use_async=True,
                        save_local=True,
                        limit_rate=1 / 1  # 1 request per second
                    )
                except Exception as e:
                    print(f"Error: {e}")

Note: If `save_local` is enabled (set to `True`), all data will be automatically saved in the specified cache directory.
