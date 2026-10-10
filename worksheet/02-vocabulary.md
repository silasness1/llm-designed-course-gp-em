# Part 2: Vocabulary by research

**Goal.** Learn the six ideas the rest of the worksheet is built from, by
finding them yourself and restating them.

**You need.** A library or the internet. Write in `notes/part-02.md`.

## How to do a research task

For each topic, read at least two sources, close them, and then write. Each
summary should be 150 to 300 words, plus any formula the prompts ask for. Use
your own words and your own example. If you cannot explain it without the
source open, you have not finished reading.

You are not expected to understand everything you read. Collect the questions
you cannot answer at the end of each summary; many are answered in Parts 3 to 5.

## Suggested sources

- Rasmussen and Williams, *Gaussian Processes for Machine Learning*, chapters 1
  and 2. Free online from the authors. The standard reference.
- Görtler, Kehlbeck and Deussen, "A Visual Exploration of Gaussian Processes",
  on distill.pub. Interactive pictures; read this first.
- Bishop, *Pattern Recognition and Machine Learning*, chapter 9 (EM) and
  section 2.3 (the Gaussian distribution). Free PDF from the publisher.
- Dempster, Laird and Rubin (1977), "Maximum likelihood from incomplete data via
  the EM algorithm". The original paper; skim the introduction and examples.
- Trefethen and Bau, *Numerical Linear Algebra*, lectures 12 (conditioning) and
  23 (Cholesky).
- Wikipedia is fine for definitions. Do not rely on it alone.

## Tasks

**2.1 (Research) Latent variables.**
Your summary must answer:

- What is a latent variable?
- How is it different from a *parameter*? Both are unobserved.
- Give two examples from outside this project.
- In OLS, $y = X\beta + \varepsilon$. Is $\varepsilon$ a latent variable? Argue
  both sides, then decide.
- In the tank scenario, what is the natural latent variable?

**2.2 (Research) Conditioning a multivariate Gaussian.**
Find and write down, with all symbols defined:

- the formula for the marginal distribution of a sub-vector of a Gaussian vector,
- the formula for the conditional distribution of one sub-vector given another.

You will use the second formula repeatedly. Also answer: the conditional
covariance does not depend on something you might have expected it to depend
on. What?

**2.3 (Research) Gaussian processes.**
Your summary must answer:

- What is the definition of a Gaussian process? (It is one sentence. Find it.)
- What two objects specify a GP completely?
- What is a kernel? What does the *lengthscale* of the RBF (also called
  squared-exponential) kernel control? Write the RBF formula.
- A GP is called a "distribution over functions", yet a computer only ever
  handles finite vectors. How are both statements true?
- Why is a GP called *nonparametric* when it has parameters?

**2.4 (Research) GP regression.**
Your summary must answer:

- What is the prior, what is the likelihood, and what is the posterior?
- In OLS the unknown is $\beta$. What plays that role here?
- What does the posterior give you that a single fitted curve does not?
- What is the "marginal likelihood" and what is being marginalised?

**2.5 (Research) The EM algorithm.**
Your summary must answer:

- What kind of problem is EM designed for?
- What happens in the E-step and what happens in the M-step? Describe each in
  one sentence without formulas.
- What does EM guarantee at every iteration?
- Name two things EM does *not* guarantee.
- Describe one classic application (the usual textbook one is a mixture of
  Gaussians) and say what the latent variable is in it.

**2.6 (Research) Cholesky decomposition.**
Your summary must answer:

- What is it, and which matrices have one?
- Why would you use it instead of computing a matrix inverse?
- How does its cost grow with matrix size?
- Give **three real-world uses**, each in a different field, each with one
  sentence on why Cholesky in particular is the tool used there.

**2.7 (Research) Condition number.**
Your summary must answer:

- What is the condition number of a matrix?
- What is the rule of thumb linking condition number to digits of accuracy lost?
- How many significant decimal digits does a double-precision number carry?
- Is ill-conditioning a property of the matrix, of the algorithm, or of the
  computer?

**2.8 (Think) Connect them.**
In five sentences or fewer, without formulas, explain how topics 2.1 to 2.5 fit
together for the tank scenario: what is latent, what is the GP doing, and why
might EM be relevant? It is fine for this to be partly a guess. You will revise
it at the end of Part 5.

## Checkpoint

Explain each of the seven terms aloud to an imaginary classmate in under a
minute each. Then compare with `answer_key/discussion.md`, Part 2.

Next: [Part 3](03-from-ols-to-gp.md)
