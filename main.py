import binance_history as bh


# agg_trades = bh.fetch_agg_trades(
#             symbol='BTCUSDT',
#             start = '2024-01-01',
#             end = '2024-05-01',
#             asset_type='spot',
#             tz='UTC'
#         )
# print(agg_trades)

# book_ticker = bh.fetch_book_ticker(
#     symbol='AAVEUSD_PERP',
#     start='2024-01-01',
#     end='2024-02-01',
#     asset_type='futures/cm',
#     tz='UTC'
# )

# print(book_ticker)

# funding_rate = bh.fetch_funding_rate(
#     symbol = 'BTCUSDT',
#     start = '2024-01-01',
#     end = '2024-07-01',
#     asset_type = 'futures/um',
#     tz = 'UTC'
# )

# print(funding_rate)

# trade = bh.fetch_trades(
#     symbol = 'ETHUSDT',
#     start = '2024-05-01',
#     end = '2024-07-01',
#     asset_type = 'spot',
#     tz = 'UTC'
# )

# print(trade)

# klines = bh.fetch_klines(
#     symbol='ETHUSDT',
#     start='2018-01-01',
#     end='2024-07-12',
#     timeframe='1m',
#     asset_type='spot',
#     tz='UTC'
# )
# print(klines)

metrics = bh.fetch_metrics(
    symbol = 'BTCUSDT',
    start = '2024-01-01',
    end = '2024-04-01',
    asset_type = 'futures/um',
    tz='UTC'
)
print(metrics)