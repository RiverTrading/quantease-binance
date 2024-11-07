Quick Start Guide
=================

Installation
------------

`quantease-binance` can be installed using `pip`:

.. code-block:: bash

   pip install quantease-binance

Usage Examples
--------------

Fetch All Trading Pairs
^^^^^^^^^^^^^^^^^^^^^^^

To fetch all trading pairs from the Binance exchange, you can use the ``fetch_all_symbols`` function:

.. code-block:: python

   import quantease_binance as qb

   symbols = qb.fetch_all_symbols()
   print(symbols)

This will return a list of trading pairs based on the specified ``asset_type``. By default, ``asset_type`` is set to "spot". If you want to get trading pairs for perpetual contracts, specify ``asset_type`` as "futures/um" or "futures/cm". The return type is `Dict[str, Symbol]` where the key is the trading pair and the value is an instance of the `Symbol` class.

Fetch Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   data = qb.fetch_data(
       symbol=s,
       data_type="klines",
       asset_type="futures/cm",
       start=i.availableSince,
       end=i.availableTo,
       timeframe="1m",
       use_async=True,
       save_local=True,
       limit_rate=2/1,  # 2 requests per second
   )
    

Fetch Aggregate Trade Data
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   agg_trades = qb.fetch_agg_trades(
       symbol='BTCUSDT',
       start='2024-01-01',
       end='2024-05-01',
       asset_type='spot',
       tz='UTC'
   )
   print(agg_trades)

Fetch Book Ticker Data
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   book_ticker = qb.fetch_book_ticker(
       symbol='AAVEUSD_PERP',
       start='2024-01-01',
       end='2024-02-01',
       asset_type='futures/cm',
       tz='UTC'
   )
   print(book_ticker)

Fetch Funding Rate Data
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   funding_rate = qb.fetch_funding_rate(
       symbol='ETHUSDT',
       start='2019-01-01',
       end='2024-07-01',
       asset_type='futures/um',
       tz='UTC'
   )
   print(funding_rate)

Fetch Trade Data
^^^^^^^^^^^^^^^^

.. code-block:: python

   trade = qb.fetch_trades(
       symbol='ETHUSDT',
       start='2024-05-01',
       end='2024-07-10',
       asset_type='spot',
       tz='UTC'
   )
   print(trade)

Fetch Kline Data
^^^^^^^^^^^^^^^^

.. code-block:: python

   klines = qb.fetch_klines(
       symbol='BTCUSDT',
       start='2018-01-01',
       end='2024-07-12',
       timeframe='1m',
       asset_type='spot',
       tz='UTC'
   )
   print(klines)

Fetch Metrics Data
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   metrics = qb.fetch_metrics(
       symbol='BTCUSDT',
       start='2024-01-01',
       end='2024-04-01',
       asset_type='futures/um',
       tz='UTC'
   )
   print(metrics)

Make sure to replace the placeholders for ``symbol``, ``start``, ``end``, and other parameters as needed.
