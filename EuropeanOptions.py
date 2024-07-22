import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt

import Modules.UserInput

POINTS_IN_BS_PLOT = 50

# Newton-Raphson for estimating implied volatility
MAX_ITERATIONS = 1000
TOLERANCE = 10e-10

class PriceNode:
    def __init__(self, parent_node, price, u, d, T, time, delta_t):
        self.price = price
        self.u = u
        self.d = d
        self.T = T
        self.time = time
        self.delta_t = delta_t

        self.parent_node = parent_node
        self.create_children()
    
    def create_children(self):
        if self.time < self.T:
            self.has_child = True
            self.up_child = PriceNode(self, self.price * self.u, self.u, self.d, self.T, self.time + self.delta_t, self.delta_t)
            self.down_child = PriceNode(self, self.price * self.d, self.u, self.d, self.T, self.time + self.delta_t, self.delta_t)
        else:
            self.has_child = False
            self.up_child = False
            self.down_child = False

class BinomialModel:
    """ 
    Parameters
        option_type: Type of option (put/call)
        S: Price of underlying asset
        K: Strike price
        T: Time until expiration [years]
        R: Risk-free interest rate
        sigma: Volatility (standard deivation) of unerlying asset
        n: Number of time steps
        position_type: Type of position (long/short)
    """
    def __init__(self, option_type, S, K, T, r, sigma, n, position_type="long"):
        self.option_type = option_type
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.n = n
        self.position_type = position_type

        self.delta_t = self.T/self.n
        self.u = math.exp(self.sigma * math.sqrt(self.delta_t))
        self.d = math.exp(-self.sigma * math.sqrt(self.delta_t))
        self.q = (math.exp(self.r * self.delta_t) - self.d) / (self.u-self.d)
        self.discount = 1 / math.exp(self.r * self.delta_t)

        self.price_tree = PriceNode(False, self.S, self.u, self.d, self.T, 0, self.delta_t)
        self.price = self.calculate_price(self.option_type, self.price_tree, self.q, self.discount)

    def __str__(self):
        self.x = []
        self.y = []
        self.create_price_tree(self.price_tree)

        for xi, yi in zip(self.x, self.y):
            plt.plot(xi, yi, color='blue')

        plt.title("Binomial Model")
        plt.xlabel("Time (years)")
        plt.ylabel("Price underlying")
        plt.show()
        return f"Price of option: {round(self.price, 2)}"

    def __neg__(self):
        return BinomialModel(self.option_type, self.S, self.K, self.T, self.r, self.sigma, self.n, position_type="short")

    def payoff(self, S):
        if self.position_type == "long":
            return self.exercise_long_position(S) - self.price
        elif self.position_type == "short":
            return -self.exercise_long_position(S) + self.price

    def exercise_long_position(self, price):
        if self.option_type == "call":
            return max(price - self.K, 0)
        elif self.option_type == "put":
            return max(self.K - price, 0)
        else:
            return 0

    def create_price_tree(self, price_node):
        if price_node.has_child:
            # Up edge
            self.x.append([price_node.time, price_node.time + price_node.delta_t])
            self.y.append([price_node.price, price_node.up_child.price])

            # Down edge
            self.x.append([price_node.time, price_node.time + price_node.delta_t])
            self.y.append([price_node.price, price_node.down_child.price])

            # Recursive call
            self.create_price_tree(price_node.up_child)
            self.create_price_tree(price_node.down_child)

    def calculate_price(self, option_type, price_node, q, disc):
        if price_node.has_child:
            return disc * (q * self.calculate_price(option_type, price_node.up_child, q, disc) + (1 - q) * self.calculate_price(option_type, price_node.down_child, q, disc))
        else:
            return self.exercise_long_position(price_node.price)

class BlackScholes:
    """ 
    Parameters
        option_type: Type of option (put/call)
        S: Price of underlying asset
        K: Strike price
        T: Time until expiration [years]
        R: Risk-free interest rate
        sigma: Volatility (standard deivation) of unerlying asset
        div_yield: Continuous dividend yield
        price: Price of option
        position_type: Type of position (long/short)
    """
    def __init__(self, option_type, S, K, T, r, div_yield=0, sigma=None, price=None, position_type="long"):
        self.option_type = option_type
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.div_yield = div_yield
        self.position_type = position_type

        # Calculating implied volatility or option price depending on input parameters
        if sigma and not price:
            self.sigma = sigma
            self.price = self.calculate_option_price(self.option_type, self.S, self.K, self.T, self.r, self.sigma)
        elif price and not sigma:
            self.price = price
            self.sigma = self.calculate_implied_volatility()
        else:
            print("Enter either option price or volatility")
            raise ValueError

    def __str__(self):
        asset_prices = np.linspace(self.S*0.5, self.S*1.5, POINTS_IN_BS_PLOT)
        time_to_expiration = np.linspace(0, self.T, POINTS_IN_BS_PLOT)
        option_prices = np.zeros((POINTS_IN_BS_PLOT, POINTS_IN_BS_PLOT))

        for i, time in enumerate(time_to_expiration):
            for j, asset_price in enumerate(asset_prices):
                option_prices[i, j] = self.calculate_option_price(self.option_type, asset_price, self.K, time, self.r, self.sigma)

        S_mesh, T_mesh = np.meshgrid(asset_prices, time_to_expiration)

        # Create plot
        fig = plt.figure(figsize=(10, 6))
        ax1 = fig.add_subplot(111, projection='3d')
        ax1.scatter([self.S], [self.T], [self.calculate_option_price(self.option_type, self.S, self.K, self.T, self.r, self.sigma)], color='red', s=100)
        ax1.plot_surface(S_mesh, T_mesh, option_prices, cmap='viridis')
        ax1.set_ylim(ax1.get_ylim()[::-1]) 
        ax1.set_xlabel('Stock Price')
        ax1.set_ylabel('Time to Expiration (Years)')
        ax1.set_zlabel('Option Price')
        ax1.set_title('Option Price Surface')
        plt.tight_layout()
        plt.show()

        return f"Price of option is: {round(self.price, 3)}"

    def __neg__(self):
        if self.position_type == "long":
            return BlackScholes(self.option_type, self.S, self.K, self.T, self.r, self.div_yield, sigma=self.sigma, position_type = "short")
        elif self.position_type == "short":
            return BlackScholes(self.option_type, self.S, self.K, self.T, self.r, self.div_yield, sigma=self.sigma, position_type = "long")

    def payoff(self, price):
        if self.position_type == "long":
            return self.exercise_long_position(price) - self.price
        elif self.position_type == "short":
            return -self.exercise_long_position(price) + self.price

    def exercise_long_position(self, price):
        if self.option_type == "call":
            return max(price - self.K, 0)
        elif self.option_type == "put":
            return max(self.K - price, 0)
        else:
            return 0

    def d1(self, S, K, T, r, sigma):
        return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        
    def d2(self, S, K, T, r, sigma):
        return self.d1(S, K, T, r, sigma) - sigma * np.sqrt(T)
    
    def calculate_option_price(self, option_type, S, K, T, r, sigma):
        S = S * np.exp(-self.div_yield * T)
        _d1 = self.d1(S, K, T, r, sigma)
        _d2 = self.d2(S, K, T, r, sigma)

        if option_type == "call":
            return S * norm.cdf(_d1) - K * np.exp(-r * T) * norm.cdf(_d2)
        elif option_type == "put":
            return K * np.exp(-r * T) * norm.cdf(-_d2) - S * norm.cdf(-_d1)
    
    def calculate_implied_volatility(self):
        if self.option_type == "call":
            sigma = np.sqrt(2*math.pi / self.T) * (self.price / self.K)            # Estimate for sigma - Brenner and Subrahmnayam (1988)
        elif self.option_type == "put":
            sigma = 0.2                                                            # TODO: Estimate for put sigma
        
        # Newton-Raphson
        for _ in range(0, MAX_ITERATIONS):
            price = self.calculate_option_price(self.option_type, self.S, self.K, self.T, self.r, sigma)
            vega = self.calculate_vega(self.S, self.K, self.T, self.r, sigma)
            diff = price - self.price
            if abs(diff) < TOLERANCE:
                return sigma
            sigma = sigma - diff/vega
        return sigma
    
    def first_order_greeks(self):
        delta = self.calculate_delta(self.S, self.K, self.T, self.r, self.sigma)
        gamma = self.calculate_gamma(self.S, self.K, self.T, self.r, self.sigma)
        vega = self.calculate_vega(self.S, self.K, self.T, self.r, self.sigma)
        theta = self.calculate_theta(self.S, self.K, self.T, self.r, self.sigma)
        rho = self.calculate_rho(self.S, self.K, self.T, self.r, self.sigma)
        return delta, gamma, vega, theta, rho
    
    def calculate_delta(self, S, K, T, r, sigma):
        if self.option_type == 'call':
            return norm.cdf(self.d1(S, K, T, r, sigma))  
        elif self.option_type == 'put':
            return norm.cdf(self.d1(S, K, T, r, sigma)) - 1

    def calculate_gamma(self, S, K, T, r, sigma):
        return norm.pdf(self.d1(S, K, T, r, sigma)) / (S * sigma * np.sqrt(T))
    
    def calculate_vega(self, S, K, T, r, sigma):
        return S * norm.pdf(self.d1(S, K, T, r, sigma)) * np.sqrt(T)
    
    def calculate_theta(self, S, K, T, r, sigma):
        if self.option_type == 'call':
            return (sigma * S * norm.pdf(self.d1(S, K, T, r, sigma))) / (2*np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(self.d2(S, K, T, r, sigma))
        elif self.option_type == 'put':
            return (sigma * S * norm.pdf(self.d1(S, K, T, r, sigma))) / (2*np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(self.d2(S, K, T, r, sigma))

    def calculate_rho(self, S, K, T, r, sigma):
        if self.option_type == 'call':
            return T * K * np.exp(-r * T) * norm.pdf(self.d2(S, K, T, r, sigma))  
        elif self.option_type == 'put':
            return - T * K * np.exp(-r * T) * norm.pdf(-self.d2(S, K, T, r, sigma)) 

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

    option_bs = BlackScholes(option_type="call", S=100, K=100, T=1, r=0.04, sigma=0.3)
    print(option_bs.price)

    option_binomial = BinomialModel(option_type="call", S=100, K=100, T=1, r=0.04, sigma=0.3, n=12)
    print(option_binomial.price)

if __name__ == '__main__':
    main()


