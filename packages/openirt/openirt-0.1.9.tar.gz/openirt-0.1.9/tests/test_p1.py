import pytest
from openirt import item_models
import numpy as np

# ---GENERIC---

def test_prob_gen():
    params = np.array([[0.45, 0.6], [0.1, 0.15]])
    abilities = np.array([0.55, 1.2])
    def p(ab, params):
        if ab > params[0]:
            return 1
        else:
            return params[1]
    model = item_models.Model(p, num_params=2)
    prob = model.p(abilities, params)
    assert prob.shape == (2,2)
    assert prob[0][0] == 1
    assert prob[0][1] == 0.15
        