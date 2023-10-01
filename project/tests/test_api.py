import unittest
import numpy as np

from fastapi.testclient import TestClient
from source.api import app

class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_root_message(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello from ESG!"})

    def test_response_dimensions(self):
        payload = {
            "N": 10,
            "T": 5,
            "s0": [224.0, 234.0, 0.03],
            "a": [0.0, 0.0, 0.09],
            "mu": [0.094, 0.094, -0.007],
            "sigma": [0.16, 0.16, 0.007],
            "corrmatrix": [
                [1.0, 1.0, 0.2], [1.0, 1.0, 0.2], [0.2, 0.2, 1.0]
            ]
        }
        response = self.client.post("/api/scenarios", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json()["gbm"]), 10)
        self.assertEqual(len(response.json()["gbm"][0]), 2)
        self.assertEqual(len(response.json()["gbm"][0][0]), 60)
        self.assertEqual(len(response.json()["vasicek"]), 10)
        self.assertEqual(len(response.json()["vasicek"][0]), 1)
        self.assertEqual(len(response.json()["vasicek"][0][0]), 60)

    def test_final_gbm_mean(self):
        payload = {
            "N": 1000,
            "T": 5,
            "s0": [224.0, 234.0, 0.03],
            "a": [0.0, 0.0, 0.09],
            "mu": [0.094, 0.094, -0.007],
            "sigma": [0.16, 0.16, 0.007],
            "corrmatrix": [
                [1.0, 1.0, 0.2], [1.0, 1.0, 0.2], [0.2, 0.2, 1.0]
            ]
        }
        response = self.client.post("/api/scenarios", json=payload)
        self.assertEqual(response.status_code, 201)

        # check mean of final value first gbm
        analytic_mean = payload["s0"][0] * np.exp(payload["mu"][0] * payload["T"])
        gbm = np.array(response.json()["gbm"])
        mean_gbm = np.mean(gbm[:, 0, -1])
        np.testing.assert_allclose(analytic_mean, mean_gbm, rtol=0.05)

if __name__ == '__main__':
    unittest.main()