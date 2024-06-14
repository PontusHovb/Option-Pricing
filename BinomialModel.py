import math
import matplotlib.pyplot as plt
import UserInput

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
class Option:
    def __init__(self, price, strike, vol, rf, T, n, option_type, position_type="long"):
        self.price = price
        self.strike = strike
        self.vol = vol
        self.rf = rf
        self.T = T
        self.n = n
        self.option_type = option_type
        self.position_type = position_type

        self.calculate_variables()
        self.price_tree = PriceNode(False, self.price, self.u, self.d, self.T, 0, self.delta_t)
        self.option_price = self.option_price(self.option_type, self.price_tree, self.q, self.discount)

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
        return f"Price of option: {round(self.option_price, 2)}"

    def __neg__(self):
        return Option(self.price, self.strike, self.vol, self.rf, self.T, self.n, self.option_type, "short")

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

    def calculate_variables(self):
        self.delta_t = self.T/self.n
        self.u = math.exp(self.vol * math.sqrt(self.delta_t))
        self.d = math.exp(-self.vol * math.sqrt(self.delta_t))
        self.q = (math.exp(self.rf * self.delta_t) - self.d) / (self.u-self.d)
        self.discount = 1 / math.exp(self.rf * self.delta_t)

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

    def option_price(self, option_type, price_node, q, disc):
        if price_node.has_child:
            return disc * (q * self.option_price(option_type, price_node.up_child, q, disc) + (1 - q) * self.option_price(option_type, price_node.down_child, q, disc))
        else:
            return self.exercise_long_position(price_node.price)

def main():
    """
    price = UserInput.input_float("Price [P]? ")
    strike = UserInput.input_float("Strike price [K]? ")
    vol = UserInput.input_percentage("Volatility? (%): ")
    rf = UserInput.input_percentage("Risk-free rate? (%): ")
    T = UserInput.input_float("Maturity [T]? ")
    n = UserInput.input_integer("Number of periods (n-period BinMod)? ")
    option_type = UserInput.input_alternative("Type of option (call/put)? ", ["call", "put"])
    option = Option(price, strike, vol, rf, T, n, option_type)
    """
    option = Option(100, 100, 0.2, 0.05, 5, 10, "call")

    print("\n-----------\n")
    print(option)

if __name__ == "__main__":
    main()
