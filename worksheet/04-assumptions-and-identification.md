# Part 4: Assumptions and identification

**Goal.** Before estimating $s^2$ and $\sigma^2$, find out whether the data can
tell them apart at all, and which assumptions that depends on.

**You need.** The model from Part 3. Pencil and paper. Write in `notes/part-04.md`.

The model again:

$$f \sim \mathcal N(0,\; s^2 K), \qquad y = f + \varepsilon, \qquad \varepsilon \sim \mathcal N(0,\; \sigma^2 I)$$

## Tasks

**4.1 (Think) An audit of assumptions.**
List every assumption this model makes about the tank and the probe. Aim for at
least eight. For each one, fill in a row:

| Assumption | Plausible for the tank? | What would it look like in the data if false? | Made because it is believed, or because it is convenient? |
|---|---|---|---|

Mark the two you consider least defensible. You will break several of these on
purpose in Part 9.

**4.2 (Think) What is $s^2$ a property of?**
Refer to your three categories in 1.2.

(a) Which category does $\sigma^2$ belong to? Which does $s^2$ belong to?

(b) You have one day of data, which is one draw of $f$. What does that suggest
about how well each can be learned?

(c) If your real goal is the temperature curve, is $s^2$ an estimand or a
nuisance? Does it matter if it is estimated badly? Write down a guess; Part 8
tests it.

**4.3 (Derive) A model where the parameters cannot be told apart.**
Suppose the lengthscale is so short that function values at different inputs
are independent: $K = I$.

(a) What is the distribution of $y$?

(b) Write the log marginal likelihood. Through what combination of $s^2$ and
$\sigma^2$ does it depend on the parameters?

(c) A parameter is **identified** if different values of it always give
different distributions for the data. Are $s^2$ and $\sigma^2$ identified here?
What is?

(d) Would more data fix this? Would a cleverer algorithm?

(e) Predict what an iterative maximum-likelihood algorithm will do if you run
it on this model from two different starting points. You will test this in
Part 6.

**4.4 (Derive) A model where one parameter is identified but barely learnable.**
Now the opposite extreme: the lengthscale is so long that $f$ is the same at
every input. $K = \mathbf 1 \mathbf 1^\top$, the matrix of all ones, so
$f_i = c$ for all $i$ with $c \sim \mathcal N(0, s^2)$.

(a) Write the model as $y_i = c + \varepsilon_i$. How would you estimate
$\sigma^2$? How precisely, with $n = 100$?

(b) What is the distribution of the sample mean $\bar y$?

(c) Propose an estimator of $s^2$. How many independent pieces of information
about $s^2$ does it use?

(d) If $z \sim \mathcal N(0, v)$, then $z^2$ estimates $v$ with a standard
deviation of $\sqrt 2\, v$. What does that say about your estimator? Does
collecting more readings on the same day help?

(e) So $s^2$ is identified in the formal sense. In what sense is that
unhelpful? This situation is often called *weak identification*.

**4.5 (Derive) The realistic case: what separates signal from noise?**
Back to the RBF kernel with a moderate lengthscale.

(a) Compute $\mathbb E\big[(y_i - y_j)^2\big]$ for $i \ne j$ in terms of $s^2$,
$\sigma^2$ and $K_{ij}$.

(b) Evaluate it for two readings so close that $K_{ij} \approx 1$, and for two
so far apart that $K_{ij} \approx 0$.

(c) In one sentence: what feature of the data tells you how much is noise?

(d) Use (b) to invent a crude estimator of $\sigma^2$ that needs no matrices at
all, only differences between consecutive readings. Write its formula. Is it
biased, and in which direction? You will race it against EM in Part 8.

(e) Which assumption from 4.1 is this estimator, and the whole separation of
signal from noise, resting on?

**4.6 (Think) When the noise is not white.**
Suppose the probe's error drifts slowly instead of being independent from one
reading to the next, so $\varepsilon \sim \mathcal N(0, \sigma^2 K_\varepsilon)$
for some smooth kernel $K_\varepsilon$.

(a) What is $\operatorname{Cov}(y)$ now?

(b) If $K_\varepsilon = K$, what is identified?

(c) Could any amount of data from this one probe distinguish "the temperature
drifted" from "the probe drifted"? What extra *design* (not analysis) would?

**4.7 (Think) Two ways to get more data.**
You can afford 400 readings instead of 100. Option A: one reading every 90
seconds for the same ten hours. Option B: one reading every six minutes for
forty hours.

Predict which option helps the estimate of $\sigma^2$ more, and which helps
$s^2$ more. Give your reasoning using 4.4 and 4.5. Part 8 tests the prediction.

**4.8 (Think) Fixed lengthscale.**
We are treating $\ell$ as known. In the tank scenario, where could knowledge of
$\ell$ come from? If it had to be estimated too, which of the difficulties in
this part would you expect to get worse?

## Checkpoint

- Define identification in one sentence.
- Give an example of a parameter that is identified but cannot be estimated
  well, and say why more data of the same kind does not help.
- State the one assumption that lets signal and noise be separated.

Then compare with `answer_key/discussion.md`, Part 4.

Next: [Part 5](05-derive-em-and-design.md)
