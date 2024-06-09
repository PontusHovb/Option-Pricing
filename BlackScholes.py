import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import UserInput

class Option:
    def __init__(self, s, K, T, r, sigma, div_yield, option_type):
        self.s = s
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.div_yield = div_yield

        if option_type == "call":
            self.price = self.calculate_option_price()
        elif option_type == "put":
            call_price = self.calculate_option_price()
            self.price = self.put_call_parity(call_price)
        else:
            self.price

    def __str__():
        return ""

    def calculate_option_price(self):
        self.s = self.s * np.exp(-self.div_yield * self.T)
        
        # Calculate d1 and d2 parameters
        d1 = (np.log(self.s / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        print("d1:", round(d1,3), round(norm.cdf(d1),3))
        print("d2:", round(d2,3), round(norm.cdf(d2),3))

        # Calculate call option price
        call_price = (self.s * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        return call_price
    
    def put_call_parity(self, call_price):
        self.s = self.s * np.exp(-self.div_yield * self.T)
        put_price = self.K * np.exp(-self.r*self.T) + call_price - self.s
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