# Part 1: Frame the investigation

**Goal.** Decide what you want to learn from the data, and what you would have
to assume to learn it, before choosing any method.

**You need.** Nothing but paper. Write your answers in `notes/part-01.md`.

## The scenario

A temperature probe sits in a fermentation tank. It logs a reading every six
minutes for ten hours: 100 readings. The true temperature of the liquid drifts
up and down smoothly as the fermentation and the cooling system fight each
other. The probe is cheap, and each reading is off by a small random amount.

You are handed the 100 numbers and their timestamps. Nothing else.

This scenario runs through the whole worksheet. Later you will simulate it, so
that you know the truth and can check your methods against it.

## Tasks

**1.1 (Think) What could someone want to know?**
List at least four different questions a person might ask of this dataset. Try
to make them different in kind, not just in detail. For each, say whether the
answer is a single number, a list of numbers, or a whole curve.

**1.2 (Think) What would be the same tomorrow?**
Suppose the experiment is repeated tomorrow with the same probe and a fresh
batch. For each quantity in 1.1, would you expect the same answer? Sort your
quantities into:

- properties of *the probe*,
- properties of *today's batch*,
- properties of *fermentation batches in general*.

Which of these three kinds can you hope to learn well from one day of data?
Which would need many days?

**1.3 (Think) The simplest possible model.**
Write one equation relating a reading to the true temperature at that moment.
Name every symbol. Then list everything you assumed by writing it that way.
Look for at least four assumptions. For example: is the timestamp exact?

**1.4 (Think) Why the problem is impossible as stated.**
You have 100 readings. Count the unknowns in your equation from 1.3.

(a) Show that there is a "solution" that fits the data perfectly and is useless.

(b) In OLS you face the same problem and escape it by assuming the truth is
$X\beta$ with only a few coefficients. What does that assumption buy you, in
terms of counting unknowns?

(c) Here you do not know a formula for the temperature curve. What weaker
statement about the curve do you actually believe? Write it in plain words, as
precisely as you can. Do not use the word "smooth" without saying what it means
for two readings taken six minutes apart, and for two readings taken five hours
apart.

**1.5 (Think) Which unknowns are you estimating, and which are in the way?**
Statisticians distinguish the *estimand* (the thing you want) from *nuisance*
quantities (things you must deal with to get it). For each question in 1.1,
state the estimand and name one nuisance quantity.

**1.6 (Design) How would you know a method worked?**
With real data you never see the true temperature.

(a) Describe a way to test a method where the truth *is* known.

(b) Define two numerical measures of success: one for "the estimate is close to
the truth", and one for "the method's stated uncertainty is honest". Be specific
enough that someone else could compute them.

(c) A method reports "temperature at 3:30 was 21.4 ± 0.3". What would have to be
true, over many uses of the method, for that "± 0.3" to be honest?

## Checkpoint

Before moving on you should be able to answer, without notes:

- What is the difference between an estimand and an estimator?
- Why can't the 100 true temperatures be estimated from 100 readings without a
  further assumption?
- Why is simulation the only way to measure whether uncertainty statements are
  honest?

Then compare with `answer_key/discussion.md`, Part 1.

Next: [Part 2](02-vocabulary.md)
