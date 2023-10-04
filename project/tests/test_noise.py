import numpy as np
import unittest

from project.source.noise import NoiseGenerator


class TestNoise(unittest.TestCase):
    NG = None  # using NoiseGenerator instance as the class variable

    @classmethod
    def setUpClass(cls):
        cls.NG = NoiseGenerator()

    def test_left_factorize(self):
        A = np.array([[1, 0.5, 0.2], [0.5, 1, 0.3], [0.2, 0.3, 1]])
        B = self.NG.left_factorize(A)
        self.assertTrue(np.allclose(A, B @ B.T))

    def test_normal_steps(self):
        Corr = np.array([[1, 0.5, 0.2], [0.5, 1, 0.3], [0.2, 0.3, 1]])
        dB = self.NG.normal_steps(Corr, 100000)
        self.assertTrue(np.allclose(np.corrcoef(dB), Corr, atol=0.01))


if __name__ == '__main__':
    unittest.main()
