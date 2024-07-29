# Black-Scholes
Black-Scholes is a well-known formula for pricing of european options, and descibes the relation between the input parameters (current stock price $`S_0`$, strike price $`K`$, volatility $`\sigma`$, risk-free rate $`r`$ and time to expiration $`T`$).

### Volatility surface
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/BlackScholes_VolatilitySurface" width="400"/>
</p>
<p align="center"><i>Volatility surface for Black-Scholes</i></p>

Since all components except volatility are known to all market actors, the Black-Scholes model can be used to find the implied volatility for options whose price is known. This can show the relation between key variables (strike and time to maturity) and the implied volatility for the current price as shown in the plot above.

### Key Components and Assumptions
- **Stock Price Dynamics:** The Black-Scholes model assumes that the stock price follows a geometric Brownian motion with constant drift and volatility. This can be expressed (where $`S_t`$ is the stock price at time $`t`$, $`\mu`$ is the drift rate, $`\sigma`$ is the volatility, and $`W_t`$ is a Brownian motion) as:
``` math
d S_t = \mu S_t dt + \sigma S_t dW_t
``` 
- **Risk-Free Rate:** The risk-free rate $`r`$ is assumed to be constant over the life of the option.
- **No Dividends:** Black-Scholes model assumes that the stock does not pay any dividends during the option's life. Extensions to the model can incorporate dividends.
- **European Option:** The model can be used to calculate the price of both call and put options, but only European options which can only be exercised at maturity.
- **Market Efficiency:** The Black-Scholes model assumes that markets are efficient, meaning that prices reflect all available information, and there are no arbitrage opportunities.
