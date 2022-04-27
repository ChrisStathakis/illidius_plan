import imp


import yfinance as yf
import pandas as pd
import os
from datetime import datetime


class StockData:

    def __init__(self, ticker):
        self.ticker = ticker

    def download_data(self,  start='2010-1-1', end=datetime.today(),):
        ticker = self.ticker
        tickerData = yf.Ticker(ticker)
        df = tickerData.history(period='1d', start=start, end=end)

        df.reset_index(inplace=True)
        df.set_index("Date", inplace=True)
        if not os.path.exists('media/stock_dfs'):
            os.makedirs('media/stock_dfs')
        df.to_csv('media/stock_dfs/{}.csv'.format(ticker))

    def read_data(self, start_date='2010-1-1', end_date=datetime.today()):
        ticker = self.ticker
        self.download_data()
        df = pd.read_csv(f'media/stock_dfs/{ticker}.csv', index_col='Date')

        if 'Stock Splits' in df.columns:
            df.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], 1, inplace=True)
        else:
            df.drop(['Open', 'High', 'Low', 'Volume'], 1, inplace=True)
        df.rename(columns={'Close': ticker}, inplace=True)
        return df

    def get_stock_data(self,  start='2010-1-1', end=datetime.today(), user=None):
        ticker = self.ticker
        tickerData = yf.Ticker(self.ticker)
        df = tickerData.history(period='1d', start=start, end=end)
        df.reset_index(inplace=True)
        df.set_index('Date', inplace=True)
        if 'Stock Splits' in df.columns:
            df.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], 1, inplace=True)
        else:
            df.drop(['Open', 'High', 'Low', 'Volume'], 1, inplace=True)
        df.rename(columns={'Close': ticker}, inplace=True)
        return df