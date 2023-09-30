# Economic Scenario Generator
## From A to Z


![error](https://github.com/holmen1/economic-scenario-generator/blob/master/images/StockSimulation.JPG)

Using Geometric Brownian Motion to model stocks and Ornstein–Uhlenbeck for interest rates.
Driving Brownian process is generated from correlation-matrix that need not be wellconditioned since truncated singular value decomposition is used.
Interdependence between paths is captured with Gaussian copula, which is easily modified to model more realistic interdependencies.


### References
Ornstein–Uhlenbeck process https://en.wikipedia.org/wiki/Ornstein%E2%80%93Uhlenbeck_process

Singular value decomposition https://en.wikipedia.org/wiki/Singular_value_decomposition

Copula https://en.wikipedia.org/wiki/Copula_(probability_theory)


### Jupyter notebooks
0. demonstration

    Qualitative plots of stock and rate

1. timeseries

    Preprocessing

    SQL -> json -> pandas -> numpy array

2. calibration

    Parameter estimation

3. simulation

    Plot realizations

4. validation

    Run calibration step on simulations


## Suggested extensions

* Reallocation s<sub>t+1</sub> += &mu;(s<sub>t</sub> + s<sub>r</sub>)dt + &sigma;(s<sub>t</sub> + s<sub>r</sub>)db
* Black-Litterman
* Non-Gaussian Copula

## TODO

* [ ] Add tests
* [ ] RequestModel parameter validation
* [ ] Add documentation
* [ ] Add logging
* [ ] Add GitHub Actions
* [ ] Add API
* [ ] Containerize