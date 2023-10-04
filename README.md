# Economic Scenario Generator


![error](https://github.com/holmen1/economic-scenario-generator/blob/master/images/StockSimulation.JPG)

Using Geometric Brownian Motion to model stocks $dS = \mu S dt + \sigma S dB$  
and Ornstein–Uhlenbeck for interest rates $dr = a(\mu - r) dt + \sigma dB$  
Driving Brownian process is generated from correlation-matrix that need not be wellconditioned since truncated singular value decomposition is used.
Interdependence between paths is captured with Gaussian copula, which is easily modified to model more realistic interdependencies.


### References
Ornstein–Uhlenbeck process https://en.wikipedia.org/wiki/Ornstein%E2%80%93Uhlenbeck_process

Singular value decomposition https://en.wikipedia.org/wiki/Singular_value_decomposition

Copula https://en.wikipedia.org/wiki/Copula_(probability_theory)


### FastAPI in Docker

```bash
docker run -d --name my_esg -p 8000:80 holmen1/economic-scenario-generator-api
```

```bash
curl -X POST "http://localhost:8000/api/scenarios" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"samples\":2,\"years\":1,\"s0\":[224.0,0.03],\"a\":[0.0,0.09],\"mu\":[0.094,-0.007],\"sigma\":[0.16,0.007],\"corrmatrix\":[[1.0,0.2],[0.2,1.0]]}" 
```
Returns 2 samples each of stock and interest rate paths with correlation 0.2
```json
{
  "gbm":
  [
    [
      [224.0,233.24412013814867,229.18547108835241,201.21767138237402,197.79405885872166,204.47744632258156,205.55080360971866,197.35847765423307,186.42121736135533,181.7706511859549,173.90476702243666,163.2463116308496]
    ],
    [
      [224.0,245.87642132422636,222.14745917168156,232.9024969635743,229.74452566362092,212.972579510549,220.10836429078336,225.67609603841169,219.71785863011573,224.02066532753028,236.47170360973624,233.02408676476088]]
  ],
  "vasicek":
  [
    [
      [0.03,0.0317490993624826,0.031126022475785314,0.028784999428232854,0.02386318403273988,0.02339283297432511,0.022223960080312615,0.02372984522270116,0.022343614082276548,0.022403681819454593,0.020849847246733787,0.01836709280417392]
    ],
    [
      [0.03,0.03175193924876177,0.029062422938180357,0.028804540622892057,0.030073175655091995,0.02909048927411122,0.030467152357563074,0.02833432423517005,0.027626317877791372,0.02643795243414647,0.026070559942345636,0.025927968228109975]
    ]
  ]
}
```

## From A to Z

* [Preprocessing of data](https://github.com/holmen1/economic-scenario-generator/blob/master/notebooks/1.timeseries.ipynb)

* [Parameter estimation](https://github.com/holmen1/economic-scenario-generator/blob/master/notebooks/2.calibration.ipynb)

* [Plot realizations](https://github.com/holmen1/economic-scenario-generator/blob/master/notebooks/3.simulation.ipynb)

* [Validation](https://github.com/holmen1/economic-scenario-generator/blob/master/notebooks/4.validation.ipynb)


## Suggested extensions

* Reallocation s<sub>t+1</sub> += &mu;(s<sub>t</sub> + s<sub>r</sub>)dt + &sigma;(s<sub>t</sub> + s<sub>r</sub>)db
* Black-Litterman
* Non-Gaussian Copula

## TODO

* [ ] RequestModel parameter validation
* [ ] Add documentation
* [ ] Add GitHub Actions
