# Hints

Each task has up to three hints, from a nudge to nearly the answer. Read one
level, close this file, and try again. Tasks not listed have no hints; ask for
a review instead.

---

## Part 1

### 1.4
1. Count: how many true temperatures are there? How many noise values?
2. For (a): what if every noise value were exactly zero?
3. For (c): try completing "if I know the temperature at 2:00, then at 2:06 I
   expect … and at 7:00 I expect …".

## Part 3

### 3.2 (c)
1. You have $\tau^2 X^\top(\tau^2 XX^\top + \sigma^2 I)^{-1}$ and want
   $(X^\top X + \lambda I)^{-1} X^\top$. One has an $n \times n$ inverse, the
   other $p \times p$.
2. Show that $X^\top (XX^\top + \lambda I) = (X^\top X + \lambda I) X^\top$ by
   expanding both sides.
3. Multiply that identity on the left by $(X^\top X + \lambda I)^{-1}$ and on
   the right by $(XX^\top + \lambda I)^{-1}$. Then factor $\tau^2$ out of your
   expression.

### 3.5
1. $y = f + \varepsilon$ with the two terms independent. Covariances of sums
   of independent vectors add.
2. $\operatorname{Cov}(f, y) = \operatorname{Cov}(f, f) + \operatorname{Cov}(f, \varepsilon)$.
3. In the conditioning formula, take "the part you want" to be $f$ and "the
   part you observed" to be $y$. The three blocks are $s^2K$, $s^2K$ and $C$.

### 3.7
1. You need the inverse of a 2 × 2 matrix:
   $\begin{pmatrix} a & b \\ b & a \end{pmatrix}^{-1} = \frac{1}{a^2 - b^2}\begin{pmatrix} a & -b \\ -b & a \end{pmatrix}$.
2. $C = \begin{pmatrix} 2 & \rho \\ \rho & 2 \end{pmatrix}$. Compute $C^{-1}y$
   first, then multiply by $K$.
3. You should find the first component of $C^{-1}y$ is $4/(4 - \rho^2)$.

## Part 4

### 4.3
1. What is $s^2 I + \sigma^2 I$?
2. The likelihood of $n$ independent $\mathcal N(0, v)$ values depends on the
   parameters only through $v$.
3. Any pair $(s^2, \sigma^2)$ with the same sum gives exactly the same
   distribution for $y$.

### 4.4
1. With $c$ shared, differences between readings do not involve $c$ at all.
2. $\bar y = c + \bar\varepsilon$. Add the variances.
3. $\bar y^2$ has expectation $s^2 + \sigma^2/n$. It is the square of a single
   normal draw.

### 4.5
1. Expand $(y_i - y_j)^2$ using $y = f + \varepsilon$, and use
   $\mathbb E[(a - b)^2] = \operatorname{Var}(a) + \operatorname{Var}(b) - 2\operatorname{Cov}(a, b)$
   for mean-zero variables.
2. $\operatorname{Var}(f_i) = s^2$ and $\operatorname{Cov}(f_i, f_j) = s^2 K_{ij}$.
3. For (d): if neighbours have nearly the same $f$, then $y_{i+1} - y_i$ is
   nearly a difference of two noise values.

## Part 5

### 5.1
1. Both factors are Gaussian densities you can write down from the model.
2. $\log \mathcal N(f; 0, s^2 K)$ contains $\log|s^2 K| = n \log s^2 + \log|K|$.
   The second piece is a constant.
3. You should end with four terms: two involving only $\sigma^2$, two involving
   only $s^2$.

### 5.2 (b)
1. Differentiate with respect to $s^2$, or substitute $u = 1/s^2$ to make it
   easier.
2. For the interpretation, substitute $f = Lz$.
3. $f^\top K^{-1} f = z^\top L^\top (LL^\top)^{-1} L z = z^\top z$: the sum of
   squares of the independent standard normals that generated $f$.

### 5.3 (a)
1. Write $f = m + e$ with $e \sim \mathcal N(0, S)$ and expand.
2. The cross terms have expectation zero. That leaves $\mathbb E[e^\top A e]$.
3. A scalar equals its own trace, and $\operatorname{tr}(e^\top A e) = \operatorname{tr}(A e e^\top)$.
   Take the expectation inside the trace.

### 5.5
1. For (a): Jensen for the concave function $\log$ says
   $\log \mathbb E[Z] \ge \mathbb E[\log Z]$. Choose $Z = p(y, f \mid \theta)/q(f)$
   with $f \sim q$.
2. For (b): $p(y, f \mid \theta) = p(f \mid y, \theta)\, p(y \mid \theta)$. What
   is $Z$ when $q$ is the posterior?
3. For (d): the first inequality is (a) applied at $\theta_1$; the second is
   the definition of the M-step; the equality is (b) at $\theta_0$.

## Part 6

### 6.1
1. You want a matrix of all pairwise differences $x_{1,i} - x_{2,j}$.
2. `a[:, None]` has shape `(n, 1)` and `b[None, :]` has shape `(1, m)`.
3. `diff = x1[:, None] - x2[None, :]`, then apply the formula elementwise.

### 6.2
1. For (a): you have seen "factor the covariance" in your Cholesky research.
2. For (c): the error says the matrix is not positive definite. In exact
   arithmetic it is. What are its smallest eigenvalues, and what does rounding
   do to a number that should be $10^{-18}$?
3. The remedy is called *jitter* (or a *nugget*): add a tiny multiple of the
   identity, such as $10^{-8} I$, before factorising.

### 6.3
1. A determinant is a product of $n$ eigenvalues. What happens to a product of
   500 numbers that are each around 0.3?
2. Look at `np.linalg.slogdet`.
3. The reference for your test is `scipy.stats.multivariate_normal(mean, cov).logpdf(y)`.

### 6.6
1. Keep three lists and append to each once before the loop and once per
   iteration.
2. Compare the last two entries of the log-likelihood list to decide whether
   to stop.

## Part 7

### 7.2
1. Print the outputs of a single M-step. One of them is a variance.
2. There are two inverses in the naive code: one of $C$, one of $K$. Check each.
3. `inv(C)` is fine. `inv(K)` is not.

### 7.3 (e)
1. Readings 0.1 apart with lengthscale 1 have correlation about 0.995.
2. So rows $i$ and $i+1$ of $K$ are almost the same vector.
3. A matrix with two equal rows is singular. One with two nearly equal rows is
   nearly singular.

### 7.4
1. Compare entries of $LL^\top$ with $A$, starting from the top-left:
   $L_{11}^2 = A_{11}$.
2. First column: $L_{i1} = A_{i1}/L_{11}$. Then $L_{22}^2 = A_{22} - L_{21}^2$.
3. $L = \begin{pmatrix} 2 & 0 & 0 \\ 1 & 2 & 0 \\ 1 & 1 & 2\end{pmatrix}$. For
   (d): look at where you take a square root.

### 7.5
1. For (a): $m = s^2 K C^{-1} y$ and $\alpha = C^{-1}y$.
2. For (b): substitute $m = s^2 K \alpha$ for *one* of the two $m$'s. $K^{-1}K$
   cancels.
3. For (c): $K^{-1} S = K^{-1}(s^2 K - s^4 K C^{-1} K) = s^2 I - s^4 C^{-1} K$.
   Now take the trace.

### 7.6 (c)
1. You have two implementations of the same mathematics.
2. They should agree to many decimal places, but only where the naive one is
   trustworthy.
3. Compare them on the well-conditioned 20-point problem.

## Part 8

### 8.1
1. Which function maps all real numbers to positive numbers?
2. Optimise over $(\log s^2, \log\sigma^2)$ and exponentiate inside the
   objective.
3. `minimize(lambda p: -log_marginal_likelihood(K, y, *np.exp(p)), np.log([s2_0, sigma2_0]), method="L-BFGS-B")`.

### 8.2
1. $\operatorname{Cov}(f_*, y) = s^2 K_*$ and $\operatorname{Var}(f_{*,i}) = s^2$.
2. Mean: $s^2 K_* C^{-1} y$. Covariance: $s^2 K_{**} - s^4 K_* C^{-1} K_*^\top$.
3. For the diagonal only, you do not need the full matrix product:
   `np.sum(K_star * cho_solve(c, K_star.T).T, axis=1)` gives the diagonal of
   $K_* C^{-1} K_*^\top$.

### 8.4 (c)
1. Start from $s^2_{\text{new}} = \big(s^2 \alpha^\top m + n s^2 - s^4 \operatorname{tr}(C^{-1}K)\big)/n$
   and substitute $m = s^2 K \alpha$.
2. You get $s^2 + \frac{s^4}{n}\big(\alpha^\top K \alpha - \operatorname{tr}(C^{-1}K)\big)$.
3. Differentiate the log marginal likelihood with respect to $s^2$ using
   $\partial C/\partial s^2 = K$, $\;\partial \log|C| = \operatorname{tr}(C^{-1}\partial C)$
   and $\partial C^{-1} = -C^{-1}(\partial C)C^{-1}$. Compare.

## Part 9

### 9.1
1. A model with too little flexibility has to call unexplained variation
   something.
2. Outliers and a jump are both "variation the smooth curve cannot follow".
   One is spread over isolated points, the other is concentrated in one place.
3. Isolated misfit tends to be absorbed by $\sigma^2$; large-scale misfit by
   $s^2$.

### 9.5 (c)
1. This is called *leave-one-out* prediction. For GP regression it has a closed
   form (Rasmussen and Williams, section 5.4.2).
2. With $\alpha = C^{-1}y$, the leave-one-out prediction error for point $i$ is
   $\alpha_i / [C^{-1}]_{ii}$ and its variance is $1/[C^{-1}]_{ii}$.
3. So the standardised residual is $\alpha_i / \sqrt{[C^{-1}]_{ii}}$.

### 9.5 (d)
1. Plot the residuals against $x$ first. Look before you summarise.
2. Candidate summaries: the share of residuals beyond ±3; the correlation
   between each residual and the next; the variance in the left half divided by
   the variance in the right half.
