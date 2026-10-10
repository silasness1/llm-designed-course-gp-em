"""Checks for Part 7: the numerically stable E and M steps.

Run with:  pytest -m part7

pytest techniques on show: comparing two implementations of the same maths,
and xfail for a known defect.
"""

import numpy as np
import pytest

import gp_em

pytestmark = pytest.mark.part7


def test_naive_and_stable_e_step_agree(small_problem):
    p = small_problem
    m_naive, S_naive = gp_em.e_step_naive(p.K, p.y, p.s2, p.sigma2)
    m, S, _, _ = gp_em.e_step(p.K, p.y, p.s2, p.sigma2)
    np.testing.assert_allclose(m, m_naive, atol=1e-8)
    np.testing.assert_allclose(S, S_naive, atol=1e-8)


def test_naive_and_stable_m_step_agree(small_problem):
    p = small_problem
    m, S, alpha, C_inv_K = gp_em.e_step(p.K, p.y, p.s2, p.sigma2)
    stable = gp_em.m_step(p.y, m, S, alpha, C_inv_K, p.s2)
    naive = gp_em.m_step_naive(p.K, p.y, m, S)
    assert stable == pytest.approx(naive, abs=1e-8)


def test_naive_and_stable_em_agree_end_to_end(small_problem):
    p = small_problem
    stable = gp_em.run_em(p.K, p.y)
    naive = gp_em.run_em(p.K, p.y, naive=True)
    np.testing.assert_allclose(stable["log_lik"], naive["log_lik"], atol=1e-8)


def test_stable_e_step_rejects_shape_mismatch(small_problem):
    with pytest.raises(ValueError):
        gp_em.e_step(small_problem.K, small_problem.y[:-1], 1.0, 1.0)


@pytest.mark.parametrize("seed", [0, 1, 2])
@pytest.mark.parametrize("start", [(1.0, 1.0), (0.01, 10.0), (50.0, 0.01)])
def test_stable_em_never_decreases_log_likelihood(seed, start):
    x, _, y = gp_em.sample_data(n=60, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=seed)
    K = gp_em.rbf_kernel(x, x, 1.0)
    history = gp_em.run_em(K, y, s2_0=start[0], sigma2_0=start[1], n_iter=100)
    assert np.all(np.diff(history["log_lik"]) >= -1e-9)


def test_stable_em_is_monotone_when_ill_conditioned(ill_conditioned_problem):
    p = ill_conditioned_problem
    assert np.linalg.cond(p.K) > 1e15  # confirm the fixture is as nasty as claimed
    history = gp_em.run_em(p.K, p.y)
    assert np.all(np.diff(history["log_lik"]) >= -1e-9)


# xfail = "expected to fail". The test still runs; a failure is reported as
# XFAIL rather than as an error. This documents a known defect in the suite
# itself instead of deleting the test or leaving the build red.
# pyproject.toml sets xfail_strict, which would turn an unexpected pass into an
# error. strict=False relaxes that here, because exactly how a naive
# implementation misbehaves depends on details of how you wrote it.
@pytest.mark.xfail(reason="m_step_naive inverts K, which is numerically singular here", strict=False)
def test_naive_em_is_monotone_when_ill_conditioned(ill_conditioned_problem):
    p = ill_conditioned_problem
    history = gp_em.run_em(p.K, p.y, naive=True)
    assert np.all(np.diff(history["log_lik"]) >= -1e-9)
