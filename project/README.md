# project



## Docker


```bash
docker build -t holmen1/economic-scenario-generator-api .
```

```bash
docker run -d --name my_esg -p 8000:80 holmen1/economic-scenario-generator-api
```

```bash
docker push holmen1/economic-scenario-generator-api
```


```bash
curl -X POST "http://localhost:8000/api/scenarios" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"N\":2,\"T\":1,\"s0\":[224.0,0.03],\"a\":[0.0,0.09],\"mu\":[0.094,-0.007],\"sigma\":[0.16,0.007],\"corrmatrix\":[[1.0,0.2],[0.2,1.0]]}" 
```

## unittest

```bash
python -m unittest discover -v project/tests
```

```bash
test_final_gbm_mean (test_api.TestApi) ... ok
test_get_ping (test_api.TestApi) ... ok
test_response_dimensions (test_api.TestApi) ... ok
test_left_factorize (test_noise.TestNoise) ... ok
test_normal_step_correlation (test_noise.TestNoise) ... ok
test_normal_step_mean_std (test_noise.TestNoise) ... ok
test_normal_step_normality (test_noise.TestNoise) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.514s

OK
```







