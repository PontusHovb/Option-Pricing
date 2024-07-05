import numpy as np
import matplotlib.pyplot as plt

def calculate_payoff(price, options):
    payoff = 0
    for option in options:
        payoff += option.payoff(price)
    return payoff

def show_payoff(strategy, options):
    x = []
    y = []

    x.append(0)
    y.append(calculate_payoff(0, options))
    # Add strike price for all options to plot
    for option in options:
        x.append(option.strike)
        y.append(calculate_payoff(option.strike, options))
        x.append(option.strike*2)
        y.append(calculate_payoff(option.strike*2, options))

    combined = list(zip(x, y))
    combined_sorted = sorted(combined)
    x, y = zip(*combined_sorted)

    plt.plot(x, y, color='blue')
    plt.plot(x, np.zeros(len(x)), 'g--')
    plt.title(f"Payoff for {strategy}")
    plt.xlabel("Price underlying")
    plt.ylabel("Payoff")
    plt.show()
    return ""