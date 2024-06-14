import numpy as np
import matplotlib.pyplot as plt
import BinomialModel

class TradingStrategy:
    def __init__(self, options, name):
        self.options = options
        self.name = name

    def __str__(self):
        x = []
        y = []

        x.append(0)
        y.append(self.calculate_payoff(0))
        # Add strike price for all options to plot
        for option in self.options:
            x.append(option.strike)
            y.append(self.calculate_payoff(option.strike))
            x.append(option.strike*2)
            y.append(self.calculate_payoff(option.strike*2))

        combined = list(zip(x, y))
        combined_sorted = sorted(combined)
        x, y = zip(*combined_sorted)

        plt.plot(x, y, color='blue')
        plt.plot(x, np.zeros(len(x)), 'g--')
        plt.title(f"Payoff for {self.name}")
        plt.xlabel("Price underlying")
        plt.ylabel("Payoff")
        plt.show()
        return ""

    def calculate_payoff(self, price):
        payoff = 0
        for option in self.options:
            payoff += option.payoff(price)
        
        return payoff
    
def long_straddle(price, vol, rf, T, n):
    call = BinomialModel.Option(price, price, vol, rf, T, n, "call")
    put = BinomialModel.Option(price, price, vol, rf, T, n, "put")
    return TradingStrategy([call, put], "Long Straddle")

def covered_call(price, vol, rf, T, n):
    stock = BinomialModel.Stock(price)
    call = -BinomialModel.Option(price, price, vol, rf, T, n, "call")
    return TradingStrategy([stock, -call], "Covered Call")

def bear_put_spread(price, vol, rf, T, n):
    put_higher_strike = BinomialModel.Option(price, price+20, vol, rf, T, n, "put")
    put_lower_strike = BinomialModel.Option(price, price-20, vol, rf, T, n, "put")
    return TradingStrategy([put_higher_strike, -put_lower_strike], "Bear put Spread")

def long_call_butterfly_spread(price, vol, rf, T, n):
    call_in_the_money = BinomialModel.Option(price, price-40, vol, rf, T, n, "call")
    call_at_the_money = BinomialModel.Option(price, price, vol, rf, T, n, "call")
    call_out_of_the_money = BinomialModel.Option(price, price+40, vol, rf, T, n, "call")
    return TradingStrategy([call_in_the_money, -call_at_the_money, -call_at_the_money, call_out_of_the_money], "Long Call Butterfly Spread")

def main():
    price = 100
    vol = 0.2
    rf = 0.05
    T = 5
    n = 10

    print(long_straddle(price, vol, rf, T, n))
    print(covered_call(price, vol, rf, T, n))
    print(bear_put_spread(price, vol, rf, T, n))
    print(long_call_butterfly_spread(price, vol, rf, T, n))

if __name__ == "__main__":
    main()