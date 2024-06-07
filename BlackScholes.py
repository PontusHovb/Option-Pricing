import numpy as np
from scipy.stats import norm
import UserInput

s = UserInput.input_float("s: ")
K = UserInput.input_float("K: ")
sigma = UserInput.input_percentage("Sigma (%): ")
r = UserInput.input_percentage("Risk-free (%): ")
T = UserInput.input_float("T: ")
div_yield = UserInput.input_percentage("Dividend yield (%): ")
print("\n-------------\n")

def black_scholes(s, K, T, r, sigma, div_yield):
    s = s * np.exp(-div_yield * T)
    # Calculate d1 and d2 parameters
    d1 = (np.log(s / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    print("d1:", round(d1,3), round(norm.cdf(d1),3))
    print("d2:", round(d2,3), round(norm.cdf(d2),3))

    # Calculate call option price
    call_price = (s * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    return call_price
    
def put_call_parity(call_price, s, K, T, r, div_yield):
    s = s * np.exp(-div_yield * T)
    put_price = K * np.exp(-r*T) + call_price - s
    return put_price

call_price = black_scholes(s, K, T, r, sigma, div_yield)
put_price = put_call_parity(call_price, s, K, T, r, div_yield)
print("Price of call option: ", round(call_price, 3))
print("Price of put option: ", round(put_price, 3))