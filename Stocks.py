import requests
import json
import pandas as pd


def hdframe(f):
    head = ['date','open','low','high','close','volume']
    def handle(*a, **b):
        z = f(*a, **b)
        hold = []
        temp = []
        for i in z:
            temp = []
            for h in head:
                temp.append(i[h])
            hold.append(temp)
        return pd.DataFrame(data=hold, columns=head)
    return handle

def hfframe(f):
    head = ['date','open','high','low','close','adjClose','volume','unadjustedVolume',
            'change','changePercent','vwap','label','changeOverTime']
    def handle(*a, **b):
        z = f(*a, **b)
        hold = []
        temp = []
        for i in z['historical']:
            temp = []
            for j in head:
                temp.append(i[j])
            hold.append(temp)
        return pd.DataFrame(data=hold, columns=head)
    return handle

def hzframe(f):
    def handle(*a, **b):
        z = f(*a, **b)
        head = z[0].keys()
        hold = []
        temp = []
        rep = []
        for i in head:
            temp = []
            for j in z:
                if i == 'date':
                    rep.append(j[i])
                else:
                    temp.append(j[i])
            hold.append(temp)
        head = list(head)
        i = head.index('date')
        del head[i]
        hold = hold[1:]
        return pd.DataFrame(data=hold, index=head, columns=rep)
    return handle
            


class FinModel:

    def __init__(self):
        self.url = 'https://financialmodelingprep.com/'
        self.key = ''

    @hzframe
    def annual_income_statement(self, ticker):
        url = self.url + 'api/v3/income-statement/{}?limit=120&apikey={}'
        return requests.get(url.format(ticker, self.key)).json()

    @hdframe  # inc = 1min; 5min; 15min; 30min; 4hour
    def historical_chart(self, ticker, inc='1min'):
        url = self.url + 'api/v3/historical-chart/{}/{}?apikey={}'
        return requests.get(url.format(inc, ticker, self.key)).json()

    @hfframe
    def historical_price_full(self, ticker):
        url = self.url + '/api/v3/historical-price-full/{}?apikey={}'
        return requests.get(url.format(ticker, self.key)).json()



