# Part 6: Implement the naive version

**Goal.** Turn your derivations into working code, one function at a time,
testing each before writing the next.

**You need.** Part 5 finished. The Python environment from Part 0. Create
`gp_em.py` in the project root (not inside `worksheet/` or `answer_key/`).

"Naive" means: transcribe the formulas exactly as you derived them, using
`np.linalg.inv` wherever a formula has an inverse. That is the right first
version. Part 7 is about what is wrong with it.

## The interface

Use these names and signatures so that the provided checks can call your code.

| Function | Returns | Notes |
|---|---|---|
| `rbf_kernel(x1, x2, lengthscale)` | array of shape `(len(x1), len(x2))` | `x1`, `x2` are 1-D arrays. Raise `ValueError` if `lengthscale <= 0`. |
| `sample_data(n, s2, sigma2, lengthscale, seed, x_max=10.0)` | `(x, f, y)` | `x = np.linspace(0, x_max, n)`. The same seed must give the same data. |
| `log_marginal_likelihood(K, y, s2, sigma2)` | float | Raise `ValueError` if either variance is `<= 0` or if `K` is not `n × n` for `n = len(y)`. |
| `e_step_naive(K, y, s2, sigma2)` | `(m, S)` | Same validation as above. |
| `m_step_naive(K, y, m, S)` | `(s2_new, sigma2_new)` | |
| `run_em(K, y, s2_0=1.0, sigma2_0=1.0, n_iter=200, tol=1e-8, naive=False)` | dict with keys `"s2"`, `"sigma2"`, `"log_lik"` | Each value is a list with one entry per parameter value visited, **including the starting point**. Stop early when the log-likelihood changes by less than `tol` in absolute value. In this part only `naive=True` needs to work. |

`K` always means the unit-variance kernel matrix; $s^2$ is passed separately.

## A ten-minute pytest primer

pytest finds files named `test_*.py`, runs every function named `test_*`, and
reports a failure if the function raises. A bare `assert` is all you need.

```python
# tests/test_mine.py
import numpy as np
import pytest
import gp_em

def test_kernel_of_a_point_with_itself_is_one():
    K = gp_em.rbf_kernel(np.array([3.0]), np.array([3.0]), lengthscale=2.0)
    assert K[0, 0] == pytest.approx(1.0)
```

| You want to | Use |
|---|---|
| Compare two floats | `assert a == pytest.approx(b)`; never `==` alone |
| Compare two arrays | `np.testing.assert_allclose(a, b)` |
| Check that bad input is rejected | `with pytest.raises(ValueError): ...` |
| Run one test over several inputs | `@pytest.mark.parametrize("n", [5, 20, 50])` |
| Share setup between tests | a function decorated with `@pytest.fixture` |

| Command | Effect |
|---|---|
| `.venv/bin/pytest tests` | run your tests |
| `.venv/bin/pytest tests -v` | one line per test |
| `.venv/bin/pytest tests -k kernel` | only tests with "kernel" in the name |
| `.venv/bin/pytest tests -x` | stop at the first failure |
| `.venv/bin/pytest -m part6` | run the provided checks for this part |
| `.venv/bin/pytest --key -m part6` | run those checks against the answer key instead of your code |

**The routine for every function below:** (1) write at least one test in
`tests/` from your list in 5.8, (2) run it and watch it fail, (3) write the
function, (4) run it and watch it pass. Watching the test fail first proves the
test is capable of failing.

Do not read the files in `checks/` until you have written your own tests for
the function concerned. Afterwards they are worth reading: each file is
commented as an example of a pytest technique.

## Tasks

**6.1 (Code) `rbf_kernel`.**
Before coding: what properties must *every* valid kernel matrix of a set of
points with itself have? You should be able to name at least three. Each is a
test. Then write the function. Avoid Python loops; look up NumPy broadcasting.

**6.2 (Code) `sample_data`.**

(a) You have a generator of independent standard normals $z$. How do you turn
$z$ into a draw from $\mathcal N(0, \Sigma)$? Prove that your recipe has the
right covariance.

(b) Write the function. Use `np.random.default_rng(seed)`.

(c) Try `n=100, lengthscale=1.0`. If something raises an error, read the
message carefully and work out what it is telling you about $K$. Find the
standard remedy (a small search will turn it up; it has a name) and explain why
it changes the answer negligibly.

(d) How do you test a function whose output is random? Write at least two
tests.

(e) Plot `f` and `y` against `x` for a few seeds and a few lengthscales. Does
it look like the tank?

**6.3 (Code) `log_marginal_likelihood`.**
Implement your formula from 3.6. Find a function in SciPy that computes the
log-density of a multivariate normal and use it *in a test* as an independent
reference, not in the implementation.

Question to answer in your notes: `np.linalg.det` of a 500 × 500 covariance
matrix will often return exactly `0.0` or `inf`. Why? Which NumPy function
avoids the problem?

**6.4 (Code) `e_step_naive`.**
Implement $m$ and $S$ from 3.5. Tests to consider: your hand calculation from
3.7; properties $S$ must have as a covariance matrix; whether $m$ is closer to
the true `f` than `y` is.

**6.5 (Code) `m_step_naive`.**
Implement the updates from 5.4.

**6.6 (Code) `run_em`.**
Implement the loop from your pseudo-code in 5.4(b). Record the log marginal
likelihood at the starting point and after every M-step.

**6.7 (Experiment) First run.**
Use a deliberately easy problem:

```python
x, f, y = gp_em.sample_data(n=20, s2=2.0, sigma2=0.25, lengthscale=0.5, seed=0)
K = gp_em.rbf_kernel(x, x, 0.5)
history = gp_em.run_em(K, y, naive=True)
```

(a) Plot the log-likelihood against iteration. Does it ever decrease? If it
does, you have a bug: 5.5 says so.

(b) Plot $s^2$ and $\sigma^2$ against iteration, each on its own axes, with the
true values marked.

(c) Do the estimates end at the true values? Should they? Distinguish "EM
failed to find the maximum" from "the maximum is not at the truth". Which is
it, and how could you tell the two apart?

(d) Run from three very different starting points. Do they end in the same
place?

**6.8 (Code) The provided checks.**
Run `.venv/bin/pytest -m part6`. Fix anything that fails. Then read
`checks/test_part6_naive.py` and `checks/conftest.py`. Note any test idea there
that you had not thought of, and any of yours that is not there.

**6.9 (Experiment) Test your identification prediction.**
Build the model from 4.3: `K = np.eye(n)` with `n = 200`, and `y` drawn as
independent normals with variance 2.25. Run EM from the starting points
`(1, 1)`, `(0.1, 5)` and `(5, 0.1)`.

(a) What do the three runs agree on? What do they disagree on?

(b) Compare with your prediction in 4.3(e).

(c) EM reported convergence in every run and raised no error. What does that
tell you about relying on an algorithm to warn you about identification?

## Checkpoint

- `pytest -m part6` passes.
- You have your own tests in `tests/`, and they pass.
- You can explain every line of `gp_em.py` by pointing at a formula in your
  notes.

Then compare with `answer_key/discussion.md`, Part 6. You may also now read the
naive functions in `answer_key/gp_em.py`, but not yet `e_step` or `m_step`.

Next: [Part 7](07-numerical-stability.md)
