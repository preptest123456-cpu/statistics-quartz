---
title: Discrete Probability Distributions
chapter: 5
tags:
  - statistics
  - probability
  - random_variables
  - binomial_distribution
  - poisson_distribution
  - hypergeometric_distribution
  - expected_value
  - variance
  - bivariate_distributions
  - financial_portfolios
---

# Discrete Probability Distributions

This chapter extends the study of probability by introducing [[random variable|random variables]] and [[probability distribution|probability distributions]]. Random variables and probability distributions serve as models for populations of data. The focus is on probability distributions for discrete data, known as **discrete probability distributions**.

---

## Random Variables

> [!definition] Random Variable
> A **random variable** is a numerical description of the outcome of an experiment. Random variables must assume numerical values.

A random variable associates a numerical value with each possible experimental outcome. The particular numerical value depends on the outcome of the experiment. A random variable can be classified as either **discrete** or **continuous** depending on the numerical values it assumes.

### Discrete Random Variables

> [!definition] Discrete Random Variable
> A **discrete random variable** may assume either a finite number of values or an infinite sequence of values such as $0, 1, 2, \ldots$

**Examples of discrete random variables:**

| Experiment | Random Variable ($x$) | Possible Values |
|---|---|---|
| Contact five customers | Number who place an order | $0, 1, 2, 3, 4, 5$ |
| Inspect shipment of 50 radios | Number of defective radios | $0, 1, 2, \ldots, 50$ |
| Operate a restaurant for one day | Number of customers | $0, 1, 2, 3, \ldots$ |
| Sell an automobile | Gender of customer | $0$ if male; $1$ if female |

### Continuous Random Variables

> [!definition] Continuous Random Variable
> A **continuous random variable** may assume any numerical value in an interval or collection of intervals.

Experimental outcomes based on measurement scales such as time, weight, distance, and temperature are described by continuous random variables.

**Examples of continuous random variables:**

| Experiment | Random Variable ($x$) | Possible Values |
|---|---|---|
| Operate a bank | Time between customer arrivals (minutes) | $x \geq 0$ |
| Fill a soft drink can | Number of ounces | $0 \leq x \leq 12.1$ |
| Construct a new library | Percentage complete after six months | $0 \leq x \leq 100$ |

---

## Developing Discrete Probability Distributions

The [[probability distribution]] for a random variable describes how probabilities are distributed over the values of the random variable. For a discrete random variable $x$, a [[probability function]], denoted by $f(x)$, provides the probability for each value of the random variable.

### Required Conditions for a Discrete Probability Function

For a valid discrete probability distribution:

$$f(x) \geq 0$$

$$\sum f(x) = 1$$

### Discrete Uniform Probability Distribution

> [!definition] Discrete Uniform Probability Function
> When each possible value of a random variable has the same probability:
> $$f(x) = \frac{1}{n}$$
> where $n$ = the number of values the random variable may assume.

### Empirical Discrete Distributions

An **empirical discrete distribution** is developed using the [[relative frequency method]] to assign probabilities based on observed data.

**Example:** DiCarlo Motors automobile sales over 300 days:

| $x$ (cars sold) | $f(x)$ |
|---|---|
| 0 | 0.18 |
| 1 | 0.39 |
| 2 | 0.24 |
| 3 | 0.14 |
| 4 | 0.04 |
| 5 | 0.01 |
| **Total** | **1.00** |

---

## Expected Value and Variance

### Expected Value

> [!definition] Expected Value
> The **expected value** (or mean) of a discrete random variable is a measure of central location, calculated as a weighted average of the values where the weights are the probabilities.

$$E(x) = \mu = \sum x f(x)$$

**Example:** For DiCarlo Motors:
$$E(x) = 0(0.18) + 1(0.39) + 2(0.24) + 3(0.14) + 4(0.04) + 5(0.01) = 1.50$$

### Variance

> [!definition] Variance of a Discrete Random Variable
> The **variance** is a weighted average of the squared deviations from the mean:
> $$\text{Var}(x) = \sigma^2 = \sum (x - \mu)^2 f(x)$$

The **standard deviation** is:
$$\sigma = \sqrt{\sigma^2}$$

**Example:** For DiCarlo Motors:
- Variance: $\sigma^2 = 1.25$
- Standard deviation: $\sigma = \sqrt{1.25} = 1.118$

---

## Bivariate Distributions, Covariance, and Financial Portfolios

A [[bivariate probability distribution]] involves two random variables. Each outcome consists of two values, one for each random variable.

### Covariance

> [!definition] Covariance
> The **covariance** measures the linear association between two random variables:
> $$\sigma_{xy} = \frac{\text{Var}(x + y) - \text{Var}(x) - \text{Var}(y)}{2}$$

### Correlation Coefficient

$$\rho_{xy} = \frac{\sigma_{xy}}{\sigma_x \sigma_y}$$

- Values near $+1$: strong positive linear relationship
- Values near $-1$: strong negative linear relationship
- Values near $0$: weak or no linear relationship

### Linear Combinations of Random Variables

For a linear combination $ax + by$:

**Expected Value:**
$$E(ax + by) = aE(x) + bE(y)$$

**Variance:**
$$\text{Var}(ax + by) = a^2\text{Var}(x) + b^2\text{Var}(y) + 2ab\sigma_{xy}$$

### Financial Portfolio Application

Portfolios are linear combinations (weighted averages) of investment returns. The effect of [[covariance]] between individual assets on portfolio variance is the basis for reducing portfolio risk through [[diversification]].

---

## Binomial Probability Distribution

The [[binomial distribution]] is associated with a **binomial experiment**.

### Properties of a Binomial Experiment

1. The experiment consists of a sequence of $n$ identical trials
2. Two outcomes are possible on each trial: **success** or **failure**
3. The probability of success $p$ does not change from trial to trial
4. The trials are **independent**

### Binomial Probability Function

$$f(x) = \binom{n}{x} p^x (1-p)^{n-x}$$

where:
- $\binom{n}{x} = \frac{n!}{x!(n-x)!}$ = number of ways to obtain $x$ successes in $n$ trials
- $p$ = probability of success on one trial
- $x$ = number of successes ($0, 1, 2, \ldots, n$)

### Expected Value and Variance for Binomial Distribution

$$E(x) = \mu = np$$

$$\text{Var}(x) = \sigma^2 = np(1-p)$$

**Example:** Martin Clothing Store with $n = 3$ customers and $p = 0.30$:
- Expected value: $E(x) = 3(0.30) = 0.9$ customers
- Variance: $\sigma^2 = 3(0.30)(0.70) = 0.63$
- Standard deviation: $\sigma = 0.79$

---

## Poisson Probability Distribution

The [[Poisson distribution]] is used to model the number of occurrences over a specified interval of time or space.

### Properties of a Poisson Experiment

1. The probability of an occurrence is the same for any two intervals of equal length
2. The occurrence or nonoccurrence in any interval is independent of any other interval

### Poisson Probability Function

$$f(x) = \frac{\mu^x e^{-\mu}}{x!}$$

where:
- $\mu$ = expected (mean) number of occurrences in an interval
- $e = 2.71828$
- $x$ = number of occurrences ($0, 1, 2, \ldots$)

> [!info] Important Property
> For the Poisson distribution, the mean and variance are equal: $E(x) = \text{Var}(x) = \mu$

**Example:** If arrivals at a bank average 10 per 15 minutes, the probability of exactly 5 arrivals is:
$$f(5) = \frac{10^5 e^{-10}}{5!} = 0.0378$$

---

## Hypergeometric Probability Distribution

The [[hypergeometric distribution]] is used when sampling **without replacement** from a finite population.

### Key Differences from Binomial Distribution

- Trials are **not independent**
- Probability of success **changes** from trial to trial

### Hypergeometric Probability Function

$$f(x) = \frac{\binom{r}{x}\binom{N-r}{n-x}}{\binom{N}{n}}$$

where:
- $N$ = population size
- $r$ = number of successes in the population
- $n$ = number of trials (sample size)
- $x$ = number of successes in the sample

### Expected Value and Variance

$$E(x) = n\frac{r}{N}$$

$$\text{Var}(x) = n\frac{r}{N}\left(1 - \frac{r}{N}\right)\left(\frac{N-n}{N-1}\right)$$

**Example:** Box of 12 fuses with 5 defective. Probability that exactly 1 of 3 selected fuses is defective:
$$f(1) = \frac{\binom{5}{1}\binom{7}{2}}{\binom{12}{3}} = \frac{(5)(21)}{220} = 0.4773$$

---

## Key Takeaways

- A **random variable** provides numerical descriptions of experimental outcomes; it can be **discrete** (countable values) or **continuous** (any value in an interval)
- The **probability function** $f(x)$ must satisfy: $f(x) \geq 0$ and $\sum f(x) = 1$
- **Expected value** $E(x) = \sum xf(x)$ measures central tendency; **variance** $\sigma^2 = \sum(x-\mu)^2f(x)$ measures dispersion
- **Covariance** and **correlation** measure the relationship between two random variables in bivariate distributions
- The **binomial distribution** applies to experiments with $n$ independent trials, each with probability $p$ of success: $E(x) = np$, $\text{Var}(x) = np(1-p)$
- The **Poisson distribution** models occurrences over intervals with mean $\mu$; uniquely, $E(x) = \text{Var}(x) = \mu$
- The **hypergeometric distribution** applies to sampling without replacement where the probability of success changes from trial to trial
- In financial portfolios, negative covariance between assets can significantly reduce overall portfolio risk through diversification