# Binomial Model
### Model of underlying price
<p align="center">
    <img src="https://github.com/PontusHovb/Option-Pricing/blob/master/Images/BinomialModel_UnderlyingPrice.png" width="400"/>
</p>
<p align="center"><i>Model of underlying asset price using binomial model</i></p>

Pricing an european option using a $`n`$-step binomial model:
``` math
\pi_i (S_i) = \frac{1}{e^{r \Delta t}} \left( q \pi_{i+1} (S_i \cdot u) + (1 - q) \pi_{i+1}(S_i \cdot d) \right) \quad \text{for i = 0, 1, ..., n - 1}
```
where $`\pi_i`$ is the price of the option, $`S_i`$ is the price of the underlying asset at time step $`i`$, $`r`$ is the risk-free rate and $`\Delta t`$ the time (in years) per time step. In a binomial model, the price in the next time step can either go up (with a factor $`u`$) or down (with a factor $`d`$). These factors reflect the volatility of the asset:
``` math
u = e^{\sigma \sqrt{\delta t}}, \quad d = e^{- \sigma \sqrt{\delta t}}
```
Lastly, $`q`$ is the martingale probability:
``` math
q = \frac{e^{r \Delta t} - d}{u - d}
```
ensuring that the expected discounted price equals the current price under the risk-neutral measure.

For last time step (step $`n`$ in time $`T`$), the option can be exercised and the value of the option is therefore:
``` math
\pi_n (S_T) = \phi(S_T)
```
where $`\phi`$ is the payoff function, positive if the option is in-the-money and 0 otherwise. For an European call option with strike $`K`$ and price $`S_T`$ at maturity, the payoff is:
``` math
\phi(S_T) = \max(S_T - K, 0)
```
The current price of the option is then recursively found through backward induction. 

### Example calculation
As an example, the price of a European call option with the following parameters:
- $`S_0 = 100`$
- $`K = 100`$
- $`T = 1`$ (years)
- $`r = 0.05`$
- $`\sigma = 0.20`$
- $`n = 2`$ (time steps)

The up and down factors are:
``` math
u = e^{0.20 \sqrt{0.5}} \approx 1.149, \quad d = e^{- 0.20 \sqrt{0.5}} \approx 0.871
```

The risk-neutral probability is:
``` math
q = \frac{e^{0.05 \cdot 0.5} - 0.871}{1.149 - 0.871} \approx 0.557
```


Using these, we can calculate the option price at each node backward from maturity to the present.

### Convergence to Black-Scholes
As the number of steps $n$ increases, the binomial model converges to the Black-Scholes model, providing a discrete-time approximation to the continuous-time model.
