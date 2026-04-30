---
title: "Chapter 6: Continuous Probability Distributions"
chapter: 6
tags:
  - statistics
  - probability
  - continuous-distributions
  - normal-distribution
  - uniform-distribution
  - exponential-distribution
---

# Continuous Probability Distributions

This chapter extends probability distributions to [[continuous random variable|continuous random variables]], covering the [[uniform distribution]], [[normal distribution]], and [[exponential distribution]]. Unlike discrete distributions where probabilities are computed directly from the probability function, continuous distributions use a [[probability density function]] where probabilities are calculated as areas under the curve.

## 6.1 Uniform Probability Distribution

The [[uniform distribution]] describes a continuous random variable where the probability of falling within any interval is proportional to the interval's length.

### Uniform Probability Density Function

> [!definition] Uniform Probability Density Function
> For a uniform random variable $x$ over the interval $[a, b]$:
> $$f(x) = \begin{cases} \frac{1}{b-a} & \text{for } a \leq x \leq b \\ 0 & \text{elsewhere} \end{cases}$$

### Area as a Measure of Probability

For continuous random variables, probability is computed as the area under the probability density function over the interval of interest:

$$P(x_1 \leq x \leq x_2) = \text{Area under } f(x) \text{ from } x_1 \text{ to } x_2$$

Key properties:
1. The total area under the curve equals 1
2. $f(x) \geq 0$ for all values of $x$
3. The probability of any single point is zero: $P(x = c) = 0$
4. $P(a \leq x \leq b) = P(a < x < b)$ (endpoints can be included or excluded)

### Expected Value and Variance

For the uniform distribution:

$$E(x) = \frac{a + b}{2}$$

$$\text{Var}(x) = \frac{(b-a)^2}{12}$$

---

## 6.2 Normal Probability Distribution

The [[normal distribution]] is the most important probability distribution for continuous random variables, characterized by its bell-shaped [[normal curve]].

### Normal Probability Density Function

> [!definition] Normal Probability Density Function
> $$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$
> where:
> - $\mu$ = mean
> - $\sigma$ = standard deviation
> - $\pi \approx 3.14159$
> - $e \approx 2.71828$

### Characteristics of the Normal Distribution

1. The distribution is defined by two parameters: $\mu$ (mean) and $\sigma$ (standard deviation)
2. The highest point occurs at the mean, which equals the median and mode
3. The mean can be any value: negative, zero, or positive
4. The distribution is symmetric about the mean (skewness = 0)
5. Larger standard deviations result in flatter, wider curves
6. The tails extend to infinity but never touch the horizontal axis
7. The total area under the curve equals 1

### Empirical Rule for Normal Distributions

| Interval | Percentage of Values |
|----------|---------------------|
| $\mu \pm 1\sigma$ | 68.3% |
| $\mu \pm 2\sigma$ | 95.4% |
| $\mu \pm 3\sigma$ | 99.7% |

### Standard Normal Probability Distribution

> [!definition] Standard Normal Distribution
> A normal distribution with $\mu = 0$ and $\sigma = 1$, denoted by the random variable $z$.
> $$f(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$$

### Converting to Standard Normal

Any normal random variable $x$ can be converted to the [[standard normal distribution]] using:

$$z = \frac{x - \mu}{\sigma}$$

The $z$ value represents the number of standard deviations that $x$ is from the mean.

### Computing Normal Probabilities

Three types of probability calculations:

1. **Cumulative probability**: $P(z \leq a)$ — read directly from standard normal table
2. **Interval probability**: $P(a \leq z \leq b) = P(z \leq b) - P(z \leq a)$
3. **Upper tail probability**: $P(z \geq a) = 1 - P(z \leq a)$

### Finding z Values for Given Probabilities

For inverse calculations (given probability, find $z$):
1. Locate the probability in the body of the standard normal table
2. Read the corresponding $z$ value from the row and column headers

---

## 6.3 Normal Approximation of Binomial Probabilities

When $np \geq 5$ and $n(1-p) \geq 5$, the [[binomial distribution]] can be approximated using the normal distribution.

### Approximation Parameters

Set:
- $\mu = np$
- $\sigma = \sqrt{np(1-p)}$

### Continuity Correction Factor

> [!definition] Continuity Correction Factor
> When approximating discrete binomial probabilities with the continuous normal distribution, add or subtract 0.5 from the value of $x$.

For binomial probability $P(x = k)$, use normal probability $P(k - 0.5 \leq x \leq k + 0.5)$

For binomial probability $P(x \leq k)$, use normal probability $P(x \leq k + 0.5)$

---

## 6.4 Exponential Probability Distribution

The [[exponential distribution]] is useful for modeling time between events or service times.

### Exponential Probability Density Function

> [!definition] Exponential Probability Density Function
> $$f(x) = \frac{1}{\mu} e^{-x/\mu} \quad \text{for } x \geq 0$$
> where $\mu$ = expected value (mean)

### Computing Exponential Probabilities

The cumulative distribution function:

$$P(x \leq x_0) = 1 - e^{-x_0/\mu}$$

The upper tail probability:

$$P(x > x_0) = e^{-x_0/\mu}$$

### Properties of the Exponential Distribution

1. The mean and standard deviation are equal: $E(x) = \sigma = \mu$
2. Variance: $\sigma^2 = \mu^2$
3. The distribution is skewed right (skewness = 2)

### Relationship Between Poisson and Exponential Distributions

> [!definition] Poisson-Exponential Relationship
> If the number of occurrences per interval follows a [[Poisson distribution]] with mean $\lambda$ occurrences per unit time, then the time between occurrences follows an exponential distribution with mean $\mu = \frac{1}{\lambda}$.

---

## Key Takeaways

- For continuous random variables, probabilities are computed as areas under the probability density function
- The probability of any single point for a continuous random variable is zero
- The [[uniform distribution]] has constant probability density over its defined interval
- The [[normal distribution]] is bell-shaped and fully characterized by its mean $\mu$ and standard deviation $\sigma$
- The [[standard normal distribution]] ($\mu = 0$, $\sigma = 1$) serves as a reference for computing all normal probabilities
- Any normal random variable can be standardized using $z = \frac{x-\mu}{\sigma}$
- The normal distribution can approximate binomial probabilities when $np \geq 5$ and $n(1-p) \geq 5$
- The [[exponential distribution]] models time between events when arrivals follow a Poisson process
- For the exponential distribution, mean equals standard deviation