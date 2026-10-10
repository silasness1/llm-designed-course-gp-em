# Part 3: From OLS to GP regression

**Goal.** Reach the GP regression formulas by a chain of small steps starting
from OLS, so that none of them has to be taken on trust.

**You need.** Parts 1 and 2, especially the conditioning formula from 2.2.
Pencil and paper. Write in `notes/part-03.md`.

## Tasks

**3.1 (Derive) Conditioning is regression.**
Let $a$ and $b$ be scalar, jointly Gaussian, both with mean zero.

(a) Using your formula from 2.2, write $\mathbb E[a \mid b]$ and
$\operatorname{Var}(a \mid b)$ in terms of variances and the covariance.

(b) If you regressed $a$ on $b$ by OLS with a very large sample, what slope
would you get? Compare with (a).

(c) Express $\operatorname{Var}(a\mid b)$ using the correlation $\rho$. What
happens at $\rho = 0$ and as $\rho \to \pm 1$?

**3.2 (Derive) Ridge regression is a posterior mean.**
Take the linear model $y = X\beta + \varepsilon$, $\varepsilon \sim \mathcal N(0, \sigma^2 I)$,
and add a prior $\beta \sim \mathcal N(0, \tau^2 I)$, independent of $\varepsilon$.

(a) Write the joint distribution of $(\beta, y)$: its mean and the three blocks
of its covariance.

(b) Use 2.2 to get $\mathbb E[\beta \mid y]$.

(c) The ridge estimator is $(X^\top X + \lambda I)^{-1} X^\top y$. Your answer
to (b) probably looks different. Show they are the same, and find $\lambda$ in
terms of $\sigma^2$ and $\tau^2$.

(d) What happens as $\tau^2 \to \infty$? Interpret.

**3.3 (Derive) Forget the coefficients.**
Define $f = X\beta$, the vector of noise-free values at the observed inputs.

(a) What is the distribution of $f$ under the prior in 3.2?

(b) Your answer involves $X$ only through one $n \times n$ matrix. Call it $K$
and write the model using only $f$, $K$, $\tau^2$ and $\sigma^2$. $\beta$ should
not appear.

(c) What is entry $(i, j)$ of $K$ in terms of rows of $X$? In words, what does
it mean for $K_{ij}$ to be large?

(d) If $X$ has $p < n$ columns, what is the rank of $K$? What does that say
about which vectors $f$ are possible?

**3.4 (Think) Change the matrix.**
The model in 3.3(b) never needed $X$, only $K$. So we may choose $K$ directly:

$$K_{ij} = \exp\!\Big(-\frac{(x_i - x_j)^2}{2\ell^2}\Big)$$

(a) Go back to your plain-words statement in 1.4(c). Does this $K$ express it?
Check both the six-minute case and the five-hour case.

(b) What must be true of a matrix for it to be usable as a covariance matrix?
Is it obvious that this one qualifies?

**The model.** From here on, with $s^2$ replacing $\tau^2$:

$$f \sim \mathcal N(0,\; s^2 K), \qquad y \mid f \sim \mathcal N(f,\; \sigma^2 I)$$

Equivalently $y = f + \varepsilon$ with $\varepsilon \sim \mathcal N(0, \sigma^2 I)$
independent of $f$. The lengthscale $\ell$ is treated as known.

**3.5 (Derive) The posterior of $f$.**

(a) Find $\operatorname{Cov}(y)$. Call it $C$.

(b) Find $\operatorname{Cov}(f, y)$.

(c) Use 2.2 to show that $f \mid y \sim \mathcal N(m, S)$ and find $m$ and $S$
in terms of $K$, $C$, $s^2$ and $y$.

(d) $S$ does not depend on $y$. Is that reasonable? What does it depend on?

**3.6 (Derive) The marginal likelihood.**

(a) What is the distribution of $y$ with $f$ integrated out? (You already have
it.)

(b) Write $\log p(y \mid s^2, \sigma^2)$ in full, including constants.

(c) It has two terms that depend on the parameters. One rewards fitting the
data; the other penalises something. Which is which, and what is penalised?

**3.7 (Derive) Two points, by hand.**
Take $n = 2$, $s^2 = 1$, $\sigma^2 = 1$, $y = (2, 0)^\top$ and
$K = \begin{pmatrix} 1 & \rho \\ \rho & 1\end{pmatrix}$.

(a) Compute $m$ as a function of $\rho$.

(b) Evaluate at $\rho = 0$, $\rho = 0.8$ and $\rho = 1$.

(c) At $\rho = 0$, each estimate is its own reading multiplied by a factor.
Explain that factor from 3.1.

(d) At $\rho = 1$ both estimates are equal. Explain the value from first
principles: what is the model saying about $f_1$ and $f_2$, and how should two
readings of the same thing be combined?

(e) At $\rho = 0.8$ the second estimate is positive although its reading was 0.
Where did the information come from?

**3.8 (Think) The hat matrix.**
$m = Hy$ with $H = s^2 K C^{-1}$, so the estimate is linear in the data, as in
OLS.

(a) The OLS hat matrix satisfies $H^2 = H$. Does this one? What does the
difference mean in words?

(b) In OLS, $\operatorname{tr}(H)$ equals the number of coefficients. Here
$\operatorname{tr}(H)$ is called the *effective degrees of freedom*. What do you
expect it to do as $\sigma^2 \to 0$? As $\sigma^2 \to \infty$? As $\ell$ grows?

## Checkpoint

- Can you write the model, $C$, $m$, $S$ and the log marginal likelihood from
  memory?
- Can you say in one sentence how GP regression differs from ridge regression?

Then compare with `answer_key/discussion.md`, Part 3.

Next: [Part 4](04-assumptions-and-identification.md)
