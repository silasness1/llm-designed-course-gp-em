# Part 8: Is the answer any good?

**Goal.** Your code now runs and satisfies its invariants. Find out how good
its answers are, by designing and running a simulation study.

**You need.** Part 7 passing. Write in `notes/part-08.md`. A notebook is the
natural place for the experiments.

## Section A: two more functions

**8.1 (Code) `fit_direct`.**

| Function | Returns |
|---|---|
| `fit_direct(K, y, s2_0=1.0, sigma2_0=1.0)` | `(s2, sigma2, log_lik)` at the maximum |

Maximise the log marginal likelihood using `scipy.optimize.minimize`. This is
an independent route to the same answer as EM.

(a) The optimiser may try negative variances. Find a way to make that
impossible without using constraints. (Hint: optimise over something else.)

(b) EM and `fit_direct` share `log_marginal_likelihood`. So what kind of bug
would their agreement *not* detect? What protects you against that kind?

**8.2 (Derive, Code) `predict`.**

| Function | Returns |
|---|---|
| `predict(x_train, y, x_test, s2, sigma2, lengthscale)` | `(mean, var)`: posterior mean and variance of $f$ at each test input |

(a) Let $f_*$ be the function values at new inputs. Write the joint
distribution of $(f_*, y)$. You need a kernel matrix between test and training
inputs; call it $K_*$.

(b) Use 2.2 to derive the posterior mean and the *diagonal* of the posterior
covariance of $f_*$.

(c) Implement it without `inv`. Two tests to write: what should `predict`
return when the test inputs equal the training inputs? What should it return
at a test input very far from all the data?

(d) Run `.venv/bin/pytest -m part8`.

(e) Plot the data, the true `f`, the posterior mean on a fine grid, and a band
of ±2 standard deviations, using the parameters EM found.

## Section B: looking at the likelihood

**8.3 (Experiment) The surface.**
With two parameters you can draw the whole function being maximised.

(a) Evaluate the log marginal likelihood on a grid over $s^2$ and $\sigma^2$
(use log-spaced values) for the 100-point dataset, and draw a contour plot.

(b) Overlay the path EM takes from a poor starting point, one marker per
iteration. Mark the `fit_direct` optimum and the true parameters.

(c) Describe the shape of the region near the top. In which direction is it
long? Connect that to 4.4 and 4.5.

(d) The true parameters are not at the top. Is that a failure? Of what?

**8.4 (Experiment) How fast is EM?**

(a) Plot (maximum log-likelihood − log-likelihood at iteration $k$) against $k$
with a log scale on the vertical axis. What shape is it? What does that shape
mean about how the error shrinks per iteration?

(b) Where on the path in 8.3(b) does EM take big steps and where small ones?

(c) *Stretch.* Show algebraically that the stable M-step for $s^2$ can be
written as $s^2 + c \cdot \partial L / \partial s^2$ for some positive $c$
depending on $s^2$ and $n$. What is EM, seen this way? Verify numerically with
a finite-difference derivative.

## Section C: a simulation study

One dataset cannot tell you whether a method is reliable. You need the
distribution of its answers over many datasets.

**8.5 (Design) Plan before running.**
Write a short plan (half a page) that states:

- the question each experiment answers,
- what is held fixed and what varies between replications,
- how many replications, and why that number is enough for the precision you
  need,
- exactly which summaries you will compute, using your success measures from
  1.6,
- what result you expect. Write it down.

**8.6 (Experiment) Are the estimators accurate?**
Simulate at least 200 datasets from the model with the true parameters
$s^2 = 2$, $\sigma^2 = 0.25$, $\ell = 1$, $n = 100$. Fit each.

(a) Plot the distribution of $\hat s^2$ and of $\hat\sigma^2$, each with the
truth marked.

(b) For each, report the mean, the median, and the interval containing the
middle 90% of estimates.

(c) Which parameter is estimated well? By roughly what factor can the other be
off? Does this match 4.2(b)?

(d) Go back to your single-dataset result from 7.7. Where does it fall in these
distributions? Was it unusual?

**8.7 (Experiment) Is the uncertainty honest?**
For each simulated dataset, compute the fraction of the 100 points at which the
true $f$ lies inside the band $m \pm 2\sqrt{S_{ii}}$.

(a) What fraction would you expect if everything were exactly right?

(b) Report the average coverage using the *true* parameters, and using the
*estimated* parameters.

(c) $\hat s^2$ is often badly wrong, by 8.6. Is the band badly wrong too?
Revisit your guess in 4.2(c).

(d) The band treats the estimated parameters as if they were known exactly. Is
that an approximation that matters here? How do you know?

**8.8 (Experiment) Test your prediction from 4.7.**
Repeat 8.6 (100 replications is enough, and `fit_direct` is faster) for 400
points on $[0, 10]$ and for 400 points on $[0, 40]$. Use the `x_max` argument.
Compare the spread of each estimator across the three designs. Were you right?
State the conclusion as advice to someone planning an experiment.

**8.9 (Experiment) Race the crude estimator.**
Implement your matrix-free estimator of $\sigma^2$ from 4.5(d). Over the same
simulated datasets, compare its mean and spread with those of the EM estimate.

(a) Is it biased as you predicted?

(b) How much precision does the full model buy over the crude estimator?

(c) The crude estimator needs far fewer assumptions. List which of the
assumptions in 4.1 it still needs and which it does not. When would you prefer
it?

## Checkpoint

- `pytest -m part8` passes, and `pytest` passes in full.
- You can state, with numbers, how well each parameter is estimated and whether
  the bands are honest when the model is right.

Then compare with `answer_key/discussion.md`, Part 8, with section 8 of
`answer_key/gp_em_tutorial.ipynb`, and with the first half of
`answer_key/investigations.ipynb`.

Next: [Part 9](09-when-the-model-is-wrong.md)
