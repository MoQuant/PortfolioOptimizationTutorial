from Stocks import FinModel
from Crypto import CBSticks


def stocks(tickers):
    fb = FinModel()
    data = {}
    for t in tickers:
        data[t] = fb.historical_price_full(t)
    return data

def crypto(tickers):
    data = {}
    for t in tickers:
        cb = CBSticks(t, 86400)
        data[t] = cb.fetch()
    return data
