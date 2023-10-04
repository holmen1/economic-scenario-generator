import multiprocessing as mp
import numpy as np
import time
from fastapi import FastAPI, Response, status
from fastapi.responses import RedirectResponse
from typing import List
from pydantic import BaseModel
from .noise import NoiseGenerator
from .esg import EconomicScenarioGenerator


class RequestModel(BaseModel):
    samples: int  # simulations
    years: int  # years
    s0: List[float]  # initial value
    a: List[float]  # speed of reversion (rates)
    mu: List[float]  # drift (stocks), long term mean level (rates)
    sigma: List[float]  # volatility
    corrmatrix: List[List[float]]

    def to_numpy(self):
        return map(np.array, (self.samples, self.years, self.s0, self.a, self.mu, self.sigma, self.corrmatrix))


class ResponseModel(BaseModel):
    gbm: List[List[List[float]]]  # geometric brownian motion
    vasicek: List[List[List[float]]]  # mean reversion with additive noise
    processors: int
    time: float


app = FastAPI(
    title="economic-scenario-generator",
    summary="A RESTful API to generate economic scenarios.",
    description="Using Geometric Brownian Motion to model stocks and Ornstein–Uhlenbeck for interest rates. Driving Brownian process is generated from correlation-matrix that need not be wellconditioned since truncated singular value decomposition is used. Interdependence between paths is captured with Gaussian copula, which is easily modified to model more realistic interdependencies.",
    version="3.2.0",
    contact={"name": "holmen1", "url": "https://github.com/holmen1/economic-scenario-generator"},
    license_info={"name": "Apache 2.0", "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}
)


@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/ping")
async def ping():
    return {"pong": "from economic-scenario-generator!"}


@app.post("/api/scenarios", status_code=200)
async def create_scenarios(req: RequestModel, response: Response) -> ResponseModel:
    samples, years, s0, a, mu, sigma, corrmatrix = req.to_numpy()
    num_processes = mp.cpu_count()

    interval = 12  # monthly
    steps = interval * years

    NG = NoiseGenerator()
    dB = NG.normal_steps(corrmatrix, samples * steps)

    ESG = EconomicScenarioGenerator(s0, a, mu, sigma, dB)
    tic = time.perf_counter()
    EQ, IR = ESG.get_scenarios(samples, steps, interval)
    toc = time.perf_counter()
    time_taken = toc - tic

    eq_list = EQ.tolist()
    ir_list = IR.tolist()
    if eq_list or ir_list:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(gbm=eq_list, vasicek=ir_list, processors=num_processes, time=time_taken)
