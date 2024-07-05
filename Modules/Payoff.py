import numpy as np
import matplotlib.pyplot as plt

PLOT_DISTANCE = 10              # Distance between points in plot

def calculate_payoff(price, options):
    payoff = 0
    for option in options:
        payoff += option.payoff(price)
    return payoff

def show_payoff(strategy, options, start, end):
    x = []
    y = []

    # Add strike price for all options to plot
    for option in options:
        x.append(option.strike)
        y.append(calculate_payoff(option.strike, options))
        
    # Add points to plot
    for price in range(start, end, PLOT_DISTANCE):
        x.append(price)
        y.append(calculate_payoff(price, options))

    combined = list(zip(x, y))
    combined_sorted = sorted(combined)
    x, y = zip(*combined_sorted)

    plt.plot(x, y, color='blue')
    plt.plot(x, np.zeros(len(x)), 'g--')
    plt.title(f"Payoff for {strategy}")
    plt.xlabel("Price underlying")
    plt.ylabel("Payoff")
    plt.show()