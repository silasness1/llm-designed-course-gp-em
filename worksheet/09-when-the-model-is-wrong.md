# Part 9: When the model is wrong

**Goal.** Every result in Part 8 assumed the data came from the model. Real
data never do. Find out which wrong assumptions matter, how much, for which
purpose, and whether the damage can be detected.

**You need.** Part 8 finished, and your assumption audit from 4.1. Write in
`notes/part-09.md`.

## The experiments

In each one, change exactly one thing and keep your fitting code untouched.
Everything else stays as in Part 8: $n = 100$ on $[0, 10]$, $s^2 = 2$,
$\sigma^2 = 0.25$, $\ell = 1$, fitted with $\ell = 1$ unless stated.

| Label | What is changed |
|---|---|
| A. Lengthscale too short | Data as before; **fit** with $\ell = 0.3$. |
| B. Lengthscale too long | Data as before; **fit** with $\ell = 3$. |
| C. Outliers | 5 randomly chosen readings out of 100 have noise with standard deviation 3 instead of 0.5. |
| D. Noise varies | The noise standard deviation rises linearly from 0.1 at $x = 0$ to 1.1 at $x = 10$. |
| E. Jump | The true function has 3 added to it for all $x > 5$ (the cooling system switched off). |

For each, identify which row of your table in 4.1 is being broken.

## Tasks

**9.1 (Think) Predict first.**
Before running anything, fill in this table with your predictions. Use words
like "up", "down", "about the same", "much worse".

| Experiment | $\hat s^2$ | $\hat\sigma^2$ | Error of $m$ against true $f$ | Coverage of the ±2 sd band |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |
| D | | | | |
| E | | | | |

For each row, write one sentence of reasoning. Ask: the model has only two
knobs. When the data contain something it cannot represent, which knob will
absorb it?

**9.2 (Experiment) Measure.**
Run each experiment over at least 200 simulated datasets. Compute the same four
columns, plus the baseline with the correct model. Compare with your
predictions. For every prediction you got wrong, explain what you missed.

**9.3 (Experiment) Averages hide things.**
For experiments D and E, the overall coverage is an average over all 100
points.

(a) For D, compute coverage separately for $x < 5$ and $x \ge 5$.

(b) For E, compute coverage separately for points within 0.5 of the jump and
for the rest.

(c) What do you conclude about reporting a single coverage number? If the
operators care most about the hours around the cooling failure, how useful is
the model's uncertainty statement to them?

**9.4 (Think) Rank the failures.**

(a) Experiments A and B are both "wrong lengthscale". Are they equally bad?
Which error would you rather make, and why?

(b) Distinguish two kinds of failure: the estimate of $f$ gets worse, and the
uncertainty statement becomes dishonest. Sort the five experiments by which
kind they cause. Which kind is more dangerous, and to whom?

(c) Return to the different questions you listed in 1.1. For each experiment,
which of those questions can still be answered acceptably and which cannot?

**9.5 (Design) A warning light that does not need the truth.**
Everything in 9.2 and 9.3 used the true $f$, which you will never have. Design
a diagnostic that uses only $x$, $y$ and the fitted model.

(a) In OLS you examine residuals. What is the analogue here? Note the problem
with using $y - m$ directly: $m$ was fitted to the same $y$.

(b) A cleaner idea: predict each $y_i$ from *all the other points*, and divide
the error by the predicted standard deviation. If the model is right, what
distribution should these standardised errors have?

(c) Implement it. The brute-force way refits 100 times. There is a closed form
that needs only $C^{-1}$; try to find or derive it (see hints).

(d) For each of the five failures, decide what feature of these residuals
should reveal it (think: too many large values, a pattern against $x$,
correlation between neighbours). Then check, with plots for single datasets and
with summary numbers over many datasets.

(e) Is there any failure the diagnostic does *not* reveal? Is there any
property of the residuals that looks fine in every experiment, and if so, why
is it uninformative?

**9.6 (Experiment) What does "fine" look like?**
A diagnostic is only useful if you know its value when nothing is wrong.

(a) Compute your summary numbers from 9.5(d) on the baseline datasets. Are they
what textbook theory for independent standard normals would give? If not, why
not?

(b) Describe a procedure, using only one real dataset and your fitted model,
for deciding whether an observed diagnostic value is alarming. (This procedure
has a name: look up *parametric bootstrap*.)

**9.7 (Think) What would you change?**
For each of C, D and E, propose a change to the *model* (not the algorithm)
that would address it. For each proposal, say what would happen to the two
things that made this project tractable: Gaussian conditioning in the E-step,
and the closed-form M-step.

**9.8 (Write) The report.**
Write one page, for the tank's operators, who know no statistics. It must
answer:

- What does the method estimate, and what does it assume?
- Which of its outputs can be trusted, and how far?
- Under what conditions does it fail, and what would they see if it did?
- What should they check before relying on it?

Use numbers from your own experiments. No formulas.

## Stretch tasks

**S1. Learn the lengthscale.** There is no closed-form M-step for $\ell$.
Implement *generalised EM*: in each M-step, after updating the variances, do a
one-dimensional numerical search over $\ell$ that increases the expected
complete-data log-likelihood. Does the monotonicity guarantee survive? Re-run
experiment B: does learning $\ell$ rescue it? What new identification problem
appears?

**S2. Port the linear algebra.** In C or C++, write by hand: Cholesky
factorisation, forward and back substitution, log-determinant from the factor,
and the trace of a product. Check each against NumPy on random positive
definite matrices, then against LAPACK's `dpotrf` and `dpotrs` for speed. The
checks in `checks/` test behaviour, not implementation, so the same ideas
transfer.

**S3. A different latent-variable model.** Implement EM for a mixture of two
Gaussians. Identify what plays the role of $f$, $m$ and $S$. Find the
identification problem that model has (hint: swap the labels).

## Checkpoint

You are finished when you can answer the four questions from the start of this
worksheet for a model you have not seen before:

1. What quantity do we actually want to estimate?
2. What assumptions connect the observations to that quantity?
3. Which of those assumptions are defensible, and is the quantity identified
   under them?
4. How far can the answer be trusted when the assumptions are wrong, and how
   would we know?

Then compare with `answer_key/discussion.md`, Part 9, and the second half of
`answer_key/investigations.ipynb`.
