---
title: "Inference About Means and Proportions with Two Populations"
chapter: 10
tags:
  - statistics
  - two-population-inference
  - hypothesis-testing
  - confidence-intervals
  - difference-of-means
  - difference-of-proportions
  - matched-samples
  - t-distribution
  - z-distribution
---

# Inference About Means and Proportions with Two Populations

This chapter extends statistical inference to compare **two populations**. The goal is to estimate or test hypotheses about the **difference between two population means** ($\mu_1 - \mu_2$) or the **difference between two population proportions** ($p_1 - p_2$).

---

## 10.1 Inferences About the Difference Between Two Population Means: $\sigma_1$ and $\sigma_2$ Known

When the [[population standard deviation|population standard deviations]] $\sigma_1$ and $\sigma_2$ are known, we use the [[standard normal distribution]] (z-distribution) for inference.

### Key Concepts

1. **[[Independent simple random samples]]**: Samples selected from two populations such that elements in one sample are chosen independently of elements in the other sample
2. **[[Point estimator]]** of $\mu_1 - \mu_2$: The difference between sample means $\bar{x}_1 - \bar{x}_2$
3. The [[sampling distribution]] of $\bar{x}_1 - \bar{x}_2$ is approximately normal for large samples

> [!definition] Standard Error of $\bar{x}_1 - \bar{x}_2$
> $$\sigma_{\bar{x}_1 - \bar{x}_2} = \sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}$$

### Interval Estimation of $\mu_1 - \mu_2$

> [!definition] Confidence Interval ($\sigma_1$, $\sigma_2$ Known)
> $$\bar{x}_1 - \bar{x}_2 \pm z_{\alpha/2} \sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}$$
> where $1 - \alpha$ is the confidence coefficient.

### Hypothesis Tests About $\mu_1 - \mu_2$

The three forms of hypothesis tests are:
- **Two-tailed**: $H_0: \mu_1 - \mu_2 = D_0$ vs $H_a: \mu_1 - \mu_2 \neq D_0$
- **Lower-tail**: $H_0: \mu_1 - \mu_2 \geq D_0$ vs $H_a: \mu_1 - \mu_2 < D_0$
- **Upper-tail**: $H_0: \mu_1 - \mu_2 \leq D_0$ vs $H_a: \mu_1 - \mu_2 > D_0$

> [!definition] Test Statistic ($\sigma_1$, $\sigma_2$ Known)
> $$z = \frac{(\bar{x}_1 - \bar{x}_2) - D_0}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}$$

### Practical Advice

- Sample sizes $n_1 \geq 30$ and $n_2 \geq 30$ are generally adequate
- For smaller samples, the populations should be approximately normally distributed

---

## 10.2 Inferences About the Difference Between Two Population Means: $\sigma_1$ and $\sigma_2$ Unknown

When population standard deviations are **unknown**, we estimate them using sample standard deviations $s_1$ and $s_2$, and use the [[t-distribution]].

### Interval Estimation of $\mu_1 - \mu_2$

> [!definition] Confidence Interval ($\sigma_1$, $\sigma_2$ Unknown)
> $$\bar{x}_1 - \bar{x}_2 \pm t_{\alpha/2} \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}$$

### Degrees of Freedom

> [!definition] Degrees of Freedom (Welch-Satterthwaite Approximation)
> $$df = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{1}{n_1-1}\left(\frac{s_1^2}{n_1}\right)^2 + \frac{1}{n_2-1}\left(\frac{s_2^2}{n_2}\right)^2}$$
> Round down to the nearest integer for a more conservative estimate.

### Hypothesis Tests About $\mu_1 - \mu_2$

> [!definition] Test Statistic ($\sigma_1$, $\sigma_2$ Unknown)
> $$t = \frac{(\bar{x}_1 - \bar{x}_2) - D_0}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$
> with degrees of freedom computed using the formula above.

### Practical Advice

- Equal or nearly equal sample sizes with $n_1 + n_2 \geq 20$ provide good results
- Larger samples are recommended for highly skewed distributions or outliers
- The procedure presented does **not** assume equal population variances (preferred approach)

---

## 10.3 Inferences About the Difference Between Two Population Means: Matched Samples

[[Matched samples]] (or paired samples) occur when each data value in one sample is paired with a corresponding value in the other sample.

### Key Concepts

1. Each sampled element provides **two data values** (one for each condition)
2. Analysis focuses on the **differences** $d_i$ between paired observations
3. Reduces sampling error by controlling for variation between subjects

### Analysis Procedure

1. Compute the difference for each pair: $d_i = x_{1i} - x_{2i}$
2. Calculate the sample mean of differences: $\bar{d} = \frac{\sum d_i}{n}$
3. Calculate the sample standard deviation: $s_d = \sqrt{\frac{\sum(d_i - \bar{d})^2}{n-1}}$

> [!definition] Test Statistic for Matched Samples
> $$t = \frac{\bar{d} - \mu_d}{s_d / \sqrt{n}}$$
> with $n - 1$ degrees of freedom.

> [!definition] Confidence Interval for Matched Samples
> $$\bar{d} \pm t_{\alpha/2} \frac{s_d}{\sqrt{n}}$$

### Advantages of Matched Sample Design

- Controls for subject-to-subject variation
- Generally provides better precision than independent samples
- Recommended when matching can be achieved without excessive cost

---

## 10.4 Inferences About the Difference Between Two Population Proportions

This section addresses inference about the difference between two [[population proportion|population proportions]] $p_1 - p_2$.

### Point Estimation

> [!definition] Point Estimator of $p_1 - p_2$
> $$\hat{p}_1 - \hat{p}_2$$
> where $\hat{p}_1 = \frac{x_1}{n_1}$ and $\hat{p}_2 = \frac{x_2}{n_2}$

> [!definition] Standard Error of $\hat{p}_1 - \hat{p}_2$
> $$\sigma_{\hat{p}_1 - \hat{p}_2} = \sqrt{\frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2}}$$

### Interval Estimation of $p_1 - p_2$

> [!definition] Confidence Interval for Difference in Proportions
> $$(\hat{p}_1 - \hat{p}_2) \pm z_{\alpha/2} \sqrt{\frac{\hat{p}_1(1-\hat{p}_1)}{n_1} + \frac{\hat{p}_2(1-\hat{p}_2)}{n_2}}$$

### Hypothesis Tests About $p_1 - p_2$

When testing $H_0: p_1 - p_2 = 0$ (no difference), we use a [[pooled estimator of p]]:

> [!definition] Pooled Estimator of $p$
> $$\bar{p} = \frac{n_1\hat{p}_1 + n_2\hat{p}_2}{n_1 + n_2}$$

> [!definition] Test Statistic for Hypothesis Tests About $p_1 - p_2$
> $$z = \frac{(\hat{p}_1 - \hat{p}_2)}{\sqrt{\bar{p}(1-\bar{p})\left(\frac{1}{n_1} + \frac{1}{n_2}\right)}}$$

### Sample Size Requirements

The normal approximation is valid when:
- $n_1 p_1 \geq 5$, $n_1(1-p_1) \geq 5$
- $n_2 p_2 \geq 5$, $n_2(1-p_2) \geq 5$

---

## Key Takeaways

- **Independent samples** with known $\sigma_1$, $\sigma_2$ use the **z-distribution** for inference about $\mu_1 - \mu_2$
- **Independent samples** with unknown $\sigma_1$, $\sigma_2$ use the **t-distribution** with degrees of freedom calculated via the Welch-Satterthwaite formula
- **Matched samples** analyze the differences between paired observations using a one-sample t-procedure
- The matched sample design often provides **better precision** than independent samples by eliminating between-subject variation
- For **proportions**, use the pooled estimator $\bar{p}$ when testing $H_0: p_1 = p_2$
- For **interval estimation** of proportion differences, use unpooled sample proportions
- Equal sample sizes ($n_1 = n_2$) are recommended when possible
- Verify sample size conditions for normal approximation validity in all procedures