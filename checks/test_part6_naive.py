"""Checks for Part 6: kernel, data simulation, likelihood, naive EM.

Run with:  pytest -m part6

pytest techniques on show: plain asserts, floating-point comparison,
pytest.raises, fixtures, parametrize, and three ways to test numerical code
when you cannot work out the right answer by hand:
  1. compare against an independent implementation you trust,
  2. check a property the answer must satisfy (an invariant),
  3. check behaviour on a problem where the truth is known.
"""

import numpy as np
import pytest
from scipy.stats import multivariate_normal

import gp_em

# A module-level `pytestmark` applies the marker to every test in the file.
pytestmark = pytest.mark.part6


# --- rbf_kernel -------------------------------------------------------------


def test_kernel_shape():
    K = gp_em.rbf_kernel(np.zeros(3), np.zeros(5), lengthscale=1.0)
    assert K.shape == (3, 5)


def test_kernel_is_symmetric():
    x = np.linspace(0, 10, 15)
    K = gp_em.rbf_kernel(x, x, lengthscale=1.0)
    # Never compare floats with ==: two correct calculations can differ in the
    # last bit. assert_allclose passes if they agree to a relative tolerance.
    np.testing.assert_allclose(K, K.T)


def test_kernel_diagonal_is_one():
    x = np.linspace(0, 10, 15)
    K = gp_em.rbf_kernel(x, x, lengthscale=1.0)
    np.testing.assert_allclose(np.diag(K), 1.0)


def test_kernel_known_value():
    # Two points exactly one lengthscale apart: exp(-1/2).
    K = gp_em.rbf_kernel(np.array([0.0]), np.array([2.0]), lengthscale=2.0)
    # pytest.approx is the scalar equivalent of assert_allclose.
    assert K[0, 0] == pytest.approx(np.exp(-0.5))


def test_kernel_is_positive_semidefinite():
    x = np.linspace(0, 10, 15)
    K = gp_em.rbf_kernel(x, x, lengthscale=1.0)
    eigenvalues = np.linalg.eigvalsh(K)
    # Allow rounding error: the smallest eigenvalues are zero to ~1e-16.
    assert eigenvalues.min() > -1e-10


def test_kernel_rejects_bad_lengthscale():
    # pytest.raises passes only if the block raises the named exception.
    with pytest.raises(ValueError):
        gp_em.rbf_kernel(np.zeros(2), np.zeros(2), lengthscale=0.0)


# --- sample_data ------------------------------------------------------------


def test_sample_data_shapes_and_grid():
    x, f, y = gp_em.sample_data(n=30, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=0)
    assert x.shape == f.shape == y.shape == (30,)
    np.testing.assert_allclose(x, np.linspace(0, 10, 30))


def test_sample_data_is_reproducible():
    a = gp_em.sample_data(n=30, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=7)
    b = gp_em.sample_data(n=30, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=7)
    c = gp_em.sample_data(n=30, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=8)
    np.testing.assert_array_equal(a[2], b[2])
    assert not np.allclose(a[2], c[2])


def test_sample_data_noise_has_the_requested_variance():
    """3. Known truth: y - f is the noise, and we know its variance."""
    _, f, y = gp_em.sample_data(n=400, s2=2.0, sigma2=0.25, lengthscale=0.5, seed=0)
    # 400 draws: the sample variance has a standard error of about 7%.
    assert np.var(y - f) == pytest.approx(0.25, rel=0.25)


# --- log_marginal_likelihood ------------------------------------------------


# `small_problem` is a fixture from conftest.py: naming it as an argument is
# enough for pytest to build it and pass it in.
def test_log_likelihood_matches_scipy(small_problem):
    """1. Independent reference: SciPy's general-purpose Gaussian density."""
    p = small_problem
    C = p.s2 * p.K + p.sigma2 * np.eye(len(p.y))
    expected = multivariate_normal(mean=np.zeros(len(p.y)), cov=C).logpdf(p.y)
    assert gp_em.log_marginal_likelihood(p.K, p.y, p.s2, p.sigma2) == pytest.approx(expected)


@pytest.mark.parametrize("s2, sigma2", [(-1.0, 1.0), (1.0, 0.0)])
def test_rejects_non_positive_variances(small_problem, s2, sigma2):
    with pytest.raises(ValueError):
        gp_em.log_marginal_likelihood(small_problem.K, small_problem.y, s2, sigma2)


def test_rejects_shape_mismatch(small_problem):
    with pytest.raises(ValueError):
        gp_em.e_step_naive(small_problem.K, small_problem.y[:-1], 1.0, 1.0)


# --- e_step_naive, m_step_naive, run_em(naive=True) --------------------------


def test_posterior_covariance_is_symmetric_psd(small_problem):
    p = small_problem
    _, S = gp_em.e_step_naive(p.K, p.y, p.s2, p.sigma2)
    np.testing.assert_allclose(S, S.T, atol=1e-10)
    assert np.linalg.eigvalsh((S + S.T) / 2).min() > -1e-10


def test_posterior_mean_is_closer_to_truth_than_data(small_problem):
    """3. Known truth: smoothing should remove noise, not add it."""
    p = small_problem
    m, _ = gp_em.e_step_naive(p.K, p.y, p.s2, p.sigma2)
    assert np.sum((m - p.f) ** 2) < np.sum((p.y - p.f) ** 2)


def test_history_has_one_entry_per_parameter_value(small_problem):
    p = small_problem
    history = gp_em.run_em(p.K, p.y, n_iter=5, tol=0.0, naive=True)
    assert len(history["s2"]) == len(history["sigma2"]) == len(history["log_lik"]) == 6


# parametrize runs the same test once per value. Stacking two decorators runs
# every combination (3 seeds x 3 starting points = 9 tests), and each one is
# reported separately, so a failure tells you exactly which case broke.
@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("start", [(1.0, 1.0), (0.01, 10.0), (50.0, 0.01)])
def test_naive_em_never_decreases_log_likelihood(seed, start):
    """2. Invariant: the defining guarantee of EM (on a well-conditioned problem)."""
    x, _, y = gp_em.sample_data(n=20, s2=2.0, sigma2=0.25, lengthscale=0.5, seed=seed)
    K = gp_em.rbf_kernel(x, x, 0.5)
    history = gp_em.run_em(K, y, s2_0=start[0], sigma2_0=start[1], n_iter=100, naive=True)
    assert np.all(np.diff(history["log_lik"]) >= -1e-9)


def test_naive_em_stops_where_the_likelihood_is_flat(small_problem):
    """2. Invariant: at convergence the gradient of the likelihood is zero."""
    p = small_problem
    history = gp_em.run_em(p.K, p.y, n_iter=5000, tol=1e-13, naive=True)
    s2, sigma2, h = history["s2"][-1], history["sigma2"][-1], 1e-5
    ll = lambda a, b: gp_em.log_marginal_likelihood(p.K, p.y, a, b)
    assert (ll(s2 + h, sigma2) - ll(s2 - h, sigma2)) / (2 * h) == pytest.approx(0, abs=1e-3)
    assert (ll(s2, sigma2 + h) - ll(s2, sigma2 - h)) / (2 * h) == pytest.approx(0, abs=1e-3)
