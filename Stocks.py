
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

GRAPH_DAYS = 500
MAX_DAYS_STOCK_HISTORY = 10

GBG_TIME_STEP = 0.1
GBG_NUM_PATHS = 50

class Stock:
    def __init__(self, ticker, date=str(date.today())):
        self.ticker = ticker
        self.stock = yf.Ticker(self.ticker)
        self.as_of_date = date
        self.price = self.get_close_price(date)

    def __str__(self):
        closing_prices = self.get_close_prices(np.datetime64(self.as_of_date), GRAPH_DAYS)
        
        plt.figure(figsize=(9, 6))
        plt.plot(closing_prices.index, closing_prices, label="Price")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title(f"{self.stock.info.get('longName')} Stock Price (Past {GRAPH_DAYS} Days)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        return "\n"*3

    def payoff(self, price):
        return price - self.strike
    
    def get_return(self, start_date, end_date):
        try:
            start_price = self.get_close_price(start_date)
            end_price = self.get_close_price(end_date)
            return end_price / start_price - 1
        except KeyError:
            print(f"Check {self.ticker} between {start_date} and {end_date}")
            return 0
    
    def get_close_prices(self, end_date, no_days):
        stock_df = self.stock.history(start=str(np.datetime64(end_date) - no_days), end=str(end_date), interval='1d')
        return stock_df[['Close']].rename(columns={'Close': 'Price'})
    
    def get_daily_returns(self, end_date, no_days):
        close_prices = self.get_close_prices(end_date, no_days)
        return close_prices.pct_change().dropna()

    def get_close_price(self, date): 
        stock_df = self.get_close_prices(date, MAX_DAYS_STOCK_HISTORY)
        return stock_df.loc[stock_df.index.max(), 'Price']
      
    def mu(self, no_days):
        daily_returns = self.get_daily_returns(self.as_of_date, no_days)
        return daily_returns.mean().iloc[0]
    
    def vol(self, no_days):
        daily_returns = self.get_daily_returns(self.as_of_date, no_days)
        no_trading_days = len(daily_returns.index)
        return np.sqrt(daily_returns.var() * np.sqrt(no_trading_days)).iloc[0]

class GeometricBrownianMotion:
    def __init__(self, S0, mu, sigma, T, delta_t=GBG_TIME_STEP, no_paths=GBG_NUM_PATHS):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma

        self.num_steps = int(T / delta_t) + 1
        self.num_paths = no_paths
        self.times = np.linspace(0, T, self.num_steps)
        self.paths = np.zeros((self.num_steps, self.num_paths))

    def get_paths(self):
        self.paths[0] = self.S0

        for i in range(self.num_paths):
            dW = np.random.normal(0, np.sqrt(GBG_TIME_STEP), self.num_steps - 1)
            cumulative_dW = np.cumsum(dW)
            self.paths[1:, i] = self.S0 * np.exp((self.mu - 0.5 * self.sigma**2) * self.times[1:] + self.sigma * cumulative_dW)

        return self.paths
    
def main():
    stock = Stock('AAPL')
    #print(stock)

    brownian_motion = GeometricBrownianMotion(stock.price, stock.mu(365), stock.vol(365), 1)
    print(brownian_motion.get_paths()[:, 1])
    print(brownian_motion.get_paths()[:, 2])

if __name__ == '__main__':
    main()