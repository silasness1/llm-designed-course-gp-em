# Part 0: Start here

## What you will build

By the end you will have written, from an empty file, a program that:

1. takes noisy measurements of an unknown smooth function,
2. estimates how large the function's variation is and how large the noise is,
3. reconstructs the function with honest uncertainty bands,

and you will be able to say when its answers can be trusted and when they cannot.

The method is Gaussian process (GP) regression fitted with the EM algorithm. The
code is about 100 lines. Most of the work is deciding what those lines should be
and how you would know they are right.

## The four questions

Every part of this worksheet is practice at answering these, for one model:

1. What quantity do we actually want to estimate?
2. What assumptions connect the observations to that quantity?
3. Which of those assumptions are defensible, and is the quantity identified
   under them?
4. How far can the answer be trusted when the assumptions are wrong, and how
   would we know?

## How the sheets are organised

| Part | Sheet | Mostly | Rough time |
|---|---|---|---|
| 1 | Frame the investigation | thinking | 1 h |
| 2 | Vocabulary by research | reading and summarising | 3–4 h |
| 3 | From OLS to GP regression | pencil and paper | 3 h |
| 4 | Assumptions and identification | pencil and paper, judgement | 2–3 h |
| 5 | Derive EM, then design the software | pencil and paper, design | 3 h |
| 6 | Implement the naive version | code | 3–4 h |
| 7 | Numerical stability | experiments, pencil and paper, code | 3 h |
| 8 | Is the answer any good? | code, experiments | 3–4 h |
| 9 | When the model is wrong | experiments, writing | 4 h |

Do them in order. Later sheets assume the earlier ones and sometimes give away
their answers.

Each task has a label saying what kind of work it is:

- **Research**: look it up, then write it in your own words.
- **Think**: no calculation, but commit to an answer in writing.
- **Derive**: pencil and paper.
- **Design**: decide how something should be built before building it.
- **Code**: write it.
- **Experiment**: run something, look at the result, explain it.

## Where things go

| Location | What it is |
|---|---|
| `worksheet/` | These sheets. Read-only. |
| `notes/` | Your written answers. One file per part, e.g. `notes/part-03.md`. Photos of handwritten derivations are fine. |
| `gp_em.py` | Your implementation. It does not exist yet; you create it in Part 6. |
| `tests/` | Tests you write yourself. |
| `checks/` | Tests provided for you, used as a grader from Part 6 on. |
| `worksheet/hints.md` | Hints, three levels per task. |
| `answer_key/` | A full implementation, a tutorial notebook, model answers and worked experiments. |

## Rules that make this work

1. **Write your answer before you check it.** A prediction you wrote down and got
   wrong teaches more than a correct answer you read.
2. **`answer_key/` stays closed until you have finished the part it answers.**
   `answer_key/discussion.md` is organised by task number, so you can read one
   answer without seeing the next.
3. **Take the smallest hint that unblocks you.** `hints.md` gives each hard task
   a nudge, then a bigger push, then nearly the answer. Read one level, close the
   file, try again.
4. **When an experiment surprises you, stop and explain it** before moving on.
   Several tasks are designed to surprise you.
5. **Thirty minutes stuck is the signal to take a hint**, not three hours.

## Getting a review

After any part, open Claude Code in this directory and say, for example,
"review my Part 3 notes against the answer key without giving away Part 4".
Useful requests:

- "Is my derivation in 3.5 correct? If not, tell me which line, not the fix."
- "Review `gp_em.py` as a strict code reviewer."
- "I predicted X in 9.1 and saw Y. Is my explanation sound?"

## Setup

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

You do not need the environment until Part 6.

## Prerequisites check

You should be comfortable with the following. If not, review before starting.

- Expectation, variance and covariance of random vectors; $\operatorname{Cov}(Ax) = A\,\operatorname{Cov}(x)A^\top$.
- The OLS estimator $\hat\beta = (X^\top X)^{-1}X^\top y$ and what assumptions make it unbiased.
- Maximum likelihood for a normal sample.
- Matrix inverse, transpose, trace, determinant, eigenvalues.
- Basic NumPy.

Next: [Part 1](01-frame-the-investigation.md)
