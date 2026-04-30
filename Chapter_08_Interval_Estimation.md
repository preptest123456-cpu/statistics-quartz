---
title: "Interval Estimation"
chapter: 8
tags:
  - statistics
  - interval_estimation
  - confidence_intervals
  - margin_of_error
  - sample_size
  - population_mean
  - population_proportion
  - t_distribution
---

# Interval Estimation

This chapter covers methods for developing **interval estimates** of a [[population mean]] ($\mu$) and a [[population proportion]] ($p$). Unlike a [[point estimate]], an interval estimate provides information about how close the estimate is to the population parameter.

## General Form of an Interval Estimate

The general form of an interval estimate is:

$$\text{Point estimate} \pm \text{Margin of error}$$

> [!definition] Interval Estimate
> An estimate of a population parameter that provides an interval believed to contain the value of the parameter. It has the form: point estimate ± margin of error.

> [!definition] Margin of Error
> The ± value added to and subtracted from a point estimate to develop an interval estimate of a population parameter.

---

## 8.1 Population Mean: σ Known

When historical data or other information provides a good estimate of the [[population standard deviation]] ($\sigma$) prior to sampling, we have the **σ known case**.

### Interval Estimate Formula

$$\bar{x} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$$

where:
- $(1 - \alpha)$ is the [[confidence coefficient]]
- $z_{\alpha/2}$ is the z-value providing an area of $\alpha/2$ in the upper tail of the [[standard normal distribution]]

### Key Concepts

1. The [[sampling distribution]] of $\bar{x}$ is used to compute the probability that $\bar{x}$ will be within a given distance of $\mu$
2. The [[standard error]] of the mean is $\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$
3. For 95% confidence, 95% of all $\bar{x}$ values are within $1.96\sigma_{\bar{x}}$ of $\mu$

### Common z-values for Confidence Levels

| Confidence Level | α     | α/2   | $z_{\alpha/2}$ |
| ---------------- | ----- | ----- | -------------- |
| 90%              | 0.10  | 0.05  | 1.645          |
| 95%              | 0.05  | 0.025 | 1.960          |
| 99%              | 0.01  | 0.005 | 2.576          |

> [!definition] Confidence Level
> The confidence associated with an interval estimate. For example, a 95% confidence level means that 95% of intervals constructed using this procedure will contain the population parameter.

> [!definition] Confidence Coefficient
> The confidence level expressed as a decimal value (e.g., 0.95 for 95% confidence level).

### Practical Advice

- If population is **normally distributed**: the confidence interval is exact
- If population is **not normally distributed**: the confidence interval is approximate
- **Sample size n ≥ 30** is adequate in most applications
- For **roughly symmetric populations**: sample sizes as small as 15 provide good approximations

---

## 8.2 Population Mean: σ Unknown

When no good basis exists for estimating $\sigma$ prior to sampling, we use the **σ unknown case**. The sample standard deviation $s$ is used to estimate $\sigma$.

### The t Distribution

> [!definition] t Distribution
> A family of probability distributions used to develop interval estimates of a population mean when $\sigma$ is unknown and estimated by $s$. Each t distribution is defined by its **degrees of freedom** parameter.

Key properties:
- Mean = 0
- As degrees of freedom increase, the t distribution approaches the [[standard normal distribution]]
- More variable (heavier tails) than the normal distribution for small samples

> [!definition] Degrees of Freedom
> A parameter of the t distribution. For interval estimation of a population mean, degrees of freedom = $n - 1$.

### Interval Estimate Formula

$$\bar{x} \pm t_{\alpha/2} \frac{s}{\sqrt{n}}$$

where:
- $s$ is the [[sample standard deviation]]
- $t_{\alpha/2}$ is the t-value with $n-1$ degrees of freedom providing area $\alpha/2$ in the upper tail

### Practical Advice

| Population Distribution | Recommended Sample Size |
| ----------------------- | ----------------------- |
| Normal distribution     | Any sample size         |
| Roughly symmetric       | n ≥ 15                  |
| General case            | n ≥ 30                  |
| Highly skewed/outliers  | n ≥ 50                  |

### Summary of Procedures

```
Is σ known?
├── Yes → Use: x̄ ± zα/2(σ/√n)
└── No → Use s to estimate σ → Use: x̄ ± tα/2(s/√n)
```

---

## 8.3 Determining the Sample Size

To achieve a desired [[margin of error]] $E$, we can calculate the required sample size before collecting data.

### Sample Size Formula (σ Known Case)

$$n = \frac{(z_{\alpha/2})^2 \sigma^2}{E^2}$$

where:
- $E$ = desired margin of error
- $z_{\alpha/2}$ = z-value for desired confidence level
- $\sigma$ = [[planning value]] for population standard deviation

### Methods for Obtaining Planning Value for σ

1. Use estimate from **previous studies** of the same or similar units
2. Conduct a **pilot study** to obtain a preliminary sample
3. Use **judgment** or best guess:
   - Estimate the range (largest - smallest values)
   - Planning value ≈ Range / 4

> [!important]
> If the computed sample size is not an integer, **round up** to the next integer value to ensure the desired margin of error is achieved.

---

## 8.4 Population Proportion

For estimating a [[population proportion]] $p$, we use the [[sample proportion]] $\bar{p}$ as the point estimate.

### Standard Error of the Proportion

$$\sigma_{\bar{p}} = \sqrt{\frac{p(1-p)}{n}}$$

Since $p$ is unknown, we substitute $\bar{p}$:

$$\text{Estimated Standard Error} = \sqrt{\frac{\bar{p}(1-\bar{p})}{n}}$$

### Interval Estimate Formula

$$\bar{p} \pm z_{\alpha/2} \sqrt{\frac{\bar{p}(1-\bar{p})}{n}}$$

where:
- $(1 - \alpha)$ is the confidence coefficient
- The normal approximation is valid when $np \geq 5$ and $n(1-p) \geq 5$

### Determining Sample Size for Proportions

$$n = \frac{(z_{\alpha/2})^2 p^*(1-p^*)}{E^2}$$

where $p^*$ is the planning value for the proportion.

### Methods for Obtaining Planning Value p*

1. Use sample proportion from **previous sample**
2. Use **pilot study** to obtain preliminary sample
3. Use **judgment** or best guess
4. Use $p^* = 0.50$ if no other information available (provides **largest sample size** needed)

| $p^*$ | $p^*(1-p^*)$ |
| ----- | ------------ |
| 0.10  | 0.09         |
| 0.30  | 0.21         |
| 0.40  | 0.24         |
| **0.50** | **0.25** (largest) |
| 0.60  | 0.24         |
| 0.70  | 0.21         |
| 0.90  | 0.09         |

---

## Key Takeaways

- **Point estimate ± margin of error** provides the general form of interval estimates
- For **σ known**: use the standard normal (z) distribution with $z_{\alpha/2}(\sigma/\sqrt{n})$ as margin of error
- For **σ unknown**: use the t distribution with $t_{\alpha/2}(s/\sqrt{n})$ as margin of error
- **Higher confidence levels** result in **wider intervals** (larger margins of error)
- **Larger sample sizes** result in **narrower intervals** (smaller margins of error)
- The **t distribution** approaches the normal distribution as degrees of freedom increase
- For **population proportions**, use $\bar{p} \pm z_{\alpha/2}\sqrt{\bar{p}(1-\bar{p})/n}$
- When determining sample size, use **planning values** for unknown parameters
- Using $p^* = 0.50$ guarantees sufficient sample size for proportion estimation
- Always **round up** computed sample sizes to the next integer