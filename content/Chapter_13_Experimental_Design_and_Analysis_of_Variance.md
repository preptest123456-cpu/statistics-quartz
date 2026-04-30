---
title: "Experimental Design and Analysis of Variance"
chapter: 13
tags:
  - statistics
  - experimental_design
  - analysis_of_variance
  - ANOVA
  - completely_randomized_design
  - randomized_block_design
  - factorial_experiment
  - multiple_comparisons
  - hypothesis_testing
---

# Experimental Design and Analysis of Variance

This chapter introduces [[experimental design]] principles and [[analysis of variance]] (ANOVA), the statistical procedure used to determine whether observed differences in sample means are large enough to reject the hypothesis that population means are equal.

---

## Key Concepts

1. **Experimental vs. Observational Studies**: In an [[experimental study]], the researcher conducts an experiment to generate data by controlling factors. In an [[observational study]], data are collected through surveys without experimental control.

2. **Factor**: The [[independent variable]] of interest; also called a treatment variable.

3. **Treatments**: Different levels of a [[factor]].

4. **Response Variable**: The [[dependent variable]] measured in the experiment.

5. **Experimental Units**: The objects or individuals to which treatments are applied.

6. **Randomization**: The process of randomly assigning treatments to experimental units to eliminate bias.

7. **Replication**: Repeating the basic experimental process to obtain additional data.

---

## Completely Randomized Design

A [[completely randomized design]] randomly assigns all experimental units to treatments. This design is appropriate when experimental units are relatively homogeneous.

### ANOVA Assumptions

> [!definition] ANOVA Assumptions
> 1. For each population, the response variable is **normally distributed**.
> 2. The variance of the response variable $\sigma^2$ is the **same for all populations**.
> 3. Observations must be **independent**.

### Conceptual Overview

ANOVA compares two independent estimates of the population variance $\sigma^2$:

- **Between-treatments estimate** (MSTR): Based on variability among sample means. If $H_0$ is true, this provides an unbiased estimate of $\sigma^2$.
- **Within-treatments estimate** (MSE): Based on variability within each sample. Always provides an unbiased estimate of $\sigma^2$.

If $H_0$ is true, both estimates should be similar, and $F = \text{MSTR}/\text{MSE}$ will be close to 1. If $H_0$ is false, MSTR will be larger, yielding a large $F$ value.

### Formulas for Completely Randomized Design

**Sample Mean for Treatment $j$:**
$$\bar{x}_j = \frac{\sum_{i=1}^{n_j} x_{ij}}{n_j}$$

**Sample Variance for Treatment $j$:**
$$s_j^2 = \frac{\sum_{i=1}^{n_j}(x_{ij} - \bar{x}_j)^2}{n_j - 1}$$

**Overall Sample Mean:**
$$\bar{\bar{x}} = \frac{\sum_{j=1}^{k} \sum_{i=1}^{n_j} x_{ij}}{n_T}$$

where $n_T = n_1 + n_2 + \cdots + n_k$.

**Sum of Squares Due to Treatments (SSTR):**
$$\text{SSTR} = \sum_{j=1}^{k} n_j (\bar{x}_j - \bar{\bar{x}})^2$$

**Mean Square Due to Treatments (MSTR):**
$$\text{MSTR} = \frac{\text{SSTR}}{k - 1}$$

**Sum of Squares Due to Error (SSE):**
$$\text{SSE} = \sum_{j=1}^{k} (n_j - 1) s_j^2$$

**Mean Square Due to Error (MSE):**
$$\text{MSE} = \frac{\text{SSE}}{n_T - k}$$

**Total Sum of Squares (SST):**
$$\text{SST} = \sum_{j=1}^{k} \sum_{i=1}^{n_j} (x_{ij} - \bar{\bar{x}})^2$$

**Partitioning Relationship:**
$$\text{SST} = \text{SSTR} + \text{SSE}$$

### Hypothesis Test for Equality of $k$ Population Means

> [!definition] Hypotheses
> - $H_0$: $\mu_1 = \mu_2 = \cdots = \mu_k$
> - $H_a$: Not all population means are equal

**Test Statistic:**
$$F = \frac{\text{MSTR}}{\text{MSE}}$$

The test statistic follows an [[F distribution]] with $k - 1$ numerator degrees of freedom and $n_T - k$ denominator degrees of freedom.

**Rejection Rule:**
- p-value approach: Reject $H_0$ if p-value $\leq \alpha$
- Critical value approach: Reject $H_0$ if $F \geq F_\alpha$

### ANOVA Table

| Source of Variation | Sum of Squares | Degrees of Freedom | Mean Square | F | p-value |
|---------------------|----------------|-------------------|-------------|---|---------|
| Treatments | SSTR | $k - 1$ | MSTR | MSTR/MSE | |
| Error | SSE | $n_T - k$ | MSE | | |
| Total | SST | $n_T - 1$ | | | |

---

## Multiple Comparison Procedures

When ANOVA rejects $H_0$, [[multiple comparison procedures]] determine which specific means differ.

### Fisher's LSD Procedure

> [!definition] Fisher's Least Significant Difference (LSD)
> A procedure for pairwise comparisons of population means after ANOVA rejects $H_0$.

**Test Statistic:**
$$t = \frac{\bar{x}_i - \bar{x}_j}{\sqrt{\text{MSE}\left(\frac{1}{n_i} + \frac{1}{n_j}\right)}}$$

**LSD Value:**
$$\text{LSD} = t_{\alpha/2} \sqrt{\text{MSE}\left(\frac{1}{n_i} + \frac{1}{n_j}\right)}$$

where $t_{\alpha/2}$ is based on $n_T - k$ degrees of freedom.

**Decision Rule:** Reject $H_0: \mu_i = \mu_j$ if $|\bar{x}_i - \bar{x}_j| \geq \text{LSD}$

**Confidence Interval for Difference:**
$$\bar{x}_i - \bar{x}_j \pm \text{LSD}$$

### Type I Error Rates

- **Comparisonwise Type I error rate**: Probability of Type I error for a single pairwise comparison ($\alpha$).
- **Experimentwise Type I error rate** ($\alpha_{EW}$): Probability of at least one Type I error across all pairwise comparisons.

**Bonferroni Adjustment:** To control $\alpha_{EW}$, use comparisonwise error rate:
$$\alpha = \frac{\alpha_{EW}}{C}$$
where $C$ is the number of pairwise comparisons.

---

## Randomized Block Design

A [[randomized block design]] controls extraneous sources of variation by grouping similar experimental units into blocks and applying each treatment within every block.

### Sum of Squares Partitioning

$$\text{SST} = \text{SSTR} + \text{SSBL} + \text{SSE}$$

**Formulas:**

**Total Sum of Squares:**
$$\text{SST} = \sum_{i=1}^{b} \sum_{j=1}^{k} (x_{ij} - \bar{\bar{x}})^2$$

**Sum of Squares Due to Treatments:**
$$\text{SSTR} = b \sum_{j=1}^{k} (\bar{x}_{.j} - \bar{\bar{x}})^2$$

**Sum of Squares Due to Blocks:**
$$\text{SSBL} = k \sum_{i=1}^{b} (\bar{x}_{i.} - \bar{\bar{x}})^2$$

**Sum of Squares Due to Error:**
$$\text{SSE} = \text{SST} - \text{SSTR} - \text{SSBL}$$

### ANOVA Table for Randomized Block Design

| Source | Sum of Squares | df | Mean Square | F |
|--------|----------------|----|--------------|----|
| Treatments | SSTR | $k - 1$ | $\text{MSTR} = \frac{\text{SSTR}}{k-1}$ | $\frac{\text{MSTR}}{\text{MSE}}$ |
| Blocks | SSBL | $b - 1$ | $\text{MSBL} = \frac{\text{SSBL}}{b-1}$ | |
| Error | SSE | $(k-1)(b-1)$ | $\text{MSE} = \frac{\text{SSE}}{(k-1)(b-1)}$ | |
| Total | SST | $n_T - 1$ | | |

where $n_T = kb$.

---

## Factorial Experiment

A [[factorial experiment]] allows simultaneous conclusions about two or more factors by including all possible combinations of factor levels.

### Terminology

- **Factor A**: Has $a$ levels
- **Factor B**: Has $b$ levels
- **Replications** ($r$): Number of observations per treatment combination
- **Total observations**: $n_T = abr$

### Sum of Squares Partitioning

$$\text{SST} = \text{SSA} + \text{SSB} + \text{SSAB} + \text{SSE}$$

**Formulas:**

**Total Sum of Squares:**
$$\text{SST} = \sum_{i=1}^{a} \sum_{j=1}^{b} \sum_{k=1}^{r} (x_{ijk} - \bar{\bar{x}})^2$$

**Sum of Squares for Factor A:**
$$\text{SSA} = br \sum_{i=1}^{a} (\bar{x}_{i.} - \bar{\bar{x}})^2$$

**Sum of Squares for Factor B:**
$$\text{SSB} = ar \sum_{j=1}^{b} (\bar{x}_{.j} - \bar{\bar{x}})^2$$

**Sum of Squares for Interaction:**
$$\text{SSAB} = r \sum_{i=1}^{a} \sum_{j=1}^{b} (\bar{x}_{ij} - \bar{x}_{i.} - \bar{x}_{.j} + \bar{\bar{x}})^2$$

**Sum of Squares for Error:**
$$\text{SSE} = \text{SST} - \text{SSA} - \text{SSB} - \text{SSAB}$$

### ANOVA Table for Two-Factor Factorial Experiment

| Source | Sum of Squares | df | Mean Square | F |
|--------|----------------|----|--------------|----|
| Factor A | SSA | $a - 1$ | $\text{MSA} = \frac{\text{SSA}}{a-1}$ | $\frac{\text{MSA}}{\text{MSE}}$ |
| Factor B | SSB | $b - 1$ | $\text{MSB} = \frac{\text{SSB}}{b-1}$ | $\frac{\text{MSB}}{\text{MSE}}$ |
| Interaction | SSAB | $(a-1)(b-1)$ | $\text{MSAB} = \frac{\text{SSAB}}{(a-1)(b-1)}$ | $\frac{\text{MSAB}}{\text{MSE}}$ |
| Error | SSE | $ab(r-1)$ | $\text{MSE} = \frac{\text{SSE}}{ab(r-1)}$ | |
| Total | SST | $n_T - 1$ | | |

> [!definition] Interaction Effect
> An **interaction effect** occurs when the effect of one factor on the response variable depends on the level of another factor.

---

## Key Takeaways

- **ANOVA** tests whether population means are equal by comparing between-treatment and within-treatment variance estimates.
- A **completely randomized design** randomly assigns treatments to experimental units and is appropriate for homogeneous units.
- A **randomized block design** removes extraneous variation by grouping similar units into blocks, providing a more powerful test.
- A **factorial experiment** tests main effects and interaction effects for two or more factors simultaneously.
- **Fisher's LSD** procedure identifies which specific means differ after ANOVA rejects $H_0$.
- The **Bonferroni adjustment** controls the experimentwise Type I error rate when making multiple pairwise comparisons.
- Rejecting $H_0$ in ANOVA means at least two population means differ—not that all means are different.
- ANOVA can be applied to both experimental and observational studies, though causal inference is stronger for experiments.