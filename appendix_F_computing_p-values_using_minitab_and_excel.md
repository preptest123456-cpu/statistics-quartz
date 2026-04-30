---
title: Computing p-Values Using Minitab and Excel
chapter: Appendix F
tags:
  - statistics
  - p-values
  - hypothesis-testing
  - Minitab
  - Excel
  - z-test
  - t-test
  - chi-square-test
  - F-test
---

# Computing p-Values Using Minitab and Excel

This appendix describes how [[Minitab]] and [[Excel]] can be used to compute [[p-value|p-values]] for the [[z-statistic]], [[t-statistic]], [[chi-square statistic|χ² statistic]], and [[F-statistic]] used in [[hypothesis testing]]. While statistical tables provide only approximate p-values for t, χ², and F statistics, computer software enables computation of exact p-values.

## Overview of p-Value Computation

> [!definition] Cumulative Probability Approach
> Both Minitab and Excel compute p-values by first determining the **cumulative probability** (area under the curve to the left of the test statistic), then converting this to the appropriate tail p-value based on the type of test.

### Key Formulas for Converting Cumulative Probability

1. **Lower tail p-value**: Equals the cumulative probability directly
2. **Upper tail p-value**: $p\text{-value} = 1 - \text{cumulative probability}$
3. **Two-tailed p-value**: $p\text{-value} = 2 \times \min(\text{lower tail}, \text{upper tail})$

## Using Minitab

Minitab provides cumulative probabilities for all four test statistics through the **Calc > Probability Distributions** menu.

### The z Test Statistic

**Example**: Hilltop Coffee lower tail test with $z = -2.67$

**Steps**:
1. Select the **Calc** menu
2. Choose **Probability Distributions**
3. Choose **Normal**
4. In the Normal Distribution dialog box:
   - Select **Cumulative probability**
   - Enter **0** in the Mean box
   - Enter **1** in the Standard deviation box
   - Select **Input Constant**
   - Enter **-2.67** in the Input Constant box
   - Click **OK**

**Result**: Cumulative probability = 0.0038 (this is the lower tail p-value)

> [!example] p-Value Calculations for z = -2.67
> - Lower tail: $p = 0.0038$
> - Upper tail: $p = 1 - 0.0038 = 0.9962$
> - Two-tailed: $p = 2(0.0038) = 0.0076$

### The t Test Statistic

**Example**: Heathrow Airport upper tail test with $t = 1.84$, $df = 59$

**Steps**:
1. Select the **Calc** menu
2. Choose **Probability Distributions**
3. Choose **t**
4. In the t Distribution dialog box:
   - Select **Cumulative probability**
   - Enter **59** in the Degrees of freedom box
   - Select **Input Constant**
   - Enter **1.84** in the Input Constant box
   - Click **OK**

**Result**: Cumulative probability = 0.9646

> [!example] p-Value Calculations for t = 1.84, df = 59
> - Lower tail: $p = 0.9646$
> - Upper tail: $p = 1 - 0.9646 = 0.0354$
> - Two-tailed: $p = 2(0.0354) = 0.0708$

### The χ² Test Statistic

**Example**: St. Louis Metro Bus upper tail test with $\chi^2 = 28.18$, $df = 23$

**Steps**:
1. Select the **Calc** menu
2. Choose **Probability Distributions**
3. Choose **Chi-Square**
4. In the Chi-Square Distribution dialog box:
   - Select **Cumulative probability**
   - Enter **23** in the Degrees of freedom box
   - Select **Input Constant**
   - Enter **28.18** in the Input Constant box
   - Click **OK**

**Result**: Cumulative probability = 0.7909

> [!example] p-Value Calculations for χ² = 28.18, df = 23
> - Lower tail: $p = 0.7909$
> - Upper tail: $p = 1 - 0.7909 = 0.2091$
> - Two-tailed: $p = 2(0.2091) = 0.4182$

### The F Test Statistic

**Example**: Dullus County Schools two-tailed test with $F = 2.40$, $df_1 = 25$, $df_2 = 15$

**Steps**:
1. Select the **Calc** menu
2. Choose **Probability Distributions**
3. Choose **F**
4. In the F Distribution dialog box:
   - Select **Cumulative probability**
   - Enter **25** in the Numerator degrees of freedom box
   - Enter **15** in the Denominator degrees of freedom box
   - Select **Input Constant**
   - Enter **2.40** in the Input Constant box
   - Click **OK**

**Result**: Cumulative probability = 0.9594

> [!example] p-Value Calculations for F = 2.40, df₁ = 25, df₂ = 15
> - Lower tail: $p = 0.9594$
> - Upper tail: $p = 1 - 0.9594 = 0.0406$
> - Two-tailed: $p = 2(0.0406) = 0.0812$

## Using Excel

Excel provides a **p-Value template** that automatically computes p-values for all test types once the test statistic and degrees of freedom are entered.

### Template Layout

| Test Statistic | Input Cell(s) | Output Cells |
|----------------|---------------|--------------|
| z statistic | B6 | B9 (lower), B10 (upper), B11 (two-tailed) |
| t statistic | E6 (value), E7 (df) | E9 (lower), E10 (upper), E11 (two-tailed) |
| χ² statistic | B18 (value), B19 (df) | B21 (lower), B23 (upper), B24 (two-tailed) |
| F statistic | E18 (value), E19 (df₁), E20 (df₂) | E22 (lower), E23 (upper), E24 (two-tailed) |

### Example Inputs and Results

| Test | Input Values | Selected p-Value |
|------|--------------|------------------|
| z (lower tail) | z = -2.67 | 0.0038 |
| t (upper tail) | t = 1.84, df = 59 | 0.0354 |
| χ² (upper tail) | χ² = 28.18, df = 23 | 0.2091 |
| F (two-tailed) | F = 2.40, df₁ = 25, df₂ = 15 | 0.0812 |

> [!tip] Viewing Excel Formulas
> To see the underlying Excel functions used in the template, click on the appropriate cell to view the formula in the formula bar.

## Summary of Minitab Menu Paths

| Distribution | Menu Path |
|--------------|-----------|
| [[Normal distribution]] (z) | Calc → Probability Distributions → Normal |
| [[t-distribution]] | Calc → Probability Distributions → t |
| [[Chi-square distribution]] | Calc → Probability Distributions → Chi-Square |
| [[F-distribution]] | Calc → Probability Distributions → F |

## Key Takeaways

- **Cumulative probability** is the foundation for computing all p-values in both Minitab and Excel
- **Lower tail p-value** equals the cumulative probability directly
- **Upper tail p-value** is calculated as $1 - \text{cumulative probability}$
- **Two-tailed p-value** is $2 \times \min(\text{lower tail p-value}, \text{upper tail p-value})$
- Minitab requires navigating through menus for each distribution type
- Excel templates automate p-value computation for all three test types simultaneously
- Computer software provides **exact p-values**, unlike statistical tables which give only approximate values
- The [[degrees of freedom]] must be specified for t, χ², and F distributions (F requires both numerator and denominator df)