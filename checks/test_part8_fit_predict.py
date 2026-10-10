"""Checks for Part 8: the direct optimiser and prediction at new inputs.

Run with:  pytest -m part8

pytest technique on show: a custom marker for slow tests.
"""

import numpy as np
import pytest

import gp_em

pytestmark = pytest.mark.part8


def test_predict_at_training_points_matches_e_step(small_problem):
    p = small_problem
    m, S, _, _ = gp_em.e_step(p.K, p.y, p.s2, p.sigma2)
    mean, var = gp_em.predict(p.x, p.y, p.x, p.s2, p.sigma2, p.lengthscale)
    np.testing.assert_allclose(mean, m)
    np.testing.assert_allclose(var, np.diag(S), atol=1e-12)


def test_predict_far_from_data_returns_the_prior(small_problem):
    """Many lengthscales away the data say nothing: mean 0, variance s2."""
    p = small_problem
    mean, var = gp_em.predict(p.x, p.y, np.array([1000.0]), p.s2, p.sigma2, p.lengthscale)
    assert mean[0] == pytest.approx(0.0, abs=1e-12)
    assert var[0] == pytest.approx(p.s2)


# Stacking a second marker. Run `pytest -m "not slow"` to skip tests carrying it.
@pytest.mark.slow
def test_em_converges_to_direct_optimum(ill_conditioned_problem):
    """EM and a general-purpose optimiser must find the same maximum."""
    p = ill_conditioned_problem
    history = gp_em.run_em(p.K, p.y, n_iter=5000, tol=1e-12)
    s2, sigma2, log_lik = gp_em.fit_direct(p.K, p.y)
    assert history["log_lik"][-1] == pytest.approx(log_lik, abs=1e-5)
    # rel=1e-2: the likelihood is flat near its peak, so the two methods agree
    # far more closely on the likelihood value than on the parameters.
    assert history["s2"][-1] == pytest.approx(s2, rel=1e-2)
    assert history["sigma2"][-1] == pytest.approx(sigma2, rel=1e-2)
