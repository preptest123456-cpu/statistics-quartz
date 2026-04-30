---
title: "Chapter 2: Descriptive Statistics – Tabular and Graphical Displays"
chapter: 2
tags:
  - statistics
  - descriptive-statistics
  - frequency-distribution
  - histogram
  - crosstabulation
  - data-visualization
  - scatter-diagram
  - bar-chart
  - pie-chart
---

# Chapter 2: Descriptive Statistics – Tabular and Graphical Displays

## Overview

This chapter introduces **tabular and graphical methods** for summarizing data so that patterns are revealed and data are more easily interpreted. The goal of [[descriptive statistics]] is to present data in a form that facilitates understanding and supports decision-making.

> [!definition] Data Visualization
> A term used to describe the use of graphical displays to summarize and present information about a data set.

---

## 2.1 Summarizing Data for a Categorical Variable

### Frequency Distribution

> [!definition] Frequency Distribution
> A tabular summary of data showing the number (frequency) of observations in each of several nonoverlapping categories or classes.

**Example:** For soft drink purchases (Coca-Cola, Diet Coke, Dr. Pepper, Pepsi, Sprite), counting occurrences yields:

| Soft Drink  | Frequency |
| ----------- | --------- |
| Coca-Cola   | 19        |
| Diet Coke   | 8         |
| Dr. Pepper  | 5         |
| Pepsi       | 13        |
| Sprite      | 5         |
| **Total**   | 50        |

### Relative Frequency and Percent Frequency Distributions

The [[relative frequency]] of a class equals the fraction of observations belonging to that class:

$$
\text{Relative frequency of a class} = \frac{\text{Frequency of the class}}{n}
$$

The [[percent frequency]] is the relative frequency multiplied by 100.

| Soft Drink | Relative Frequency | Percent Frequency |
| ---------- | ------------------ | ----------------- |
| Coca-Cola  | 0.38               | 38                |
| Diet Coke  | 0.16               | 16                |
| Dr. Pepper | 0.10               | 10                |
| Pepsi      | 0.26               | 26                |
| Sprite     | 0.10               | 10                |
| **Total**  | 1.00               | 100               |

### Bar Charts and Pie Charts

> [!definition] Bar Chart
> A graphical device for depicting categorical data summarized in a frequency, relative frequency, or percent frequency distribution. Bars are separated to emphasize distinct categories.

> [!definition] Pie Chart
> A graphical device that subdivides a circle into sectors proportional to the relative frequency of each class.

For a pie chart, the angle for each sector is calculated as:
$$
\text{Degrees} = \text{Relative frequency} \times 360
$$

**Best Practice:** Pie charts are less effective than bar charts for comparing categories because people judge lengths more accurately than angles.

---

## 2.2 Summarizing Data for a Quantitative Variable

### Frequency Distribution for Quantitative Data

Three steps to construct a frequency distribution:

1. **Determine the number of classes** (typically 5–20)
2. **Determine the class width**
3. **Determine the class limits**

**Approximate class width:**
$$
\text{Approximate class width} = \frac{\text{Largest data value} - \text{Smallest data value}}{\text{Number of classes}}
$$

> [!definition] Class Midpoint
> The value halfway between the lower and upper class limits of a class.

**Example:** Audit time data with 5 classes of width 5 days:

| Audit Time (days) | Frequency |
| ----------------- | --------- |
| 10–14             | 4         |
| 15–19             | 8         |
| 20–24             | 5         |
| 25–29             | 2         |
| 30–34             | 1         |
| **Total**         | 20        |

### Dot Plot

> [!definition] Dot Plot
> A graphical display where each data value is represented by a dot placed above a horizontal axis showing the range of the data.

Dot plots are useful for small data sets and for comparing distributions of two or more variables.

### Histogram

> [!definition] Histogram
> A graphical display of a frequency distribution where class intervals are placed on the horizontal axis and frequencies on the vertical axis. Adjacent rectangles touch one another.

**Shapes of distributions:**
- **Skewed left:** Tail extends farther to the left
- **Skewed right:** Tail extends farther to the right
- **Symmetric:** Left tail mirrors the right tail

### Cumulative Distributions

> [!definition] Cumulative Frequency Distribution
> A tabular summary showing the number of data values that are less than or equal to the upper class limit of each class.

**Cumulative relative frequency** = Cumulative frequency / n

**Cumulative percent frequency** = Cumulative relative frequency × 100

### Stem-and-Leaf Display

> [!definition] Stem-and-Leaf Display
> A graphical display that shows both the rank order and shape of a distribution. Leading digits form the stem; trailing digits form the leaves.

**Advantages over histograms:**
1. Easier to construct by hand
2. Shows actual data values within each class

**Stretched stem-and-leaf:** Uses two lines per stem value (0–4 and 5–9) for more detail.

---

## 2.3 Summarizing Data for Two Variables Using Tables

### Crosstabulation

> [!definition] Crosstabulation
> A tabular summary of data for two variables where classes for one variable are represented by rows and classes for the other variable by columns.

**Example:** Quality rating vs. meal price for 300 restaurants:

| Quality Rating | $10–19 | $20–29 | $30–39 | $40–49 | Total |
| -------------- | ------ | ------ | ------ | ------ | ----- |
| Good           | 42     | 40     | 2      | 0      | 84    |
| Very Good      | 34     | 64     | 46     | 6      | 150   |
| Excellent      | 2      | 14     | 28     | 22     | 66    |
| **Total**      | 78     | 118    | 76     | 28     | 300   |

**Row percentages** and **column percentages** can reveal relationships between variables.

### Simpson's Paradox

> [!definition] Simpson's Paradox
> A phenomenon where conclusions drawn from aggregated data are reversed when the data are disaggregated into subgroups.

**Key insight:** When analyzing crosstabulations, be aware that a hidden variable could affect results. Always investigate whether aggregated or disaggregated data provides better insight.

---

## 2.4 Summarizing Data for Two Variables Using Graphical Displays

### Scatter Diagram and Trendline

> [!definition] Scatter Diagram
> A graphical display showing the relationship between two quantitative variables, with one variable on the horizontal axis and the other on the vertical axis.

> [!definition] Trendline
> A line that provides an approximation of the relationship between two variables in a scatter diagram.

**Types of relationships:**
- **Positive relationship:** As x increases, y tends to increase
- **Negative relationship:** As x increases, y tends to decrease
- **No apparent relationship:** No discernible pattern

### Side-by-Side and Stacked Bar Charts

> [!definition] Side-by-Side Bar Chart
> A graphical display depicting multiple bar charts on the same display for comparing two variables.

> [!definition] Stacked Bar Chart
> A bar chart where each bar is divided into rectangular segments showing the relative frequency of each class.

---

## 2.5 Data Visualization: Best Practices

### Creating Effective Graphical Displays

**Guidelines:**
- Give the display a clear and concise title
- Keep the display simple (avoid unnecessary 3D effects)
- Clearly label each axis with units of measure
- Use distinct colors to distinguish categories
- Place legends close to the data representation

### Choosing the Type of Graphical Display

**Displays for showing distribution:**
- [[Bar Chart]] – categorical data
- [[Pie Chart]] – relative/percent frequency for categorical data
- [[Dot Plot]] – quantitative data over entire range
- [[Histogram]] – frequency distribution for quantitative data
- [[Stem-and-Leaf Display]] – rank order and shape for quantitative data

**Displays for comparisons:**
- [[Side-by-Side Bar Chart]] – compare two variables
- [[Stacked Bar Chart]] – compare relative frequencies of categorical variables

**Displays for relationships:**
- [[Scatter Diagram]] – relationship between two quantitative variables
- [[Trendline]] – approximate relationship in scatter diagram

### Data Dashboards

> [!definition] Data Dashboard
> A set of visual displays that organizes and presents information used to monitor the performance of a company or organization in a manner that is easy to read, understand, and interpret.

**Key Performance Indicators (KPIs):** Metrics that need to be monitored to assess company performance (e.g., inventory levels, daily sales, on-time delivery rates).

**Dashboard best practices:**
- Minimize need for screen scrolling
- Avoid unnecessary use of color or 3D displays
- Use borders between charts to improve readability
- Simpler is almost always better

---

## Key Formulas

| Formula | Expression |
|---------|------------|
| Relative Frequency | $\displaystyle \frac{\text{Frequency of the class}}{n}$ |
| Approximate Class Width | $\displaystyle \frac{\text{Largest value} - \text{Smallest value}}{\text{Number of classes}}$ |
| Pie Chart Sector Angle | $\text{Relative frequency} \times 360°$ |

---

## Key Takeaways

- **Frequency distributions** summarize data by counting observations in nonoverlapping classes
- **Relative and percent frequency distributions** express frequencies as proportions or percentages
- **Bar charts** are preferred over pie charts for comparing categories
- **Histograms** reveal the shape of quantitative data distributions (symmetric, skewed left, skewed right)
- **Cumulative distributions** show the count/proportion of values up to each class limit
- **Stem-and-leaf displays** preserve actual data values while showing distribution shape
- **Crosstabulations** reveal relationships between two variables
- **Simpson's paradox** warns that aggregated data may lead to opposite conclusions from disaggregated data
- **Scatter diagrams** with trendlines visualize relationships between quantitative variables
- **Data dashboards** consolidate multiple KPIs for effective organizational monitoring
- Effective visualizations are simple, clearly labeled, and appropriate for the data type and purpose