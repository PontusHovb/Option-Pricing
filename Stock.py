
class Stock:
    def __init__(self, price):
        self.strike = price

    def payoff(self, price):
        return price - self.strike