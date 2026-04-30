---
title: Sampling and Sampling Distributions
chapter: 7
tags:
  - statistics
  - sampling
  - sampling_distributions
  - point_estimation
  - central_limit_theorem
  - probability
---

# Chapter 7: Sampling and Sampling Distributions

This chapter introduces the fundamental concepts of **sampling** and **sampling distributions**, which form the backbone of [[statistical inference]]. We learn how to select samples from populations, how to use sample data to estimate population parameters, and how the variability of sample statistics can be characterized through their [[sampling distribution]].

---

## 7.1 The Electronics Associates Sampling Problem

The **Electronics Associates, Inc. (EAI)** problem serves as a running example throughout this chapter. EAI has 2500 managers, and the director of personnel wants to develop a profile including:
- The **mean annual salary** of managers
- The **proportion** of managers who completed the management training program

### Population Parameters

For the EAI population:
- Population mean annual salary: $\mu = \$51,800$
- Population standard deviation: $\sigma = \$4,000$
- Population proportion who completed training: $p = 0.60$

> [!definition] Parameter
> A **parameter** is a numerical characteristic of a population, such as $\mu$, $\sigma$, or $p$.

The question is: *Can we estimate these parameters using a sample of only 30 managers instead of surveying all 2500?*

---

## 7.2 Selecting a Sample

### Sampling from a Finite Population

> [!definition] Simple Random Sample (Finite Population)
> A **simple random sample** of size $n$ from a finite population of size $N$ is a sample selected such that each possible sample of size $n$ has the same probability of being selected.

**Procedure:**
1. Construct a **frame** (a list of all population elements)
2. Assign a unique number to each element
3. Use a **random number table** or computer-generated random numbers to select elements

**Key Concepts:**
- [[Sampling without replacement]]: Once selected, an element cannot be selected again
- [[Sampling with replacement]]: A selected element can appear multiple times in the sample

### Sampling from an Infinite Population

> [!definition] Random Sample (Infinite Population)
> A **random sample** of size $n$ from an infinite population is a sample selected such that:
> 1. Each element selected comes from the same population
> 2. Each element is selected independently

**Applications:**
- Production processes (e.g., filling cereal boxes)
- Customer arrivals at a service location
- Transactions over time

**Key concern:** Avoid [[selection bias]] by ensuring elements are selected independently.

---

## 7.3 Point Estimation

> [!definition] Point Estimator
> A **point estimator** is a sample statistic used to estimate a population parameter.

> [!definition] Point Estimate
> A **point estimate** is the numerical value of the point estimator computed from a particular sample.

### Summary of Point Estimators

| Population Parameter | Point Estimator | Formula |
|---------------------|-----------------|---------|
| Mean ($\mu$) | Sample mean ($\bar{x}$) | $\bar{x} = \frac{\sum x_i}{n}$ |
| Standard deviation ($\sigma$) | Sample standard deviation ($s$) | $s = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n-1}}$ |
| Proportion ($p$) | Sample proportion ($\bar{p}$) | $\bar{p} = \frac{x}{n}$ |

### Practical Advice

The [[sampled population]] (population from which the sample is drawn) should closely match the [[target population]] (population about which inferences are made).

---

## 7.4 Introduction to Sampling Distributions

Because different samples produce different values of sample statistics, $\bar{x}$ and $\bar{p}$ are **random variables** with their own probability distributions.

> [!definition] Sampling Distribution
> The **sampling distribution** of a statistic is the probability distribution of all possible values of that statistic computed from samples of the same size.

The sampling distribution allows us to make **probability statements** about how close sample estimates are to population parameters.

---

## 7.5 Sampling Distribution of $\bar{x}$

> [!definition] Sampling Distribution of $\bar{x}$
> The **sampling distribution of $\bar{x}$** is the probability distribution of all possible values of the sample mean $\bar{x}$.

### Expected Value of $\bar{x}$

$$E(\bar{x}) = \mu$$

where $\mu$ is the population mean.

This shows that $\bar{x}$ is an **unbiased estimator** of $\mu$.

### Standard Deviation of $\bar{x}$ (Standard Error)

**Finite Population:**
$$\sigma_{\bar{x}} = \sqrt{\frac{N-n}{N-1}} \cdot \frac{\sigma}{\sqrt{n}}$$

**Infinite Population (or when $n/N \leq 0.05$):**
$$\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$$

The term $\sqrt{\frac{N-n}{N-1}}$ is called the **[[finite population correction factor]]**.

> [!tip] Rule of Thumb
> Use $\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$ whenever $n/N \leq 0.05$ (sample is at most 5% of population).

### Form of the Sampling Distribution

**Case 1: Population is normally distributed**
- The sampling distribution of $\bar{x}$ is **exactly normal** for any sample size $n$

**Case 2: Population is not normally distributed**
- The [[Central Limit Theorem]] applies

> [!definition] Central Limit Theorem
> In selecting random samples of size $n$ from a population, the sampling distribution of $\bar{x}$ can be **approximated by a normal distribution** as the sample size becomes large (typically $n \geq 30$).

### Example: EAI Problem

For $n = 30$, $\mu = \$51,800$, $\sigma = \$4,000$:

$$\sigma_{\bar{x}} = \frac{4000}{\sqrt{30}} = 730.3$$

**Probability that $\bar{x}$ is within $500 of $\mu$:**

$$P(51,300 \leq \bar{x} \leq 52,300)$$

Computing z-scores:
- At $\bar{x} = 52,300$: $z = \frac{52,300 - 51,800}{730.3} = 0.68$
- At $\bar{x} = 51,300$: $z = \frac{51,300 - 51,800}{730.3} = -0.68$

$$P = P(z \leq 0.68) - P(z \leq -0.68) = 0.7517 - 0.2483 = 0.5034$$

### Effect of Sample Size

Increasing sample size **decreases** the standard error, making $\bar{x}$ more likely to be close to $\mu$.

For $n = 100$:
$$\sigma_{\bar{x}} = \frac{4000}{\sqrt{100}} = 400$$

The probability of being within $500 increases from 0.5034 to **0.7888**.

---

## 7.6 Sampling Distribution of $\bar{p}$

> [!definition] Sampling Distribution of $\bar{p}$
> The **sampling distribution of $\bar{p}$** is the probability distribution of all possible values of the sample proportion $\bar{p}$.

### Expected Value of $\bar{p}$

$$E(\bar{p}) = p$$

where $p$ is the population proportion. This shows $\bar{p}$ is an **unbiased estimator** of $p$.

### Standard Deviation of $\bar{p}$ (Standard Error)

**Finite Population:**
$$\sigma_{\bar{p}} = \sqrt{\frac{N-n}{N-1}} \cdot \sqrt{\frac{p(1-p)}{n}}$$

**Infinite Population (or when $n/N \leq 0.05$):**
$$\sigma_{\bar{p}} = \sqrt{\frac{p(1-p)}{n}}$$

### Normal Approximation Conditions

The sampling distribution of $\bar{p}$ can be approximated by a normal distribution whenever:
$$np \geq 5 \quad \text{and} \quad n(1-p) \geq 5$$

### Example: EAI Problem

For $n = 30$, $p = 0.60$:
- Check: $np = 30(0.60) = 18 \geq 5$ ✓
- Check: $n(1-p) = 30(0.40) = 12 \geq 5$ ✓

$$\sigma_{\bar{p}} = \sqrt{\frac{0.60(0.40)}{30}} = 0.0894$$

**Probability that $\bar{p}$ is within 0.05 of $p$:**

$$P(0.55 \leq \bar{p} \leq 0.65) = P(-0.56 \leq z \leq 0.56) = 0.4246$$

---

## 7.7 Properties of Point Estimators

Three desirable properties of point estimators:

### 1. Unbiased

> [!definition] Unbiased Estimator
> A point estimator $\hat{\theta}$ is **unbiased** if $E(\hat{\theta}) = \theta$, where $\theta$ is the population parameter being estimated.

- $\bar{x}$ is an unbiased estimator of $\mu$
- $\bar{p}$ is an unbiased estimator of $p$
- $s^2$ is an unbiased estimator of $\sigma^2$

### 2. Efficiency

> [!definition] Relative Efficiency
> Given two unbiased estimators of the same parameter, the one with the **smaller standard error** is **more efficient**.

Example: The sample mean $\bar{x}$ is more efficient than the sample median when sampling from a normal population (standard error of median is about 25% larger).

### 3. Consistency

> [!definition] Consistent Estimator
> A point estimator is **consistent** if its values tend to become closer to the population parameter as sample size increases.

Both $\bar{x}$ and $\bar{p}$ are consistent estimators because their standard errors decrease as $n$ increases.

---

## 7.8 Other Sampling Methods

### Probability Sampling Methods

| Method | Description | Best When |
|--------|-------------|-----------|
| [[Stratified Random Sampling]] | Divide population into strata, then take SRS from each | Elements within strata are homogeneous |
| [[Cluster Sampling]] | Divide population into clusters, randomly select clusters, sample all elements in selected clusters | Each cluster is representative of the population |
| [[Systematic Sampling]] | Select every $k$th element after a random start | Population list is available and randomly ordered |

### Non-Probability Sampling Methods

| Method | Description | Limitation |
|--------|-------------|------------|
| [[Convenience Sampling]] | Select elements based on convenience | Cannot evaluate goodness of sample |
| [[Judgment Sampling]] | Expert selects elements believed to be representative | Quality depends on expert's judgment |

> [!warning] Caution
> Non-probability sampling methods do not allow valid statistical inferences about populations.

---

## Key Takeaways

- A **simple random sample** gives every possible sample of size $n$ an equal probability of selection
- **Point estimators** ($\bar{x}$, $s$, $\bar{p}$) provide single-value estimates of population parameters ($\mu$, $\sigma$, $p$)
- The **sampling distribution** describes the probability distribution of a sample statistic
- $E(\bar{x}) = \mu$ and $E(\bar{p}) = p$, making both unbiased estimators
- The **standard error** measures variability: $\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}}$ and $\sigma_{\bar{p}} = \sqrt{\frac{p(1-p)}{n}}$
- The **Central Limit Theorem** ensures $\bar{x}$ is approximately normal for $n \geq 30$
- **Larger sample sizes** reduce standard errors and improve precision of estimates
- **Probability sampling** methods (SRS, stratified, cluster, systematic) allow valid statistical inference
- Good estimators are **unbiased**, **efficient**, and **consistent**