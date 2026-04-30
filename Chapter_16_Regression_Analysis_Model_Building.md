---
title: "Chapter 16: Regression Analysis - Model Building"
chapter: 16
tags:
  - statistics
  - regression-analysis
  - model-building
  - curvilinear-relationships
  - interaction-effects
  - variable-selection
  - autocorrelation
  - durbin-watson-test
  - stepwise-regression
  - experimental-design
---

# Chapter 16: Regression Analysis - Model Building

**Model building** is the process of developing an [[estimated regression equation]] that describes the relationship between a [[dependent variable]] and one or more [[independent variables]]. The major issues involve finding the proper **functional form** of the relationship and **selecting the independent variables** to be included in the model.

---

## 16.1 General Linear Model

The [[general linear model]] provides a flexible framework for developing complex relationships among variables.

> [!definition] General Linear Model
> A model of the form:
> $$y = \beta_0 + \beta_1 z_1 + \beta_2 z_2 + \ldots + \beta_p z_p + \varepsilon$$
> where each independent variable $z_j$ (for $j = 1, 2, \ldots, p$) is a function of $x_1, x_2, \ldots, x_k$ (the variables for which data are collected).

The term "linear" refers to the fact that $\beta_0, \beta_1, \ldots, \beta_p$ all have exponents of 1; it does **not** imply that the relationship between $y$ and the $x_i$'s is linear.

### Modeling Curvilinear Relationships

When a [[scatter diagram]] suggests a curvilinear pattern, we can use polynomial terms to capture the curvature.

**Simple First-Order Model (One Predictor Variable):**
$$y = \beta_0 + \beta_1 x_1 + \varepsilon$$

**Second-Order Model (One Predictor Variable):**
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_1^2 + \varepsilon$$

This model accounts for curvature by including the squared term $x_1^2$.

> [!example] Reynolds, Inc. Example
> A manufacturer investigated the relationship between months employed ($x$) and sales ($y$). The second-order estimated regression equation:
> $$\hat{y} = 45.3 + 6.34x - 0.0345x^2$$
> provided a better fit ($R^2_{adj} = 88.6\%$) than the simple linear model ($R^2_{adj} = 76.4\%$).

### Interaction

> [!definition] Interaction
> The effect of two independent variables acting together. When interaction is present, the effect of one variable on the response depends on the value of another variable.

**Second-Order Model with Two Predictor Variables:**
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_1^2 + \beta_4 x_2^2 + \beta_5 x_1 x_2 + \varepsilon$$

The term $x_1 x_2$ accounts for interaction effects.

**Model with Interaction Term Only:**
$$y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_1 x_2 + \varepsilon$$

When interaction is present, meaningful conclusions require considering the **joint effect** of both variables.

### Transformations Involving the Dependent Variable

When problems such as **nonconstant variance** are detected in residual plots (e.g., a wedge-shaped pattern), transforming the dependent variable can help.

**Common Transformations:**

1. **Logarithmic Transformation:** Use $\ln(y)$ or $\log(y)$ as the dependent variable
   - Compresses values and diminishes effects of nonconstant variance
   - To predict original $y$: compute $\hat{y}' = b_0 + b_1 x$, then $\hat{y} = e^{\hat{y}'}$

2. **Reciprocal Transformation:** Use $1/y$ as the dependent variable

### Nonlinear Models That Are Intrinsically Linear

**Exponential Model:**
$$E(y) = \beta_0 \beta_1^x$$

This is appropriate when $y$ increases or decreases by a **constant percentage** as $x$ increases.

**Linearization through logarithms:**
$$\log E(y) = \log \beta_0 + x \log \beta_1$$

Letting $y' = \log E(y)$, $\beta_0' = \log \beta_0$, and $\beta_1' = \log \beta_1$:
$$y' = \beta_0' + \beta_1' x$$

---

## 16.2 Determining When to Add or Delete Variables

An [[F-test]] determines whether adding or deleting variables significantly improves the model.

### F Test for Adding One Variable

To test whether adding $x_2$ to a model containing only $x_1$ is significant:

$$F = \frac{SSE(x_1) - SSE(x_1, x_2)}{1} \div \frac{SSE(x_1, x_2)}{n - p - 1}$$

**Decision Rule:** Reject $H_0$ if $F > F_\alpha$ (with 1 numerator and $n - p - 1$ denominator degrees of freedom).

### General Case: Adding Multiple Variables

To test whether adding variables $x_{q+1}, x_{q+2}, \ldots, x_p$ to a model with $x_1, x_2, \ldots, x_q$:

**Hypotheses:**
- $H_0: \beta_{q+1} = \beta_{q+2} = \ldots = \beta_p = 0$
- $H_a:$ One or more parameters $\neq 0$

**F Statistic:**
$$F = \frac{[SSE(\text{reduced}) - SSE(\text{full})] / (\text{number of extra terms})}{MSE(\text{full})}$$

Or equivalently:
$$F = \frac{[SSR(\text{full}) - SSR(\text{reduced})] / (\text{number of extra terms})}{MSE(\text{full})}$$

**Degrees of freedom:** $p - q$ numerator, $n - p - 1$ denominator

### Use of p-Values

The [[p-value]] criterion provides the same conclusion:
- If p-value $\leq \alpha$: the additional variables are statistically significant
- If p-value $> \alpha$: the additional variables are not significant

---

## 16.3 Analysis of a Larger Problem

For problems with many potential independent variables, systematic approaches are needed to identify the best subset of variables.

### Key Considerations

1. **Correlation Matrix Analysis:**
   - High correlations between $y$ and independent variables suggest good predictors
   - High correlations between independent variables indicate potential [[multicollinearity]]
   - Rule of thumb: multicollinearity may be a problem if $|r| > 0.7$ between independent variables

2. **Adjusted R-Squared ($R^2_{adj}$):**
   - Accounts for the number of predictors in the model
   - Better for comparing models with different numbers of variables

---

## 16.4 Variable Selection Procedures

### Key Concepts

1. **Alpha to enter:** Significance level for adding a variable
2. **Alpha to remove:** Significance level for removing a variable
3. These procedures are **heuristics**—they find good models but don't guarantee the best model

### Stepwise Regression

An iterative procedure that can both add and remove variables.

**Algorithm:**
1. Start with no variables (or a specified set)
2. At each step:
   - Check if any variable should be **removed** (p-value > Alpha to remove)
   - If no removal, check if any variable should be **entered** (p-value ≤ Alpha to enter)
3. Continue until no variables can be added or removed

**Key Property:** Variables can enter, leave, and re-enter the model.

### Forward Selection

**Algorithm:**
1. Start with no independent variables
2. Add variables one at a time (smallest p-value ≤ Alpha to enter)
3. Once entered, a variable **cannot be removed**
4. Stop when no variable can be added

### Backward Elimination

**Algorithm:**
1. Start with **all** independent variables
2. Remove variables one at a time (largest p-value > Alpha to remove)
3. Once removed, a variable **cannot re-enter**
4. Stop when no variable can be removed

> [!warning] Important
> Forward selection and backward elimination may lead to **different models**. Analyst judgment is required for final model selection.

### Best-Subsets Regression

Evaluates all possible regression models and identifies the best models for each number of predictors.

**Criterion:** Coefficient of determination ($R^2$)

**Output:** For each number of predictors $k$, shows the best models ranked by $R^2$.

**Advantage:** Guaranteed to find the best model for any given number of variables.

### Making the Final Choice

1. Review adjusted $R^2$ values across competing models
2. Perform residual analysis on candidate models
3. Consider parsimony: simpler models with fewer variables are often preferred
4. Apply subject matter expertise and practical considerations

---

## 16.5 Multiple Regression Approach to Experimental Design

[[Dummy variables]] enable the use of multiple regression for [[analysis of variance]] problems.

### Completely Randomized Design

For $k$ treatments, define $k - 1$ dummy variables.

**Example:** Three treatments (A, B, C)
- $A = 1$ if observation uses method A, 0 otherwise
- $B = 1$ if observation uses method B, 0 otherwise

**Model:**
$$E(y) = \beta_0 + \beta_1 A + \beta_2 B$$

**Interpretation:**
- $\beta_0$ = mean for treatment C
- $\beta_0 + \beta_1$ = mean for treatment A
- $\beta_0 + \beta_2$ = mean for treatment B

**Testing for Differences:**

$H_0: \beta_1 = \beta_2 = 0$ (means are equal)

Use the F test for overall significance of the regression.

---

## 16.6 Autocorrelation and the Durbin-Watson Test

> [!definition] Autocorrelation (Serial Correlation)
> Correlation in the error terms that arises when error terms at successive points in time are related. First-order autocorrelation occurs when $\varepsilon_t$ is related to $\varepsilon_{t-1}$.

**First-Order Autocorrelation Model:**
$$\varepsilon_t = \rho \varepsilon_{t-1} + z_t$$

where:
- $|\rho| < 1$
- $z_t$ is normally and independently distributed with mean 0 and variance $\sigma^2$
- $\rho > 0$: positive autocorrelation
- $\rho < 0$: negative autocorrelation
- $\rho = 0$: no autocorrelation

### Durbin-Watson Test Statistic

$$d = \frac{\sum_{t=2}^{n}(e_t - e_{t-1})^2}{\sum_{t=1}^{n}e_t^2}$$

**Properties:**
- Range: $0 \leq d \leq 4$
- $d \approx 2$: no autocorrelation
- $d$ small: positive autocorrelation
- $d$ large: negative autocorrelation

### Testing for Autocorrelation

Using critical values $d_L$ (lower) and $d_U$ (upper) from tables:

**Test for Positive Autocorrelation** ($H_a: \rho > 0$):
- $d < d_L$: positive autocorrelation present
- $d_L \leq d \leq d_U$: inconclusive
- $d > d_U$: no evidence of positive autocorrelation

**Test for Negative Autocorrelation** ($H_a: \rho < 0$):
- $d > 4 - d_L$: negative autocorrelation present
- $4 - d_U \leq d \leq 4 - d_L$: inconclusive
- $d < 4 - d_U$: no evidence of negative autocorrelation

**Two-Sided Test** ($H_a: \rho \neq 0$):
- $d < d_L$ or $d > 4 - d_L$: autocorrelation present
- $d_U < d < 4 - d_U$: no evidence of autocorrelation

### Correcting for Autocorrelation

1. Include omitted time-ordered independent variables
2. Add a time variable (1 for first observation, 2 for second, etc.)
3. Apply transformations to dependent or independent variables

---

## Key Takeaways

- The **general linear model** framework enables modeling of curvilinear relationships and interaction effects using transformations of the original variables
- **Second-order models** include squared terms to capture curvature; **interaction terms** capture joint effects of variables
- **Transformations** of the dependent variable (logarithmic, reciprocal) can address violations of regression assumptions like nonconstant variance
- The **F test** provides a formal procedure for determining whether adding or removing variables significantly improves model fit
- **Variable selection procedures** (stepwise, forward, backward, best-subsets) help identify good models but require analyst judgment for final selection
- **Multiple regression** provides an alternative approach to **experimental design** problems using dummy variables
- The **Durbin-Watson test** detects **autocorrelation** in time-ordered data; $d \approx 2$ indicates no autocorrelation
- **Adjusted R-squared** ($R^2_{adj}$) is preferred over $R^2$ when comparing models with different numbers of predictors
- **Multicollinearity** can be identified through correlation matrices and should be considered when building models