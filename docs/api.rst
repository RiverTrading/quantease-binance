API Documentation
=================

fetch_klines
------------

.. py:function:: fetch_klines(symbol, start, end, timeframe='1m', asset_type='spot', tz=None)

   Convenience function to fetch Kline data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str timeframe: Kline interval. Default is "1m".
   :param str asset_type: Asset type for the data request. Default is "spot".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``open``, ``high``, ``low``, ``close``, ``volume``, ``trades``, ``close_datetime`` columns.
   :rtype: DataFrame

fetch_trades
------------

.. py:function:: fetch_trades(symbol, start, end, asset_type='spot', tz=None)

   Convenience function to fetch trade data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str asset_type: Asset type for the data request. Default is "spot".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``id``, ``price``, ``qty``, ``quoteQty``, ``time``, ``isBuyerMaker``, ``isBestMatch`` columns.
   :rtype: DataFrame

fetch_agg_trades
----------------

.. py:function:: fetch_agg_trades(symbol, start, end, asset_type='spot', tz=None)

   Convenience function to fetch aggregate trade data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str asset_type: Asset type for the data request. Default is "spot".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``id``, ``price``, ``qty``, ``firstTradeId``, ``lastTradeId``, ``time``, ``isBuyerMaker``, ``isBestMatch`` columns.
   :rtype: DataFrame

fetch_book_ticker
-----------------

.. py:function:: fetch_book_ticker(symbol, start, end, asset_type='spot', tz=None)

   Convenience function to fetch book ticker data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str asset_type: Asset type for the data request. Default is "spot".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``symbol``, ``bidPrice``, ``bidQty``, ``askPrice``, ``askQty``, ``time`` columns.
   :rtype: DataFrame

fetch_funding_rate
------------------

.. py:function:: fetch_funding_rate(symbol, start, end, asset_type, tz=None)

   Convenience function to fetch funding rate data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str asset_type: Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``symbol``, ``fundingRate``, ``fundingTime`` columns.
   :rtype: DataFrame

fetch_metrics
-------------

.. py:function:: fetch_metrics(symbol, start, end, asset_type, tz=None)

   Convenience function to fetch metrics data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str/datetime start: Start time for the data request.
   :param str/datetime end: End time for the data request.
   :param str asset_type: Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is None.
   :return: A pandas DataFrame containing ``symbol``, ``openInterest``, ``numberOfTrades``, ``volume``, ``quoteVolume``, ``takerBuyBaseAssetVolume``, ``takerBuyQuoteAssetVolume``, ``openTime``, ``closeTime`` columns.
   :rtype: DataFrame

fetch_data
----------

.. py:function:: fetch_data(symbol, asset_type, data_type, start, end, tz='UTC', timeframe=None)

   Main function to fetch data.

   :param str symbol: Binance market pair name, e.g., "BTCUSDT".
   :param str asset_type: Asset type for the data request. Must be one of "spot", "futures/um", or "futures/cm".
   :param str data_type: Type of data to request. Must be one of "klines", "aggTrades", "bookTicker", "fundingRate", "metrics".
   :param datetime start: Start time for the data request.
   :param datetime end: End time for the data request.
   :param str tz: Timezone for the returned DataFrame's datetime parameters. Default is "UTC".
   :param str timeframe: Kline interval. Default is None.
   :param bool use_async: Whether to use asynchronous requests. Default is False. It would increase the speed of the data fetching process but may cause issues with the Binance API rate limits.
   :param bool save_local: Whether to save the fetched data locally. Default is False. The data will be saved in the ``.cache`` directory.
   :return: A pandas DataFrame containing the requested data.
   :rtype: DataFrame

fetch_all_symbols
-----------------

.. py:function:: fetch_all_symbols(exchange=config.EXCHANGE, asset_type='spot')

   Function to fetch all trading pairs from the Binance exchange.

   :param object exchange: Exchange object initialized using the ccxt library. Default is ``config.EXCHANGE``.
   :param str asset_type: Asset type for the trading pairs to fetch. Must be one of "spot", "futures/um", or "futures/cm". Default is "spot".
   :return: List of trading pair IDs based on the specified ``asset_type``.
   :rtype: List[str]
