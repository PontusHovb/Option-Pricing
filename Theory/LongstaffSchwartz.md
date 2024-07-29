# Longstaff Schwartz
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/LongstaffSchwartz_Paths.png" width="400"/>
</p>
<p align="center"><i>Simulated paths for Longstaff-Schwartz method</i></p>
The Longstaff-Schwartz method is a powerful technique for pricing American options, which can be exercised at any time before expiration. 
Unlike European options, which have closed-form solutions under certain models like Black-Scholes, American options require more complex approaches due to their early exercise feature. 
The Longstaff-Schwartz method leverages Monte Carlo simulation combined with least squares regression to estimate the option price.

### Key Concepts and Methodology
- **American Option Characteristics:** American options differ from European options in that they can be exercised at any time before expiration, providing additional flexibility to the holder. This feature makes American options more valuable and also more challenging to price.
- **Monte Carlo Simulation:** The method uses Monte Carlo simulation to generate multiple possible paths for the underlying asset price. These paths simulate the possible future movements of the asset based on assumptions about volatility, drift, and the risk-free rate.
- **Least Squares Regression:** At each potential exercise date, the method uses least squares regression to estimate the continuation value of holding the option. The continuation value is the expected value of holding the option for one more period rather than exercising it immediately. The regression uses basis functions of the state variables (typically polynomials of the underlying asset price) to approximate this value.
- **Optimal Exercise Strategy:** By comparing the immediate exercise payoff to the estimated continuation value, the method determines the optimal exercise strategy at each point in time. If the immediate payoff exceeds the continuation value, it is optimal to exercise the option; otherwise, the holder should continue holding the option.

### Detailed Steps
1. **Simulate Asset Price Paths:** Simulate a large number of paths for the underlying asset price using a model such as geometric Brownian motion. These paths represent possible future movements of the asset price.
2. **Backward Induction:** Start at the final time step and move backward through each potential exercise date. At the final time step, the payoff is simply the intrinsic value of the option.
3. **Calculate Payoffs:** At each exercise date, calculate the immediate exercise payoff for each path. For a call option, this is $(S_t - K)^+$, and for a put option, it is $(K - S_t)^+$, where $S_t$ is the underlying asset price at time $t$ and $K$ is the strike price.
4. **Estimate Continuation Value:** Use least squares regression to estimate the continuation value of the option. The continuation value is the discounted expected payoff of holding the option, calculated using basis functions of the underlying asset price.
5. **Determine Optimal Exercise:** Compare the immediate exercise payoff to the estimated continuation value. If the immediate payoff is greater, exercise the option; otherwise, continue holding it.
6. **Compute Option Value:** Aggregate the payoffs from the optimal exercise strategy across all paths to estimate the option price.
