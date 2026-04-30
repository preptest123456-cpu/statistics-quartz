---
title: Chapter 9 - Hypothesis Tests
chapter: 9
tags:
  - statistics
  - hypothesis-testing
  - type-I-error
  - type-II-error
  - p-value
  - test-statistic
  - confidence-interval
  - population-mean
  - population-proportion
  - sample-size
---

# Chapter 9: Hypothesis Tests

Hypothesis testing is a statistical procedure that uses sample data to determine whether a statement about the value of a [[population parameter]] should or should not be rejected. This chapter covers the development of null and alternative hypotheses, types of errors, and methods for testing claims about population means and proportions.

---

## 9.1 Developing Null and Alternative Hypotheses

In hypothesis testing, we begin with a tentative assumption about a population parameter called the **null hypothesis** ($H_0$). We then define an **alternative hypothesis** ($H_a$), which is the opposite of what is stated in the null hypothesis. The testing procedure uses sample data to test these two competing statements.

> [!definition] Null Hypothesis ($H_0$)
> A tentative assumption about a population parameter that is assumed to be true unless sample evidence provides sufficient grounds to reject it.

> [!definition] Alternative Hypothesis ($H_a$)
> A statement that is the opposite of the null hypothesis; it is concluded to be true if the null hypothesis is rejected.

### The Alternative Hypothesis as a Research Hypothesis

When research aims to support a new method, product, or conclusion, the research hypothesis is stated as the alternative hypothesis:

1. **New teaching method**: $H_a$: New method is better than current method
2. **New sales bonus plan**: $H_a$: New plan increases sales
3. **New drug**: $H_a$: New drug lowers blood pressure more than existing drug

**Example (Fuel Injection System):**
$$H_0: \mu \le 24$$
$$H_a: \mu > 24$$

If $H_0$ is rejected, the research conclusion that the new fuel injection system improves miles-per-gallon is supported.

### The Null Hypothesis as an Assumption to Be Challenged

When we begin with a belief or assumption about a parameter value, the null hypothesis expresses that belief:

**Example (Soft Drink Labeling):**
- Label states 67.6 fluid ounces
- From government agency perspective:
$$H_0: \mu \ge 67.6$$
$$H_a: \mu < 67.6$$

- From manufacturer's perspective (quality control):
$$H_0: \mu = 67.6$$
$$H_a: \mu \ne 67.6$$

### Summary of Forms for Null and Alternative Hypotheses

For hypothesis tests involving a population mean with hypothesized value $\mu_0$:

| Test Type | Null Hypothesis | Alternative Hypothesis |
|-----------|----------------|----------------------|
| Lower Tail Test | $H_0: \mu \ge \mu_0$ | $H_a: \mu < \mu_0$ |
| Upper Tail Test | $H_0: \mu \le \mu_0$ | $H_a: \mu > \mu_0$ |
| Two-Tailed Test | $H_0: \mu = \mu_0$ | $H_a: \mu \ne \mu_0$ |

**Key Principle:** The equality part of the expression ($\le$, $\ge$, or $=$) always appears in the null hypothesis.

---

## 9.2 Type I and Type II Errors

| | $H_0$ True | $H_a$ True |
|---|-----------|-----------|
| **Accept $H_0$** | Correct Conclusion | Type II Error |
| **Reject $H_0$** | Type I Error | Correct Conclusion |

> [!definition] Type I Error
> The error of rejecting $H_0$ when it is actually true.

> [!definition] Type II Error
> The error of accepting $H_0$ when it is actually false.

> [!definition] Level of Significance ($\alpha$)
> The probability of making a Type I error when the null hypothesis is true as an equality. Common choices are $\alpha = 0.05$ and $\alpha = 0.01$.

**Important Practice:** Because we typically do not control for Type II error, statisticians recommend using "**do not reject $H_0$**" instead of "accept $H_0$" to avoid the risk of Type II error.

---

## 9.3 Population Mean: σ Known

When the [[population standard deviation]] $\sigma$ is known (often from historical data), the test statistic follows a [[standard normal distribution]].

### Test Statistic

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

where:
- $\bar{x}$ = sample mean
- $\mu_0$ = hypothesized population mean
- $\sigma$ = population standard deviation
- $n$ = sample size

### One-Tailed Test

**Example (Hilltop Coffee - Lower Tail Test):**
- $H_0: \mu \ge 3$ (pounds per can)
- $H_a: \mu < 3$
- $\alpha = 0.01$, $\sigma = 0.18$, $n = 36$
- Sample: $\bar{x} = 2.92$

$$z = \frac{2.92 - 3}{0.18/\sqrt{36}} = \frac{-0.08}{0.03} = -2.67$$

> [!definition] p-Value
> A probability that provides a measure of the evidence against the null hypothesis. Smaller p-values indicate more evidence against $H_0$.

**p-Value Interpretation Guidelines:**
- Less than 0.01: Overwhelming evidence to conclude $H_a$ is true
- 0.01 to 0.05: Strong evidence to conclude $H_a$ is true
- 0.05 to 0.10: Weak evidence to conclude $H_a$ is true
- Greater than 0.10: Insufficient evidence to conclude $H_a$ is true

**Rejection Rules:**

| Approach | Lower Tail | Upper Tail | Two-Tailed |
|----------|------------|------------|------------|
| p-Value | Reject $H_0$ if p-value $\le \alpha$ | Reject $H_0$ if p-value $\le \alpha$ | Reject $H_0$ if p-value $\le \alpha$ |
| Critical Value | Reject $H_0$ if $z \le -z_\alpha$ | Reject $H_0$ if $z \ge z_\alpha$ | Reject $H_0$ if $z \le -z_{\alpha/2}$ or $z \ge z_{\alpha/2}$ |

### Two-Tailed Test

**Example (MaxFlight Golf Balls):**
- $H_0: \mu = 295$ yards
- $H_a: \mu \ne 295$ yards
- $\alpha = 0.05$, $\sigma = 12$, $n = 50$
- Sample: $\bar{x} = 297.6$

$$z = \frac{297.6 - 295}{12/\sqrt{50}} = \frac{2.6}{1.7} = 1.53$$

For a two-tailed test: p-value $= 2 \times P(z \ge 1.53) = 2(0.0630) = 0.1260$

Since $0.1260 > 0.05$, do not reject $H_0$.

### Relationship Between Interval Estimation and Hypothesis Testing

A **confidence interval approach** can be used for two-tailed tests:
1. Construct a $100(1-\alpha)\%$ confidence interval: $\bar{x} \pm z_{\alpha/2} \frac{\sigma}{\sqrt{n}}$
2. If the interval contains $\mu_0$, do not reject $H_0$
3. If the interval does not contain $\mu_0$, reject $H_0$

---

## 9.4 Population Mean: σ Unknown

When $\sigma$ is unknown, we use the sample standard deviation $s$ as an estimate, and the test statistic follows a [[t-distribution]] with $n-1$ degrees of freedom.

### Test Statistic

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

### Summary of Hypothesis Tests (σ Unknown)

| | Lower Tail Test | Upper Tail Test | Two-Tailed Test |
|---|----------------|-----------------|-----------------|
| Hypotheses | $H_0: \mu \ge \mu_0$ | $H_0: \mu \le \mu_0$ | $H_0: \mu = \mu_0$ |
| | $H_a: \mu < \mu_0$ | $H_a: \mu > \mu_0$ | $H_a: \mu \ne \mu_0$ |
| Critical Value Rejection | $t \le -t_\alpha$ | $t \ge t_\alpha$ | $t \le -t_{\alpha/2}$ or $t \ge t_{\alpha/2}$ |

**Practical Guidelines:**
- Population normally distributed: Procedure works for any sample size
- Population approximately normal: Sample sizes as small as $n = 15$ acceptable
- Population highly skewed or with outliers: Sample sizes approaching 50 recommended
- General guideline: $n \ge 30$ provides good results in most cases

---

## 9.5 Population Proportion

For hypothesis tests about a [[population proportion]] $p$ with hypothesized value $p_0$:

### Test Statistic

$$z = \frac{\bar{p} - p_0}{\sqrt{\frac{p_0(1-p_0)}{n}}}$$

**Conditions for validity:** $np \ge 5$ and $n(1-p) \ge 5$

### Summary of Hypothesis Tests for Proportions

| | Lower Tail | Upper Tail | Two-Tailed |
|---|-----------|-----------|-----------|
| $H_0$ | $p \ge p_0$ | $p \le p_0$ | $p = p_0$ |
| $H_a$ | $p < p_0$ | $p > p_0$ | $p \ne p_0$ |
| Reject $H_0$ if | $z \le -z_\alpha$ | $z \ge z_\alpha$ | $\|z\| \ge z_{\alpha/2}$ |

**Example (Pine Creek Golf Course):**
- $H_0: p \le 0.20$ (proportion of women players)
- $H_a: p > 0.20$
- $\alpha = 0.05$, $n = 400$, sample: 100 women

$$\bar{p} = \frac{100}{400} = 0.25$$

$$z = \frac{0.25 - 0.20}{\sqrt{\frac{0.20(0.80)}{400}}} = \frac{0.05}{0.02} = 2.50$$

p-value $= P(z \ge 2.50) = 0.0062 < 0.05$, so reject $H_0$.

---

## 9.6 Hypothesis Testing and Decision Making

In **significance tests**, we control only Type I error ($\alpha$). Conclusions are either:
- "Reject $H_0$" (results are statistically significant)
- "Do not reject $H_0$" (evidence is inconclusive)

In **decision-making contexts** (e.g., [[lot-acceptance sampling]]), where action must be taken regardless of the conclusion, it's recommended to control both Type I and Type II errors.

---

## 9.7 Calculating the Probability of Type II Errors

The probability of Type II error ($\beta$) depends on:
1. The true value of the population parameter
2. The sample size
3. The level of significance $\alpha$

### Steps to Calculate β

1. Formulate null and alternative hypotheses
2. Determine the critical value and rejection rule using $\alpha$
3. Find the sample mean value ($c$) corresponding to the critical value
4. Define the acceptance region for $H_0$
5. Compute the probability that $\bar{x}$ falls in the acceptance region when $H_a$ is true

**For the battery example** ($H_0: \mu \ge 120$, $H_a: \mu < 120$, $\alpha = 0.05$, $\sigma = 12$, $n = 36$):

Critical value: $\bar{x} = 120 - 1.645 \times \frac{12}{\sqrt{36}} = 116.71$

If $\mu = 112$:
$$z = \frac{116.71 - 112}{12/\sqrt{36}} = 2.36$$
$$\beta = P(z > 2.36) = 0.0091$$

> [!definition] Power of the Test
> The probability of correctly rejecting $H_0$ when it is false: Power $= 1 - \beta$

---

## 9.8 Determining Sample Size for Hypothesis Tests

To control both Type I ($\alpha$) and Type II ($\beta$) errors:

### Sample Size Formula (One-Tailed Test)

$$n = \frac{(z_\alpha + z_\beta)^2 \sigma^2}{(\mu_0 - \mu_a)^2}$$

where:
- $z_\alpha$ = z-value for area $\alpha$ in upper tail
- $z_\beta$ = z-value for area $\beta$ in upper tail
- $\mu_0$ = hypothesized mean under $H_0$
- $\mu_a$ = specific mean value under $H_a$ for Type II error calculation

**For two-tailed tests:** Replace $z_\alpha$ with $z_{\alpha/2}$

**Example (Battery Test):**
- $\alpha = 0.05 \Rightarrow z_{0.05} = 1.645$
- $\beta = 0.10 \Rightarrow z_{0.10} = 1.28$
- $\mu_0 = 120$, $\mu_a = 115$, $\sigma = 12$

$$n = \frac{(1.645 + 1.28)^2 (12)^2}{(120 - 115)^2} = \frac{(2.925)^2 (144)}{25} = 49.3 \approx 50$$

### Key Relationships

1. Once two of $\alpha$, $\beta$, and $n$ are specified, the third is determined
2. For a given $\alpha$, increasing $n$ will reduce $\beta$
3. For a given $n$, decreasing $\alpha$ will increase $\beta$

---

## Steps of Hypothesis Testing

1. Develop the null and alternative hypotheses
2. Specify the level of significance ($\alpha$)
3. Collect sample data and compute the test statistic

**p-Value Approach:**
4. Use the test statistic to compute the p-value
5. Reject $H_0$ if p-value $\le \alpha$
6. Interpret the conclusion in context

**Critical Value Approach:**
4. Determine the critical value(s) using $\alpha$
5. Compare test statistic to critical value(s) and decide
6. Interpret the conclusion in context

---

## Key Takeaways

- The **null hypothesis** ($H_0$) contains the equality; the **alternative hypothesis** ($H_a$) is what we hope to conclude
- **Type I error** (rejecting true $H_0$) is controlled by the level of significance $\alpha$
- **Type II error** (failing to reject false $H_0$) probability $\beta$ depends on the true parameter value
- Use $z$-statistic when $\sigma$ is known; use $t$-statistic when $\sigma$ is unknown
- **p-value** represents the probability of observing results as extreme as the sample, given $H_0$ is true
- Smaller p-values provide stronger evidence against $H_0$
- **Power** ($1 - \beta$) is the probability of correctly rejecting a false $H_0$
- Sample size can be determined to achieve desired levels of both $\alpha$ and $\beta$
- The relationship between [[confidence intervals]] and two-tailed hypothesis tests provides an alternative testing approach