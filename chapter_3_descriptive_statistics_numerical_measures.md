---
title: "Chapter 3: Descriptive Statistics - Numerical Measures"
chapter: 3
tags:
  - statistics
  - descriptive_statistics
  - measures_of_location
  - measures_of_variability
  - correlation
  - covariance
  - outliers
  - box_plots
---

# Descriptive Statistics: Numerical Measures

This chapter introduces numerical measures that summarize data beyond tabular and graphical presentations. These measures describe the **location**, **variability**, **shape**, and **association** within datasets.

When computed from a **sample**, these measures are called [[sample statistics]]. When computed from a **population**, they are called [[population parameters]].

---

## 3.1 Measures of Location

Measures of location provide information about the central tendency of data.

### Mean

The [[mean]] (or average) is the most common measure of central location.

> [!definition] Sample Mean
> $$\bar{x} = \frac{\sum x_i}{n}$$
> where $n$ is the number of observations in the sample.

> [!definition] Population Mean
> $$\mu = \frac{\sum x_i}{N}$$
> where $N$ is the number of observations in the population.

**Key concepts:**
1. The sample mean $\bar{x}$ is a [[point estimator]] of the population mean $\mu$
2. The mean is influenced by extreme values (outliers)
3. Each observation receives equal weight of $1/n$

### Weighted Mean

When observations have different importance levels, use the [[weighted mean]]:

> [!definition] Weighted Mean
> $$\bar{x} = \frac{\sum w_i x_i}{\sum w_i}$$
> where $w_i$ is the weight assigned to observation $i$.

### Median

The [[median]] is the middle value when data are arranged in ascending order.

> [!definition] Median
> - For **odd** $n$: The middle value
> - For **even** $n$: Average of the two middle values

**Key concepts:**
1. Not affected by extreme values
2. Preferred when data are highly skewed
3. Found by trimming pairs from both ends until one or two values remain

### Geometric Mean

The [[geometric mean]] is used for multiplicative processes like growth rates:

> [!definition] Geometric Mean
> $$\bar{x}_g = \sqrt[n]{(x_1)(x_2)\cdots(x_n)} = [(x_1)(x_2)\cdots(x_n)]^{1/n}$$

**Key concepts:**
1. Used for calculating mean growth rates over time
2. Arithmetic mean overstates true growth rates
3. Growth factor = $1 + (\text{rate}/100)$

### Mode

The [[mode]] is the value that occurs with greatest frequency.

**Key concepts:**
1. Data can be **bimodal** (two modes) or **multimodal** (more than two modes)
2. Useful for categorical data

### Percentiles

The $p$th [[percentile]] divides data such that at least $p\%$ are below and $(100-p)\%$ are above.

**Calculating the $p$th percentile:**
1. Arrange data in ascending order
2. Compute index: $i = \frac{p}{100} \cdot n$
3. If $i$ is not an integer, round up to find position
4. If $i$ is an integer, average values at positions $i$ and $i+1$

### Quartiles

[[Quartiles]] divide data into four equal parts:
- $Q_1$ = 25th percentile (first quartile)
- $Q_2$ = 50th percentile (median)
- $Q_3$ = 75th percentile (third quartile)

---

## 3.2 Measures of Variability

Measures of variability describe how spread out the data are.

### Range

> [!definition] Range
> $$\text{Range} = \text{Largest value} - \text{Smallest value}$$

**Limitation:** Highly influenced by extreme values.

### Interquartile Range (IQR)

> [!definition] Interquartile Range
> $$\text{IQR} = Q_3 - Q_1$$

The IQR represents the middle 50% of the data and is not affected by extreme values.

### Variance

The [[variance]] measures variability based on squared deviations from the mean.

> [!definition] Population Variance
> $$\sigma^2 = \frac{\sum(x_i - \mu)^2}{N}$$

> [!definition] Sample Variance
> $$s^2 = \frac{\sum(x_i - \bar{x})^2}{n-1}$$

**Note:** The sample variance uses $n-1$ (degrees of freedom) to provide an unbiased estimate of population variance.

### Standard Deviation

The [[standard deviation]] is the positive square root of the variance.

> [!definition] Standard Deviation
> $$s = \sqrt{s^2} \quad \text{(sample)}$$
> $$\sigma = \sqrt{\sigma^2} \quad \text{(population)}$$

**Key advantage:** Measured in the same units as the original data.

### Coefficient of Variation

The [[coefficient of variation]] measures relative variability:

> [!definition] Coefficient of Variation
> $$CV = \left(\frac{\text{Standard deviation}}{\text{Mean}}\right) \times 100\%$$

Useful for comparing variability across datasets with different means or units.

---

## 3.3 Measures of Distribution Shape, Relative Location, and Detecting Outliers

### Distribution Shape (Skewness)

[[Skewness]] measures the asymmetry of a distribution:
- **Negative skewness**: Skewed left (tail extends left)
- **Zero skewness**: Symmetric
- **Positive skewness**: Skewed right (tail extends right)

For symmetric distributions, $\text{mean} = \text{median}$.

### z-Scores

A [[z-score]] (standardized value) indicates how many standard deviations an observation is from the mean:

> [!definition] z-Score
> $$z_i = \frac{x_i - \bar{x}}{s}$$

**Interpretation:**
- $z > 0$: Value is above the mean
- $z < 0$: Value is below the mean
- $z = 0$: Value equals the mean

### Chebyshev's Theorem

[[Chebyshev's theorem]] applies to **any** distribution:

> [!definition] Chebyshev's Theorem
> At least $(1 - 1/z^2)$ of the data values lie within $z$ standard deviations of the mean, for $z > 1$.

| $z$ | Minimum % within |
|-----|------------------|
| 2 | 75% |
| 3 | 89% |
| 4 | 94% |

### Empirical Rule

The [[empirical rule]] applies only to **bell-shaped (normal) distributions**:

> [!definition] Empirical Rule
> - Approximately **68%** within 1 standard deviation
> - Approximately **95%** within 2 standard deviations
> - Approximately **99.7%** within 3 standard deviations

### Detecting Outliers

[[Outliers]] are unusually small or large values.

**Method 1: z-scores**
- Values with $|z| > 3$ are potential outliers

**Method 2: IQR method**
- Lower limit: $Q_1 - 1.5(\text{IQR})$
- Upper limit: $Q_3 + 1.5(\text{IQR})$
- Values outside these limits are outliers

---

## 3.4 Five-Number Summaries and Box Plots

### Five-Number Summary

The [[five-number summary]] consists of:
1. Smallest value
2. First quartile ($Q_1$)
3. Median ($Q_2$)
4. Third quartile ($Q_3$)
5. Largest value

### Box Plot

A [[box plot]] graphically displays the five-number summary:

**Construction:**
1. Draw a box from $Q_1$ to $Q_3$
2. Draw a vertical line at the median
3. Calculate limits: $Q_1 - 1.5(\text{IQR})$ and $Q_3 + 1.5(\text{IQR})$
4. Draw whiskers to smallest/largest values within limits
5. Mark outliers with symbols (e.g., *)

---

## 3.5 Measures of Association Between Two Variables

### Covariance

[[Covariance]] measures the linear association between two variables.

> [!definition] Sample Covariance
> $$s_{xy} = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{n-1}$$

> [!definition] Population Covariance
> $$\sigma_{xy} = \frac{\sum(x_i - \mu_x)(y_i - \mu_y)}{N}$$

**Interpretation:**
- $s_{xy} > 0$: Positive linear relationship
- $s_{xy} < 0$: Negative linear relationship
- $s_{xy} \approx 0$: No linear relationship

**Limitation:** Value depends on units of measurement.

### Correlation Coefficient

The [[correlation coefficient]] standardizes covariance to a scale of -1 to +1:

> [!definition] Sample Correlation Coefficient (Pearson)
> $$r_{xy} = \frac{s_{xy}}{s_x \cdot s_y}$$

> [!definition] Population Correlation Coefficient
> $$\rho_{xy} = \frac{\sigma_{xy}}{\sigma_x \cdot \sigma_y}$$

**Interpretation:**
| Value | Interpretation |
|-------|----------------|
| $r = +1$ | Perfect positive linear relationship |
| $r = -1$ | Perfect negative linear relationship |
| $r = 0$ | No linear relationship |
| $r$ close to $\pm 1$ | Strong linear relationship |

**Important:** Correlation measures linear association only and does not imply causation.

---

## 3.6 Data Dashboards: Adding Numerical Measures

[[Data dashboards]] can be enhanced by adding:
- Summary statistics (mean, median, standard deviation)
- Benchmarks and target values
- Box plots for comparison
- Time-series displays of individual observations

Numerical measures provide:
1. Performance benchmarks
2. Context for graphical displays
3. Basis for identifying problems (e.g., outliers, trends)

---

## Key Takeaways

- The **mean** is the most common measure of central location but is sensitive to outliers; the **median** is preferred for skewed data
- The **geometric mean** should be used for growth rates and multiplicative processes
- **Variance** and **standard deviation** measure data dispersion; standard deviation is in original units
- **z-scores** standardize data and help identify outliers (typically $|z| > 3$)
- **Chebyshev's theorem** applies to any distribution; the **empirical rule** applies only to bell-shaped distributions
- **Box plots** provide visual summaries of location, spread, and outliers
- **Covariance** measures direction of linear association; **correlation** measures both direction and strength on a standardized scale
- Correlation does not imply causation
- Sample statistics ($\bar{x}$, $s^2$, $s$) are point estimators of population parameters ($\mu$, $\sigma^2$, $\sigma$)