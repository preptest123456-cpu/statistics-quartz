---
title: "Chapter 4: Introduction to Probability"
chapter: 4
tags:
  - statistics
  - probability
  - sample_space
  - conditional_probability
  - bayes_theorem
  - counting_rules
  - events
---

# Chapter 4: Introduction to Probability

## 4.1 Experiments, Counting Rules, and Assigning Probabilities

[[Probability]] is a numerical measure of the likelihood that an [[event]] will occur. Probability values range from 0 (impossible) to 1 (certain), with values in between representing degrees of likelihood.

> [!definition] Experiment
> An **experiment** is a process that generates well-defined outcomes. On any single repetition, one and only one of the possible experimental outcomes will occur.

> [!definition] Sample Space
> The **sample space** for an experiment is the set of all experimental outcomes. It is denoted by $S$.

> [!definition] Sample Point
> An **experimental outcome** is also called a **sample point** to identify it as an element of the sample space.

### Counting Rules, Combinations, and Permutations

#### 1. Counting Rule for Multiple-Step Experiments

If an experiment can be described as a sequence of $k$ steps with $n_1$ possible outcomes on the first step, $n_2$ on the second, and so on, then the total number of experimental outcomes is:

$$
(n_1)(n_2) \cdots (n_k)
$$

A [[tree diagram]] is a graphical representation that helps visualize multiple-step experiments.

#### 2. Counting Rule for Combinations

The number of [[combinations]] of $N$ objects taken $n$ at a time is:

$$
C_n^N = \binom{N}{n} = \frac{N!}{n!(N-n)!}
$$

where $N! = N(N-1)(N-2)\cdots(2)(1)$ and $0! = 1$ by definition.

#### 3. Counting Rule for Permutations

The number of [[permutations]] of $N$ objects taken $n$ at a time is:

$$
P_n^N = \frac{N!}{(N-n)!}
$$

Permutations account for the order of selection, while combinations do not.

### Assigning Probabilities

> [!definition] Basic Requirements for Assigning Probabilities
> 1. For each experimental outcome $E_i$: $0 \leq P(E_i) \leq 1$
> 2. The sum of all probabilities must equal 1: $P(E_1) + P(E_2) + \cdots + P(E_n) = 1$

**Three Methods for Assigning Probabilities:**

1. **Classical Method**: Appropriate when all outcomes are equally likely. Each outcome has probability $\frac{1}{n}$.

2. **Relative Frequency Method**: Based on historical data; probability equals the proportion of times an outcome occurred in repeated experiments.

3. **Subjective Method**: Based on judgment, experience, or intuition when outcomes are not equally likely and little historical data exists.

---

## 4.2 Events and Their Probabilities

> [!definition] Event
> An **event** is a collection of sample points.

> [!definition] Probability of an Event
> The probability of any event equals the sum of the probabilities of the sample points in the event.

If event $A = \{E_1, E_2, E_3\}$, then:
$$
P(A) = P(E_1) + P(E_2) + P(E_3)
$$

---

## 4.3 Some Basic Relationships of Probability

### Complement of an Event

> [!definition] Complement
> The **complement of event $A$**, denoted $A^c$, is the event consisting of all sample points not in $A$.

$$
P(A) + P(A^c) = 1
$$

Therefore:
$$
P(A) = 1 - P(A^c)
$$

### Union and Intersection of Events

> [!definition] Union of Events
> The **union of $A$ and $B$**, denoted $A \cup B$, contains all sample points belonging to $A$ or $B$ or both.

> [!definition] Intersection of Events
> The **intersection of $A$ and $B$**, denoted $A \cap B$, contains all sample points belonging to both $A$ and $B$.

### Addition Law

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

> [!definition] Mutually Exclusive Events
> Two events are **mutually exclusive** if they have no sample points in common: $P(A \cap B) = 0$.

For mutually exclusive events:
$$
P(A \cup B) = P(A) + P(B)
$$

---

## 4.4 Conditional Probability

> [!definition] Conditional Probability
> The **conditional probability** of $A$ given $B$ is the probability of $A$ occurring given that $B$ has already occurred:
> $$P(A \mid B) = \frac{P(A \cap B)}{P(B)}$$

Similarly:
$$
P(B \mid A) = \frac{P(A \cap B)}{P(A)}
$$

### Joint and Marginal Probabilities

- **Joint probability**: $P(A \cap B)$ — the probability of both events occurring
- **Marginal probability**: The probability of a single event, found by summing joint probabilities

### Independent Events

> [!definition] Independent Events
> Two events $A$ and $B$ are **independent** if:
> $$P(A \mid B) = P(A) \quad \text{or equivalently} \quad P(B \mid A) = P(B)$$

If events are independent: $P(A \cap B) = P(A) \cdot P(B)$

### Multiplication Law

**General form:**
$$
P(A \cap B) = P(B) \cdot P(A \mid B) = P(A) \cdot P(B \mid A)
$$

**For independent events:**
$$
P(A \cap B) = P(A) \cdot P(B)
$$

---

## 4.5 Bayes' Theorem

[[Bayes' theorem]] provides a method for revising prior probabilities based on new information to obtain posterior probabilities.

> [!definition] Bayes' Theorem (Two-Event Case)
> $$P(A_1 \mid B) = \frac{P(A_1)P(B \mid A_1)}{P(A_1)P(B \mid A_1) + P(A_2)P(B \mid A_2)}$$

**General Form (for $n$ mutually exclusive events):**

$$
P(A_i \mid B) = \frac{P(A_i)P(B \mid A_i)}{\sum_{j=1}^{n} P(A_j)P(B \mid A_j)}
$$

**Key Terms:**
- **Prior probabilities**: Initial probability estimates before new information
- **Posterior probabilities**: Revised probabilities after incorporating new information

### Tabular Approach to Bayes' Theorem

| Events $A_i$ | Prior $P(A_i)$ | Conditional $P(B \mid A_i)$ | Joint $P(A_i \cap B)$ | Posterior $P(A_i \mid B)$ |
|--------------|----------------|-----------------------------|-----------------------|---------------------------|
| $A_1$        | $P(A_1)$       | $P(B \mid A_1)$             | $P(A_1) \cdot P(B \mid A_1)$ | Joint ÷ $P(B)$ |
| $A_2$        | $P(A_2)$       | $P(B \mid A_2)$             | $P(A_2) \cdot P(B \mid A_2)$ | Joint ÷ $P(B)$ |
| **Total**    | 1.00           |                             | $P(B)$                | 1.00 |

---

## Key Takeaways

- **Probability** measures likelihood on a scale from 0 to 1
- The **sample space** contains all possible outcomes; an **event** is a subset of sample points
- **Counting rules** (combinations and permutations) help enumerate outcomes in complex experiments
- The **complement rule** states $P(A) = 1 - P(A^c)$
- The **addition law** computes $P(A \cup B)$ by adjusting for double-counting the intersection
- **Conditional probability** adjusts probabilities based on known information
- **Independent events** do not influence each other's probabilities
- The **multiplication law** computes intersection probabilities
- **Bayes' theorem** revises prior probabilities when new evidence is obtained
- Joint probability tables and tree diagrams are useful tools for organizing probability calculations