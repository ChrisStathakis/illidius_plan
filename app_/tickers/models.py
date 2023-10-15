from django.db import models

import datetime
import time
import numpy as np
import pandas as pd
from .helpers import StockData


class Ticker(models.Model):
    updated = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    ticker = models.CharField(max_length=200, null=True)
    beta = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True)
    coverage = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    market_variance = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    camp = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=30, decimal_places=8, blank=True, null=True, default=0)

    simply_return = models.DecimalField(max_digits=30, decimal_places=8, default=0, help_text='Simply Rate of Return')
    log_return = models.DecimalField(max_digits=30, decimal_places=8, default=0, help_text='Log Return')
    standard_deviation = models.DecimalField(max_digits=30, decimal_places=8, default=0)
    sharp = models.DecimalField(max_digits=30, decimal_places=8, default=0)

    def create_data(self):
        pass

    def update_data(self):
        group = '^GSPC'
        tic = self.ticker
        tickers = [self.ticker, group]
        data = pd.DataFrame()
        for ticker in tickers:
            new_clas = StockData(ticker)
            df = new_clas.read_data()
            data = df if data.empty else data.join(df, how='outer')

        try:
            data['log_return'] = np.log(data[tic] / data[tic].shift(1))
        except:
            return pd.DataFrame.empty
        log_return = (data['log_return'].mean() * 250) * 100
        self.log_return = log_return
        data['simply_return'] = (data[tic] / data[tic].shift(1)) - 1
        simply_return = (data['simply_return'].mean() * 250) * 100

        sec_returns = np.log(data / data.shift(1))
        standard_deviation = sec_returns[tic].std() * 250 ** 0.5
        cov = sec_returns.cov() * 250
        cov_with_market = cov.iloc[0, 1]
        market_var = sec_returns[group].var() * 250
        PG_beta = cov_with_market / market_var
        PG_er = 0.025 + PG_beta * 0.05
        Sharpe = (PG_er - 0.025) / (sec_returns[tic].std() * 250 ** 0.5)

        self.beta = round(float(PG_beta), 4) if isinstance(PG_beta, float) else 0
        self.simply_return = round(float(simply_return), 4) if isinstance(simply_return, float) else 0
        price = round(float(data[tic].iloc[-1]), 8) if isinstance(data[tic].iloc[-1], float) else 0
        if np.isnan(price):
            self.price = 0
            price = 0
        else:
            self.price = 0 if isinstance(price, str) else price

        self.coverage = round(float(cov_with_market), 4) if isinstance(cov_with_market, float) else 0
        self.camp = round(float(PG_er), 4) if isinstance(PG_er, float) else 0
        self.market_variance = round(float(market_var), 4) if isinstance(market_var, float) else 0
        self.standard_deviation = round(standard_deviation, 4) if isinstance(standard_deviation, float) else 0
        self.sharp = round(standard_deviation, 4) if isinstance(Sharpe, float) else 0
        self.updated = datetime.datetime.now()
        time.sleep(2)