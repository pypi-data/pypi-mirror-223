import unittest
from openirt import item_models
import numpy as np


class TestPL3(unittest.TestCase):
    def test_prob_shape(self):
        params = np.array([[-1, 0, 1], [-1.5, 0, 1.5], [0.1, 0.1, 0.1]])
        abilities = np.array([-1.2, 1.2])
        pl3 = item_models.PL3()
        prob = pl3.p(abilities, params)
        assert prob.shape == (2, 3)

    def test_valid_prob(self):
        pl3 = item_models.PL3()
        params = np.array(
            [
                np.linspace(*pl3.param_bounds[0]),
                np.linspace(*pl3.param_bounds[1]),
                np.linspace(*pl3.param_bounds[2]),
            ]
        )
        abilities = np.array([np.linspace(-10, 10)])
        prob = pl3.p(abilities, params)
        assert np.all(prob >= 0)
        assert np.all(prob <= 1)

    def test_prob_value(self):
        params = np.array([[1, 0, -1], [-1.5, 0, 1.5], [0.1, 0.2, 0.3]])
        abilities = np.array([-10, 1.5, 10])
        pl3 = item_models.PL3()
        prob = pl3.p(abilities, params)
        assert prob[0][0] < 1e-3 + 0.1
        assert prob[2][0] > 1 - 1e-3

    def test_simulated_resp(self):
        params = np.array([[1, 0, -1], [-1.5, 0, 1.5], [0.1, 0.2, 0.3]])
        abilities = np.array([-10, 1.5])
        pl3 = item_models.PL1()
        resp = pl3.simulated_responses(abilities, params)
        assert resp.shape == (2, 3)
        assert np.all(resp >= 0)
        assert np.all(resp <= 1)
