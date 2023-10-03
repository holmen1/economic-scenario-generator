# -*- coding: utf-8 -*-
"""
Created June 2019

@author: holmen1
"""
import multiprocessing as mp
import numpy as np


class EconomicScenarioGenerator(object):
    """
    Using Eulers method to approximate numerical solutions to stochastic differential equation (SDE)
 
    - Stocks: dS = mu S dt + sigma S dB
    - Rates: dr = a (mu - r) dt + sigma dB
    """

    def __init__(self, s0, a, mu, sdev, noise):
        """
        Initialize a Scenario Generator.
        Inputs:
        - s0: Array Initial values
        - a: Speed of reversion in Vasicek
        - mu: Array Mean returns (yearly)
        - sdev: Array standard deviation (yearly)
        - noise: Array of noise with marginal distributions N(0, 1) 
        """
        self.s0 = s0
        self.a = a
        self.mu = mu
        self.sigma = sdev
        self.Noise = noise
        self.stock_id = np.where(a == 0.0)[0]
        self.rate_id = np.where(a != 0.0)[0]

    def get_scenarios_partial(self, sim_start, sim_steps, steps, partition):
        """
        Generate Geometric Brownian motions or
        Mean Reversion w Additive Noice (Vasicek)

        Inputs:
        - N: Integer Number of simulations
        - steps: Integer Number of steps in each simulation
        - partition: Integer Parts of a year, 252 => daily
        """
        scaled_sigma = self.sigma / np.sqrt(partition)

        dt = 1 / partition
        s = np.zeros((sim_steps, len(self.stock_id), steps))
        r = np.zeros((sim_steps, len(self.rate_id), steps))
        for n in np.arange(sim_start, sim_start + sim_steps):
            dB = self.Noise[:, n * steps:(n + 1) * steps]
            s[n - sim_start] = self.gbm(self.s0[self.stock_id], self.mu[self.stock_id], scaled_sigma[self.stock_id], dt,
                                        dB[self.stock_id, 1:])
            r[n - sim_start] = self.vasicek(self.s0[self.rate_id], self.a[self.rate_id], self.mu[self.rate_id],
                                            scaled_sigma[self.rate_id], dt, dB[self.rate_id, 1:])
        return (s, r)

    def get_scenarios(self, N, steps, partition):
        num_processes = mp.cpu_count()

        # create inputs for multiprocessing
        # each input is a tuple of (start, end, steps, partition)
        inputs = []
        for i in range(num_processes):
            start = int(np.floor(i * N / num_processes))
            end = int(np.floor((i + 1) * N / num_processes))
            inputs.append((start, end - start, steps, partition))

        # create a pool for multiprocessing
        pool = mp.Pool(processes=num_processes)
        result = pool.starmap(self.get_scenarios_partial, inputs)

        S = np.concatenate([r[0] for r in result], axis=0)
        R = np.concatenate([r[1] for r in result], axis=0)
        return (S, R)

    def gbm(self, s0, mu, sigma, dt, dB):
        """
        Geometric Brownian Motion
        """

        s = s0.copy()
        S = np.zeros((dB.shape[0], dB.shape[1] + 1))
        S[:, 0], n = s, 1

        for db in dB.T:
            s += mu * s * dt + sigma * s * db
            S[:, n] = s
            n += 1

        return S

    def vasicek(self, r0, a, mu, sigma, dt, dB):
        """
        Mean reversion rate model
        """
        r = r0.copy()
        R = np.zeros((dB.shape[0], dB.shape[1] + 1))
        R[:, 0], n = r, 1

        for db in dB.T:
            r += a * (mu - r) * dt + sigma * db
            R[:, n] = r
            n += 1

        return R
