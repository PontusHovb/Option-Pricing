
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

GRAPH_DAYS = 500
class Stock:
    def __init__(self, ticker, date=str(date.today())):
        self.ticker = ticker
        self.stock = yf.Ticker(self.ticker)
        self.strike = self.get_close_price(date)

    def __str__(self):
        stock_df = self.get_stock_history(np.datetime64(date.today()), GRAPH_DAYS)
        closing_prices = stock_df['Close'].to_frame(name='Price')
        
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
    
    def get_return(self, start_date, end_date, all_prices):
        try:
            start_price = self.get_close_price(start_date, all_prices)
            end_price = self.get_close_price(end_date, all_prices)
            return end_price / start_price - 1
        except KeyError:
            print(f"Check {self.ticker} between {start_date} and {end_date}")
            return 0
    
    def get_stock_history(self, end_date, days):
        stock_df = self.stock.history(start=str(end_date - days), end=str(end_date), interval='1d')
        return stock_df

    def get_close_price(self, date_str):     
        stock_df = self.get_stock_history(np.datetime64(date_str), 10)                      # To make sure latest trading day is included
        price = stock_df.loc[stock_df.index.max(), 'Close']
        return price
    
    def get_historical_volatility(self, no_days):
        # Calculate daily returns
        stock_df = self.get_stock_history(np.datetime64(date.today()), no_days)
        closing_prices = stock_df['Close'].to_frame(name='Price')
        closing_prices['Daily return'] = closing_prices['Price'] / closing_prices['Price'].shift() - 1
        
        # Calculate historic volatility
        daily_var = closing_prices['Daily return'].var()
        trading_days = len(closing_prices.index)
        return daily_var * np.sqrt(trading_days)

def main():
    stock = Stock('AAPL')
    print(stock)

if __name__ == '__main__':
    main()