import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys

with open('stocks.txt', 'r') as file:
    moduledir = file.read().strip()
if moduledir not in sys.path: 
    sys.path.append(moduledir)
    
import Stocks

class LongstaffSchwartz:
    def __init__(self, option_type, S, K, T, r, sigma, mu):
        self.option_type = option_type
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

        brownian_motion = Stocks.GeometricBrownianMotion(S, mu, sigma, T)
        self.disc_cash_flows = self.calculate_disc_cash_flows(brownian_motion.get_paths(), self.K, self.r)

        final_cfs = np.zeros((self.disc_cash_flows.shape[1], 1), dtype=float)
        for i, row in enumerate(final_cfs):
            final_cfs[i] = sum(self.disc_cash_flows[:, i])
        self.price = np.mean(final_cfs)
    
    def calculate_disc_cash_flows(self, paths, K, r):
        cash_flows = np.zeros_like(paths)
        for i in range(0, cash_flows.shape[0]):
            if self.option_type == "call":
                cash_flows[i] = [max(round(x - K, 2), 0) for x in paths[i]]
            elif self.option_type == "put":
                cash_flows[i] = [max(-round(x - K, 2), 0) for x in paths[i]]

        discounted_cash_flows = np.zeros_like(cash_flows)
        T = cash_flows.shape[0] - 1

        for t in range(1,T):
            in_the_money = paths[t, :] < K

            # Run Regression
            X = (paths[t, in_the_money])
            Xs = np.column_stack([X, X*X])
            Y = cash_flows[t-1, in_the_money] * np.exp(-r)
            model_sklearn = LinearRegression()
            model = model_sklearn.fit(Xs, Y)
            conditional_exp = model.predict(Xs)
            continuations = np.zeros_like(paths[t, :])
            continuations[in_the_money] = conditional_exp

            # If continuation is greater in t = 0, then cash flow in t = 1 is zero
            cash_flows[t, :] = np.where(continuations> cash_flows[t, :], 0, cash_flows[t, :])

            # If stopped ahead of time, subsequent cashflows = 0
            exercised_early = continuations < cash_flows[t, :]
            cash_flows[0:t, :][:, exercised_early] = 0
            discounted_cash_flows[t-1, :] = cash_flows[t-1, :]* np.exp(-r * 3)

        discounted_cash_flows[T-1, :] = cash_flows[T-1, :]* np.exp(-r * 1)
        return discounted_cash_flows

def main():
    option = LongstaffSchwartz(option_type="call", S=100, K=100, T=1, r=0.04, sigma=0.3, mu=0)
    print(option.price)

if __name__ == '__main__':
    main()