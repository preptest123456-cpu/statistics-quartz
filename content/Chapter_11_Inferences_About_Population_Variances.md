---
title: "Inferences About Population Variances"
chapter: 11
tags:
  - statistics
  - variance
  - chi-square-distribution
  - F-distribution
  - hypothesis-testing
  - confidence-intervals
---

# Inferences About Population Variances

This chapter introduces statistical methods for making inferences about [[population variance|population variances]] using the [[chi-square distribution]] for single populations and the [[F distribution]] for comparing two populations.

## Statistics in Practice: U.S. Government Accountability Office

The GAO used hypothesis testing on variance to detect fraudulent data in a pollution control program. When testing pH levels at a waste treatment plant, an unusually **low variance** led to rejection of the null hypothesis:

$$H_0: \sigma^2 = \sigma_0^2 \quad \text{vs} \quad H_a: \sigma^2 \neq \sigma_0^2$$

Investigation revealed that the operator had been recording fabricated values rather than conducting actual measurements, demonstrating how variance testing can detect data quality issues.

## 11.1 Inferences About a Population Variance

### Point Estimation

> [!definition] Sample Variance
> The [[sample variance]] serves as the point estimator of the population variance $\sigma^2$:
> $$s^2 = \frac{\sum(x_i - \bar{x})^2}{n-1}$$

### Sampling Distribution

When sampling from a [[normal distribution]], the quantity $(n-1)s^2/\sigma^2$ follows a specific distribution:

> [!definition] Chi-Square Sampling Distribution
> When a simple random sample of size $n$ is selected from a normal population:
> $$\chi^2 = \frac{(n-1)s^2}{\sigma^2}$$
> has a **chi-square distribution** with $n-1$ degrees of freedom.

Key characteristics of the chi-square distribution:
1. Not symmetric (positively skewed)
2. Values are never negative
3. Shape depends on degrees of freedom
4. Approaches normality as degrees of freedom increase

### Interval Estimation

The [[confidence interval]] for a population variance uses chi-square critical values:

$$\frac{(n-1)s^2}{\chi^2_{\alpha/2}} \leq \sigma^2 \leq \frac{(n-1)s^2}{\chi^2_{(1-\alpha/2)}}$$

where:
- $\chi^2_{\alpha/2}$ = upper tail critical value
- $\chi^2_{(1-\alpha/2)}$ = lower tail critical value
- $1 - \alpha$ = confidence coefficient

> [!tip] Standard Deviation Interval
> To obtain a confidence interval for the [[population standard deviation]] $\sigma$, take the square root of both interval endpoints.

### Hypothesis Testing

The three forms of hypothesis tests about population variance:

| Lower Tail Test | Upper Tail Test | Two-Tailed Test |
|-----------------|-----------------|-----------------|
| $H_0: \sigma^2 \geq \sigma_0^2$ | $H_0: \sigma^2 \leq \sigma_0^2$ | $H_0: \sigma^2 = \sigma_0^2$ |
| $H_a: \sigma^2 < \sigma_0^2$ | $H_a: \sigma^2 > \sigma_0^2$ | $H_a: \sigma^2 \neq \sigma_0^2$ |

> [!definition] Test Statistic for Population Variance
> $$\chi^2 = \frac{(n-1)s^2}{\sigma_0^2}$$
> where $\sigma_0^2$ is the hypothesized population variance.

**Decision Rules:**
- **Lower tail:** Reject $H_0$ if $\chi^2 < \chi^2_{(1-\alpha)}$
- **Upper tail:** Reject $H_0$ if $\chi^2 > \chi^2_{\alpha}$
- **Two-tailed:** Reject $H_0$ if $\chi^2 < \chi^2_{(1-\alpha/2)}$ or $\chi^2 > \chi^2_{\alpha/2}$

## 11.2 Inferences About Two Population Variances

### The F Distribution

When comparing variances from two normal populations with equal variances, the ratio of sample variances follows an [[F distribution]]:

> [!definition] Sampling Distribution of Variance Ratio
> When independent samples of sizes $n_1$ and $n_2$ are selected from two normal populations with equal variances ($\sigma_1^2 = \sigma_2^2$):
> $$F = \frac{s_1^2}{s_2^2}$$
> has an F distribution with $n_1 - 1$ numerator degrees of freedom and $n_2 - 1$ denominator degrees of freedom.

Key characteristics of the F distribution:
1. Not symmetric
2. Values are never negative
3. Shape depends on both numerator and denominator degrees of freedom

### Hypothesis Testing for Two Variances

**Two-Tailed Test:**
$$H_0: \sigma_1^2 = \sigma_2^2 \quad \text{vs} \quad H_a: \sigma_1^2 \neq \sigma_2^2$$

**One-Tailed Test:**
$$H_0: \sigma_1^2 \leq \sigma_2^2 \quad \text{vs} \quad H_a: \sigma_1^2 > \sigma_2^2$$

> [!definition] Test Statistic for Comparing Two Variances
> $$F = \frac{s_1^2}{s_2^2}$$
> **Convention:** Denote the population with the larger sample variance as population 1. This ensures the test statistic falls in the upper tail.

**Decision Rules:**

| Upper Tail Test | Two-Tailed Test |
|-----------------|-----------------|
| Reject $H_0$ if $F > F_\alpha$ | Reject $H_0$ if $F > F_{\alpha/2}$ |

> [!warning] Assumption
> The F distribution test for comparing variances is **sensitive to the assumption of normal populations**. It should not be used unless both populations are at least approximately normally distributed.

### Example: School Bus Service Comparison

Testing whether Milbank and Gulf Park bus companies have different arrival time variances:
- Milbank (population 1): $n_1 = 26$, $s_1^2 = 48$
- Gulf Park (population 2): $n_2 = 16$, $s_2^2 = 20$

Test statistic: $F = \frac{48}{20} = 2.40$

With $\alpha = 0.10$ and critical value $F_{.05} = 2.28$ (for a two-tailed test), we reject $H_0$ since $2.40 > 2.28$.

## Key Formulas Summary

| Purpose | Formula |
|---------|---------|
| Chi-square test statistic | $\chi^2 = \frac{(n-1)s^2}{\sigma_0^2}$ |
| CI for variance | $\frac{(n-1)s^2}{\chi^2_{\alpha/2}} \leq \sigma^2 \leq \frac{(n-1)s^2}{\chi^2_{(1-\alpha/2)}}$ |
| F test statistic | $F = \frac{s_1^2}{s_2^2}$ |

## Key Takeaways

- The [[chi-square distribution]] is used for inferences about a **single population variance** when sampling from a normal population
- The [[F distribution]] is used for comparing **two population variances** using independent samples from normal populations
- For F tests, always place the larger sample variance in the numerator to use upper-tail critical values only
- Confidence intervals for $\sigma$ are obtained by taking square roots of the variance interval endpoints
- Upper-tail tests for variance are most common in quality control applications where excessive variance is undesirable
- Both tests are sensitive to the normality assumption and should only be used when populations are approximately normal
- Low variance indicates consistency; high variance may signal quality problems or process issues