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
        self.option_price = self.calculate_option_price(self.price, self.T, self.option_type)

    def __str__(self):
        no_elements = 50
        stock_prices = np.linspace(self.price*0.5, self.price*1.5, no_elements)
        time_to_expiration = np.linspace(0, self.T, no_elements)
        option_prices = np.zeros((no_elements, no_elements))

        for i, time in enumerate(time_to_expiration):
            for j, stock_price in enumerate(stock_prices):
                option_prices[i, j] = self.calculate_option_price(stock_price, time, self.option_type)

        S_mesh, T_mesh = np.meshgrid(stock_prices, time_to_expiration)

        # Create plot
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.scatter([self.price], [self.T], [self.calculate_option_price(self.price, self.T, self.option_type)], color='red', s=100)
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

    def calculate_option_price(self, price, T, option_type):
        price = price * np.exp(-self.div_yield * T)
        
        # Calculate d1 and d2 parameters
        d1 = (np.log(price/ self.strike) + (self.r + 0.5 * self.sigma ** 2) * T) / (self.sigma * np.sqrt(T))
        d2 = d1 - self.sigma * np.sqrt(T)

        # Calculate call option price
        call_price = (price* norm.cdf(d1) - self.strike * np.exp(-self.r * T) * norm.cdf(d2))

        if option_type == "call":
            return call_price
        elif option_type == "put":
            return self.put_call_parity(price, T, call_price)
    
    def put_call_parity(self, price, T, call_price):
        price = price * np.exp(-self.div_yield * T)
        put_price = self.strike * np.exp(-self.r*T) + call_price - price
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

    option = Option(100, 100, 3, 0.04, 0.20, 0, "put")
    print(option)

if __name__ == '__main__':
    main()