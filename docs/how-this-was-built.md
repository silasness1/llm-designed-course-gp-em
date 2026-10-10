# How this course was built

A condensed account of the single Claude Code session that produced this
repository, arranged to show the five-part strategy from the README. Prompts
are the learner's, lightly edited for spelling and length. Claude's side is
summarised, not quoted.

The session had three requests. Nothing here was planned in advance; the
worksheet idea came after seeing the first result.

---

## 1. Work backward from a meaningful goal

> I want to implement an EM algorithm for a very simple Gaussian process. I'm
> thinking of implementing this at a high level first, like in a Jupyter
> notebook using linear algebra packages, and possibly expanding the project
> afterwards to teach me about numerical linear algebra using C++ or C. […]
> The goal is for me to learn more about the EM algorithm and Gaussian
> processes because I really have little to no understanding. So it's more like
> a tutorial for me in watching you build it. Thoughts?

The goal was specific and slightly out of reach, which gave everything after it
a direction.

**What Claude did first was correct the premise.** EM is not the usual way to
fit a Gaussian process; that is normally done by maximising the marginal
likelihood directly. EM needs a hidden variable, so "EM for a GP" could mean
several things. It offered three and recommended one:

| Option | Hidden variable | Verdict |
|---|---|---|
| GP regression with the noise-free function hidden | the function values | recommended: teaches both topics, and every step is a Cholesky, a solve, a trace or a log-determinant, which suits a later C/C++ port |
| Mixture of Gaussians first, then the GP | cluster labels | gentler, more material |
| State-space GP with a Kalman smoother | the state sequence | classic, heavier |

It also asked how much of the linear algebra to write out. The learner chose
"naive first, then stable" over the recommended option. That choice later
became the most instructive part of the course.

*Takeaway: before any code, the useful output was a sharper statement of the
problem and three decisions put back in the learner's hands.*

## 2. Rapid feedback

After seeing the plan, one addition:

> Can you make like 5–10% of the effort about showing how testing frameworks in
> Python work, so I learn to check the projects I develop in the future as
> well? So maybe a slightly more robust testing scenario than this example
> actually calls for.

The result was a test suite in which each pytest feature appears once for a
real reason:

| Technique | What it checks here |
|---|---|
| Comparison with an independent reference | the likelihood against SciPy's Gaussian density |
| Testing an invariant | the likelihood never decreases between EM iterations |
| Two implementations of the same maths | naive and stable versions agree where the naive one is trustworthy |
| A recorded known failure (`xfail`) | the naive version breaks on a realistic problem |
| Fixtures, parametrisation, custom markers, coverage | supporting machinery |

The first build was a 100-line module, 28 tests and a narrated notebook. Three
things it showed, all measured:

- With 100 data points the kernel matrix has a condition number near
  $10^{20}$. Inverting it returns noise, with no error or warning. The
  likelihood goes *down*, which EM cannot do, and that is the only symptom.
- Removing the inverse by algebra and using a Cholesky factorisation fixes it.
- EM and a general-purpose optimiser reach the same answer, and that answer is
  not the true parameter value. One dataset does not pin it down.

## 3. Make the learner do the cognitive work

Then the request that changed the project:

> So let's treat your implementation as the answer key in a way. But I firmly
> believe in learning by doing. Can you help build almost a worksheet-like
> approach of problems organized in a way to lead me to implementing this like
> you have here? It should make me critically consider questions like: what
> quantities do we actually want to estimate? What assumptions connect our
> observations to that quantity? Which assumptions are defensible? How should
> we trust the model when the assumptions are misspecified? […] think of me as
> an undergraduate who has a deep understanding of random variables and OLS
> […] Maybe it even starts with tasks like "go look up how EM works online and
> write a small summary of what you found" […] But also eventually the tasks
> should be more about implementation. Like: what functions do you think you
> would use to write gp_em.py? And then task me with writing individual
> functions.

The worksheet assigns each kind of mental work to the learner in turn:

| Kind of work | Where | Example task |
|---|---|---|
| Framing | Part 1 | List four different questions someone could ask of the data. Which answers would be the same tomorrow? |
| Retrieval | Part 2 | Look up Cholesky decomposition and give three real uses in different fields. |
| Derivation | Parts 3, 5 | Starting from OLS, show that ridge regression is a posterior mean; derive the EM updates; prove the likelihood cannot decrease. |
| Judgement | Part 4 | Show that with one particular kernel only the sum of the two variances can be learned. Would more data fix it? |
| Design | Part 5 | List the functions you would write and how you would know each is right, before seeing the reference design. |
| Implementation | Parts 6, 7 | One function at a time; write your own test first, watch it fail, then write the function. |
| Prediction | Parts 4, 8, 9 | Predict the effect of each broken assumption before measuring it. |
| Investigation | Parts 8, 9 | Design a simulation study; build a diagnostic that does not need the true answer. |

The bridge from what the learner already knew was chosen deliberately: Part 3
goes from OLS to ridge regression to a Bayesian linear model, then observes
that the model only ever uses one matrix built from the design matrix, and
replaces that matrix. Nothing in it has to be taken on trust.

Several tasks are built to surprise. In Part 6 the learner's correct code
passes every test on 20 points. In Part 7 the same code is run on 100 points
and fails, and the task is to find out why without being told.

## 4. Personalise the difficulty

Three mechanisms:

- **Graded hints.** `worksheet/hints.md` has up to three levels per hard task:
  a nudge, a push, nearly the answer. The instruction is to read one level,
  close the file and try again.
- **A stated starting point.** The sheets assume random variables and OLS and
  nothing about EM or Gaussian processes, because that is what the learner
  said. A different learner would ask for a different bridge.
- **Review on request.** The learner can ask the assistant to review one part's
  notes or code and to say where an error is without giving the fix or
  revealing later parts.

## 5. Turn the learning into a verifiable artifact

- The earlier test suite was regrouped by worksheet part and became a grader:
  `pytest -m part6` checks the learner's own `gp_em.py`, and `pytest --key`
  runs the same checks against the answer key. The checks test behaviour, not
  specific numbers, so any correct implementation passes.
- Model answers for every written question are organised by task number, so
  one can be read without seeing the next.
- The experiments behind the model answers for Parts 8 and 9 were actually
  run, in a second notebook. Some measured results:

| Finding | Number |
|---|---|
| Noise variance, middle 90% of estimates over 200 datasets (truth 0.25) | 0.19 to 0.31 |
| Signal variance, same (truth 2.0) | 0.71 to 3.73 |
| Coverage of the ±2 sd band when the model is right | 94.6% |
| Coverage when the assumed lengthscale is three times too long | 60.4% |
| Coverage when it is about three times too short | 95.9% |
| Coverage within 0.5 of an unmodelled jump | 24.6% |

---

## What went wrong while building it

The assistant's work needed checking too. Each of these was caught because
something could fail visibly:

- **The grader did not work the first time.** The option to switch between the
  learner's code and the answer key was read after a shared test file had
  already imported the module. Running the checks exposed it at once.
- **A batch of experiments stalled for over ten minutes.** The linear algebra
  library was spreading each small matrix operation over several threads.
  Limiting it to one thread brought each experiment down to about ten seconds.
- **A sentence in the tutorial was wrong.** It said the matrix inverse became
  meaningless "by about 25 points". The plot showed about 35. It was corrected
  after looking at the figure.
- **A claim was written before it was measured.** A sentence about the
  residuals' variance being close to 1 in every experiment went into the
  notebook before that column existed. The column was then added and the claim
  held.
- **The tutorial's example dataset turned out to be unusual.** Its
  signal-variance estimate sits above the 95th percentile of what the
  simulation study later produced. It was kept and turned into a question in
  Part 8.

## What this does not show

- Whether the course works. At the time of writing nobody has taken it.
- Whether the explanations are free of errors. They pass the checks that code
  can make; no expert has read them. See section 4 of the README.
- Whether the difficulty is right. The time estimates are guesses.
