import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

import UserInput

class Option:
    def __init__(self, option_type, asset_price, strike, T, r, div_yield=0, sigma=None, price=None, position_type="long"):
        self.asset_price = asset_price
        self.strike = strike
        self.T = T
        self.r = r
        self.div_yield = div_yield
        self.option_type = option_type
        self.position_type = position_type

        if sigma and not price:
            self.sigma = sigma
            self.price = self.calculate_option_price(self.option_type, self.asset_price, self.strike, self.T, self.r, self.sigma)
        elif price and not sigma:
            self.price = price
            self.sigma = self.calculate_implied_volatility()
        else:
            print("Enter either option price or volatility")
            raise ValueError

    def __str__(self):
        no_elements = 50
        stock_prices = np.linspace(self.asset_price*0.5, self.asset_price*1.5, no_elements)
        time_to_expiration = np.linspace(0, self.T, no_elements)
        option_prices = np.zeros((no_elements, no_elements))

        for i, time in enumerate(time_to_expiration):
            for j, stock_price in enumerate(stock_prices):
                option_prices[i, j] = self.calculate_option_price(stock_price, time, self.option_type)

        S_mesh, T_mesh = np.meshgrid(stock_prices, time_to_expiration)

        # Create plot
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.scatter([self.asset_price], [self.T], [self.calculate_option_price(self.asset_price, self.T, self.option_type)], color='red', s=100)
        ax1.plot_surface(S_mesh, T_mesh, option_prices, cmap='viridis')
        ax1.set_ylim(ax1.get_ylim()[::-1]) 
        ax1.set_xlabel('Stock Price')
        ax1.set_ylabel('Time to Expiration (Years)')
        ax1.set_zlabel('Option Price')
        ax1.set_title('Option Price Surface')
        plt.tight_layout()
        plt.show()

        return f"Price of option is: {round(self.option_price, 3)}"

    def __neg__(self):
        return Option(self.option_type, self.asset_price, self.strike, self.T, self.r, self.div_yield, self.sigma, position_type = "short")
    
    def payoff(self, price):
        if self.position_type == "long":
            return self.exercise_long_position(price) - self.price
        elif self.position_type == "short":
            return -self.exercise_long_position(price) + self.price

    def exercise_long_position(self, price):
        if self.option_type == "call":
            return max(price - self.strike, 0)
        elif self.option_type == "put":
            return max(self.strike - price, 0)
        else:
            return 0

    def calculate_d1(self, asset_price, strike, T, r, sigma):
        return (np.log(asset_price / strike) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
    # TODO: Rewrite
    def calculate_d2(self, asset_price, strike, T, r, sigma):
        d1 = self.calculate_d1(asset_price, strike, T, r, sigma)
        return d1 - sigma * np.sqrt(T)
    
    def calculate_option_price(self, option_type, asset_price, strike, T, r, sigma):
        asset_price = asset_price * np.exp(-self.div_yield * T)
        d1 = self.calculate_d1(asset_price, strike, T, r, sigma)
        d2 = self.calculate_d2(asset_price, strike, T, r, sigma)

        call_price = asset_price * norm.cdf(d1) - strike * np.exp(-r * T) * norm.cdf(d2)    # Calculate call option price

        if option_type == "call":
            return call_price
        elif option_type == "put":
            return self.put_call_parity(asset_price, T, call_price)
    
    def put_call_parity(self, asset_price, T, call_price):
        asset_price = asset_price * np.exp(-self.div_yield * T)
        put_price = self.strike * np.exp(-self.r*T) + call_price - asset_price
        return put_price
    
    def calculate_implied_volatility(self):
        if self.option_type == "call":
            sigma = np.sqrt(2*math.pi / self.T) * (self.price / self.strike)            # Estimate for sigma - Brenner and Subrahmnayam (1988)
        elif self.option_type == "put":
            sigma = 0.2                                                                 # TODO: Estimate for put sigma
        
        # Newton-Raphson
        MAX_ITERATIONS = 1000
        TOLERANCE = 10e-10

        for i in range(0, MAX_ITERATIONS):
            price = self.calculate_option_price(self.option_type, self.asset_price, self.strike, self.T, self.r, sigma)
            vega = self.calculate_vega(self.asset_price, self.strike, self.T, self.r, sigma)
            diff = price - self.price
            if abs(diff) < TOLERANCE:
                return sigma
            sigma = sigma - diff/vega
        return sigma
    
    # TODO: Convert to private functions
    def first_order_greeks(self):
        d1 = self.calculate_d1(self.asset_price, self.strike, self.T, self.r, self.sigma)
        d2 = self.calculate_d2(self.asset_price, self.strike, self.T, self.r, self.sigma)
        delta = self.calculate_delta(d1)
        gamma = self.calculate_gamma(d1)
        vega = self.calculate_vega(self.asset_price, self.strike, self.T, self.r, self.sigma)
        theta = self.calculate_theta(d1, d2)
        rho = self.calculate_rho(d2)
        return delta, gamma, vega, theta, rho
    
    def calculate_delta(self, d1):
        if self.option_type == 'call':
            return norm.cdf(d1)  
        elif self.option_type == 'put':
            return norm.cdf(d1) - 1

    def calculate_gamma(self, d1):
        return norm.pdf(d1) / (self.asset_price * self.sigma * np.sqrt(self.T))
    
    def calculate_vega(self, asset_price, strike, T, r, sigma):
        d1 = self.calculate_d1(asset_price, strike, T, r, sigma)
        return asset_price * norm.pdf(d1) * np.sqrt(T)
    
    def calculate_theta(self, d1, d2):
        if self.option_type == 'call':
            theta = (self.sigma * self.asset_price * norm.pdf(d1)) / (2*np.sqrt(self.T)) + self.r * self.strike * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == 'put':
            theta = (self.sigma * self.asset_price * norm.pdf(d1)) / (2*np.sqrt(self.T)) - self.r * self.strike * np.exp(-self.r * self.T) * norm.cdf(d2)

    def calculate_rho(self, d2):
        if self.option_type == 'call':
            return self.T * self.strike * np.exp(-self.r * self.T) * norm.pdf(d2)  
        elif self.option_type == 'put':
            return - self.T * self.strike * np.exp(-self.r * self.T) * norm.pdf(-d2) 

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

    option = Option(option_type="call", asset_price=100, strike=100, T=0.01, r=0.04, price=1.216645)
    print(option.price)
    print(option.sigma)

if __name__ == '__main__':
    main()