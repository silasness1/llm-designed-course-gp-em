# Model answers

**Spoilers.** Read only the part you have finished.

For open questions these are examples of a strong answer, not the only one.
Numbers come from `answer_key/gp_em.py`, `gp_em_tutorial.ipynb` and
`investigations.ipynb`. Your own numbers will differ in detail if your
`sample_data` draws its random numbers in a different order; the conclusions
should not.

---

## Part 1

**1.1** Different in kind:

- The temperature at a logged time (one number per time; 100 numbers).
- The temperature between logged times, or the whole curve (a function).
- The noise level of the probe (one number).
- How much the temperature typically varies in a batch (one number).
- Derived features: the peak, the time of the peak, time spent above a threshold.

**1.2** The probe's noise level is a property of the probe and should repeat.
Today's curve is a property of today's batch and will not repeat. The typical
size of temperature swings is a property of batches in general. One day gives
100 looks at the probe's noise, one look at one curve, and one draw from the
population of curves. The last is the one that needs many days.

**1.3** $y_i = f(t_i) + \varepsilon_i$. Assumptions hidden in it: the error is
additive (not, say, proportional); the timestamps are exact; the probe measures
the temperature that matters (not a lagged or spatially local one); the probe
is not biased, which needs a further statement that $\varepsilon$ has mean zero.

**1.4** (a) 100 true temperatures plus 100 errors: 200 unknowns, 100 equations.
Setting every error to zero and $f(t_i) = y_i$ fits perfectly and says the
probe is perfect. (b) OLS replaces 100 unknown function values with $p$
coefficients, leaving $n - p$ degrees of freedom to estimate the noise. (c)
Something like: "readings six minutes apart are of nearly the same true
temperature; readings five hours apart tell me almost nothing about each
other." That is a statement about how *correlation between true values decays
with separation*, and it is exactly what a kernel encodes.

**1.5** For "the curve": estimand $f$, nuisances $\sigma^2$ and whatever
describes smoothness. For "how noisy is the probe": estimand $\sigma^2$,
nuisance $f$. The same quantity can be the estimand in one question and a
nuisance in another.

**1.6** (a) Simulate: generate a curve, add known noise, hide the curve, run
the method, compare. (b) Accuracy: root-mean-square error of the estimated
curve against the true one. Honesty: the fraction of points at which the truth
falls inside the stated interval (coverage). (c) Over many uses, intervals
stated as "±2 standard deviations" should contain the truth about 95% of the
time. Honesty is a property of the procedure over repetitions, not of one
interval.

---

## Part 2

A strong summary hits these points.

**2.1** A latent variable is a random quantity in the model that is never
observed. A parameter is a fixed unknown; a latent variable has a distribution
*given* the parameters, and usually there is one per observation, so their
number grows with the data. Examples: a student's ability behind exam scores;
which cluster a data point belongs to; the true position behind GPS readings.
$\varepsilon$ in OLS: it is random and unobserved, so formally latent, but once
$\beta$ is known it is determined by the data ($\varepsilon = y - X\beta$), so
nobody treats it as one. In the tank, the latent variable is the true
temperature $f$.

**2.2** For $\begin{pmatrix} a \\ b\end{pmatrix} \sim \mathcal N\!\left(\begin{pmatrix}\mu_a \\ \mu_b\end{pmatrix}, \begin{pmatrix}\Sigma_{aa} & \Sigma_{ab} \\ \Sigma_{ba} & \Sigma_{bb}\end{pmatrix}\right)$:

- marginal: $a \sim \mathcal N(\mu_a, \Sigma_{aa})$ (just read off the blocks);
- conditional: $a \mid b \sim \mathcal N\big(\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(b - \mu_b),\; \Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}\big)$.

The conditional covariance does not depend on the observed value $b$.

**2.3** Definition: a collection of random variables, any finite number of
which are jointly Gaussian. Specified by a mean function and a covariance
function (kernel). The kernel gives the covariance between function values at
two inputs. RBF: $k(x, x') = s^2\exp(-(x - x')^2/(2\ell^2))$; $\ell$ sets the
distance over which values stay correlated, hence how wiggly draws are. Both
statements are true because the definition is about finite subsets: evaluate at
your $n$ inputs and you have an ordinary $n$-dimensional Gaussian.
"Nonparametric" because the number of unknowns describing the function ($f$ at
every input) is not fixed in advance; $s^2$, $\ell$ are few *hyperparameters*
describing the prior, not the function.

**2.4** Prior: the GP on $f$. Likelihood: $y \mid f$, Gaussian noise. Posterior:
$f \mid y$, also a GP. The role of $\beta$ is played by $f$ itself. The
posterior gives a full distribution, so uncertainty at every input, not just a
curve. Marginal likelihood: $p(y \mid \text{hyperparameters})$ with $f$
integrated out.

**2.5** For maximum likelihood when the model has latent variables that make
the likelihood awkward but would make it easy if observed. E-step: using
current parameters, work out the distribution of the latent variables given the
data. M-step: choose new parameters to best fit the data together with that
distribution of latent variables. Guarantee: the likelihood never decreases.
Not guaranteed: reaching the global maximum; reaching anything quickly.
Mixture of Gaussians: latent variable is which component each point came from.

**2.6** $A = LL^\top$ with $L$ lower triangular; exists for symmetric positive
definite matrices. Solving with it is about twice as fast as general
elimination, numerically stable without pivoting, and gives the determinant
from the diagonal. Cost about $n^3/3$ operations. Uses (any three, in different
fields): solving the normal equations in least squares; generating correlated
random numbers in Monte Carlo simulation (finance, risk); Kalman filtering in
navigation (square-root filters); interior-point optimisation solvers; finite
element structural analysis; Gaussian process software.

**2.7** $\kappa(A) = \lVert A\rVert\,\lVert A^{-1}\rVert$, equal to the ratio of
largest to smallest singular value. Rule of thumb: solving with a matrix of
condition number $10^k$ loses about $k$ decimal digits. A double carries about
16. Conditioning is a property of the *problem* (the matrix); stability is a
property of the *algorithm*. A good algorithm cannot rescue an ill-conditioned
problem; it can only avoid making it worse.

---

## Part 3

**3.1** (a) $\mathbb E[a \mid b] = \dfrac{\sigma_{ab}}{\sigma_b^2}\, b$,
$\;\operatorname{Var}(a \mid b) = \sigma_a^2 - \dfrac{\sigma_{ab}^2}{\sigma_b^2}$.
(b) The OLS slope converges to $\sigma_{ab}/\sigma_b^2$: the same. Conditioning
a Gaussian *is* population regression. (c) $\sigma_a^2(1 - \rho^2)$: no
reduction at $\rho = 0$, zero remaining variance as $\rho \to \pm1$.

**3.2** (a) Mean zero; $\operatorname{Cov}(\beta) = \tau^2 I$,
$\operatorname{Cov}(\beta, y) = \tau^2 X^\top$,
$\operatorname{Cov}(y) = \tau^2 XX^\top + \sigma^2 I$.
(b) $\mathbb E[\beta \mid y] = \tau^2 X^\top(\tau^2 XX^\top + \sigma^2 I)^{-1} y$.
(c) From $X^\top(XX^\top + \lambda I) = (X^\top X + \lambda I)X^\top$ it follows
that $X^\top (XX^\top + \lambda I)^{-1} = (X^\top X + \lambda I)^{-1} X^\top$.
With $\lambda = \sigma^2/\tau^2$ the two forms agree. (d) $\lambda \to 0$: OLS.
An infinitely vague prior gives no shrinkage.

**3.3** (a) $f \sim \mathcal N(0, \tau^2 XX^\top)$. (b) $K = XX^\top$:
$f \sim \mathcal N(0, \tau^2 K)$, $y \mid f \sim \mathcal N(f, \sigma^2 I)$.
(c) $K_{ij} = x_i^\top x_j$, the inner product of the feature vectors of
observations $i$ and $j$: large when the two observations have similar
features, hence similar $f$. (d) Rank at most $p$: $f$ is confined to the
$p$-dimensional column space of $X$. A linear model only allows a
$p$-dimensional family of functions.

**3.4** (a) Yes: for inputs much closer than $\ell$, $K_{ij} \approx 1$; for
inputs several $\ell$ apart, $K_{ij} \approx 0$. (b) Symmetric and positive
semi-definite. Symmetry is obvious; positive semi-definiteness is not. It is a
theorem (Bochner's) about this function. A sensible response is to take it on
trust and check eigenvalues numerically, which becomes a test in Part 6. The
RBF kernel has full rank in exact arithmetic: unlike 3.3(d), any $f$ is possible.

**3.5** (a) $C = s^2 K + \sigma^2 I$. (b) $\operatorname{Cov}(f, y) = s^2 K$.
(c) $m = s^2 K C^{-1} y$, $\;S = s^2 K - s^2 K C^{-1} s^2 K$. (d) It depends on
where the inputs are and on the parameters, not on the readings. The same is
true in OLS: $\operatorname{Var}(\hat\beta) = \sigma^2 (X^\top X)^{-1}$ does not
involve $y$. It is a special property of Gaussian models, and a warning: the
stated uncertainty cannot react to data that contradict the model.

**3.6** (a) $y \sim \mathcal N(0, C)$.
(b) $\log p(y) = -\tfrac12 y^\top C^{-1} y - \tfrac12 \log|C| - \tfrac n2 \log 2\pi$.
(c) The quadratic term rewards fit: it is small when $C$ assigns large variance
in the directions $y$ points. The log-determinant penalises volume: a $C$ with
large variances spreads probability over many possible datasets and so gives
less to any one of them. This trade-off is why maximising it does not simply
drive the noise to zero.

**3.7** (a) $C^{-1} = \dfrac{1}{4 - \rho^2}\begin{pmatrix} 2 & -\rho \\ -\rho & 2\end{pmatrix}$,
so $m = \dfrac{1}{4 - \rho^2}\begin{pmatrix} 4 - 2\rho^2 \\ 2\rho \end{pmatrix}$.
(b) $\rho = 0$: $(1, 0)$. $\rho = 0.8$: $(0.810, 0.476)$. $\rho = 1$: $(2/3, 2/3)$.
(c) Factor $\tfrac12 = s^2/(s^2 + \sigma^2)$: the regression slope of $f_i$ on
$y_i$ from 3.1, with signal and noise variance equal. (d) $\rho = 1$ says
$f_1 = f_2$, so the two readings measure the same thing. Average them: 1, with
noise variance $\tfrac12$. Shrink by $1/(1 + \tfrac12) = \tfrac23$. (e) From the
first reading, through the prior correlation: the model believes $f_2$ is
probably near $f_1$, and $y_1$ says $f_1$ is positive.

**3.8** (a) No. Its eigenvalues are $s^2\lambda_i/(s^2\lambda_i + \sigma^2)$,
strictly between 0 and 1 (for the 100-point dataset at the true parameters they
range from 0 to 0.995), so it shrinks rather than projects. Smoothing an
already smoothed curve smooths it further. (b) $\sigma^2 \to 0$: towards the
rank of $K$, at most $n$ (interpolate the data). $\sigma^2 \to \infty$: towards
0 (ignore the data). Larger $\ell$: fewer. For the 100-point dataset at the
true parameters it is 11.3: the model behaves like a regression with about 11
coefficients.

**Checkpoint.** GP regression is ridge regression in which you specify the
similarity matrix $K$ between observations directly instead of building it from
a design matrix.

---

## Part 4

**4.1** A list of ten:

| Assumption | Comment for the tank |
|---|---|
| Noise is additive | Plausible for electrical noise. |
| Noise has mean zero | Unverifiable from this data: a constant bias is invisible. |
| Noise is independent between readings | Doubtful: cheap sensors drift. The key identifying assumption (4.5, 4.6). |
| Noise has constant variance | Doubtful if noise depends on temperature or on what the cooling system is doing. |
| Noise is Gaussian | Convenient. Occasional glitches would violate it. |
| $f$ is a draw from a GP | Convenient. Nobody believes it literally. |
| $f$ has mean zero | False for a temperature; in practice subtract the average or add a mean term. |
| Same smoothness and scale everywhere | Doubtful: a cooling failure is a sudden event. |
| The lengthscale is known | Rarely true. |
| Input times are exact | Usually fine. |

Least defensible for most people: independent noise and uniform smoothness.
Symptoms are the subject of Part 9.

**4.2** (a) $\sigma^2$: the probe. $s^2$: batches in general. (b) 100
independent looks at the noise; one draw of the curve. Expect $\sigma^2$ to be
learned well and $s^2$ poorly. (c) A nuisance. Part 8 shows the curve estimate
and its bands are good even when $\hat s^2$ is far off.

**4.3** (a) $y \sim \mathcal N(0, (s^2 + \sigma^2) I)$.
(b) $-\tfrac{1}{2v}\sum y_i^2 - \tfrac n2 \log v - \tfrac n2\log 2\pi$ with
$v = s^2 + \sigma^2$. (c) Neither is identified; the sum is. (d) No and no.
Non-identification is a property of the model: the data distribution is
literally the same for different parameter values. (e) The sum converges to the
mean of $y_i^2$; the split is arbitrary and depends on the start.

**4.4** (a) Differences between readings are free of $c$, so the sample
variance of $y$ estimates $\sigma^2$ with 99 degrees of freedom: relative
standard deviation about $\sqrt{2/99} \approx 14\%$.
(b) $\bar y \sim \mathcal N(0, s^2 + \sigma^2/n)$.
(c) $\hat s^2 = \bar y^2 - \hat\sigma^2/n$. It uses one piece of information:
a single draw of $c$. (d) Its standard deviation is about $\sqrt 2 \approx 1.4$
times the thing being estimated. More readings only shrink $\sigma^2/n$, which
was already negligible. (e) Identified means "could be learned with infinite
data of the right kind". Here the right kind is more *days*, not more readings.

**4.5** (a) $\mathbb E[(y_i - y_j)^2] = 2\sigma^2 + 2s^2(1 - K_{ij})$.
(b) Close together: $2\sigma^2$. Far apart: $2\sigma^2 + 2s^2$. (c) How much
readings taken close together disagree. (d)
$\hat\sigma^2_{\text{crude}} = \dfrac{1}{2(n-1)}\sum_{i}(y_{i+1} - y_i)^2$.
Biased upward by $s^2(1 - K_{i,i+1})$, because neighbouring $f$ values are not
quite equal. For the worksheet's setup that bias is 0.010, about 4%.
(e) That the noise is independent between readings while the signal is smooth.

**4.6** (a) $s^2 K + \sigma^2 K_\varepsilon$. (b) Only $s^2 + \sigma^2$, as in
4.3. (c) No. Two probes side by side would: they share the temperature but not
the drift, so their difference isolates probe error. So would calibration
against a trusted reference. Identification problems are usually fixed by
design, not by analysis.

**4.7** Both options give 400 noise draws, so both sharpen $\hat\sigma^2$, and
equally. Only option B, which observes four times as many wiggles, does much
for $\hat s^2$. Measured in Part 8.

**4.8** From physics (thermal mass and the response time of the cooling system)
or from earlier batches. If $\ell$ is estimated too, it trades off against
$s^2$: a taller, slower-varying function and a shorter, faster one can look
alike over a finite window, which makes the weak identification of $s^2$ worse.

---

## Part 5

**5.1** $\log p(y, f \mid \theta) = -\dfrac n2\log\sigma^2 - \dfrac{\lVert y - f\rVert^2}{2\sigma^2} - \dfrac n2\log s^2 - \dfrac{f^\top K^{-1} f}{2 s^2} + \text{const}$.
The two parameters are completely separated: $\sigma^2$ appears only with
$y - f$, $s^2$ only with $f$.

**5.2** (a) $\hat\sigma^2 = \lVert y - f\rVert^2/n$: the mean squared residual.
(b) $\hat s^2 = f^\top K^{-1} f / n$. With $f = sLz$, $f^\top K^{-1} f = s^2 z^\top z$:
it undoes the correlations and measures the size of the $n$ independent
standard normals behind $f$. $f^\top f$ would treat 100 highly correlated
values as 100 independent pieces of evidence.

**5.3** (a) Write $f = m + e$; cross terms vanish;
$\mathbb E[e^\top A e] = \operatorname{tr}(A\,\mathbb E[ee^\top]) = \operatorname{tr}(AS)$.
(b) $\lVert y - m\rVert^2 + \operatorname{tr}(S)$ and
$m^\top K^{-1} m + \operatorname{tr}(K^{-1}S)$. (c) Plugging in $m$ drops both
trace terms, which are positive, so it underestimates both variances. $m$ is
the *average* of the plausible curves, and an average is smoother and smaller
than the things averaged.

**5.4** (a) $\sigma^2_{\text{new}} = \big(\lVert y - m\rVert^2 + \operatorname{tr}(S)\big)/n$,
$\;s^2_{\text{new}} = \big(m^\top K^{-1} m + \operatorname{tr}(K^{-1}S)\big)/n$,
with $m$, $S$ computed from the old parameters. (c) The log marginal likelihood.

**5.5** (a) $L(\theta) = \log\mathbb E_q\!\left[\dfrac{p(y, f\mid\theta)}{q(f)}\right] \ge \mathbb E_q\!\left[\log\dfrac{p(y, f\mid\theta)}{q(f)}\right]$.
(b) With $q = p(f \mid y, \theta)$ the ratio equals $p(y \mid \theta)$, a
constant in $f$, and Jensen is an equality for a constant. (c) Only
$\mathbb E_q[\log p(y, f\mid\theta)]$: the expected complete-data
log-likelihood from 5.1 to 5.4. (d) First step: the bound (a) holds for any
$q$ and $\theta$. Second: $\theta_1$ maximises $F(q_0, \cdot)$. Third: (b) at
$\theta_0$. (e) It is an invariant that must hold on every dataset at every
iteration, so any violation proves there is a bug, without needing to know the
right answer.

**5.6** (a) No and no. It can stop at a local maximum or crawl along a ridge.
(b) The proof holds; the likelihood still never decreases. But the likelihood
is constant along the line $s^2 + \sigma^2 = v$, so there are infinitely many
maximisers and EM stops at whichever one the starting point leads to.

**5.7–5.10** The answer key's design is the interface table in Part 6 plus
`e_step`, `m_step`, `fit_direct` and `predict`. Defensible alternatives:
wrapping everything in a class; having `run_em` take `x` and a lengthscale and
build $K$ itself (simpler to call, but recomputes $K$ and hides the object the
maths is about); merging the E and M steps (shorter, but you lose the ability
to test each against its formula). Things that can make correct-looking code
wrong (5.9): rounding error in ill-conditioned inverses; confusing variance
with standard deviation; using new parameters where old ones belong; a kernel
matrix with $s^2$ already folded in being scaled twice.

---

## Part 6

**6.1** Symmetric; ones on the diagonal; all entries in $(0, 1]$; positive
semi-definite; entries decrease with distance.

**6.2** (a) $f = \sqrt{s^2}\,Lz$ with $K = LL^\top$:
$\operatorname{Cov}(f) = s^2 L\,\mathbb E[zz^\top]L^\top = s^2 K$. (c) Cholesky
reports that $K$ is not positive definite. In exact arithmetic it is, but its
smallest eigenvalues are far below $10^{-16}$ and rounding makes some slightly
negative. The remedy is *jitter*: factor $K + 10^{-8} I$. That changes each
variance by one part in $10^8$. (d) Same seed gives identical output; different
seeds differ; shapes; with large $n$, the sample variance of $y - f$ is near
$\sigma^2$ within a tolerance chosen from its standard error.

**6.3** A determinant is a product of $n$ eigenvalues; 500 factors each around
0.3 underflow to zero (and large ones overflow). `np.linalg.slogdet` returns
the logarithm directly. Reference for the test:
`scipy.stats.multivariate_normal.logpdf`.

**6.7** With the answer key's data: 165 iterations to $\hat s^2 = 1.638$,
$\hat\sigma^2 = 0.084$, against truth 2 and 0.25. (c) The maximum is not at the
truth. Evidence: different starting points reach the same place, the
log-likelihood there is higher than at the true parameters, and (in Part 8) an
independent optimiser agrees. Twenty noisy points simply do not determine the
parameters well.

**6.9** With the answer key (mean of $y_i^2$ was 2.079):

| Start $(s^2, \sigma^2)$ | End | Sum |
|---|---|---|
| (1, 1) | (1.040, 1.040) | 2.079 |
| (0.1, 5) | (0.099, 1.981) | 2.079 |
| (5, 0.1) | (1.981, 0.099) | 2.079 |

All agree on the sum; the split is whatever the start led to. EM converged and
reported nothing unusual each time. An algorithm cannot tell you a parameter is
unidentified; you find out by analysis (4.3) or by trying several starts.

---

## Part 7

**7.1** The naive log-likelihood rises for a step or two, then drops and
lurches about; in the answer key's run it ends with $\hat s^2 \approx 2\times
10^{-11}$. The monotonicity proved in 5.5 is violated. The mathematics and the
code are unchanged from a version that works, so the cause is the arithmetic.

**7.2** `inv(C)` times $C$ is the identity to about $10^{-15}$. `inv(K)` times
$K$ differs from the identity by an amount of order 10 (the exact value varies
between machines because the result is rounding noise). No error and no
warning. The failing operation is the inversion of $K$ in the $s^2$ update.

**7.3** (a) $\kappa(K) \approx 8\times10^{19}$; $\kappa(C) \approx 190$ at the
true parameters. (b) None: 19 or 20 digits lost out of 16. (c) The condition
number passes $10^{16}$ between 30 and 35 points. (d) At $n = 100$:

| $\ell$ | 0.05 | 0.1 | 0.2 | 0.5 | 1.0 |
|---|---|---|---|---|---|
| $\kappa(K)$ | 1.7 | 63 | $10^{8}$ | $3\times10^{19}$ | $8\times10^{19}$ |

(Values above about $10^{16}$ are themselves unreliable; read them as "too
large to measure".) (e) Neighbouring inputs are so strongly correlated that
neighbouring rows of $K$ are almost identical, and a matrix with two equal rows
is singular. (f) Twenty points at lengthscale 0.5 have condition number about
40. Tests on small, easy problems do not exercise the regime that matters; test
at realistic size. (g) No. With `solve` the first $s^2$ update is still wrong
(about 0.3 where the correct value is 1.085) and the likelihood still
decreases. The *problem* "apply $K^{-1}$" is ill-conditioned; no algorithm for
that problem can help. The fix is to stop needing $K^{-1}$.

**7.4** (a) $L = \begin{pmatrix} 2 & 0 & 0 \\ 1 & 2 & 0 \\ 1 & 1 & 2 \end{pmatrix}$.
(b) $z = (3, 1, 2)^\top$, then $x = (1, 0, 1)^\top$.
(c) $\log\det A = 2(\log 2 + \log 2 + \log 2) = \log 64$, and $\det A = 64$.
(d) At a square root of a non-positive number. That is the "not positive
definite" error from 6.2. (e) About $n^3/3$ for the factorisation and $n^2$ for
each triangular solve.

**7.5** (a) $m = s^2 K\alpha$. (b) $m^\top K^{-1} m = s^2\alpha^\top K K^{-1} m = s^2 \alpha^\top m$.
(c) $\operatorname{tr}(K^{-1}S) = n s^2 - s^4\operatorname{tr}(C^{-1}K)$.
(d) $s^2_{\text{new}} = \big(s^2\alpha^\top m + n s^2 - s^4\operatorname{tr}(C^{-1}K)\big)/n$;
the M-step needs $\alpha$, $C^{-1}K$ and the old $s^2$. (e) Eigenvalues of $C$
are $s^2\lambda_i + \sigma^2 \ge \sigma^2$, so
$\kappa(C) \le (s^2\lambda_{\max} + \sigma^2)/\sigma^2$. The noise variance acts
as a floor under every eigenvalue.

**7.6** (c) Agreement between the naive and stable versions, on a
well-conditioned problem where the naive one can be trusted.

**7.8** Deleting the test loses the knowledge that the defect exists. Leaving
it failing trains everyone to ignore failures. An expected failure records the
defect, keeps the suite green, and (with strict mode) alerts you when it stops
failing.

**7.9** (a) Only the tracked invariant. Without it the program would have
returned a confident, wrong noise variance. (b) For example: monitor a quantity
with a known invariant; check a computed inverse or solution by substituting it
back; look at condition numbers before trusting a solve; test at realistic
problem sizes; keep a simple reference implementation to compare against. (c)
Two different things were fixed. Removing $K^{-1}$ by algebra fixed an
ill-conditioned *problem*. Replacing `inv(C)` with Cholesky solves is about
using a better *algorithm* on a well-conditioned problem: faster, a little more
accurate, and it gives the log-determinant, but it was not what made the
likelihood decrease.

---

## Part 8

**8.1** (a) Optimise over $\log s^2$ and $\log\sigma^2$. (b) A bug in
`log_marginal_likelihood` itself: both methods would agree on the wrong
maximum. The test against SciPy's multivariate normal density guards that.

**8.2** Mean $s^2 K_* C^{-1} y$; variance
$s^2 - s^4\operatorname{diag}(K_* C^{-1} K_*^\top)$. At the training inputs it
must reproduce $m$ and the diagonal of $S$. Far from all data it must return
the prior: mean 0, variance $s^2$.

**8.3** The top of the surface is a ridge, long in the $s^2$ direction and
narrow in $\sigma^2$: the picture of "little information about $s^2$". The
truth not being at the top is not a failure of anything. The maximum is the
best explanation of this dataset; the truth is one of many parameter values
that explain it nearly as well.

**8.4** (a) A straight line on the log scale: each iteration removes a fixed
fraction of the remaining gap (linear convergence). In the answer key's run
from $(0.1, 4)$ it takes 81 iterations to get within $10^{-6}$. (c)
$s^2_{\text{new}} = s^2 + \dfrac{2s^4}{n}\dfrac{\partial L}{\partial s^2}$, and
the same form for $\sigma^2$. EM here is gradient ascent with a step size
chosen for you. That step size is safe, which is why the likelihood never
drops, and conservative, which is why it is slow.

**8.6** Over 200 datasets:

| | Truth | Mean | Median | Middle 90% of estimates |
|---|---|---|---|---|
| $\hat s^2$ | 2.00 | 1.93 | 1.74 | 0.71 to 3.73 |
| $\hat\sigma^2$ | 0.25 | 0.251 | 0.249 | 0.19 to 0.31 |

$\hat\sigma^2$ is good to roughly ±25%. $\hat s^2$ ranges over more than a
factor of five. (d) The tutorial's seed-0 dataset gave $\hat s^2 = 3.90$, above
the 95th percentile: an unlucky but legitimate draw.

**8.7** (a) 95.4% for ±2 standard deviations. (b) True parameters: 95.1%.
Estimated parameters: 94.6%. (c) No. The band depends mainly on the *balance*
of signal and noise near each point, which the data determine well, not on the
overall scale of $f$ across the whole day. (d) Ignoring parameter uncertainty
costs about half a percentage point of coverage on average here. But averages
hide spread: in 5% of datasets the coverage was below 85%.

**8.8** Middle 90% of estimates:

| Design | $\hat s^2$ | $\hat\sigma^2$ |
|---|---|---|
| 100 points on $[0, 10]$ | 0.67 to 3.57 | 0.189 to 0.304 |
| 400 points on $[0, 10]$ | 0.85 to 3.31 | 0.222 to 0.285 |
| 400 points on $[0, 40]$ | 1.27 to 2.84 | 0.220 to 0.285 |

Both larger designs sharpen $\hat\sigma^2$ equally. Sampling faster narrows the
$\hat s^2$ range only slightly; observing for longer narrows it much more.
Advice: to learn the noise, take more readings of any kind; to learn about the
process, observe more of it.

**8.9** Crude estimator: mean 0.259, standard deviation 0.043. EM: mean 0.251,
standard deviation 0.036. (a) The crude one is biased up by about 0.01, as 4.5
predicted. (b) The full model's estimate is about 16% less variable. A modest
gain. (c) The crude estimator needs independent noise, constant noise variance
and a curve that changes little between consecutive readings. It does not need
Gaussian noise, the kernel's shape, the lengthscale, or anything about $s^2$.
Prefer it as a cross-check, and whenever you doubt the GP assumptions: a large
disagreement between the two is itself a diagnostic.

---

## Part 9

Rows broken: A and B, known lengthscale; C, Gaussian noise; D, constant noise
variance; E, uniform smoothness (and zero mean).

**9.2** Over 200 datasets each:

| Experiment | Median $\hat s^2$ | Median $\hat\sigma^2$ | RMSE of $m$ | Coverage |
|---|---|---|---|---|
| Model correct | 1.74 | 0.249 | 0.167 | 94.6% |
| A. Lengthscale too short | 0.98 | 0.236 | 0.244 | 95.9% |
| B. Lengthscale too long | 73 | 0.333 | 0.347 | 60.4% |
| C. Outliers | 1.77 | 0.639 | 0.259 | 94.1% |
| D. Noise varies | 1.78 | 0.441 | 0.214 | 93.4% |
| E. Jump | 5.01 | 0.329 | 0.324 | 89.3% |

- A: the model is more flexible than needed, so it follows some noise (worse
  RMSE) but knows it is flexible and keeps wide bands.
- B: the model cannot bend fast enough. Real signal is left over, gets called
  noise ($\hat\sigma^2$ up), and the bands, computed as if the smooth model
  were true, are far too narrow. $\hat s^2$ runs off to huge values.
- C: one noise variance must cover ordinary and wild readings, so it inflates
  (0.64 against 0.25) and the curve is over-smoothed everywhere.
- D: $\hat\sigma^2$ settles near the average noise variance (0.445).
- E: a smooth kernel cannot represent a step; $\hat s^2$ inflates trying.

**9.3** (a) D: 99.3% coverage where the noise is small, 87.5% where it is
large. (b) E: 24.6% within 0.5 of the jump, 96.5% elsewhere. (c) A single
coverage number can be nearly nominal while the bands are useless exactly
where they are needed. For the hours around the cooling failure the model's
uncertainty is wrong three times out of four.

**9.4** (a) Not equally. Too short costs accuracy but stays honest; too long
is confidently wrong. If unsure, err short. (b) Mainly accuracy loss with
honest bands: A, C. Dishonest bands: B (everywhere), D and E (locally).
Dishonest uncertainty is the more dangerous because the user has no reason to
doubt it. (c) The noise level is no longer a meaningful single number in C and
D. The curve away from the jump is still fine in E. Nothing is reliable in B.

**9.5** (a) $y - m$ is shrunk towards zero by the fit, by different amounts at
different points. (b) Standard normal, approximately. (c)
$z_i = \alpha_i/\sqrt{[C^{-1}]_{ii}}$ with $\alpha = C^{-1}y$. (d) Averages
over 200 datasets:

| Experiment | Variance of $z$ | Lag-1 autocorrelation | Share with $\lvert z\rvert > 3$ | Variance ratio, left half / right half |
|---|---|---|---|---|
| Model correct | 1.00 | −0.11 | 0.20% | 0.95 |
| A. Too short | 1.00 | −0.37 | 0.27% | 0.94 |
| B. Too long | 1.00 | +0.21 | 0.18% | 0.98 |
| C. Outliers | 1.00 | −0.10 | 2.04% | 1.02 |
| D. Noise varies | 1.00 | −0.12 | 1.16% | 0.20 |
| E. Jump | 1.00 | +0.04 | 0.74% | 1.03 |

Wrong lengthscale shows in the autocorrelation (runs of same-sign misses when
too long). Outliers show as ten times too many large residuals. Varying noise
shows as a fan shape. The jump is the subtlest in these summaries (a modest
excess of large residuals and a shift in autocorrelation) but obvious in a plot
against $x$, where the large residuals sit together at $x \approx 5$. Look at
the plot before trusting summaries. (e) The overall variance is 1.00 in every
experiment: the fitted variances are chosen to make it so, so it carries no
information. A check that the fit forces to pass is not a check.

**9.6** (a) No. The baseline lag-1 autocorrelation is −0.11, not 0:
leave-one-out residuals are dependent even when the model is right. (b)
Parametric bootstrap: simulate many datasets from the *fitted* model, compute
the diagnostic on each, and see where the observed value falls in that
distribution.

**9.7** C: a heavy-tailed noise distribution such as Student-t. The posterior
of $f$ is then no longer Gaussian, so the E-step loses its closed form (though
writing the t as a Gaussian with a random variance adds a second latent
variable and EM still applies). D: let the noise variance depend on $x$. The
E-step survives with $\sigma^2 I$ replaced by a diagonal matrix; the M-step is
no longer one closed-form line. E: add a step or change-point term to the mean,
or allow the kernel to change at the jump. A mean that is linear in unknown
coefficients keeps everything Gaussian.

**9.8** A good report says: the method estimates the underlying temperature
curve and the probe's noise level, assuming the temperature changes smoothly on
a timescale of about an hour and the probe's errors are independent and equally
sized. The curve and its band can be trusted (truth inside the band about 95%
of the time) when those hold. The noise estimate is good to about ±25%. The
"typical swing size" is not reliable from one day. The method fails at sudden
changes (near one, the band is wrong three times in four), when the probe
glitches, and badly if the assumed timescale is too long. Before relying on it:
plot the leave-one-out residuals against time and look for clusters, fans and
runs.

**S1.** The guarantee survives as long as each M-step does not decrease the
expected complete-data log-likelihood; it need not maximise it. The new
identification problem is the trade-off between $\ell$ and $s^2$ noted in 4.8.
