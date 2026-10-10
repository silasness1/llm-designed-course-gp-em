"""Shared fixtures.

pytest imports this file automatically. A fixture is a function that builds
something tests need; a test asks for it simply by naming it as an argument,
and pytest calls the fixture and passes the result in. That keeps setup code
in one place instead of copied into every test.
"""

from types import SimpleNamespace

import pytest


def _make_problem(n, lengthscale, seed):
    # Imported here, not at the top, because which gp_em.py to use (yours or
    # the answer key) is only decided after pytest has read its options.
    import gp_em

    s2, sigma2 = 2.0, 0.25
    # A fixed seed makes the "random" data identical on every run, so a test
    # that passes today cannot fail tomorrow by bad luck.
    x, f, y = gp_em.sample_data(n, s2, sigma2, lengthscale, seed)
    K = gp_em.rbf_kernel(x, x, lengthscale)
    return SimpleNamespace(x=x, f=f, y=y, K=K, s2=s2, sigma2=sigma2, lengthscale=lengthscale)


@pytest.fixture
def small_problem():
    """20 points, short lengthscale: K is well conditioned (cond about 40)."""
    return _make_problem(n=20, lengthscale=0.5, seed=0)


@pytest.fixture
def ill_conditioned_problem():
    """100 points, long lengthscale: K is singular to machine precision."""
    return _make_problem(n=100, lengthscale=1.0, seed=0)
