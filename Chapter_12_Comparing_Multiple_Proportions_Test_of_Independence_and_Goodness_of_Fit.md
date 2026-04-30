---
title: Comparing Multiple Proportions, Test of Independence and Goodness of Fit
chapter: 12
tags:
  - statistics
  - chi-square-test
  - proportions
  - test-of-independence
  - goodness-of-fit
  - hypothesis-testing
  - categorical-data
---

# Comparing Multiple Proportions, Test of Independence and Goodness of Fit

This chapter introduces three hypothesis-testing procedures using the [[chi-square distribution]] for categorical data:
1. Testing the equality of [[population proportions]] for three or more populations
2. Testing the [[independence]] of two [[categorical variables]]
3. Testing whether a [[probability distribution]] follows a specific historical or theoretical distribution

## Testing the Equality of Population Proportions for Three or More Populations

### Hypotheses and Framework

For $k \geq 3$ populations with proportions $p_1, p_2, \ldots, p_k$:

$$H_0: p_1 = p_2 = \ldots = p_k$$
$$H_a: \text{Not all population proportions are equal}$$

> [!definition] Expected Frequency
> The expected frequency for a cell in row $i$ and column $j$ under the null hypothesis:
> $$e_{ij} = \frac{(\text{Row } i \text{ Total})(\text{Column } j \text{ Total})}{\text{Total Sample Size}}$$

### Chi-Square Test Statistic

> [!definition] Chi-Square Test Statistic
> $$\chi^2 = \sum_i \sum_j \frac{(f_{ij} - e_{ij})^2}{e_{ij}}$$
> 
> where:
> - $f_{ij}$ = observed frequency for cell $(i,j)$
> - $e_{ij}$ = expected frequency for cell $(i,j)$
> - Degrees of freedom = $k - 1$ (for $k$ populations with two response categories)

### Key Conditions

1. Each expected frequency $e_{ij}$ must be **5 or more**
2. Independent random samples from each population
3. The test is always **upper-tailed** (rejection in the upper tail)

### Multiple Comparison Procedure (Marascuilo Procedure)

When $H_0$ is rejected, use pairwise comparisons to identify which proportions differ.

> [!definition] Marascuilo Critical Value
> For comparing populations $i$ and $j$:
> $$CV_{ij} = \sqrt{\chi^2_\alpha} \sqrt{\frac{\bar{p}_i(1-\bar{p}_i)}{n_i} + \frac{\bar{p}_j(1-\bar{p}_j)}{n_j}}$$
> 
> A significant difference exists if $|\bar{p}_i - \bar{p}_j| > CV_{ij}$

---

## Test of Independence

Tests whether two [[categorical variables]] are independent within a single population.

### Hypotheses

$$H_0: \text{The two categorical variables are independent}$$
$$H_a: \text{The two categorical variables are not independent (associated)}$$

### Procedure

1. **Collect data**: One sample, record two categorical variables per element
2. **Organize**: Create a contingency table with $r$ rows and $c$ columns
3. **Compute expected frequencies**:
   $$e_{ij} = \frac{(\text{Row } i \text{ Total})(\text{Column } j \text{ Total})}{\text{Sample Size}}$$

4. **Calculate test statistic**:
   $$\chi^2 = \sum_i \sum_j \frac{(f_{ij} - e_{ij})^2}{e_{ij}}$$

5. **Degrees of freedom**: $(r-1)(c-1)$

### Decision Rule

- **p-value approach**: Reject $H_0$ if p-value $< \alpha$
- **Critical value approach**: Reject $H_0$ if $\chi^2 > \chi^2_\alpha$

> [!tip] Interpretation After Rejection
> If $H_0$ is rejected, compute conditional probabilities (row or column percentages) to understand the nature of the association between variables.

---

## Goodness of Fit Test

Tests whether a population follows a specific probability distribution.

### Multinomial Probability Distribution

> [!definition] Multinomial Distribution
> A probability distribution where each outcome belongs to one of three or more categories, with probabilities summing to 1. Extends the [[binomial distribution]] to multiple outcomes.

#### Hypotheses

$$H_0: \text{The population follows the specified multinomial distribution}$$
$$H_a: \text{The population does not follow the specified distribution}$$

#### Test Statistic

$$\chi^2 = \sum_{i=1}^{k} \frac{(f_i - e_i)^2}{e_i}$$

where:
- $f_i$ = observed frequency for category $i$
- $e_i$ = expected frequency = $n \cdot p_i$ (sample size × hypothesized probability)
- $k$ = number of categories
- Degrees of freedom = $k - 1$

### Normal Probability Distribution

For testing whether data comes from a [[normal distribution]]:

#### Procedure

1. **Estimate parameters**: Compute sample mean $\bar{x}$ and standard deviation $s$
2. **Create intervals**: Divide the normal distribution into $k$ equal-probability intervals
3. **Determine expected frequencies**: Each interval should have expected frequency ≥ 5
4. **Count observed frequencies** in each interval
5. **Compute test statistic**:
   $$\chi^2 = \sum_{i=1}^{k} \frac{(f_i - e_i)^2}{e_i}$$

> [!important] Degrees of Freedom for Normal Distribution
> When parameters are estimated from sample data:
> $$\text{df} = k - p - 1$$
> where $p$ = number of parameters estimated (for normal: $p = 2$ for mean and standard deviation)

---

## Chi-Square Distribution Properties

The [[chi-square distribution]] characteristics:
- Always positive (right-skewed)
- Shape depends on degrees of freedom
- As df increases, distribution becomes more symmetric
- Test is always **upper-tailed**

| Upper Tail Area | .10 | .05 | .025 | .01 | .005 |
|----------------|-----|-----|------|-----|------|
| df = 1 | 2.706 | 3.841 | 5.024 | 6.635 | 7.879 |
| df = 2 | 4.605 | 5.991 | 7.378 | 9.210 | 10.597 |
| df = 3 | 6.251 | 7.815 | 9.348 | 11.345 | 12.838 |

---

## Key Takeaways

- All three tests use the **chi-square distribution** and require **categorical data**
- Expected frequencies must be **≥ 5** for valid chi-square tests
- Tests are always **upper-tailed**: large $\chi^2$ values lead to rejection of $H_0$
- **Test for equality of proportions**: Compares $k \geq 3$ populations using independent samples
- **Test of independence**: Examines association between two categorical variables in one sample
- **Goodness of fit test**: Determines if data follows a specified probability distribution
- Degrees of freedom vary by application:
  - Equality of $k$ proportions: $k - 1$
  - Independence ($r \times c$ table): $(r-1)(c-1)$
  - Goodness of fit: $k - 1$ (or $k - p - 1$ if $p$ parameters estimated)
- Use **bar charts** and **conditional probabilities** to interpret significant results
- The **Marascuilo procedure** identifies specific pairwise differences after rejecting $H_0$ for multiple proportions