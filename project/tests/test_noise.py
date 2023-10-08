import numpy as np
import unittest

from project.source.noise import NoiseGenerator
from scipy.stats import shapiro


class TestNoise(unittest.TestCase):
    NG = None  # using NoiseGenerator instance as the class variable

    @classmethod
    def setUpClass(cls):
        cls.NG = NoiseGenerator()

    def test_left_factorize(self):
        A = np.array([[1, 0.5, 0.2], [0.5, 1, 0.3], [0.2, 0.3, 1]])
        B = self.NG.left_factorize(A)
        self.assertTrue(np.allclose(A, B @ B.T))

    def test_normal_step_correlation(self):
        Corr = np.array([[1.0, 1.0, 0.5, -0.8],
                         [1.0, 1.0, 0.5, -0.8],
                         [0.5, 0.5, 1.0, 0.0],
                         [-0.8, -0.8, 0.0, 1.0]])
        dB = self.NG.normal_steps(Corr, 1000000)
        self.assertTrue(np.allclose(np.corrcoef(dB), Corr, atol=0.01))

    def test_normal_step_mean_std(self):
        Corr = np.array([[1.0, 1.0, 0.5, -0.8],
                         [1.0, 1.0, 0.5, -0.8],
                         [0.5, 0.5, 1.0, 0.0],
                         [-0.8, -0.8, 0.0, 1.0]])
        dB = self.NG.normal_steps(Corr, 10000)
        self.assertTrue(np.allclose(np.mean(dB, axis=1), 0, atol=0.04))
        self.assertTrue(np.allclose(np.std(dB, axis=1), 1, atol=0.01))

    def test_normal_step_normality(self):
        Corr = np.array([[1.0, 1.0, 0.5, -0.8],
                         [1.0, 1.0, 0.5, -0.8],
                         [0.5, 0.5, 1.0, 0.0],
                         [-0.8, -0.8, 0.0, 1.0]])
        dB = self.NG.normal_steps(Corr, 1000)

        for db in dB:
            _, p = shapiro(db)
            self.assertGreater(p, 0.05)


if __name__ == '__main__':
    unittest.main()
