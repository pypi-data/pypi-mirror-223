import unittest
from openirt import item_models
import numpy as np


# class TestNorm(unittest.TestCase):
#     def test_prob_shape(self):
#         params = np.array([[-1, 0, 1], [-1.5, 0, 1.5]])
#         abilities = np.array([-1.2, 1.2])
#         norm = item_models.Norm()
#         prob = norm.p(abilities, params)
#         assert prob.shape == (2, 3)

#     def test_valid_prob(self):
#         pl2 = item_models.PL2()
#         params = np.array(
#             [np.linspace(*pl2.param_bounds[0]), np.linspace(*pl2.param_bounds[1])]
#         )
#         abilities = np.array([np.linspace(-10, 10)])
#         prob = pl2.p(abilities, params)
#         assert np.all(prob >= 0)
#         assert np.all(prob <= 1)

#     def test_prob_value(self):
#         params = np.array([[1, 0, -1], [-1.5, 0, 1.5]])
#         abilities = np.array([-10, 1.5, 10])
#         pl2 = item_models.PL2()
#         prob = pl2.p(abilities, params)
#         assert prob[0][0] < 1e-3
#         assert abs(prob[1][2] - 0.5) < 1e-3
#         assert prob[2][0] > 1 - 1e-3

#     def test_simulated_resp(self):
#         params = np.array([[1, 0, -1], [-1.5, 0, 1.5]])
#         abilities = np.array([-1.2, 1.2])
#         pl2 = item_models.PL2()
#         resp = pl2.simulated_responses(abilities, params)
#         assert resp.shape == (2, 3)
#         assert np.all(resp >= 0)
#         assert np.all(resp <= 1)
