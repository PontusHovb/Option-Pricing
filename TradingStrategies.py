import numpy as np
import matplotlib.pyplot as plt
import Modules.Stock as Stock
import Modules.BinomialModel as BinomialModel
import Modules.BlackScholes as BlackScholes

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

def option(price, strike, vol, rf, T, n, div_yield, option_type, pricing_model):
    if pricing_model == "BinomialModel":
        return BinomialModel.Option(price, strike, vol, rf, T, n, option_type)
    elif pricing_model == "BlackScholes":
        return BlackScholes.Option(price, strike, T, rf, vol, div_yield, option_type)

def long_straddle(price, vol, rf, T, n, pricing_model):
    call = option(price, price, vol, rf, T, n, 0, "call", pricing_model)
    put = option(price, price, vol, rf, T, n, 0, "put", pricing_model)
    return TradingStrategy([call, put], "Long Straddle")

def covered_call(price, vol, rf, T, n, pricing_model):
    stock = Stock.Stock(price)
    call = option(price, price, vol, rf, T, n, 0, "call", pricing_model)
    return TradingStrategy([stock, -call], "Covered Call")

def bear_put_spread(price, vol, rf, T, n, pricing_model):
    put_higher_strike = option(price, price+20, vol, rf, T, n, 0, "put", pricing_model)
    put_lower_strike = option(price, price-20, vol, rf, T, n, 0, "put", pricing_model)
    return TradingStrategy([put_higher_strike, -put_lower_strike], "Bear put Spread")

def long_call_butterfly_spread(price, vol, rf, T, n, pricing_model):
    call_in_the_money = option(price, price-40, vol, rf, T, n, 0, "call", pricing_model)
    call_at_the_money = option(price, price, vol, rf, T, n, 0, "call", pricing_model)
    call_out_of_the_money = option(price, price+40, vol, rf, T, n, 0, "call", pricing_model)
    return TradingStrategy([call_in_the_money, -call_at_the_money, -call_at_the_money, call_out_of_the_money], "Long Call Butterfly Spread")

def main():
    pricing_model = "BinomialModel"
    price = 100
    vol = 0.2
    rf = 0.05
    T = 5
    n = 10

    print(long_straddle(price, vol, rf, T, n, pricing_model))
    print(covered_call(price, vol, rf, T, n, pricing_model))
    print(bear_put_spread(price, vol, rf, T, n, pricing_model))
    print(long_call_butterfly_spread(price, vol, rf, T, n, pricing_model))

if __name__ == "__main__":
    main()