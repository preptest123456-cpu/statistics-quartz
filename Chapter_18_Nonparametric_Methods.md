---
title: "Nonparametric Methods"
chapter: 18
tags:
  - statistics
  - nonparametric_methods
  - sign_test
  - wilcoxon_test
  - mann_whitney_wilcoxon
  - kruskal_wallis
  - rank_correlation
  - distribution_free_methods
  - hypothesis_testing
---

# Chapter 18: Nonparametric Methods

## Overview

**Nonparametric methods** are statistical procedures that do not require assumptions about the specific form of the population's probability distribution. Unlike [[parametric methods]] (which typically assume normality), nonparametric methods are also called **distribution-free methods**.

### Key Advantages of Nonparametric Methods
1. Can be applied to both [[categorical data]] and [[quantitative data]]
2. No assumption required about population distribution shape
3. Often use rank-ordered data for analysis
4. Robust to outliers and non-normal distributions

> [!definition] Parametric Methods
> Statistical methods that begin with an assumption about the probability distribution of the population (often normal distribution), then derive sampling distributions to make inferences about population parameters like $\mu$ or $\sigma$.

> [!definition] Nonparametric Methods
> Statistical methods requiring no assumption about the specific form of the population's probability distribution; applicable to both categorical and quantitative data.

---

## 18.1 Sign Test

The [[sign test]] is a versatile nonparametric method using the [[binomial distribution]] with $p = 0.50$ as the sampling distribution. It has two primary applications:
1. Hypothesis test about a population median
2. Hypothesis test with matched samples

### Hypothesis Test About a Population Median

When testing a hypothesis about a [[population median]], each observation is compared to the hypothesized median value:
- **Plus sign (+):** observation > hypothesized median
- **Minus sign (−):** observation < hypothesized median
- **Equal values:** discarded from analysis

> [!example] Cape May Potato Chips Example
> Lawler's management tests whether median weekly sales equal \$450:
> - $H_0$: Median = 450
> - $H_a$: Median ≠ 450
> 
> With 7 plus signs and 3 minus signs from 10 stores, the test uses binomial distribution with $n = 10$ and $p = 0.50$.

The hypotheses convert to:
- $H_0: p = 0.50$
- $H_a: p \neq 0.50$

### Normal Approximation for Large Samples

When $n > 20$, use the normal distribution approximation:

> [!formula] Normal Approximation for Sign Test
> $$\mu = 0.50n$$
> $$\sigma = \sqrt{0.25n}$$
> 
> Distribution form: Approximately normal for $n > 20$

> [!example] New Home Prices Example
> Testing whether median home price < \$236,000:
> - Sample: $n = 60$ (after removing one observation equal to hypothesized value)
> - Plus signs: 22, Minus signs: 38
> - $\mu = 0.50(60) = 30$
> - $\sigma = \sqrt{0.25(60)} = 3.873$
> 
> With continuity correction:
> $$z = \frac{22.5 - 30}{3.873} = -1.94$$
> p-value = 0.0262

### Hypothesis Test with Matched Samples

For matched-sample designs where individuals compare two products/treatments:
- Record **+** if preference for item 1
- Record **−** if preference for item 2
- Discard observations with no preference

> [!example] Sun Coast Farms Taste Test
> 14 individuals compare two orange juice brands:
> - 2 plus signs (Citrus Valley)
> - 10 minus signs (Tropical Orange)
> - 2 no preference (discarded)
> - $n = 12$, p-value = 2(0.0002 + 0.0029 + 0.0161) = 0.0384
> - Conclusion: Consumer preferences differ significantly

---

## 18.2 Wilcoxon Signed-Rank Test

The [[Wilcoxon signed-rank test]] analyzes matched-sample data when quantitative differences are available. It requires only that the distribution of differences be **symmetric**.

### Procedure

1. Compute differences between paired observations
2. Discard zero differences
3. Rank absolute values of differences (ties get average rank)
4. Assign signs to ranks based on original difference signs
5. Sum positive signed ranks ($T^+$)

> [!definition] Wilcoxon Signed-Rank Test
> A nonparametric test for the difference between medians of two populations based on matched samples. Requires symmetric distribution of paired differences.

### Sampling Distribution of $T^+$

> [!formula] Wilcoxon Signed-Rank Test Statistics
> $$\mu_{T^+} = \frac{n(n+1)}{4}$$
> 
> $$\sigma_{T^+} = \sqrt{\frac{n(n+1)(2n+1)}{24}}$$
> 
> Distribution form: Approximately normal for $n \geq 10$

> [!example] Production Methods Comparison
> Testing whether two production methods have equal median completion times:
> - $n = 10$ (after removing one zero difference)
> - $T^+ = 49.5$
> - $\mu_{T^+} = \frac{10(11)}{4} = 27.5$
> - $\sigma_{T^+} = \sqrt{\frac{10(11)(21)}{24}} = 9.8107$
> 
> With continuity correction:
> $$z = \frac{49 - 27.5}{9.8107} = 2.19$$
> p-value = 2(1 - 0.9857) = 0.0286

---

## 18.3 Mann-Whitney-Wilcoxon Test

The [[Mann-Whitney-Wilcoxon test]] (MWW test) compares two populations using independent samples. Also known as:
- **Mann-Whitney test**
- **Wilcoxon rank-sum test**

### Hypotheses

$$H_0: \text{The two populations are identical}$$
$$H_a: \text{The two populations are not identical}$$

If populations have the same shape, hypotheses can be expressed in terms of medians:

| Two-Tailed | Lower Tail | Upper Tail |
|------------|------------|------------|
| $H_0$: Median$_1$ − Median$_2$ = 0 | $H_0$: Median$_1$ − Median$_2$ ≥ 0 | $H_0$: Median$_1$ − Median$_2$ ≤ 0 |
| $H_a$: Median$_1$ − Median$_2$ ≠ 0 | $H_a$: Median$_1$ − Median$_2$ < 0 | $H_a$: Median$_1$ − Median$_2$ > 0 |

### Procedure

1. Rank all observations from both samples combined (lowest to highest)
2. Assign average ranks for tied values
3. Sum ranks for sample 1: $W = \sum \text{ranks from sample 1}$
4. Use $W$ as test statistic

### Sampling Distribution of $W$

> [!formula] MWW Test Statistics (Normal Approximation)
> $$\mu_W = \frac{1}{2}n_1(n_1 + n_2 + 1)$$
> 
> $$\sigma_W = \sqrt{\frac{1}{12}n_1 n_2 (n_1 + n_2 + 1)}$$
> 
> Distribution form: Approximately normal for $n_1 \geq 7$ and $n_2 \geq 7$

> [!example] Third National Bank Account Balances
> Comparing account balances at two branches:
> - Branch 1: $n_1 = 12$, Branch 2: $n_2 = 10$
> - $W = 169.5$ (sum of ranks for branch 1)
> - $\mu_W = \frac{1}{2}(12)(23) = 138$
> - $\sigma_W = \sqrt{\frac{1}{12}(12)(10)(23)} = 15.1658$
> 
> With continuity correction:
> $$z = \frac{169 - 138}{15.1658} = 2.04$$
> p-value = 2(1 - 0.9793) = 0.0414

---

## 18.4 Kruskal-Wallis Test

The [[Kruskal-Wallis test]] extends the MWW test to **three or more populations**. It is the nonparametric alternative to one-way [[ANOVA]].

### Hypotheses

$$H_0: \text{All populations are identical}$$
$$H_a: \text{Not all populations are identical}$$

If populations have the same shape:
$$H_0: \text{Median}_1 = \text{Median}_2 = \cdots = \text{Median}_k$$
$$H_a: \text{Not all medians are equal}$$

### Test Statistic

> [!formula] Kruskal-Wallis Test Statistic
> $$H = \frac{12}{n_T(n_T + 1)} \sum_{i=1}^{k} \frac{R_i^2}{n_i} - 3(n_T + 1)$$
> 
> Where:
> - $k$ = number of populations
> - $n_i$ = number of observations in sample $i$
> - $n_T = \sum_{i=1}^{k} n_i$ = total observations
> - $R_i$ = sum of ranks for sample $i$

### Sampling Distribution

Under $H_0$, the test statistic $H$ follows a [[chi-square distribution]] with $(k-1)$ degrees of freedom (when all sample sizes ≥ 5).

> [!example] Williams Manufacturing Performance Ratings
> Comparing employees from three colleges:
> - College A: $n_1 = 7$, $R_1 = 95$
> - College B: $n_2 = 6$, $R_2 = 27$
> - College C: $n_3 = 7$, $R_3 = 88$
> - $n_T = 20$
> 
> $$H = \frac{12}{20(21)}\left[\frac{95^2}{7} + \frac{27^2}{6} + \frac{88^2}{7}\right] - 3(21) = 8.92$$
> 
> With $df = 2$, p-value = 0.0116

---

## 18.5 Rank Correlation

The [[Spearman rank-correlation coefficient]] measures association between two variables using ordinal (rank-ordered) data.

> [!formula] Spearman Rank-Correlation Coefficient
> $$r_s = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}$$
> 
> Where:
> - $n$ = number of observations
> - $x_i$ = rank of observation $i$ for first variable
> - $y_i$ = rank of observation $i$ for second variable
> - $d_i = x_i - y_i$

### Interpretation

| $r_s$ Value | Interpretation |
|-------------|----------------|
| Near +1.0 | Strong positive rank correlation |
| Near −1.0 | Strong negative rank correlation |
| Near 0 | No rank correlation |

### Hypothesis Test for Rank Correlation

Testing $H_0: \rho_s = 0$ vs $H_a: \rho_s \neq 0$

> [!formula] Sampling Distribution of $r_s$
> $$\mu_{r_s} = 0$$
> $$\sigma_{r_s} = \frac{1}{\sqrt{n-1}}$$
> 
> Distribution form: Approximately normal for $n \geq 10$

Test statistic:
$$z = \frac{r_s - \mu_{r_s}}{\sigma_{r_s}} = \frac{r_s}{\frac{1}{\sqrt{n-1}}}$$

> [!example] Sales Potential and Performance
> Testing correlation between employment potential ranking and actual sales ranking for 10 salespeople:
> - $\sum d_i^2 = 44$
> - $r_s = 1 - \frac{6(44)}{10(99)} = 0.733$
> - $\sigma_{r_s} = \frac{1}{\sqrt{9}} = 0.333$
> - $z = \frac{0.733}{0.333} = 2.20$
> - p-value = 0.0278

---

## Summary of Methods

| Method | Application | Data Type | Key Assumption |
|--------|-------------|-----------|----------------|
| **Sign Test** | Population median; Matched samples | Categorical/Quantitative | None |
| **Wilcoxon Signed-Rank** | Matched samples; Symmetric population median | Quantitative | Symmetric differences |
| **Mann-Whitney-Wilcoxon** | Two independent samples | Ordinal/Quantitative | None (or same shape for median test) |
| **Kruskal-Wallis** | Three+ independent samples | Ordinal/Quantitative | None (or same shape for median test) |
| **Spearman Correlation** | Association between ranked variables | Ordinal | None |

---

## Key Takeaways

- **Nonparametric methods** are distribution-free and require no assumptions about population distribution shape
- The **sign test** uses the binomial distribution with $p = 0.50$ for testing population medians and matched samples
- The **Wilcoxon signed-rank test** requires symmetric distribution of differences and is more powerful than the sign test when this assumption holds
- The **Mann-Whitney-Wilcoxon test** compares two populations using combined ranking of independent samples; test statistic $W$ is the sum of ranks for sample 1
- The **Kruskal-Wallis test** extends MWW to three or more populations; uses chi-square distribution with $k-1$ degrees of freedom
- **Spearman's rank correlation** ($r_s$) measures monotonic relationships between variables using ranked data
- Normal approximations are used for larger samples (typically $n \geq 7$ to $n \geq 20$ depending on the test)
- Tied observations are assigned **average ranks** in all ranking procedures
- When populations have the same shape, nonparametric tests about "identical populations" become tests about **population medians**