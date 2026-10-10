# EM for a simple Gaussian process: a build-it-yourself worksheet

An experiment in using an LLM coding assistant (Claude Code) to design a
personalised course for one learner, instead of using it to do the work.

The course leads from "what are we trying to estimate?" to a working, tested
implementation of the EM algorithm for Gaussian process regression, and then to
finding out when its answers can be trusted.

- To take the course: start at [worksheet/00-start-here.md](worksheet/00-start-here.md).
- To see how it was made: read [docs/how-this-was-built.md](docs/how-this-was-built.md).

## Why this exists

An LLM can produce a correct, tested implementation of this method in minutes.
That is worth knowing, and it could be discouraging to someone learning to
program. This repository is an argument that it need not be. The same tool that
can do the task for you can be pointed at a different job: building the
exercises, the feedback and the answer key for *you* to do the task, pitched at
what you already know.

The strategy, in five parts:

1. **Work backward from a meaningful goal.** Pick something real that is just
   beyond current ability. Here: a statistical method I had heard about and
   could not have implemented.
2. **Do the cognitive work myself.** Retrieval, derivation, prediction and
   implementation are assigned to the learner, not the model.
3. **Get rapid feedback.** A test suite grades each stage of the implementation
   in seconds.
4. **Personalise the difficulty.** Hints come in three levels, so I can take the
   smallest one that unblocks me.
5. **Turn the learning into a verifiable artifact.** The course is reusable by
   someone else, and my own answers and code are evidence of what I did.

Finishing tasks is not the same as learning; the two are only correlated. The
safeguards against mistaking one for the other are listed under
[What I would change](#5-what-worked-what-failed-and-what-i-would-change).

## 1. What I am trying to learn

- What the EM algorithm is, why it works, and what it does and does not promise.
- What a Gaussian process is and how it becomes a regression method.
- How to design a statistical investigation, not just run one:
  - What quantity do we actually want to estimate?
  - What assumptions connect the observations to that quantity?
  - Which assumptions are defensible, and is the quantity identified under them?
  - How far can the answer be trusted when the assumptions are wrong?
- Numerical stability: why mathematically correct code can give wrong numbers.
- Testing practice in Python (pytest), enough to check my own future projects.
- Later, possibly: the numerical linear algebra underneath, by porting it to C
  or C++.

Starting point: comfortable with random variables and OLS, some exposure to
other statistical ideas, little to no understanding of EM or Gaussian processes.

## 2. How I used Claude Code to design the learning experience

Three requests in one session. The full account, with the prompts, is in
[docs/how-this-was-built.md](docs/how-this-was-built.md).

1. **"Build it and let me watch."** I asked for a demonstration implementation.
   Claude first pointed out that EM is not the usual way to fit a Gaussian
   process and offered three models to choose from. It then built a small
   module, a test suite and a narrated notebook.
2. **"Teach me testing too."** I asked for 5 to 10% of the effort to go on
   showing how Python testing works. The test suite was written so that each
   pytest feature appears once with a real reason to exist.
3. **"Now make me do it."** I asked for the implementation to become the answer
   key and for a worksheet that would lead me to write it from scratch, starting
   from research tasks and ending with implementation and investigation. Claude
   produced ten problem sheets, graded hints, model answers, a grader built from
   the earlier tests, and a second notebook of experiments so that the model
   answers quote measured results.

What Claude contributed without being asked: reusing the test suite as a
per-stage grader; the observation that the tutorial's example dataset was an
unlucky draw; the connection between EM's update and a gradient step.

What I contributed: the goal, my background, the four design questions above,
the choice of model and format, the decision to see the naive version fail
before the stable one, the request for testing as a topic, and the idea of
turning the result into a worksheet with research tasks first.

## 3. What tasks I completed myself

At the time of first publishing: **none of the worksheet tasks yet.** This
repository currently contains the course, not my work through it. This section
is a log to be filled in as I go.

| Part | Topic | Done | Hints used | Notes |
|---|---|---|---|---|
| 1 | Frame the investigation | | | |
| 2 | Vocabulary by research | | | |
| 3 | From OLS to GP regression | | | |
| 4 | Assumptions and identification | | | |
| 5 | Derive EM, design the software | | | |
| 6 | Implement the naive version | | | |
| 7 | Numerical stability | | | |
| 8 | Is the answer any good? | | | |
| 9 | When the model is wrong | | | |

My answers will be in `notes/`, my implementation in `gp_em.py`, and my own
tests in `tests/`.

## 4. How I independently verify that the explanations are real

An LLM wrote the explanations, the answer key and the tests. Each of those can
be wrong. What has and has not been checked:

**Checked by running code (done, reproducible by anyone):**

- The reference implementation's likelihood agrees with SciPy's multivariate
  normal density.
- The naive and stable implementations agree on a well-conditioned problem.
- The EM result agrees with a general-purpose optimiser on the same likelihood.
- The log-likelihood never decreases across iterations, over several datasets
  and starting points.
- Both answer-key notebooks execute from top to bottom.
- Every number quoted in `answer_key/discussion.md` was produced by a run, and
  the experiments are in `answer_key/investigations.ipynb` to re-run.

Run them with `.venv/bin/pytest --key`.

**Not yet independently checked:**

- The derivations and model answers have not been reviewed by a statistician.
- The reading list and the textbook section cited in the hints were written
  from the model's memory and have not been checked against the sources.
- The worksheet's time estimates are guesses.

**How I intend to check as I go** (to be reported here):

- Derive each result by hand before reading the model answer, and treat any
  disagreement as something to resolve against a textbook, not against the LLM.
- Confirm each definition in Part 2 from at least two sources that are not an
  LLM.
- Reproduce the key numerical claims with my own implementation, which shares
  no code with the answer key.
- Record here every error I find in the course material.

## 5. What worked, what failed, and what I would change

**On building the course (known now):**

- Worked: asking for a plan and answering questions before any code was written.
  The most useful early output was a correction to my framing, not code.
- Worked: asking for the naive version first. The failure it produces (a
  likelihood that goes down, with no error raised) became the centrepiece of
  Part 7.
- Failed along the way, and fixed: the first version of the grader could not
  switch between my code and the answer key; a batch of experiments stalled for
  ten minutes because of thread contention; a sentence in the tutorial claimed
  the wrong threshold and was corrected after looking at the plot. Details are
  in the build notes. The lesson is that the LLM's output also needed checking
  against something that could fail.
- Not done: no human has reviewed the sheets for difficulty, ordering or
  spoilers.

**On taking the course:** _to be filled in after working through it._

**Safeguards against confusing task completion with learning:**

| Safeguard | Status |
|---|---|
| Commit to a prediction before running an experiment | Present as instructions (for example 4.7, 8.5, 9.1). Not enforced by tooling. |
| Explain a surprising result before moving on | Present as instructions (Parts 6.9, 7.1). Not enforced. |
| Write my own test before reading the provided one | Present as an instruction in Part 6. Not enforced. |
| Transfer to an altered problem | One stretch task (a different latent-variable model) and one extension (learn the lengthscale). No graded transfer test. |
| Answer key kept out of sight | By convention only: it is in a separate folder. |

What I would add next: a small tool that refuses to run a part's checks until a
prediction file for that part exists and is committed; a graded transfer problem
at the end with its own hidden checks; and a closed-book retake of the
checkpoints a week later.

---

## Using the course

| Location | What it is |
|---|---|
| `worksheet/` | The problem sheets, Parts 0 to 9, and `hints.md` |
| `notes/` | Where you write your answers |
| `gp_em.py` | Your implementation; you create it in Part 6 |
| `tests/` | Tests you write |
| `checks/` | Provided tests, used as a grader from Part 6 on |
| `answer_key/` | Reference implementation, tutorial notebook, model answers, worked experiments. Spoilers. |
| `docs/` | How the course was built |

### Setup

Requires Python 3.

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Checking your work

| Command | What it does |
|---|---|
| `.venv/bin/pytest -m part6` | Provided checks for Part 6 (also `part7`, `part8`) |
| `.venv/bin/pytest tests` | Only your own tests |
| `.venv/bin/pytest` | Everything |
| `.venv/bin/pytest --key` | Run the provided checks against the answer key instead of your code |
| `.venv/bin/pytest -v`, `-x`, `-k name` | Verbose; stop at first failure; filter by name |
| `.venv/bin/pytest -m "not slow"` | Skip slow checks |
| `.venv/bin/pytest --cov=gp_em --cov-report=term-missing` | Show which lines of your `gp_em.py` no test executes |

Until `gp_em.py` exists, `pytest` stops with a message saying so.

### The answer key

Open only what the sheet you have just finished points you to.

| File | Answers |
|---|---|
| `answer_key/discussion.md` | Every written question, by task number |
| `answer_key/gp_em.py` | Parts 6 to 8 |
| `answer_key/gp_em_tutorial.ipynb` | A narrated walkthrough of Parts 3 to 8 |
| `answer_key/investigations.ipynb` | The simulation study (Part 8) and misspecification experiments (Part 9) |

To open a notebook: `.venv/bin/jupyter lab answer_key/gp_em_tutorial.ipynb`

### Getting a review from an LLM

Ask for the location of an error and the smallest useful hint, not the fix. For
example: "Is my derivation in 3.5 correct? If not, tell me which line, not the
answer, and do not reveal anything from Part 4."
