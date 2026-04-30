---
title: Data and Statistics
chapter: 1
tags:
  - statistics
  - data_types
  - measurement_scales
  - descriptive_statistics
  - statistical_inference
  - data_sources
  - data_mining
  - ethics
---

# Chapter 1: Data and Statistics

## 1.1 Applications in Business and Economics

Statistics is the art and science of **collecting, analyzing, presenting, and interpreting data**. It provides managers and decision makers with information to understand the business environment and make informed decisions.

### Business Applications by Field

1. **Accounting** - Statistical sampling procedures for audits; selecting a [[sample]] to validate accounts receivable
2. **Finance** - Analyzing financial data (price/earnings ratios, dividend yields) to guide investment recommendations
3. **Marketing** - Point-of-sale scanner data analysis; understanding relationships between promotional activities and sales
4. **Production** - [[Statistical Quality Control|Quality control charts]] (e.g., $\bar{x}$-charts) to monitor production processes
5. **Economics** - Forecasting inflation rates using indicators like Producer Price Index and unemployment rates
6. **Information Systems** - Performance assessment of computer networks using statistics on users, downtime, and bandwidth utilization

---

## 1.2 Data

> [!definition] Data
> **Data** are the facts and figures collected, analyzed, and summarized for presentation and interpretation. All data collected in a particular study form the **data set**.

### Elements, Variables, and Observations

| Term | Definition |
|------|------------|
| **[[Element]]** | Entity on which data are collected |
| **[[Variable]]** | Characteristic of interest for the elements |
| **[[Observation]]** | Set of measurements obtained for a particular element |

> [!example]
> In a data set of 60 nations: each nation is an **element**, characteristics like Per Capita GDP are **variables**, and all measurements for Armenia constitute one **observation**.

### Scales of Measurement

1. **[[Nominal Scale]]** - Labels or names identify attributes; no meaningful order
   - *Example:* WTO Status (Member/Observer)
   
2. **[[Ordinal Scale]]** - Data can be ranked or ordered; differences not meaningful
   - *Example:* Credit ratings (AAA, AA, A, BBB, etc.)
   
3. **[[Interval Scale]]** - Ordered data with meaningful differences; no true zero
   - *Example:* SAT scores (difference of 70 points is meaningful)
   
4. **[[Ratio Scale]]** - All properties of interval scale plus meaningful ratios; true zero exists
   - *Example:* Price, distance, weight, time

### Categorical and Quantitative Data

> [!definition] Categorical Data
> Labels or names used to identify an attribute of each element. Uses **nominal** or **ordinal** scale.

> [!definition] Quantitative Data
> Numeric values indicating how much or how many. Uses **interval** or **ratio** scale.

**Key distinction:** Arithmetic operations (addition, subtraction, multiplication, division) provide meaningful results only for [[quantitative data]].

| Data Type | Quantitative Subtype | Description |
|-----------|---------------------|-------------|
| Quantitative | **Discrete** | Counts (how many) |
| Quantitative | **Continuous** | Measurements (how much) |

### Cross-Sectional and Time Series Data

- **[[Cross-Sectional Data]]** - Data collected at the same or approximately the same point in time
- **[[Time Series Data]]** - Data collected over several time periods

---

## 1.3 Data Sources

### Existing Sources

| Source Type | Examples |
|-------------|----------|
| **Internal company records** | Employee records, production data, sales records, customer profiles |
| **External data providers** | Dun & Bradstreet, Bloomberg, ACNielsen |
| **Industry associations** | Travel Industry Association, Graduate Management Admission Council |
| **Government agencies** | Census Bureau, Bureau of Labor Statistics, Federal Reserve Board |
| **Internet** | Company websites, online databases |

### Statistical Studies

1. **[[Experimental Study]]** - Variables are controlled to measure effects on a variable of interest
   - *Example:* Testing how drug dosage affects blood pressure
   
2. **[[Observational Study]]** - No attempt to control variables; data collected through observation or surveys
   - *Example:* Customer satisfaction surveys

### Data Acquisition Errors

> [!warning] Data Acquisition Errors
> Errors occur when the data value obtained does not equal the true value. Common causes include:
> - Recording errors (transpositions)
> - Misinterpreted questions
> - [[Outliers]] requiring verification

---

## 1.4 Descriptive Statistics

> [!definition] Descriptive Statistics
> Tabular, graphical, and numerical summaries used to present and describe data.

### Types of Descriptive Summaries

1. **Tabular** - Frequency tables, percent frequency tables
2. **Graphical** - [[Bar Chart|Bar charts]], [[Histogram|histograms]], time series graphs
3. **Numerical** - Averages (means), medians, percentages

> [!example] 
> For 60 nations' Fitch Outlook ratings:
> - Stable: 65%
> - Negative: 18.3%
> - Positive: 16.7%

The **average** (mean) Per Capita GDP for 60 nations:
$$\bar{x} = \frac{\sum_{i=1}^{60} x_i}{60} = \$21{,}387$$

---

## 1.5 Statistical Inference

> [!definition] Population
> The set of **all** elements of interest in a particular study.

> [!definition] Sample
> A **subset** of the population.

| Survey Type | Definition |
|-------------|------------|
| **[[Census]]** | Survey collecting data on the entire population |
| **[[Sample Survey]]** | Survey collecting data on a sample |

> [!definition] Statistical Inference
> The process of using data obtained from a sample to make **estimates** or **test hypotheses** about the characteristics of a population.

### Example: Norris Electronics

- **Population:** All lightbulbs that could be produced with the new filament
- **Sample:** 200 lightbulbs manufactured and tested
- **Sample average lifetime:** 76 hours
- **Point estimate:** Average lifetime for population ≈ 76 hours
- **Interval estimate with margin of error:** $76 \pm 4$ hours → (72 to 80 hours)

---

## 1.6 Computers and Statistical Analysis

Computer software is essential for statistical computations with large data sets. Common tools include:
- **Minitab**
- **Microsoft Excel**
- **StatTools** (Excel add-in)

---

## 1.7 Data Mining

> [!definition] Data Mining
> The automated extraction of predictive information from large databases, combining procedures from statistics, mathematics, and computer science.

### Key Concepts

- **[[Data Warehousing]]** - Process of capturing, storing, and maintaining large volumes of data
- **Applications:** Retail recommendations, customer segmentation, predictive modeling
- **Model validation approach:**
  1. Divide data into **training set** and **test set**
  2. Develop model on training data
  3. Validate predictions on test data

> [!warning] Overfitting
> With large amounts of data, there is danger of finding misleading associations. Careful interpretation and additional testing are essential.

---

## 1.8 Ethical Guidelines for Statistical Practice

The American Statistical Association's ethical guidelines cover eight areas:

1. Professionalism
2. Responsibilities to Funders, Clients, and Employers
3. Responsibilities in Publications and Testimony
4. Responsibilities to Research Subjects
5. Responsibilities to Research Team Colleagues
6. Responsibilities to Other Statisticians
7. Responsibilities Regarding Allegations of Misconduct
8. Responsibilities of Employers

### Common Ethical Violations

| Violation | Example |
|-----------|---------|
| **Running multiple tests until desired result obtained** | Repeating samples until achieving favorable average |
| **Selectively discarding data** | Removing observations to improve results without valid justification |
| **Using unrepresentative samples** | Surveying only in restaurants that allow smoking about smoking preferences |
| **Slanting work toward predetermined outcomes** | Biased sampling or analysis |

> [!important] Ethical Requirement
> Statisticians must account for **all data** considered in a study and explain how the sample actually used was obtained.

---

## Key Takeaways

- **Statistics** involves collecting, analyzing, presenting, and interpreting data to support decision-making
- **Data types**: Categorical (nominal/ordinal) vs. Quantitative (interval/ratio)
- **Quantitative data** can be discrete (counts) or continuous (measurements)
- **Cross-sectional data** = same time point; **Time series data** = multiple time periods
- **Descriptive statistics** summarize data; **Statistical inference** uses samples to draw conclusions about populations
- The **margin of error** quantifies the precision of sample-based estimates
- **Data mining** extracts predictive information from large databases using automated methods
- **Ethical practice** requires transparency, objectivity, and avoiding manipulation of data or results