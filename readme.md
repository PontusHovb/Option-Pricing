# Option Pricing
## Binomial Model
<img align="left" width="300" src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/BinomialModel_UnderlyingPrice.png"/>  
Pricing an european option using a $n$-step binomial model is done through the following formula:
$$\pi_i (S_i) = \frac{1}{e^{r \Delta t}} \left( q \pi_{i+1} (S_i \cdot u) + (1 - q) \pi_{i+1}(S_i \cdot d) \right) \quad \text{for i = 0, 1, ..., n - 1}$$
where $\pi_i$ is the price of option and $S_i$ is the price of underlying asset at time step $i$. $u$ is the factor which price rises and $d$ the factor which the price falls. $r$ is the risk-free rate and $\Delta t$ the time (in years) per time step. Lastly, $q$ is the martingale measure.
For last time step (step $n$ in time $T$), the option can be exercised and the value of the option is therefore:
$$\pi_n (S_T) = \phi(S_T)$$ where $\phi$ is the payoff function, positive if the option is in-the-money and 0 otherwise. In a binomial model, the price in next time step can either go up (with a factor $u$) or down (with a factor $d$). 
<br clear="all"/>

## Black-Scholes
<img align="left" width="300" src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/BlackScholes_OptionPrice.png"/>  
Black-Scholes is a well-known formula for pricing of options, and descibes the relation between the input parameters (current stock price, strike price, volatiility, risk-free rate and time to expiration). The plot to the left visualises the relation between underlying stock price, time to expiration and the price of an European call option.
<br clear="all"/>

### European Options
European options are options that gives the buyer right, but not the obligation to buy (call option) or sell (put option) an underlying asset at a specific price (strike price) _**on a**_ specific date (expiration date). 

### American Options
European options are options that gives the buyer right, but not the obligation to buy (call option) or sell (put option) an underlying asset at a specific price (strike price) _**at any point in time before a**_ specific date (expiration date). 
