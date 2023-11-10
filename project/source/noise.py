# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 16:23:06 2019

Modified June 2020

@author: holmen1
"""
import check_mod
check_mod.install_if_missing("numpy")
check_mod.install_if_missing("scipy")
from numpy import linalg as la
from numpy import sqrt, diag, max, where, random
from scipy.stats import norm


class NoiseGenerator(object):
    """
    Modelling the distribution of random vectors by estimating marginals and copulae separately
    """

    def __init__(self, seed=0):
        """
        Initialize a Noice Generator.
        Inputs:
        - seed: Integer
        """
        if seed != 0:
            random.seed(seed)

    def normal_steps(self, Corr, steps):
        """
        Generates [X1, X2,...,Xn]
        where X ~ N(0,cor^0.5)

        Inputs:
        - Corr: Correlation matrix
        - steps: Integer, number of samples
        """

        # C ~ U(0,1)
        C = self.copula(Corr, steps)
        dB = norm.ppf(C)

        return dB

    def copula(self, Corr, n):
        """
        Gaussian Copula generator

        Inputs:
        - Corr: Correlation matrix
        - n: Integer, number of samples
        """

        # dot(B,B.T) = Corr
        B = self.left_factorize(Corr)
        rank = B.shape[1]

        Z = random.standard_normal(n * rank).reshape(-1, n)
        X = B @ Z
        C = norm.cdf(X)

        return C

    def left_factorize(self, A, tol=1e-6):
        """
        Factors A via truncated SVD such that
        A = B * B.T

        Inputs:
        - A: any symmetric matrix
        - tol: Scalar, use left-singular vectors corresponding to singular value > tol
        """
        U, Sigma, _ = la.svd(A)
        rank = max(where(Sigma > tol))
        B = U[:, :rank + 1] @ sqrt(diag(Sigma[:rank + 1]))

        return B
