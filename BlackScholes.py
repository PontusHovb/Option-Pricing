import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import UserInput

class Option:
    def __init__(self, price, strike, T, r, sigma, div_yield, option_type, position_type="long"):
        self.price = price
        self.strike = strike
        self.T = T
        self.r = r
        self.sigma = sigma
        self.div_yield = div_yield
        self.option_type = option_type
        self.position_type = position_type

        if option_type == "call":
            self.option_price = self.calculate_option_price()
        elif option_type == "put":
            call_price = self.calculate_option_price()
            self.option_price = self.put_call_parity(call_price)
        else:
            self.option_price = 0

    def __str__():
        return ""

    def __neg__(self):
        return Option(self.price, self.strike, self.T, self.r, self.sigma, self.div_yield, self.option_type, "short")
    
    def payoff(self, price):
        if self.position_type == "long":
            return self.exercise_long_position(price) - self.option_price
        elif self.position_type == "short":
            return -self.exercise_long_position(price) + self.option_price

    def exercise_long_position(self, price):
        if self.option_type == "call":
            return max(price - self.strike, 0)
        elif self.option_type == "put":
            return max(self.strike - price, 0)
        else:
            return 0

    def calculate_option_price(self):
        self.price = self.price * np.exp(-self.div_yield * self.T)
        
        # Calculate d1 and d2 parameters
        d1 = (np.log(self.price / self.strike) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        # Calculate call option price
        call_price = (self.price * norm.cdf(d1) - self.strike * np.exp(-self.r * self.T) * norm.cdf(d2))
        return call_price
    
    def put_call_parity(self, call_price):
        self.price = self.price * np.exp(-self.div_yield * self.T)
        put_price = self.strike * np.exp(-self.r*self.T) + call_price - self.price
        return put_price

def main():
    """
    s = UserInput.input_float("s: ")
    K = UserInput.input_float("K: ")
    sigma = UserInput.input_percentage("Sigma (%): ")
    r = UserInput.input_percentage("Risk-free (%): ")
    T = UserInput.input_float("T: ")
    div_yield = UserInput.input_percentage("Dividend yield (%): ")
    option_type = UserInput.input_alternative("Type of option (call/put)? ", ["call", "put"])
    option = Option(s, K, T, r, sigma, div_yield, option_type)
    print("\n-------------\n")
    """

    option = Option(100, 100, 5, 0.04, 0.20, 0, "put")
    print("Price of option:", round(option.price, 3))

if __name__ == '__main__':
    main()