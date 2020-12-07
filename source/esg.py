# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:23:06 2019

@author: mhoc
"""
import numpy as np
from numpy import linalg as la
from numpy import dot, cumsum, sqrt, outer, diag, exp, max, zeros, roll
from scipy.stats import norm
class EconomicScenarioGenerator(object):
    """
    
    """

    def __init__(self, s0, a, mu, sdev, noise):
        """
        Initialize a Scenario Generator.
        Inputs:
        - s0: Array Initial values
        - a: Speed of reversion in Vasicek
        - mu: Array Mean returns (yearly)
        - cov: Array Covariance (yearly)
        """
        ############################################################################
        # TODO: Check dimensions                                                   #
        ############################################################################
        self.s0 = s0
        self.a = a
        self.mu = mu
        self.sigma = sdev
        self.Noise = noise
        self.stock_id = np.where(a == 0.0)[0]
        self.rate_id = np.where(a != 0.0)[0]
        #np.random.seed(905)

    def get_scenarios(self, N, steps, partition=252):
        """
        Generate Geometric Brownian motions or Mean Reversion w Additive Noice (Vasicek)

        Inputs:
        - N: Integer Number of simulations
        - steps: Integer Number of steps in each simulation
        - partion: Integer Parts of a year, 252 => daily
        """
        scaled_sigma = self.sigma / sqrt(partition)
        
        dt = 1/partition
        S = zeros((N, len(self.stock_id), steps))
        R = zeros((N, len(self.rate_id), steps))
        for n in np.arange(N):
            dB = self.Noise[:,n*steps:(n+1)*steps]
            S[n] = self.gbm(self.s0[self.stock_id], self.mu[self.stock_id], scaled_sigma[self.stock_id], dt, dB[self.stock_id,1:])
            R[n] = self.vasicek(self.s0[self.rate_id], self.a[self.rate_id], self.mu[self.rate_id], scaled_sigma[self.rate_id], dt, dB[self.rate_id,1:])
        return (S,R)

    # Geometric Brownian Motion
    def gbm(self, s0, mu, sigma, dt, dB):
        """
        Inputs:
        - s0: Array of input data of shape (N, d_1, ..., d_k)
        - mu:
        - sdev:
        - dt:
        - dB:
        """
        s = s0.copy()
        S = zeros((dB.shape[0],dB.shape[1]+1))
        S[:,0], n = s, 1

        for db in dB.T:
            s += mu*s*dt + sigma*s*db
            S[:,n] = s
            n += 1
            
        return S

    # Mean reversion rate model
    def vasicek(self, r0, a, mu, sigma, dt, dB):
        """
        Inputs:
        - r0: Array of input data of shape (N, d_1, ..., d_k)
        - a: Array of labels, of shape (N,). y[i] gives the label for X[i].
        - mu:
        - sdev:
        - dB:
        """
        r = r0.copy()
        R = zeros((dB.shape[0],dB.shape[1]+1))
        R[:,0], n = r, 1

        for db in dB.T:
            r += a*(mu - r)*dt + sigma*db
            R[:,n] = r
            n += 1
            
        return R


