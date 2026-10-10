# Part 7: Numerical stability

**Goal.** Discover that your correct implementation gives wrong answers, find
out why, and fix it properly.

**You need.** Part 6 passing. Your research from 2.6 and 2.7. Write in
`notes/part-07.md`.

## Section A: something is wrong

**7.1 (Experiment) The real dataset.**
Run your naive EM on the tank-sized problem:

```python
x, f, y = gp_em.sample_data(n=100, s2=2.0, sigma2=0.25, lengthscale=1.0, seed=0)
K = gp_em.rbf_kernel(x, x, 1.0)
history = gp_em.run_em(K, y, naive=True)
```

(a) Plot the log-likelihood against iteration. Describe what you see. (If your
code raises an exception instead, that is also an answer; note where.)

(b) Which property that you proved is violated?

(c) The same code passed all its tests on 20 points. Your derivation is
unchanged. So list the possible kinds of cause. Is this a bug in the maths, in
the code, or in something else?

**7.2 (Experiment) Find the line.**
Do not guess. Narrow it down.

(a) Take one E-step and one M-step from the starting parameters. Which outputs
look unreasonable? (Could $s^2$ be negative? Could it be estimated from this
formula as a sum of things that must be positive?)

(b) For each matrix your code inverts, compute the inverse and multiply it by
the original. How far is each product from the identity? Use
`np.abs(A @ A_inv - np.eye(n)).max()`.

(c) Did NumPy raise an error or a warning?

(d) State precisely which operation is failing.

**7.3 (Experiment) Why that matrix?**

(a) Compute `np.linalg.cond(K)` and the condition number of $C = s^2K + \sigma^2 I$.

(b) Using your rule of thumb from 2.7, how many correct digits should you
expect in `inv(K)`?

(c) Plot the condition number of $K$ against $n$ for $n = 5, 10, \dots, 100$
with the interval $[0, 10]$ and lengthscale 1 fixed. Use a log scale. At
roughly what $n$ does the inverse become meaningless?

(d) Fix $n = 100$ and vary the lengthscale from 0.05 to 1 instead. What happens?

(e) Explain *without formulas* why $K$ is nearly singular. Think about what two
neighbouring rows of $K$ look like.

(f) Why did the 20-point test problem not reveal this? What does that say about
how to choose test cases?

(g) Would replacing `inv(K) @ m` with `np.linalg.solve(K, m)` fix the problem?
Predict, then try it. Refer to your answer to the last question of 2.7.

## Section B: the fix

There are two separate ideas. Do not blur them.

**7.4 (Derive) Cholesky by hand.**

$$A = \begin{pmatrix} 4 & 2 & 2 \\ 2 & 5 & 3 \\ 2 & 3 & 6 \end{pmatrix}$$

(a) Find the lower-triangular $L$ with positive diagonal such that $A = LL^\top$.
Work column by column and write down the general rule you are using.

(b) Solve $Ax = b$ for $b = (6, 5, 8)^\top$ **without inverting anything**:
first solve $Lz = b$ from the top down, then $L^\top x = z$ from the bottom up.

(c) Compute $\log\det A$ from the diagonal of $L$ alone. Verify against the
determinant computed the usual way.

(d) In your algorithm for (a), where would it break down if $A$ were not
positive definite? Connect this to the error you met in 6.2(c).

(e) Count roughly how many multiplications (a) takes for an $n \times n$
matrix, and how many each triangular solve takes.

**7.5 (Derive) Remove $K^{-1}$ from the M-step.**
The trouble is $K^{-1}$, and $K$ is the thing that is ill-conditioned. $C$ is
not. So try to rewrite the $s^2$ update so that only $C^{-1}$ appears. Let
$\alpha = C^{-1} y$.

(a) Write $m$ in terms of $K$, $\alpha$ and $s^2$.

(b) Use (a) to simplify $m^\top K^{-1} m$ until no $K^{-1}$ remains.

(c) Use your formula for $S$ from 3.5 to simplify $\operatorname{tr}(K^{-1} S)$
until no $K^{-1}$ remains.

(d) Write the new $s^2$ update. Which quantities from the E-step does the
M-step now need?

(e) Why is $C$ well conditioned when $K$ is not? If $K$ has eigenvalues
$\lambda_i \ge 0$, what are the eigenvalues of $C$? Give an upper bound on the
condition number of $C$.

**7.6 (Code) Stable functions.**
Add to `gp_em.py`:

| Function | Returns | Notes |
|---|---|---|
| `e_step(K, y, s2, sigma2)` | `(m, S, alpha, C_inv_K)` | `alpha` is $C^{-1}y$; `C_inv_K` is $C^{-1}K$. Same validation as `e_step_naive`. No call to `inv`. |
| `m_step(y, m, S, alpha, C_inv_K, s2)` | `(s2_new, sigma2_new)` | `s2` is the value the E-step was run with. No $K^{-1}$ in any form. |

Use `scipy.linalg.cho_factor` and `cho_solve`. Then:

(a) Rewrite `log_marginal_likelihood` to use the Cholesky factor for both the
solve and the log-determinant, if it does not already.

(b) Make `run_em` use the stable functions when `naive=False`.

(c) Before running anything: what is the single most informative test you can
write for the stable functions, given that you already have naive ones? On
which kind of problem is that test valid?

**7.7 (Experiment) Confirm.**
Repeat 7.1 with `naive=False`. Plot both log-likelihood traces on one figure.
Is the invariant restored? Run `.venv/bin/pytest -m part7`.

**7.8 (Code) Record the defect.**
The naive functions are still in your file and still broken on ill-conditioned
problems. Look up `pytest.mark.xfail`. Write a test in `tests/` that asserts
naive EM is monotone on the 100-point problem and mark it as an expected
failure with a reason. Why is this better than deleting the test, and better
than leaving it failing?

## Section C: reflect

**7.9 (Think)**

(a) NumPy returned a matrix of ordinary-looking numbers and no error. What
alerted you? What would have happened if you had not been tracking it?

(b) Write down three habits, general enough to apply to any numerical project,
that this part suggests.

(c) "Never invert a matrix" is common advice. Based on this part, state the
advice more precisely: which of your two fixes addressed which problem?

## Checkpoint

- `pytest -m part7` passes (one test is reported as `xfailed`; read it to see why).
- You can explain the difference between an ill-conditioned *problem* and an
  unstable *algorithm*.

Then compare with `answer_key/discussion.md`, Part 7, and with `e_step` and
`m_step` in `answer_key/gp_em.py`.

Next: [Part 8](08-is-the-answer-good.md)
