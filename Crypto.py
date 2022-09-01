import requests
import json
import time
import datetime
import pandas as pd



class CBSticks:

    #granularity_list = [60, 300, 900, 3600, 21600, 86400]

    def __init__(self, ticker, granularity, fetches=4):
        self.ticker = ticker
        self.fetches = fetches
        self.granularity = granularity
        self.url = 'https://api.exchange.coinbase.com/products/{}/candles?granularity={}&start={}&end={}'
        self.dt = self.pre_run()

    def pre_run(self):
        url = 'https://api.exchange.coinbase.com/products/{}/candles?granularity={}'
        r = requests.get(url.format(self.ticker, self.granularity)).json()
        dt = r[0][0] - r[-1][0]
        return dt

    def fetch(self):
        hold = []
        t1 = int(time.time())
        t0 = t1 - self.dt

        for i in range(self.fetches):
            T0, T1 = self.ctime(t0), self.ctime(t1)
            #print('Time Range: ',T0, T1)
            r = requests.get(self.url.format(self.ticker,
                                             self.granularity,
                                             T0,
                                             T1)).json()
            hold += r
            t1 -= self.dt
            t0 -= self.dt
            time.sleep(1)
        
        for i in range(len(hold)):
            hold[i][0] = self.dtime(hold[i][0])
        print("Crypto Fetched")
        return pd.DataFrame(data=hold, columns=['Time','Low','High','Open','Close','Volume'])
            
    def ctime(self, x):
        return datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%dT%H:%M:%SZ')

    def dtime(self, x):
        return datetime.datetime.fromtimestamp(x).strftime('%m-%d-%Y %H:%M:%S')
    



