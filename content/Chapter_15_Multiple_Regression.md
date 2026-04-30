# Multiple Regression

## Statistics in Practice: dunnhumby

Founded in 1989 by the husband-and-wife team of Clive Humby (a mathematician) and Edwina Dunn (a marketer), dunnhumby combines proven natural abilities with big ideas to find clues and patterns as to what customers are buying and why. The company turns these insights into actionable strategies that create dramatic growth and sustainable loyalty, ultimately improving brand value and the customer experience.

Employing more than 950 people in Europe, Asia, and the Americas, dunnhumby serves a prestigious list of companies, including Kroger, Tesco, Coca-Cola, General Mills, Kimberly-Clark, PepsiCo, Procter & Gamble, and Home Depot. dunnhumbyUSA is a joint venture between the Kroger Company and dunnhumby and has offices in New York, Chicago, Atlanta, Minneapolis, Cincinnati, and Portland.

The company's research begins with data collected about a client's customers. Data come from customer reward or discount card purchase records, electronic point-of-sale transactions, and traditional market research. Analysis of the data often translates billions of data points into detailed insights about the behavior, preferences, and lifestyles of the customers. Such insights allow for more effective merchandising programs to be activated, including strategy recommendations on pricing, promotion, advertising, and product assortment decisions.

Researchers have used a multiple regression technique referred to as logistic regression to help in their analysis of customer-based data. Using logistic regression, an estimated multiple regression equation of the following form is developed:

$$\hat{y} = b_0 + b_1x_1 + b_2x_2 + b_3x_3 + \ldots + b_px_p$$

The dependent variable is a prediction of the probability that a customer belongs to a particular customer group. The independent variables $x_1, x_2, x_3, \ldots, x_p$ are measures of the customer's actual shopping behavior and may include the specific items purchased, number of items purchased, amount purchased, day of the week, hour of the day, and so on. The analysis helps identify the independent variables that are most relevant in predicting the customer's group and provides a better understanding of the customer population, enabling further analysis with far greater confidence. The focus of the analysis is on understanding the customer to the point of developing merchandising, marketing, and direct marketing programs that will maximize the relevancy and service to the customer group.

In this chapter, we will introduce multiple regression and show how the concepts of simple linear regression introduced in Chapter 14 can be extended to the multiple regression case. In addition, we will show how computer software packages are used for multiple regression. In the final section of the chapter we introduce logistic regression using an example that illustrates how the technique is used in a marketing research application.

---

## 15.1 Multiple Regression Model

In Chapter 14 we presented simple linear regression and demonstrated its use in developing an estimated regression equation that describes the relationship between two variables. Recall that the variable being predicted or explained is called the **dependent variable** and the variable being used to predict or explain the dependent variable is called the **independent variable**. In this chapter we continue our study of regression analysis by considering situations involving two or more independent variables. This subject area, called **multiple regression analysis**, enables us to consider more factors and thus obtain better predictions than are possible with simple linear regression.

### Regression Model and Regression Equation

The concepts of a regression model and a regression equation introduced in the preceding chapter are applicable in the multiple regression case. The equation that describes how the dependent variable $y$ is related to the independent variables $x_1, x_2, \ldots, x_p$ and an error term is called the **multiple regression model**. We begin with the assumption that the multiple regression model takes the following form.

**Multiple Regression Model**

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p + \epsilon \tag{15.1}$$

In the multiple regression model, $\beta_0, \beta_1, \beta_2, \ldots, \beta_p$ are the parameters and the error term $\epsilon$ (the Greek letter epsilon) is a random variable. A close examination of this model reveals that $y$ is a linear function of $x_1, x_2, \ldots, x_p$ (the $\beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p$ part) plus the error term $\epsilon$. The error term accounts for the variability in $y$ that cannot be explained by the linear effect of the $p$ independent variables.

In Section 15.4 we will discuss the assumptions for the multiple regression model and $\epsilon$. One of the assumptions is that the mean or expected value of $\epsilon$ is zero. A consequence of this assumption is that the mean or expected value of $y$, denoted $E(y)$, is equal to $\beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p$. The equation that describes how the mean value of $y$ is related to $x_1, x_2, \ldots, x_p$ is called the **multiple regression equation**.

**Multiple Regression Equation**

$$E(y) = \beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p \tag{15.2}$$

### Estimated Multiple Regression Equation

If the values of $\beta_0, \beta_1, \beta_2, \ldots, \beta_p$ were known, equation (15.2) could be used to compute the mean value of $y$ at given values of $x_1, x_2, \ldots, x_p$. Unfortunately, these parameter values will not, in general, be known and must be estimated from sample data. A simple random sample is used to compute sample statistics $b_0, b_1, b_2, \ldots, b_p$ that are used as the point estimators of the parameters $\beta_0, \beta_1, \beta_2, \ldots, \beta_p$. These sample statistics provide the following estimated multiple regression equation.

**Estimated Multiple Regression Equation**

$$\hat{y} = b_0 + b_1x_1 + b_2x_2 + \ldots + b_px_p \tag{15.3}$$

where:
- $b_0, b_1, b_2, \ldots, b_p$ are the estimates of $\beta_0, \beta_1, \beta_2, \ldots, \beta_p$
- $\hat{y}$ = predicted value of the dependent variable

> In simple linear regression, $b_0$ and $b_1$ were the sample statistics used to estimate the parameters $\beta_0$ and $\beta_1$. Multiple regression parallels this statistical inference process, with $b_0, b_1, b_2, \ldots, b_p$ denoting the sample statistics used to estimate the parameters $\beta_0, \beta_1, \beta_2, \ldots, \beta_p$.

The estimation process for multiple regression is shown in Figure 15.1.

---

## 15.2 Least Squares Method

In Chapter 14, we used the least squares method to develop the estimated regression equation that best approximated the straight-line relationship between the dependent and independent variables. This same approach is used to develop the estimated multiple regression equation. The least squares criterion is restated as follows.

**Least Squares Criterion**

$$\min \sum(y_i - \hat{y}_i)^2 \tag{15.4}$$

where:
- $y_i$ = observed value of the dependent variable for the $i$th observation
- $\hat{y}_i$ = predicted value of the dependent variable for the $i$th observation

The predicted values of the dependent variable are computed by using the estimated multiple regression equation:

$$\hat{y} = b_0 + b_1x_1 + b_2x_2 + \ldots + b_px_p$$

As expression (15.4) shows, the least squares method uses sample data to provide the values of $b_0, b_1, b_2, \ldots, b_p$ that make the sum of squared residuals [the deviations between the observed values of the dependent variable ($y_i$) and the predicted values of the dependent variable ($\hat{y}_i$)] a minimum.

In Chapter 14 we presented formulas for computing the least squares estimators $b_0$ and $b_1$ for the estimated simple linear regression equation $\hat{y} = b_0 + b_1x$. With relatively small data sets, we were able to use those formulas to compute $b_0$ and $b_1$ by manual calculations. In multiple regression, however, the presentation of the formulas for the regression coefficients $b_0, b_1, b_2, \ldots, b_p$ involves the use of matrix algebra and is beyond the scope of this text. Therefore, in presenting multiple regression, we focus on how computer software packages can be used to obtain the estimated regression equation and other information. The emphasis will be on how to interpret the computer output rather than on how to make the multiple regression computations.

### An Example: Butler Trucking Company

As an illustration of multiple regression analysis, we will consider a problem faced by the Butler Trucking Company, an independent trucking company in southern California. A major portion of Butler's business involves deliveries throughout its local area. To develop better work schedules, the managers want to predict the total daily travel time for their drivers.

Initially the managers believed that the total daily travel time would be closely related to the number of miles traveled in making the daily deliveries. A simple random sample of 10 driving assignments provided the data shown in Table 15.1 and the scatter diagram shown in Figure 15.2.

**Table 15.1: Preliminary Data for Butler Trucking**

| Driving Assignment | $x_1$ = Miles Traveled | $y$ = Travel Time (hours) |
|---|---|---|
| 1 | 100 | 9.3 |
| 2 | 50 | 4.8 |
| 3 | 100 | 8.9 |
| 4 | 100 | 6.5 |
| 5 | 50 | 4.2 |
| 6 | 80 | 6.2 |
| 7 | 75 | 7.4 |
| 8 | 65 | 6.0 |
| 9 | 90 | 7.6 |
| 10 | 90 | 6.1 |

After reviewing this scatter diagram, the managers hypothesized that the simple linear regression model $y = \beta_0 + \beta_1x_1 + \epsilon$ could be used to describe the relationship between the total travel time ($y$) and the number of miles traveled ($x_1$). To estimate the parameters $\beta_0$ and $\beta_1$, the least squares method was used to develop the estimated regression equation.

$$\hat{y} = b_0 + b_1x_1 \tag{15.5}$$

In Figure 15.3, we show the Minitab computer output from applying simple linear regression to the data in Table 15.1. The estimated regression equation is:

$$\hat{y} = 1.27 + .0678x_1$$

At the .05 level of significance, the F value of 15.81 and its corresponding p-value of .004 indicate that the relationship is significant; that is, we can reject $H_0: \beta_1 = 0$ because the p-value is less than $\alpha = .05$. Note that the same conclusion is obtained from the t value of 3.98 and its associated p-value of .004. Thus, we can conclude that the relationship between the total travel time and the number of miles traveled is significant; longer travel times are associated with more miles traveled. With a coefficient of determination (expressed as a percentage) of R-Sq = 66.4%, we see that 66.4% of the variability in travel time can be explained by the linear effect of the number of miles traveled. This finding is fairly good, but the managers might want to consider adding a second independent variable to explain some of the remaining variability in the dependent variable.

In attempting to identify another independent variable, the managers felt that the number of deliveries could also contribute to the total travel time. The Butler Trucking data, with the number of deliveries added, are shown in Table 15.2. The Minitab computer solution with both miles traveled ($x_1$) and number of deliveries ($x_2$) as independent variables is shown in Figure 15.4. The estimated regression equation is:

$$\hat{y} = -.869 + .0611x_1 + .923x_2 \tag{15.6}$$

**Table 15.2: Data for Butler Trucking with Miles Traveled ($x_1$) and Number of Deliveries ($x_2$) as the Independent Variables**

| Driving Assignment | $x_1$ = Miles Traveled | $x_2$ = Number of Deliveries | $y$ = Travel Time (hours) |
|---|---|---|---|
| 1 | 100 | 4 | 9.3 |
| 2 | 50 | 3 | 4.8 |
| 3 | 100 | 4 | 8.9 |
| 4 | 100 | 2 | 6.5 |
| 5 | 50 | 2 | 4.2 |
| 6 | 80 | 2 | 6.2 |
| 7 | 75 | 3 | 7.4 |
| 8 | 65 | 4 | 6.0 |
| 9 | 90 | 3 | 7.6 |
| 10 | 90 | 2 | 6.1 |

In the next section we will discuss the use of the coefficient of multiple determination in measuring how good a fit is provided by this estimated regression equation. Before doing so, let us examine more carefully the values of $b_1 = .0611$ and $b_2 = .923$ in equation (15.6).

### Note on Interpretation of Coefficients

One observation can be made at this point about the relationship between the estimated regression equation with only the miles traveled as an independent variable and the equation that includes the number of deliveries as a second independent variable. The value of $b_1$ is not the same in both cases. In simple linear regression, we interpret $b_1$ as an estimate of the change in $y$ for a one-unit change in the independent variable. In multiple regression analysis, this interpretation must be modified somewhat. That is, in multiple regression analysis, we interpret each regression coefficient as follows: **$b_i$ represents an estimate of the change in $y$ corresponding to a one-unit change in $x_i$ when all other independent variables are held constant**.

In the Butler Trucking example involving two independent variables, $b_1 = .0611$. Thus, .0611 hours is an estimate of the expected increase in travel time corresponding to an increase of one mile in the distance traveled when the number of deliveries is held constant. Similarly, because $b_2 = .923$, an estimate of the expected increase in travel time corresponding to an increase of one delivery when the number of miles traveled is held constant is .923 hours.

---

## 15.3 Multiple Coefficient of Determination

In simple linear regression we showed that the total sum of squares can be partitioned into two components: the sum of squares due to regression and the sum of squares due to error. The same procedure applies to the sum of squares in multiple regression.

**Relationship Among SST, SSR, and SSE**

$$SST = SSR + SSE \tag{15.7}$$

where:
- $SST$ = total sum of squares = $\sum(y_i - \bar{y})^2$
- $SSR$ = sum of squares due to regression = $\sum(\hat{y}_i - \bar{y})^2$
- $SSE$ = sum of squares due to error = $\sum(y_i - \hat{y}_i)^2$

Because of the computational difficulty in computing the three sums of squares, we rely on computer packages to determine those values. The analysis of variance part of the Minitab output in Figure 15.4 shows the three values for the Butler Trucking problem with two independent variables: SST = 23.900, SSR = 21.601, and SSE = 2.299. With only one independent variable (number of miles traveled), the Minitab output in Figure 15.3 shows that SST = 23.900, SSR = 15.871, and SSE = 8.029. The value of SST is the same in both cases because it does not depend on $\hat{y}$, but SSR increases and SSE decreases when a second independent variable (number of deliveries) is added. The implication is that the estimated multiple regression equation provides a better fit for the observed data.

In Chapter 14, we used the coefficient of determination, $r^2 = SSR/SST$, to measure the goodness of fit for the estimated regression equation. The same concept applies to multiple regression. The term **multiple coefficient of determination** indicates that we are measuring the goodness of fit for the estimated multiple regression equation. The multiple coefficient of determination, denoted $R^2$, is computed as follows.

**Multiple Coefficient of Determination**

$$R^2 = \frac{SSR}{SST} \tag{15.8}$$

The multiple coefficient of determination can be interpreted as the proportion of the variability in the dependent variable that can be explained by the estimated multiple regression equation. Hence, when multiplied by 100, it can be interpreted as the percentage of the variability in $y$ that can be explained by the estimated regression equation.

In the two-independent-variable Butler Trucking example, with SSR = 21.601 and SST = 23.900, we have:

$$R^2 = \frac{21.601}{23.900} = .904$$

Therefore, 90.4% of the variability in travel time $y$ is explained by the estimated multiple regression equation with miles traveled and number of deliveries as the independent variables. In Figure 15.4, we see that the multiple coefficient of determination (expressed as a percentage) is also provided by the Minitab output; it is denoted by R-Sq = 90.4%.

Figure 15.3 shows that the R-Sq value for the estimated regression equation with only one independent variable, number of miles traveled ($x_1$), is 66.4%. Thus, the percentage of the variability in travel times that is explained by the estimated regression equation increases from 66.4% to 90.4% when number of deliveries is added as a second independent variable. In general, $R^2$ always increases as independent variables are added to the model.

> Adding independent variables causes the prediction errors to become smaller, thus reducing the sum of squares due to error, SSE. Because SSR = SST − SSE, when SSE becomes smaller, SSR becomes larger, causing $R^2 = SSR/SST$ to increase.

Many analysts prefer adjusting $R^2$ for the number of independent variables to avoid overestimating the impact of adding an independent variable on the amount of variability explained by the estimated regression equation. With $n$ denoting the number of observations and $p$ denoting the number of independent variables, the **adjusted multiple coefficient of determination** is computed as follows.

**Adjusted Multiple Coefficient of Determination**

$$R_a^2 = 1 - (1 - R^2)\frac{n - 1}{n - p - 1} \tag{15.9}$$

> If a variable is added to the model, $R^2$ becomes larger even if the variable added is not statistically significant. The adjusted multiple coefficient of determination compensates for the number of independent variables in the model.

For the Butler Trucking example with $n = 10$ and $p = 2$, we have:

$$R_a^2 = 1 - (1 - .904)\frac{10 - 1}{10 - 2 - 1} = .88$$

Thus, after adjusting for the two independent variables, we have an adjusted multiple coefficient of determination of .88. This value (expressed as a percentage) is provided by the Minitab output in Figure 15.4 as R-Sq(adj) = 87.6%; the value we calculated differs because we used a rounded value of $R^2$ in the calculation.

> **Notes and Comments:** If the value of $R^2$ is small and the model contains a large number of independent variables, the adjusted coefficient of determination can take a negative value; in such cases, Minitab sets the adjusted coefficient of determination to zero.

---

## 15.4 Model Assumptions

In Section 15.1 we introduced the following multiple regression model.

**Multiple Regression Model**

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p + \epsilon \tag{15.10}$$

The assumptions about the error term $\epsilon$ in the multiple regression model parallel those for the simple linear regression model.

**Assumptions About the Error Term $\epsilon$ in the Multiple Regression Model $y = \beta_0 + \beta_1x_1 + \ldots + \beta_px_p + \epsilon$**

1. **The error term $\epsilon$ is a random variable with mean or expected value of zero; that is, $E(\epsilon) = 0$.**
   
   *Implication:* For given values of $x_1, x_2, \ldots, x_p$, the expected, or average, value of $y$ is given by:
   
   $$E(y) = \beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p \tag{15.11}$$
   
   Equation (15.11) is the multiple regression equation we introduced in Section 15.1. In this equation, $E(y)$ represents the average of all possible values of $y$ that might occur for the given values of $x_1, x_2, \ldots, x_p$.

2. **The variance of $\epsilon$ is denoted by $\sigma^2$ and is the same for all values of the independent variables $x_1, x_2, \ldots, x_p$.**
   
   *Implication:* The variance of $y$ about the regression line equals $\sigma^2$ and is the same for all values of $x_1, x_2, \ldots, x_p$.

3. **The values of $\epsilon$ are independent.**
   
   *Implication:* The value of $\epsilon$ for a particular set of values for the independent variables is not related to the value of $\epsilon$ for any other set of values.

4. **The error term $\epsilon$ is a normally distributed random variable reflecting the deviation between the $y$ value and the expected value of $y$ given by $\beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p$.**
   
   *Implication:* Because $\beta_0, \beta_1, \ldots, \beta_p$ are constants for the given values of $x_1, x_2, \ldots, x_p$, the dependent variable $y$ is also a normally distributed random variable.

To obtain more insight about the form of the relationship given by equation (15.11), consider the following two-independent-variable multiple regression equation:

$$E(y) = \beta_0 + \beta_1x_1 + \beta_2x_2$$

The graph of this equation is a plane in three-dimensional space. Figure 15.5 provides an example of such a graph. Note that the value of $\epsilon$ shown is the difference between the actual $y$ value and the expected value of $y$, $E(y)$, when $x_1 = x_1^*$ and $x_2 = x_2^*$.

In regression analysis, the term **response variable** is often used in place of the term dependent variable. Furthermore, since the multiple regression equation generates a plane or surface, its graph is called a **response surface**.

---

## 15.5 Testing for Significance

In this section we show how to conduct significance tests for a multiple regression relationship. The significance tests we used in simple linear regression were a t test and an F test. In simple linear regression, both tests provide the same conclusion; that is, if the null hypothesis is rejected, we conclude that $\beta_1 \neq 0$. In multiple regression, the t test and the F test have different purposes.

1. The **F test** is used to determine whether a significant relationship exists between the dependent variable and the set of all the independent variables; we will refer to the F test as the **test for overall significance**.

2. If the F test shows an overall significance, the **t test** is used to determine whether each of the individual independent variables is significant. A separate t test is conducted for each of the independent variables in the model; we refer to each of these t tests as a **test for individual significance**.

In the material that follows, we will explain the F test and the t test and apply each to the Butler Trucking Company example.

### F Test

The multiple regression model as defined in Section 15.4 is:

$$y = \beta_0 + \beta_1x_1 + \beta_2x_2 + \ldots + \beta_px_p + \epsilon$$

The hypotheses for the F test involve the parameters of the multiple regression model.

$$H_0: \beta_1 = \beta_2 = \ldots = \beta_p = 0$$
$$H_a: \text{One or more of the parameters is not equal to zero}$$

If $H_0$ is rejected, the test gives us sufficient statistical evidence to conclude that one or more of the parameters is not equal to zero and that the overall relationship between $y$ and the set of independent variables $x_1, x_2, \ldots, x_p$ is significant. However, if $H_0$ cannot be rejected, we do not have sufficient evidence to conclude that a significant relationship is present.

Before describing the steps of the F test, we need to review the concept of mean square. A **mean square** is a sum of squares divided by its corresponding degrees of freedom. In the multiple regression case, the total sum of squares has $n - 1$ degrees of freedom, the sum of squares due to regression (SSR) has $p$ degrees of freedom, and the sum of squares due to error has $n - p - 1$ degrees of freedom. Hence, the mean square due to regression (MSR) is SSR/$p$ and the mean square due to error (MSE) is SSE/$(n - p - 1)$.

$$MSR = \frac{SSR}{p} \tag{15.12}$$

and

$$MSE = \frac{SSE}{n - p - 1} \tag{15.13}$$

As discussed in Chapter 14, MSE provides an unbiased estimate of $\sigma^2$, the variance of the error term $\epsilon$. If $H_0: \beta_1 = \beta_2 = \ldots = \beta_p = 0$ is true, MSR also provides an unbiased estimate of $\sigma^2$, and the value of MSR/MSE should be close to 1. However, if $H_0$ is false, MSR overestimates $\sigma^2$ and the value of MSR/MSE becomes larger. To determine how large the value of MSR/MSE must be to reject $H_0$, we make use of the fact that if $H_0$ is true and the assumptions about the multiple regression model are valid, the sampling distribution of MSR/MSE is an F distribution with $p$ degrees of freedom in the numerator and $n - p - 1$ in the denominator. A summary of the F test for significance in multiple regression follows.

**F Test for Overall Significance**

$$H_0: \beta_1 = \beta_2 = \ldots = \beta_p = 0$$
$$H_a: \text{One or more of the parameters is not equal to zero}$$

**Test Statistic**

$$F = \frac{MSR}{MSE} \tag{15.14}$$

**Rejection Rule**

- *p-value approach:* Reject $H_0$ if p-value $\leq \alpha$
- *Critical value approach:* Reject $H_0$ if $F \geq F_\alpha$

where $F_\alpha$ is based on an F distribution with $p$ degrees of freedom in the numerator and $n - p - 1$ degrees of freedom in the denominator.

Let us apply the F test to the Butler Trucking Company multiple regression problem. With two independent variables, the hypotheses are written as follows:

$$H_0: \beta_1 = \beta_2 = 0$$
$$H_a: \beta_1 \text{ and/or } \beta_2 \text{ is not equal to zero}$$

Figure 15.6 is the Minitab output for the multiple regression model with miles traveled ($x_1$) and number of deliveries ($x_2$) as the two independent variables. In the analysis of variance part of the output, we see that MSR = 10.8 and MSE = .328. Using equation (15.14), we obtain the test statistic:

$$F = \frac{10.8}{.328} = 32.9$$

Note that the F value on the Minitab output is F = 32.88; the value we calculated differs because we used rounded values for MSR and MSE in the calculation. Using $\alpha = .01$, the p-value = 0.000 in the last column of the analysis of variance table (Figure 15.6) indicates that we can reject $H_0: \beta_1 = \beta_2 = 0$ because the p-value is less than $\alpha = .01$. Alternatively, Table 4 of Appendix B shows that with two degrees of freedom in the numerator and seven degrees of freedom in the denominator, $F_{.01} = 9.55$. With $32.9 > 9.55$, we reject $H_0: \beta_1 = \beta_2 = 0$ and conclude that a significant relationship is present between travel time $y$ and the two independent variables, miles traveled and number of deliveries.

As noted previously, the mean square error provides an unbiased estimate of $\sigma^2$, the variance of the error term $\epsilon$. Referring to Figure 15.6, we see that the estimate of $\sigma^2$ is MSE = .328. The square root of MSE is the estimate of the standard deviation of the error term. As defined in Section 14.5, this standard deviation is called the **standard error of the estimate** and is denoted $s$. Hence, we have $s = \sqrt{MSE} = \sqrt{.328} = .573$. Note that the value of the standard error of the estimate appears in the Minitab output in Figure 15.6.

**Table 15.3: ANOVA Table for a Multiple Regression Model with $p$ Independent Variables**

| Source | Sum of Squares | Degrees of Freedom | Mean Square | F |
|---|---|---|---|---|
| Regression | SSR | $p$ | $MSR = \frac{SSR}{p}$ | $F = \frac{MSR}{MSE}$ |
| Error | SSE | $n - p - 1$ | $MSE = \frac{SSE}{n - p - 1}$ | |
| Total | SST | $n - 1$ | | |

Table 15.3 is the general analysis of variance (ANOVA) table that provides the F test results for a multiple regression model. The value of the F test statistic appears in the last column and can be compared to $F_\alpha$ with $p$ degrees of freedom in the numerator and $n - p - 1$ degrees of freedom in the denominator to make the hypothesis test conclusion. By reviewing the Minitab output for Butler Trucking Company in Figure 15.6, we see that Minitab's analysis of variance table contains this information. Moreover, Minitab also provides the p-value corresponding to the F test statistic.

### t Test

If the F test shows that the multiple regression relationship is significant, a t test can be conducted to determine the significance of each of the individual parameters. The t test for individual significance follows.

**t Test for Individual Significance**

For any parameter $\beta_i$:

$$H_0: \beta_i = 0$$
$$H_a: \beta_i \neq 0$$

**Test Statistic**

$$t = \frac{b_i}{s_{b_i}} \tag{15.15}$$

**Rejection Rule**

- *p-value approach:* Reject $H_0$ if p-value $\leq \alpha$
- *Critical value approach:* Reject $H_0$ if $

## Logistic Regression

The dependent variables x₁, x₂, . . . , xₚ. If the two values of the dependent variable y are coded as 0 or 1, the value of E(y) in equation (15.27) provides the probability that y = 1 given a particular set of values for the study using a random sample of 50 Simmons credit card customers and 50 other customers who do not have a Simmons credit card. Simmons sent the catalog to each of the 100 customers selected. At the end of a test period, Simmons noted whether the customer used the coupon. The sample data for the first 10 catalog recipients are shown in Table 15.11. The amount each customer spent last year at Simmons is shown in thousands of dollars and the credit card information has been coded as 1 if the customer has a Simmons credit card and 0 if not. In the Coupon column, a 1 is recorded if the sampled customer used the coupon and 0 if not.

We might think of building a multiple regression model using the data in Table 15.11 to help Simmons estimate whether a catalog recipient will use the coupon. We would use Annual Spending ($1000) and Simmons Card as independent variables and Coupon as the dependent variable. Because the dependent variable may only assume the values of 0 or 1, however, the ordinary multiple regression model is not applicable. This example shows the type of situation for which logistic regression was developed. Let us see how logistic regression can be used to help Simmons estimate which type of customer is most likely to take advantage of their promotion.

### Logistic Regression Equation

In many ways logistic regression is like ordinary regression. It requires a dependent variable, y, and one or more independent variables. In multiple regression analysis, the mean or expected value of y is referred to as the multiple regression equation.

$$E(y) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p \tag{15.26}$$

In logistic regression, statistical theory as well as practice has shown that the relationship between E(y) and x₁, x₂, . . . , xₚ is better described by the following nonlinear equation.

| Customer | Annual Spending ($1000) | Simmons Card | Coupon |
|----------|------------------------|--------------|--------|
| 1 | 2.291 | 1 | 0 |
| 2 | 3.215 | 1 | 0 |
| 3 | 2.135 | 1 | 0 |
| 4 | 3.924 | 0 | 0 |
| 5 | 2.528 | 1 | 0 |
| 6 | 2.473 | 0 | 1 |
| 7 | 2.384 | 0 | 0 |
| 8 | 7.076 | 0 | 0 |
| 9 | 1.182 | 1 | 1 |
| 10 | 3.345 | 0 | 0 |

**TABLE 15.11** PARTIAL SAMPLE DATA FOR THE SIMMONS STORES EXAMPLE

> **LOGISTIC REGRESSION EQUATION**
> $$E(y) = \frac{e^{\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p}}{1 + e^{\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p}} \tag{15.27}$$

> **INTERPRETATION OF E(y) AS A PROBABILITY IN LOGISTIC REGRESSION**
> $$E(y) = P(y = 1 | x_1, x_2, \ldots, x_p) \tag{15.28}$$

To provide a better understanding of the characteristics of the logistic regression equation, suppose the model involves only one independent variable x and the values of the model parameters are β₀ = −7 and β₁ = 3. The logistic regression equation corresponding to these parameter values is

$$E(y) = P(y = 1 | x) = \frac{e^{-7+3x}}{1 + e^{-7+3x}} \tag{15.29}$$

Figure 15.12 shows a graph of equation (15.29). Note that the graph is S-shaped. The value of E(y) ranges from 0 to 1, with the value of E(y) gradually approaching 1 as the value of x becomes larger and the value of E(y) approaching 0 as the value of x becomes smaller. Note also that the values of E(y), representing probability, increase fairly rapidly as x increases from 2 to 3. The fact that the values of E(y) range from 0 to 1 and that the curve is S-shaped makes equation (15.29) ideally suited to model the probability the dependent variable is equal to 1.

![[Figure 15.12 - S-shaped logistic curve showing E(y) vs Independent Variable (x), with E(y) ranging from 0 to 1.0 on y-axis and x ranging from 0 to 5 on x-axis]]

**FIGURE 15.12** LOGISTIC REGRESSION EQUATION FOR β₀ = −7 AND β₁ = 3

### Estimating the Logistic Regression Equation

In simple linear and multiple regression the least squares method is used to compute b₀, b₁, . . . , bₚ as estimates of the model parameters (β₀, β₁, . . . , βₚ). The nonlinear form of the logistic regression equation makes the method of computing estimates more complex and beyond the scope of this text. We will use computer software to provide the estimates. The estimated logistic regression equation is

> **ESTIMATED LOGISTIC REGRESSION EQUATION**
> $$\hat{y} = \text{estimate of } P(y = 1 | x_1, x_2, \ldots, x_p) = \frac{e^{b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_p x_p}}{1 + e^{b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_p x_p}} \tag{15.30}$$

Here, ŷ provides an estimate of the probability that y = 1 given a particular set of values for the independent variables.

Let us now return to the Simmons Stores example. The variables in the study are defined as follows:

$$y = \begin{cases} 0 & \text{if the customer did not use the coupon} \\ 1 & \text{if the customer used the coupon} \end{cases}$$

$$x_1 = \text{annual spending at Simmons Stores (\$1000s)}$$

$$x_2 = \begin{cases} 0 & \text{if the customer does not have a Simmons credit card} \\ 1 & \text{if the customer has a Simmons credit card} \end{cases}$$

Thus, we choose a logistic regression equation with two independent variables.

$$E(y) = \frac{e^{\beta_0 + \beta_1 x_1 + \beta_2 x_2}}{1 + e^{\beta_0 + \beta_1 x_1 + \beta_2 x_2}} \tag{15.31}$$

Using the sample data (see Table 15.11), Minitab's binary logistic regression procedure was used to compute estimates of the model parameters β₀, β₁, and β₂. A portion of the output obtained is shown in Figure 15.13. We see that b₀ = −2.14637, b₁ = .341643, and b₂ = 1.09873. Thus, the estimated logistic regression equation is

$$\hat{y} = \frac{e^{b_0 + b_1 x_1 + b_2 x_2}}{1 + e^{b_0 + b_1 x_1 + b_2 x_2}} = \frac{e^{-2.14637 + .341643x_1 + 1.09873x_2}}{1 + e^{-2.14637 + .341643x_1 + 1.09873x_2}} \tag{15.32}$$

We can now use equation (15.32) to estimate the probability of using the coupon for a particular type of customer. For example, to estimate the probability of using the coupon for customers who spend $2000 annually and do not have a Simmons credit card, we substitute x₁ = 2 and x₂ = 0 into equation (15.32).

$$\hat{y} = \frac{e^{-2.14637 + .341643(2) + 1.09873(0)}}{1 + e^{-2.14637 + .341643(2) + 1.09873(0)}} = \frac{e^{-1.4631}}{1 + e^{-1.4631}} = \frac{.2315}{1.2315} = .1880$$

Thus, an estimate of the probability of using the coupon for this particular group of customers is approximately 0.19. Similarly, to estimate the probability of using the coupon for customers who spent $2000 last year and have a Simmons credit card, we substitute x₁ = 2 and x₂ = 1 into equation (15.32).

$$\hat{y} = \frac{e^{-2.14637 + .341643(2) + 1.09873(1)}}{1 + e^{-2.14637 + .341643(2) + 1.09873(1)}} = \frac{e^{-.3644}}{1 + e^{-.3644}} = \frac{.6946}{1.6946} = .4099$$

Thus, for this group of customers, the probability of using the coupon is approximately 0.41. It appears that the probability of using the coupon is much higher for customers with a Simmons credit card. Before reaching any conclusions, however, we need to assess the statistical significance of our model.

**Logistic Regression Table**

| Predictor | Coef | SE Coef | Z | p | Odds Ratio | 95% CI Lower | Upper |
|-----------|------|---------|---|---|------------|--------------|-------|
| Constant | -2.14637 | 0.577245 | -3.72 | 0.000 | | | |
| Spending | 0.341643 | 0.128672 | 2.66 | 0.008 | 1.41 | 1.09 | 1.81 |
| Card | 1.09873 | 0.444696 | 2.47 | 0.013 | 3.00 | 1.25 | 7.17 |

Log-Likelihood = -60.487
Test that all slopes are zero: G = 13.628, DF = 2, P-Value = 0.001

**FIGURE 15.13** PARTIAL LOGISTIC REGRESSION OUTPUT FOR THE SIMMONS STORES EXAMPLE

*In the Minitab output, x₁ = Spending and x₂ = Card.*

### Testing for Significance

Testing for significance in logistic regression is similar to testing for significance in multiple regression. First we conduct a test for overall significance. For the Simmons Stores example, the hypotheses for the test of overall significance follow:

$$H_0: \beta_1 = \beta_2 = 0$$
$$H_a: \text{One or both of the parameters is not equal to zero}$$

The test for overall significance is based upon the value of a G test statistic. If the null hypothesis is true, the sampling distribution of G follows a chi-square distribution with degrees of freedom equal to the number of independent variables in the model. Although the computation of G is beyond the scope of the book, the value of G and its corresponding p-value are provided as part of Minitab's binary logistic regression output. Referring to the last line in Figure 15.13, we see that the value of G is 13.628, its degrees of freedom are 2, and its p-value is .001. Thus, at any level of significance α ≥ .001, we would reject the null hypothesis and conclude that the overall model is significant.

If the G test shows an overall significance, a z test can be used to determine whether each of the individual independent variables is making a significant contribution to the overall model. For the independent variables xᵢ, the hypotheses are

$$H_0: \beta_i = 0$$
$$H_a: \beta_i \neq 0$$

If the null hypothesis is true, the value of the estimated coefficient divided by its standard error follows a standard normal probability distribution. The column labeled Z in the Minitab output contains the values of zᵢ = bᵢ/sbᵢ for each of the estimated coefficients and the column labeled p contains the corresponding p-values. Suppose we use α = .05 to test for the significance of the independent variables in the Simmons model. For the independent variable x₁ the z value is 2.66 and the corresponding p-value is .008. Thus, at the .05 level of significance we can reject H₀: β₁ = 0. In a similar fashion we can also reject H₀: β₂ = 0 because the p-value corresponding to z = 2.47 is .013. Hence, at the .05 level of significance, both independent variables are statistically significant.

### Managerial Use

We described how to develop the estimated logistic regression equation and how to test it for significance. Let us now use it to make a decision recommendation concerning the Simmons Stores catalog promotion. For Simmons Stores, we already computed P(y = 1 | x₁ = 2, x₂ = 1) = .4099 and P(y = 1 | x₁ = 2, x₂ = 0) = .1880. These probabilities indicate that for customers with annual spending of $2000 the presence of a Simmons credit card increases the probability of using the coupon. In Table 15.12 we show estimated probabilities for values of annual spending ranging from $1000 to $7000 for both customers who have a Simmons credit card and customers who do not have a Simmons credit card.

| Annual Spending | $1000 | $2000 | $3000 | $4000 | $5000 | $6000 | $7000 |
|-----------------|-------|-------|-------|-------|-------|-------|-------|
| Credit Card Yes | .3305 | .4099 | .4943 | .5791 | .6594 | .7315 | .7931 |
| Credit Card No | .1413 | .1880 | .2457 | .3144 | .3922 | .4759 | .5610 |

**TABLE 15.12** ESTIMATED PROBABILITIES FOR SIMMONS STORES

How can Simmons use this information to better target customers for the new promotion? Suppose Simmons wants to send the promotional catalog only to customers who have a 0.40 or higher probability of using the coupon. Using the estimated probabilities in Table 15.12, Simmons promotion strategy would be:

**Customers who have a Simmons credit card:** Send the catalog to every customer who spent $2000 or more last year.

**Customers who do not have a Simmons credit card:** Send the catalog to every customer who spent $6000 or more last year.

Looking at the estimated probabilities further, we see that the probability of using the coupon for customers who do not have a Simmons credit card but spend $5000 annually is .3922. Thus, Simmons may want to consider revising this strategy by including those customers who do not have a credit card, as long as they spent $5000 or more last year.

### Interpreting the Logistic Regression Equation

Interpreting a regression equation involves relating the independent variables to the business question that the equation was developed to answer. With logistic regression, it is difficult to interpret the relation between the independent variables and the probability that y = 1 directly because the logistic regression equation is nonlinear. However, statisticians have shown that the relationship can be interpreted indirectly using a concept called the **odds ratio**.

The odds in favor of an event occurring is defined as the probability the event will occur divided by the probability the event will not occur. In logistic regression the event of interest is always y = 1. Given a particular set of values for the independent variables, the odds in favor of y = 1 can be calculated as follows:

$$\text{odds} = \frac{P(y = 1 | x_1, x_2, \ldots, x_p)}{P(y = 0 | x_1, x_2, \ldots, x_p)} = \frac{P(y = 1 | x_1, x_2, \ldots, x_p)}{1 - P(y = 1 | x_1, x_2, \ldots, x_p)} \tag{15.33}$$

The odds ratio measures the impact on the odds of a one-unit increase in only one of the independent variables. The odds ratio is the odds that y = 1 given that one of the independent variables has been increased by one unit (odds₁) divided by the odds that y = 1 given no change in the values for the independent variables (odds₀).

> **ODDS RATIO**
> $$\text{Odds Ratio} = \frac{\text{odds}_1}{\text{odds}_0} \tag{15.34}$$

For example, suppose we want to compare the odds of using the coupon for customers who spend $2000 annually and have a Simmons credit card (x₁ = 2 and x₂ = 1) to the odds of using the coupon for customers who spend $2000 annually and do not have a Simmons credit card (x₁ = 2 and x₂ = 0). We are interested in interpreting the effect of a one-unit increase in the independent variable x₂. In this case

$$\text{odds}_1 = \frac{P(y = 1 | x_1 = 2, x_2 = 1)}{1 - P(y = 1 | x_1 = 2, x_2 = 1)}$$

and

$$\text{odds}_0 = \frac{P(y = 1 | x_1 = 2, x_2 = 0)}{1 - P(y = 1 | x_1 = 2, x_2 = 0)}$$

Previously we showed that an estimate of the probability that y = 1 given x₁ = 2 and x₂ = 1 is .4099, and an estimate of the probability that y = 1 given x₁ = 2 and x₂ = 0 is .1880. Thus,

$$\text{estimate of odds}_1 = \frac{.4099}{1 - .4099} = .6946$$

and

$$\text{estimate of odds}_0 = \frac{.1880}{1 - .1880} = .2315$$

The estimated odds ratio is

$$\text{Estimated odds ratio} = \frac{.6946}{.2315} = 3.00$$

Thus, we can conclude that the estimated odds in favor of using the coupon for customers who spent $2000 last year and have a Simmons credit card are 3 times greater than the estimated odds in favor of using the coupon for customers who spent $2000 last year and do not have a Simmons credit card.

The odds ratio for each independent variable is computed while holding all the other independent variables constant. But it does not matter what constant values are used for the other independent variables. For instance, if we computed the odds ratio for the Simmons credit card variable (x₂) using $3000, instead of $2000, as the value for the annual spending variable (x₁), we would still obtain the same value for the estimated odds ratio (3.00). Thus, we can conclude that the estimated odds of using the coupon for customers who have a Simmons credit card are 3 times greater than the estimated odds of using the coupon for customers who do not have a Simmons credit card.

The odds ratio is standard output for logistic regression software packages. Refer to the Minitab output in Figure 15.13. The column with the heading Odds Ratio contains the estimated odds ratios for each of the independent variables. The estimated odds ratio for x₁ is 1.41 and the estimated odds ratio for x₂ is 3.00. We already showed how to interpret the estimated odds ratio for the binary independent variable x₂. Let us now consider the interpretation of the estimated odds ratio for the continuous independent variable x₁.

The value of 1.41 in the Odds Ratio column of the Minitab output tells us that the estimated odds in favor of using the coupon for customers who spent $3000 last year is 1.41 times greater than the estimated odds in favor of using the coupon for customers who spent $2000 last year. Moreover, this interpretation is true for any one-unit change in x₁. For instance, the estimated odds in favor of using the coupon for someone who spent $5000 last year is 1.41 times greater than the odds in favor of using the coupon for a customer who spent $4000 last year. But suppose we are interested in the change in the odds for an increase of more than one unit for an independent variable. Note that x₁ can range from 1 to 7. The odds ratio given by the Minitab output does not answer this question. To answer this question we must explore the relationship between the odds ratio and the regression coefficients.

A unique relationship exists between the odds ratio for a variable and its corresponding regression coefficient. For each independent variable in a logistic regression equation it can be shown that

$$\text{Odds ratio} = e^{\beta_i}$$

To illustrate this relationship, consider the independent variable x₁ in the Simmons example. The estimated odds ratio for x₁ is

$$\text{Estimated odds ratio} = e^{b_1} = e^{.341643} = 1.41$$

Similarly, the estimated odds ratio for x₂ is

$$\text{Estimated odds ratio} = e^{b_2} = e^{1.09873} = 3.00$$

This relationship between the odds ratio and the coefficients of the independent variables makes it easy to compute estimated odds ratios once we develop estimates of the model parameters. Moreover, it also provides us with the ability to investigate changes in the odds ratio of more than or less than one unit for a continuous independent variable.

The odds ratio for an independent variable represents the change in the odds for a one-unit change in the independent variable holding all the other independent variables constant. Suppose that we want to consider the effect of a change of more than one unit, say c units. For instance, suppose in the Simmons example that we want to compare the odds of using the coupon for customers who spend $5000 annually (x₁ = 5) to the odds of using the coupon for customers who spend $2000 annually (x₁ = 2). In this case c = 5 − 2 = 3 and the corresponding estimated odds ratio is

$$e^{c b_1} = e^{3(.341643)} = e^{1.0249} = 2.79$$

This result indicates that the estimated odds of using the coupon for customers who spend $5000 annually is 2.79 times greater than the estimated odds of using the coupon for customers who spend $2000 annually. In other words, the estimated odds ratio for an increase of $3000 in annual spending is 2.79.

In general, the odds ratio enables us to compare the odds for two different events. If the value of the odds ratio is 1, the odds for both events are the same. Thus, if the independent variable we are considering (such as Simmons credit card status) has a positive impact on the probability of the event occurring, the corresponding odds ratio will be greater than 1. Most logistic regression software packages provide a confidence interval for the odds ratio. The Minitab output in Figure 15.13 provides a 95% confidence interval for each of the odds ratios. For example, the point estimate of the odds ratio for x₁ is 1.41 and the 95% confidence interval is 1.09 to 1.81. Because the confidence interval does not contain the value of 1, we can conclude that x₁ has a significant effect on the estimated odds ratio. Similarly, the 95% confidence interval for the odds ratio for x₂ is 1.25 to 7.17. Because this interval does not contain the value of 1, we can also conclude that x₂ has a significant effect on the odds ratio.

### Logit Transformation

An interesting relationship can be observed between the odds in favor of y = 1 and the exponent for e in the logistic regression equation. It can be shown that

$$\ln(\text{odds}) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p$$

This equation shows that the natural logarithm of the odds in favor of y = 1 is a linear function of the independent variables. This linear function is called the **logit**. We will use the notation g(x₁, x₂, . . . , xₚ) to denote the logit.

> **LOGIT**
> $$g(x_1, x_2, \ldots, x_p) = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \ldots + \beta_p x_p \tag{15.35}$$

Substituting g(x₁, x₂, . . . , xₚ) for β₀ + β₁x₁ + β₂x₂ + . . . + βₚxₚ in equation (15.27), we can write the logistic regression equation as

$$E(y) = \frac{e^{g(x_1, x_2, \ldots, x_p)}}{1 + e^{g(x_1, x_2, \ldots, x_p)}} \tag{15.36}$$

Once we estimate the parameters in the logistic regression equation, we can compute an estimate of the logit. Using ĝ(x₁, x₂, . . . , xₚ) to denote the estimated logit, we obtain

> **ESTIMATED LOGIT**
> $$\hat{g}(x_1, x_2, \ldots, x_p) = b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_p x_p \tag{15.37}$$

Thus, in terms of the estimated logit, the estimated regression equation is

$$\hat{y} = \frac{e^{b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_p x_p}}{1 + e^{b_0 + b_1 x_1 + b_2 x_2 + \ldots + b_p x_p}} = \frac{e^{\hat{g}(x_1, x_2, \ldots, x_p)}}{1 + e^{\hat{g}(x_1, x_2, \ldots, x_p)}} \tag{15.38}$$

For the Simmons Stores example, the estimated logit is

$$\hat{g}(x_1, x_2) = -2.14637 + .341643x_1 + 1.09873x_2$$

and the estimated regression equation is

$$\hat{y} = \frac{e^{\hat{g}(x_1, x_2)}}{1 + e^{\hat{g}(x_1, x_2)}} = \frac{e^{-2.14637 + .341643x_1 + 1.09873x_2}}{1 + e^{-2.14637 + .341643x_1 + 1.09873x_2}}$$

Thus, because of the unique relationship between the estimated logit and the estimated logistic regression equation, we can compute the estimated probabilities for Simmons Stores by dividing e^ĝ(x₁,x₂) by 1 + e^ĝ(x₁,x₂).

---

> **NOTES AND COMMENTS**
> 1. Because of the unique relationship between the estimated coefficients in the model and the corresponding odds ratios, the overall test for significance based upon the G statistic is also a test of overall significance for the odds ratios. In addition, the z test for the individual significance of a model parameter also provides a statistical test of significance for the corresponding odds ratio.
> 2. In simple and multiple regression, the coefficient of determination is used to measure the goodness of fit. In logistic regression, no single measure provides a similar interpretation. A discussion of goodness of fit is beyond the scope of our introductory treatment of logistic regression.

---

## Exercises

### Applications

**44.** Refer to the Simmons Stores example introduced in this section. The dependent variable is coded as y = 1 if the customer used the coupon and 0 if not. Suppose that the only information available to help predict whether the customer will use the coupon is the customer's credit card status, coded as x = 1 if the customer has a Simmons credit card and x = 0 if not.

a. Write the logistic regression equation relating x to y.
b. What is the interpretation of E(y) when x = 0?
c. For the Simmons data in Table 15.11, use Minitab to compute the estimated logit.
d. Use the estimated logit computed in part (c) to estimate the probability of using the coupon for customers who do not have a Simmons credit card and to estimate the probability of using the coupon for customers who have a Simmons credit card.
e. What is the estimated odds ratio? What is its interpretation?

**45.** In Table 15.12 we provided estimates of the probability of using the coupon in the Simmons Stores catalog promotion. A different value is obtained for each combination of values for the independent variables.

a. Compute the odds in favor of using the coupon for a customer with annual spending of $4000 who does not have a Simmons credit card (x₁ = 4, x₂ = 0).
b. Use the information in Table 15.12 and part (a) to compute the odds ratio for the Simmons credit card variable x₂ = 0, holding annual spending constant at x₁ = 4.
c. In the text, the odds ratio for the credit card variable was computed using the information in the $2000 column of Table 15.12. Did you get the same value for the odds ratio in part (b)?

**46.** Community Bank would like to increase the number of customers who use payroll direct deposit. Management is considering a new sales campaign that will require each branch manager to call each customer who does not currently use payroll direct deposit. As an incentive to sign up for payroll direct deposit, each customer contacted will be offered free checking for two years. Because of the time and cost associated with the new campaign, management would like to focus their efforts on customers who have the highest probability of signing up for payroll direct deposit. Management believes that the average monthly balance in a customer's checking account may be a useful predictor of whether the customer will sign up for direct payroll deposit. To investigate the relationship between these two variables, Community Bank tried the new campaign using a sample of 50 checking account customers who do not currently use payroll direct deposit. The sample data show the average monthly checking account balance (in hundreds of dollars) and whether the customer contacted signed up for payroll direct deposit (coded 1 if the customer signed up for payroll direct deposit and 0 if not). The data are contained in the data set named Bank; a portion of the data follows.

| Customer | x = Monthly Balance | y = Direct Deposit |
|----------|--------------------|--------------------|
| 1 | 1.22 | 0 |
| 2 | 1.56 | 0 |
| 3 | 2.10 | 0 |
| 4 | 2.25 | 0 |
| 5 | 2.89 | 0 |
| 6 | 3.55 | 0 |
| 7 | 3.56