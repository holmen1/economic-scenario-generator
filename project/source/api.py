import multiprocessing as mp
import numpy as np
import logging
import time
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Response, status
from typing import List
from pydantic import BaseModel
from .noise import NoiseGenerator
from .esg import EconomicScenarioGenerator


def configure_logging():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler('./api.log', maxBytes=100000, backupCount=1)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.DEBUG)
    uvicorn_file_handler = RotatingFileHandler('./api.log', maxBytes=100000, backupCount=1)
    uvicorn_file_handler.setFormatter(formatter)
    uvicorn_logger.addHandler(uvicorn_file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    uvicorn_logger.addHandler(stream_handler)

    return logger, uvicorn_logger


class RequestModel(BaseModel):
    N: int  # simulations
    T: int  # years
    s0: List[float]  # initial value
    a: List[float]  # speed of reversion (rates)
    mu: List[float]  # drift (stocks), long term mean level (rates)
    sigma: List[float]  # volatility
    corrmatrix: List[List[float]]

    def to_numpy(self):
        return map(np.array, (self.N, self.T, self.s0, self.a, self.mu, self.sigma, self.corrmatrix))


class ResponseModel(BaseModel):
    gbm: List[List[List[float]]]  # geometric brownian motion
    vasicek: List[List[List[float]]]  # mean reversion with additive noise


log, uvicorn_log = configure_logging()

app = FastAPI(
    title="economic-scenario-generator",
    description="A RESTful API to generate",
    version="1.5.1",
    logger=uvicorn_log
)


@app.get("/")
async def root():
    log.info("Hello!")
    return {"message": "Hello from ESG!"}


@app.post("/api/scenarios", status_code=200)
async def create_scenarios(req: RequestModel, response: Response) -> ResponseModel:
    N, T, s0, a, mu, sigma, corrmatrix = req.to_numpy()
    num_processes = mp.cpu_count()
    log.info(f"Number of processes: {num_processes}")

    interval = 12  # monthly
    steps = interval * T

    NG = NoiseGenerator()
    tic = time.perf_counter()
    dB = NG.normal_steps(corrmatrix, N * steps)
    toc = time.perf_counter()
    log.info(f"Generated {N * steps} steps noise  {toc - tic:0.4f} seconds")

    ESG = EconomicScenarioGenerator(s0, a, mu, sigma, dB)
    tic = time.perf_counter()
    # (N, 2, steps)
    EQ, IR = ESG.get_scenarios(N, steps, interval)
    toc = time.perf_counter()
    log.info(f"Generated {N} scenarios in {toc - tic:0.4f} seconds")

    eq_list = EQ.tolist()
    ir_list = IR.tolist()
    if eq_list or ir_list:
        response.status_code = status.HTTP_201_CREATED

    return ResponseModel(gbm=eq_list, vasicek=ir_list)

