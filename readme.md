# Option Pricing
This project focuses on different methods for pricing option, focused on European and American options.

💡 Click on links to find relevant code and/or theory for respective pricing method

### European Options
European options are options that gives the buyer right, but not the obligation to buy (call option) or sell (put option) an underlying asset at a specific price (strike price) _**on a**_ specific date (expiration date). Both [Binomial Model](https://github.com/PontusHovb/Option-Pricing/blob/master/Theory/BinomialModel.md) and [Black-Scholes](https://github.com/PontusHovb/Option-Pricing/blob/master/Theory/BlackScholes.md) are implemented [here](https://github.com/PontusHovb/Option-Pricing/blob/master/EuropeanOptions.py) to calculate price of European options.

### American Options
American options are options that gives the buyer right, but not the obligation to buy (call option) or sell (put option) an underlying asset at a specific price (strike price) _**on or before a**_ specific date (expiration date). [Longstaff Schwartz](https://github.com/PontusHovb/Option-Pricing/blob/master/Theory/LongstaffSchwartz.md) is implemented [here](https://github.com/PontusHovb/Option-Pricing/blob/master/AmericanOptions.py) to calculate price of American options.

## [Trading Strategies](https://github.com/PontusHovb/Option-Pricing/blob/master/TradingStrategies.ipynb)
In this notebook a few of the most popular option trading strategies are implemented (Long Straddle, Covered Call, Bear Put Spread, Long Call Butterfly Spead) showing their respective payoff-functions.
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/TradingStrategies1.png" width="800"/>
</p>
<p align="center"><i>Bear Put Spread (left) and Covered Call (right)</i></p>
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/TradingStrategies2.png" width="800"/>
</p>
<p align="center"><i>Long Straddle (left) and Long Call Butterfly (right)</i></p>

## [Option Theory](https://github.com/PontusHovb/Option-Pricing/blob/master/OptionTheory.ipynb)
In this notebook, some important concepts in option pricing are shown such as convergence of option price in binomial model to Black-Scholes, put-call parity, price of american options compared to european.
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/ConvergenceBinMod.png" width="400"/>
</p>
<p align="center"><i>Convergence of Binomial Model price to Black-Scholes price with increasing no. of steps</i></p>
With smaller timte steps, the option price using binomial model will convergence to the price from Black-Scholes.

<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/GBM.png" width="400"/>
</p>
<p align="center"><i>Example of GBM (Geometric Brownian Motion) outcomes</i></p>
By simulating future possible stock movements (using GBM), Longstaff-Schwartz can calculate optimal exercise timing. Since American options can also be exercised before maturity, the expected value and probability of being in-the-money is higher for American options and hence their price is higher.

<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/AmericanOptionPrice.png" width="400"/>
</p>
<p align="center"><i>Price of American Option compared to European</i></p>

The gap in price increases with time to maturity since this gives American options more time to be exercised in-the-money. Even at shorter maturity and options out-of-money, it holds that American options always are as expensive or more expensive than their European counterparts.
