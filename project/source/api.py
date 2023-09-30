from fastapi import FastAPI, Response, status

from typing import List
from pydantic import BaseModel
from .noise import NoiseGenerator
from .esg import EconomicScenarioGenerator
import numpy as np


class RequestModel(BaseModel):
    s0: List[float]  # initial value
    a: List[float]  # speed of reversion (rates)
    mu: List[float]  # drift (stocks), long term mean level (rates)
    sigma: List[float]  # volatility
    corrmatrix: List[List[float]]

    def to_numpy(self):
        return map(np.array, [self.s0, self.a, self.mu, self.sigma, self.corrmatrix])


class ResponseModel(BaseModel):
    gbm: List[List[List[float]]]  # geometric brownian motion
    vasicek: List[List[List[float]]]  # mean reversion with additive noise


app = FastAPI(
    title="economic-scenario-generator",
    description="A RESTful API to generate",
    version="1.5.1",
)


@app.get("/")
async def root():
    return {"message": "Hello from ESG!"}


@app.post("/api/scenarios", status_code=200)
async def create_scenarios(req: RequestModel, response: Response) -> ResponseModel:
    s0, a, mu, sigma, corrmatrix = req.to_numpy()

    N = 10  # simulations
    interval = 12  # monthly
    T = 5  # years
    steps = interval * T

    NG = NoiseGenerator()
    dB = NG.normal_steps(corrmatrix, N * steps)
    ESG = EconomicScenarioGenerator(s0, a, mu, sigma, dB)

    # (10,2,60)
    EQ, IR = ESG.get_scenarios(N, steps, interval)

    eq_list = EQ.tolist()
    ir_list = IR.tolist()
    if eq_list or ir_list:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(gbm=eq_list, vasicek=ir_list)
