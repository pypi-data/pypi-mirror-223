import numpy as np
from item_models import Model, PL2


def estimate_ability_max_lik(
    params: np.ndarray,
    results: np.ndarray,
    end=0.00000001,
    eps=0.01,
    eps2=0.000001,
) -> np.ndarray:
    """
    Estimate abilities using maximum likelihood estimation.

    Parameters
    ----------
        params : np.ndarray
            Item parameters. Each column is a different item, each row is
            a different parameter.
        results : np.ndarray
            Results. Each row is a different individual, each column is a
            different item.
        end : float
            Convergence threshold.
        eps : float
            Threshold for detecting a near-singular matrix.
        eps2 : float
            Threshold for detecting small values of P*Q.

    Returns
    -------
        np.ndarray
            Array of abilities.
    """
    params = np.array(params)
    results = np.array(results)
    est = 0.5
    prev_est = 0
    while abs(est - prev_est) > end:
        P = PL2.pl2_p(est, params)[0]
        W = (1 - P) * P
        denom = np.sum(params[1] ** 2 * W)
        if abs(denom) < eps or np.any(np.abs(W) < eps2):
            print('break1')
            break
        prev_est = est
        est = est + (np.sum(params[1] * W * ((results - P) / W)) / denom)
    return est


def estimate_item_params_max_lik(
    model: Model,
    ability: np.ndarray,
    result: np.ndarray,
    a_orig=1,
    b_orig=0,
    end=1e-10,
    eps=1e-10,
) -> np.ndarray:
    """
    Estimate item parameters using maximum likelihood estimation.

    Parameters
    ----------
        model : Model
            Instance of PL2 model.
        ability : np.ndarray
            Array of abilities.
        result : np.ndarray
            Results. Each row is a different individual, each column is a
            different item.
        sigm_orig : float
            Initial value for the discrimination parameter.
        lamb_orig : float
            Initial value for the difficulty parameter.
        end : float
            Convergence threshold.
        eps : float
            Threshold for detecting a near-singular matrix.

    Returns
    -------
        np.ndarray
            Array of item parameters.
    """
    ability = np.array(ability)
    result = np.array(result)
    est = np.array([a_orig, b_orig])
    prev_est = est + 2 * end
    while np.all(np.abs(est - prev_est) > end):
        P = PL2.pl2_p(ability, [[est[0]], [est[1]]]).transpose()[0]
        W = P * (1 - P)
        lamb11 = -np.sum((ability - est[1]) ** 2 * W)
        lamb12 = est[0] * np.sum((ability - est[1]) * W)
        lamb22 = -np.sum(est[0] ** 2 * W)
        L = np.array([[lamb11, lamb12], [lamb12, lamb22]])
        if abs(np.linalg.det(L)) < eps:
            L += np.identity(2) * 1e-10
        L_inv = np.linalg.inv(L)

        L1 = np.sum((result - P) * (ability - est[1]))
        L2 = np.sum((P - result) * est[0])
        obs_mat = np.array([L1, L2])
        prev_est = est
        est = est - np.matmul(L_inv, obs_mat)
        
        # enforce bounds
        for par in range(model.num_params):
            est[par] = model.param_bounds[par][0] if est[par] < model.param_bounds[par][0] else est[par]
            est[par] = model.param_bounds[par][1] if est[par] > model.param_bounds[par][1] else est[par]
    return est
