import unittest
from openirt import item_models
import numpy as np


class TestPL1(unittest.TestCase):
    def test_prob_shape(self):
        params = np.array([[-1.5, 0, 1.5]])
        abilities = np.array([-1.2, 1.2])
        pl1 = item_models.PL1()
        prob = pl1.p(abilities, params)
        assert prob.shape == (2, 3)

    def test_valid_prob(self):
        pl1 = item_models.PL1()
        params = np.array([np.linspace(*pl1.param_bounds[0])])
        abilities = np.array([np.linspace(-10, 10)])
        prob = pl1.p(abilities, params)
        assert np.all(prob >= 0)
        assert np.all(prob <= 1)

    def test_prob_value(self):
        params = np.array([[1.5, 0]])
        abilities = np.array([-10, 1.5, 10])
        pl1 = item_models.PL1()
        prob = pl1.p(abilities, params)
        assert prob[0][0] < 1e-3
        assert abs(prob[1][0] - 0.5) < 1e-3
        assert prob[2][0] > 1 - 1e-3

    def test_simulated_resp(self):
        params = np.array([[-1.5, 0, 1.5]])
        abilities = np.array([-1.2, 1.2])
        pl1 = item_models.PL1()
        resp = pl1.simulated_responses(abilities, params)
        assert resp.shape == (2, 3)
        assert np.all(resp >= 0)
        assert np.all(resp <= 1)

    def test_plot_icc(self):
        import matplotlib
        matplotlib.use('Agg')  # Set the backend to Agg before importing pyplot
        import matplotlib.pyplot as plt
        params = np.array([[-1.5, 0, 1.5]])
        pl1 = item_models.PL1()
        pl1.plot_icc(params)