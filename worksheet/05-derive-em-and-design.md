# Part 5: Derive EM, then design the software

**Goal.** Derive the EM updates for $s^2$ and $\sigma^2$ yourself, understand
why they cannot make things worse, and plan the code before writing any.

**You need.** Parts 3 and 4. Pencil and paper. Write in `notes/part-05.md`.

We want the values of $\theta = (s^2, \sigma^2)$ that maximise the marginal
likelihood from 3.6. You could hand that function to a numerical optimiser, and
in Part 8 you will. EM is a different route to the same place, and the one this
worksheet is about.

## Section A: deriving the algorithm

**5.1 (Derive) The complete-data log-likelihood.**
"Complete data" means $y$ together with the latent $f$, as if both were observed.

(a) Write $\log p(y, f \mid \theta)$ as $\log p(y \mid f, \sigma^2) + \log p(f \mid s^2)$.

(b) Expand both terms. Collect everything that does not depend on $\theta$ into
a constant.

(c) Notice which parameter appears in which term. Compare with the marginal
log-likelihood in 3.6, where both parameters are tangled inside $C^{-1}$ and
$\log|C|$. This difference is the reason EM exists.

**5.2 (Derive) If $f$ were known.**
Maximise your expression from 5.1 over $\sigma^2$ and over $s^2$, treating $f$
as given.

(a) Find $\hat\sigma^2$. What familiar estimator is it?

(b) Find $\hat s^2$. Explain the role of $K^{-1}$: what does $f^\top K^{-1} f$
measure that $f^\top f$ does not? (Hint: if $f = Lz$ with $K = LL^\top$, what
is $f^\top K^{-1} f$ in terms of $z$?)

**5.3 (Derive) But $f$ is not known.**
We have the posterior $f \mid y \sim \mathcal N(m, S)$ from 3.5. The obvious
idea is to plug $m$ in for $f$.

(a) Show that for $f \sim \mathcal N(m, S)$ and any fixed matrix $A$,
$\;\mathbb E[f^\top A f] = m^\top A m + \operatorname{tr}(AS)$.

(b) Use (a) to compute $\mathbb E\big[\lVert y - f\rVert^2 \mid y\big]$ and
$\mathbb E\big[f^\top K^{-1} f \mid y\big]$.

(c) Compare with plugging in $m$. In which direction is the plug-in wrong for
each quantity? Explain in words why $m$ is not a typical $f$.

**5.4 (Derive) The two steps.**
The E-step computes the expectation of the complete-data log-likelihood under
the posterior of $f$, using the current parameters. The M-step maximises that
expectation over new parameters.

(a) Using 5.1 to 5.3, write the M-step updates $s^2_{\text{new}}$ and
$\sigma^2_{\text{new}}$.

(b) Write the whole algorithm as pseudo-code: inputs, initialisation, loop,
stopping rule, outputs. Be explicit about which quantities use the *old*
parameters.

(c) What would you monitor to decide when to stop?

**5.5 (Derive) Why the likelihood never goes down.**
A guided proof. Let $L(\theta) = \log p(y \mid \theta)$ and let $q$ be *any*
probability density over $f$.

(a) Starting from $p(y \mid \theta) = \int p(y, f \mid \theta)\, df$, multiply
and divide by $q(f)$ inside the integral, and apply Jensen's inequality to show

$$L(\theta) \;\ge\; \mathbb E_q\big[\log p(y, f \mid \theta)\big] - \mathbb E_q\big[\log q(f)\big] \;=:\; F(q, \theta)$$

(b) Show that if $q(f) = p(f \mid y, \theta)$ the inequality is an equality.

(c) Now let $\theta_0$ be the current parameters and $q_0 = p(f \mid y, \theta_0)$.
The M-step picks $\theta_1$ to maximise $F(q_0, \theta)$. Only one of the two
terms of $F$ depends on $\theta$. Which, and where have you seen it?

(d) Complete the chain and justify each step:
$L(\theta_1) \ge F(q_0, \theta_1) \ge F(q_0, \theta_0) = L(\theta_0)$.

(e) This gives you a property your code must satisfy at every iteration,
whatever the data. Why is that valuable to a programmer?

**5.6 (Think) What EM does not promise.**

(a) The proof says the likelihood does not decrease. Does it say EM finds the
global maximum? Does it say anything about speed?

(b) Return to the unidentified model in 4.3. Does the proof in 5.5 still hold
there? Reconcile that with your prediction in 4.3(e).

(c) Revise your five-sentence summary from 2.8.

## Section B: designing the software

Do this section before opening Part 6.

**5.7 (Design) What functions?**
You will write a module `gp_em.py` that can simulate data from the model, run
EM, and report enough to plot what happened.

List the functions you would write. For each give: a name, its inputs, its
outputs, and one sentence on what it does. Aim for small functions that each
correspond to one formula or one job. Decide deliberately:

- Should the kernel matrix be computed inside the EM functions or passed in?
- Should the E-step and M-step be separate functions?
- What should the main loop return so that you can later plot convergence?

**5.8 (Design) How will you know each one is right?**
You cannot check EM's output by hand for 100 data points. For each function in
5.7, write down at least one check that would catch a mistake. Useful kinds of
check:

- a case small enough to do by hand (you have one from 3.7),
- a mathematical property the output must have,
- agreement with an independent calculation,
- a problem where you know the truth because you simulated it.

**5.9 (Design) What could go wrong?**
List three things that could make a correct-looking implementation give wrong
numbers. For each, say how you would notice.

**5.10 (Think) Compare.**
Now read the interface table at the top of [Part 6](06-implement-naive.md). It
is one reasonable design, not the only one. Note two places where yours
differs and say which you prefer and why. From Part 6 on, use the interface in
the table so that the provided checks can run against your code.

## Checkpoint

- Can you state the E-step and M-step for this model from memory?
- Can you reproduce the chain of inequalities in 5.5(d) and say what each step
  uses?

Then compare with `answer_key/discussion.md`, Part 5.

Next: [Part 6](06-implement-naive.md)
