"""EM for a very simple Gaussian process regression model.

Model
-----
    f ~ N(0, s2 * K)          hidden smooth function, evaluated at n inputs
    y | f ~ N(f, sigma2 * I)  what we actually observe: f plus white noise

K is a fixed, unit-variance RBF kernel matrix. EM learns two numbers:

    s2      signal variance (how tall the wiggles of f are)
    sigma2  noise variance  (how far y scatters around f)

Throughout, C = s2*K + sigma2*I is the covariance of y, and alpha = C^-1 y.

Every function here is a direct transcription of one formula, so that it can
later be ported line by line to C or C++.
"""

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize


def rbf_kernel(x1, x2, lengthscale):
    """Unit-variance RBF kernel: K[i, j] = exp(-(x1[i] - x2[j])^2 / (2 l^2)).

    Inputs closer together than about one lengthscale are strongly correlated.
    """
    if lengthscale <= 0:
        raise ValueError("lengthscale must be positive")
    diff = np.asarray(x1)[:, None] - np.asarray(x2)[None, :]
    return np.exp(-0.5 * (diff / lengthscale) ** 2)


def sample_data(n, s2, sigma2, lengthscale, seed, x_max=10.0):
    """Draw (x, f, y) from the model, so the true parameters are known.

    To sample f ~ N(0, s2*K) we factor K = L L^T and set f = sqrt(s2) * L z
    with z standard normal. The tiny "jitter" added to the diagonal keeps the
    factorisation from failing when K is singular to machine precision.
    """
    rng = np.random.default_rng(seed)
    x = np.linspace(0.0, x_max, n)
    K = rbf_kernel(x, x, lengthscale)
    L = np.linalg.cholesky(K + 1e-8 * np.eye(n))
    f = np.sqrt(s2) * L @ rng.standard_normal(n)
    y = f + np.sqrt(sigma2) * rng.standard_normal(n)
    return x, f, y


def _check_inputs(K, y, s2, sigma2):
    n = len(y)
    if K.shape != (n, n):
        raise ValueError(f"K has shape {K.shape}, expected ({n}, {n})")
    if s2 <= 0 or sigma2 <= 0:
        raise ValueError(f"variances must be positive, got s2={s2}, sigma2={sigma2}")


def log_marginal_likelihood(K, y, s2, sigma2):
    """log p(y | s2, sigma2) with f integrated out, i.e. log N(y; 0, C).

        -1/2 y^T C^-1 y  -  1/2 log|C|  -  n/2 log(2 pi)

    With C = L L^T:  C^-1 y comes from two triangular solves, and
    log|C| = 2 * sum(log(diag(L))). No inverse, no determinant.
    """
    _check_inputs(K, y, s2, sigma2)
    n = len(y)
    C = s2 * K + sigma2 * np.eye(n)
    L, lower = cho_factor(C, lower=True)
    alpha = cho_solve((L, lower), y)
    return -0.5 * y @ alpha - np.sum(np.log(np.diag(L))) - 0.5 * n * np.log(2 * np.pi)


# ---------------------------------------------------------------------------
# Naive version: the formulas exactly as they are written on paper.
# ---------------------------------------------------------------------------


def e_step_naive(K, y, s2, sigma2):
    """Posterior of f given y under the current parameters: f | y ~ N(m, S).

        m = s2 K C^-1 y
        S = s2 K - s2 K C^-1 s2 K
    """
    _check_inputs(K, y, s2, sigma2)
    n = len(y)
    C_inv = np.linalg.inv(s2 * K + sigma2 * np.eye(n))
    m = s2 * K @ C_inv @ y
    S = s2 * K - s2 * K @ C_inv @ (s2 * K)
    return m, S


def m_step_naive(K, y, m, S):
    """Parameters that maximise the expected complete-data log-likelihood.

        sigma2 = ( |y - m|^2 + tr(S) ) / n          average squared residual
        s2     = ( m^T K^-1 m + tr(K^-1 S) ) / n    average "whitened" f^2

    Each is what you would compute if f were known, with f replaced by its
    posterior mean m, plus a trace term that accounts for still being
    uncertain about f.
    """
    n = len(y)
    K_inv = np.linalg.inv(K)  # the problem: K is nearly singular
    sigma2 = (np.sum((y - m) ** 2) + np.trace(S)) / n
    s2 = (m @ K_inv @ m + np.trace(K_inv @ S)) / n
    return s2, sigma2


# ---------------------------------------------------------------------------
# Stable version: same maths, one Cholesky factor of C, K is never inverted.
# ---------------------------------------------------------------------------


def e_step(K, y, s2, sigma2):
    """Same posterior as e_step_naive, computed from C = L L^T.

    Also returns alpha = C^-1 y and C^-1 K, which the M-step reuses so that it
    never has to touch K^-1.
    """
    _check_inputs(K, y, s2, sigma2)
    n = len(y)
    c = cho_factor(s2 * K + sigma2 * np.eye(n), lower=True)
    alpha = cho_solve(c, y)
    C_inv_K = cho_solve(c, K)
    m = s2 * K @ alpha
    S = s2 * K - s2**2 * K @ C_inv_K
    return m, S, alpha, C_inv_K


def m_step(y, m, S, alpha, C_inv_K, s2):
    """Same updates as m_step_naive, with K^-1 eliminated by algebra.

    Because m = s2 K alpha:
        m^T K^-1 m = s2 * alpha^T m
    Because S = s2 K - s2^2 K C^-1 K:
        tr(K^-1 S) = n*s2 - s2^2 * tr(C^-1 K)

    `s2` is the value the E-step was run with.
    """
    n = len(y)
    sigma2_new = (np.sum((y - m) ** 2) + np.trace(S)) / n
    s2_new = (s2 * alpha @ m + n * s2 - s2**2 * np.trace(C_inv_K)) / n
    return s2_new, sigma2_new


def run_em(K, y, s2_0=1.0, sigma2_0=1.0, n_iter=200, tol=1e-8, naive=False):
    """Alternate E and M steps until the log-likelihood stops changing.

    Returns a dict of lists, one entry per parameter value visited (including
    the starting point): "s2", "sigma2" and "log_lik".
    """
    s2, sigma2 = s2_0, sigma2_0
    history = {
        "s2": [s2],
        "sigma2": [sigma2],
        "log_lik": [log_marginal_likelihood(K, y, s2, sigma2)],
    }
    for _ in range(n_iter):
        if naive:
            m, S = e_step_naive(K, y, s2, sigma2)
            s2, sigma2 = m_step_naive(K, y, m, S)
        else:
            m, S, alpha, C_inv_K = e_step(K, y, s2, sigma2)
            s2, sigma2 = m_step(y, m, S, alpha, C_inv_K, s2)
        history["s2"].append(s2)
        history["sigma2"].append(sigma2)
        history["log_lik"].append(log_marginal_likelihood(K, y, s2, sigma2))
        if abs(history["log_lik"][-1] - history["log_lik"][-2]) < tol:
            break
    return history


def fit_direct(K, y, s2_0=1.0, sigma2_0=1.0):
    """Reference answer: maximise the marginal likelihood with a general optimiser.

    Optimising over log-parameters keeps both variances positive without
    needing constraints. Returns (s2, sigma2, log_lik).
    """

    def negative_log_lik(log_params):
        s2, sigma2 = np.exp(log_params)
        return -log_marginal_likelihood(K, y, s2, sigma2)

    result = minimize(negative_log_lik, np.log([s2_0, sigma2_0]), method="L-BFGS-B")
    s2, sigma2 = np.exp(result.x)
    return s2, sigma2, -result.fun


def predict(x_train, y, x_test, s2, sigma2, lengthscale):
    """Posterior mean and variance of f at new inputs x_test.

        mean = s2 K_* C^-1 y
        var  = s2 - s2^2 * diag(K_* C^-1 K_*^T)

    where K_* is the kernel between test and training inputs.
    """
    K = rbf_kernel(x_train, x_train, lengthscale)
    K_star = rbf_kernel(x_test, x_train, lengthscale)
    _check_inputs(K, y, s2, sigma2)
    c = cho_factor(s2 * K + sigma2 * np.eye(len(y)), lower=True)
    mean = s2 * K_star @ cho_solve(c, y)
    var = s2 - s2**2 * np.sum(K_star * cho_solve(c, K_star.T).T, axis=1)
    return mean, var
