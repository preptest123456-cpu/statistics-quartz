# Simple Linear Regression

## Statistics in Practice: Alliance Data Systems

Alliance Data Systems (ADS) provides transaction processing, credit services, and marketing services for clients in the rapidly growing customer relationship management (CRM) industry. ADS clients are concentrated in four industries: retail, petroleum/convenience stores, utilities, and transportation. In 1983, Alliance began offering end-to-end credit processing services to the retail, petroleum, and casual dining industries; today they employ more than 6500 employees who provide services to clients around the world. Operating more than 140,000 point-of-sale terminals in the United States alone, ADS processes in excess of 2.5 billion transactions annually. The company ranks second in the United States in private label credit services by representing 49 private label programs with nearly 72 million cardholders. In 2001, ADS made an initial public offering and is now listed on the New York Stock Exchange.

As one of its marketing services, ADS designs direct mail campaigns and promotions. With its database containing information on the spending habits of more than 100 million consumers, ADS can target those consumers most likely to benefit from a direct mail promotion. The Analytical Development Group uses regression analysis to build models that measure and predict the responsiveness of consumers to direct market campaigns. Some regression models predict the probability of purchase for individuals receiving a promotion, and others predict the amount spent by those consumers making a purchase.

For one particular campaign, a retail store chain wanted to attract new customers. To predict the effect of the campaign, ADS analysts selected a sample from the consumer database, sent the sampled individuals promotional materials, and then collected transaction data on the consumers' response. Sample data were collected on the amount of purchase made by the consumers responding to the campaign, as well as a variety of consumer-specific variables thought to be useful in predicting sales. The consumer-specific variable that contributed most to predicting the amount purchased was the total amount of credit purchases at related stores over the past 39 months.

ADS analysts developed an estimated regression equation relating the amount of purchase to the amount spent at related stores:

$$\hat{y} = 26.7 + 0.00205x$$

where:
- $\hat{y}$ = amount of purchase
- $x$ = amount spent at related stores

Using this equation, we could predict that someone spending $10,000 over the past 39 months at related stores would spend $47.20 when responding to the direct mail promotion. In this chapter, you will learn how to develop this type of estimated regression equation.

The final model developed by ADS analysts also included several other variables that increased the predictive power of the preceding equation. Some of these variables included the absence/presence of a bank credit card, estimated income, and the average amount spent per trip at a selected store. In the following chapter, we will learn how such additional variables can be incorporated into a multiple regression model.

---

Managerial decisions often are based on the relationship between two or more variables. For example, after considering the relationship between advertising expenditures and sales, a marketing manager might attempt to predict sales for a given level of advertising expenditures. In another case, a public utility might use the relationship between the daily high temperature and the demand for electricity to predict electricity usage on the basis of next month's anticipated daily high temperatures. Sometimes a manager will rely on intuition to judge how two variables are related. However, if data can be obtained, a statistical procedure called **regression analysis** can be used to develop an equation showing how the variables are related.

In regression terminology, the variable being predicted is called the **dependent variable**. The variable or variables being used to predict the value of the dependent variable are called the **independent variables**. For example, in analyzing the effect of advertising expenditures on sales, a marketing manager's desire to predict sales would suggest making sales the dependent variable. Advertising expenditure would be the independent variable used to help predict sales. In statistical notation, $y$ denotes the dependent variable and $x$ denotes the independent variable.

In this chapter we consider the simplest type of regression analysis involving one independent variable and one dependent variable in which the relationship between the variables is approximated by a straight line. It is called **simple linear regression**. Regression analysis involving two or more independent variables is called **multiple regression analysis**; multiple regression and cases involving curvilinear relationships are covered in Chapters 15 and 16.

## 14.1 Simple Linear Regression Model

Armand's Pizza Parlors is a chain of Italian-food restaurants located in a five-state area. Armand's most successful locations are near college campuses. The managers believe that quarterly sales for these restaurants (denoted by $y$) are related positively to the size of the student population (denoted by $x$); that is, restaurants near campuses with a large student population tend to generate more sales than those located near campuses with a small student population. Using regression analysis, we can develop an equation showing how the dependent variable $y$ is related to the independent variable $x$.

### Regression Model and Regression Equation

In the Armand's Pizza Parlors example, the population consists of all the Armand's restaurants. For every restaurant in the population, there is a value of $x$ (student population) and a corresponding value of $y$ (quarterly sales). The equation that describes how $y$ is related to $x$ and an error term is called the **regression model**. The regression model used in simple linear regression follows.

> **Simple Linear Regression Model**
> $$y = \beta_0 + \beta_1 x + \epsilon \tag{14.1}$$

$\beta_0$ and $\beta_1$ are referred to as the parameters of the model, and $\epsilon$ (the Greek letter epsilon) is a random variable referred to as the **error term**. The error term accounts for the variability in $y$ that cannot be explained by the linear relationship between $x$ and $y$.

The population of all Armand's restaurants can also be viewed as a collection of subpopulations, one for each distinct value of $x$. For example, one subpopulation consists of all Armand's restaurants located near college campuses with 8000 students; another subpopulation consists of all Armand's restaurants located near college campuses with 9000 students; and so on. Each subpopulation has a corresponding distribution of $y$ values. Thus, a distribution of $y$ values is associated with restaurants located near campuses with 8000 students; a distribution of $y$ values is associated with restaurants located near campuses with 9000 students; and so on. Each distribution of $y$ values has its own mean or expected value. The equation that describes how the expected value of $y$, denoted $E(y)$, is related to $x$ is called the **regression equation**. The regression equation for simple linear regression follows.

> **Simple Linear Regression Equation**
> $$E(y) = \beta_0 + \beta_1 x \tag{14.2}$$

The graph of the simple linear regression equation is a straight line; $\beta_0$ is the y-intercept of the regression line, $\beta_1$ is the slope, and $E(y)$ is the mean or expected value of $y$ for a given value of $x$.

Examples of possible regression lines are shown in Figure 14.1. The regression line in Panel A shows that the mean value of $y$ is related positively to $x$, with larger values of $E(y)$ associated with larger values of $x$. The regression line in Panel B shows the mean value of $y$ is related negatively to $x$, with smaller values of $E(y)$ associated with larger values of $x$. The regression line in Panel C shows the case in which the mean value of $y$ is not related to $x$; that is, the mean value of $y$ is the same for every value of $x$.

### Estimated Regression Equation

If the values of the population parameters $\beta_0$ and $\beta_1$ were known, we could use equation (14.2) to compute the mean value of $y$ for a given value of $x$. In practice, the parameter values are not known and must be estimated using sample data. Sample statistics (denoted $b_0$ and $b_1$) are computed as estimates of the population parameters $\beta_0$ and $\beta_1$. Substituting the values of the sample statistics $b_0$ and $b_1$ for $\beta_0$ and $\beta_1$ in the regression equation, we obtain the **estimated regression equation**. The estimated regression equation for simple linear regression follows.

> **Estimated Simple Linear Regression Equation**
> $$\hat{y} = b_0 + b_1 x \tag{14.3}$$

The graph of the estimated simple linear regression equation is called the **estimated regression line**; $b_0$ is the y-intercept and $b_1$ is the slope. In the next section, we show how the least squares method can be used to compute the values of $b_0$ and $b_1$ in the estimated regression equation.

In general, $\hat{y}$ is the point estimator of $E(y)$, the mean value of $y$ for a given value of $x$. Thus, to estimate the mean or expected value of quarterly sales for all restaurants located near campuses with 10,000 students, Armand's would substitute the value of 10,000 for $x$ in equation (14.3). In some cases, however, Armand's may be more interested in predicting sales for one particular restaurant. For example, suppose Armand's would like to predict quarterly sales for the restaurant they are considering building near Talbot College, a school with 10,000 students. As it turns out, the best predictor of $y$ for a given value of $x$ is also provided by $\hat{y}$. Thus, to predict quarterly sales for the restaurant located near Talbot College, Armand's would also substitute the value of 10,000 for $x$ in equation (14.3).

> The value of $\hat{y}$ provides both a point estimate of $E(y)$ for a given value of $x$ and a prediction of an individual value of $y$ for a given value of $x$.

> The estimation of $\beta_0$ and $\beta_1$ is a statistical process much like the estimation of $\mu$ discussed in Chapter 7. $\beta_0$ and $\beta_1$ are the unknown parameters of interest, and $b_0$ and $b_1$ are the sample statistics used to estimate the parameters.

**Notes and Comments:**
1. Regression analysis cannot be interpreted as a procedure for establishing a cause-and-effect relationship between variables. It can only indicate how or to what extent variables are associated with each other. Any conclusions about cause and effect must be based upon the judgment of those individuals most knowledgeable about the application.
2. The regression equation in simple linear regression is $E(y) = \beta_0 + \beta_1 x$. More advanced texts in regression analysis often write the regression equation as $E(y|x) = \beta_0 + \beta_1 x$ to emphasize that the regression equation provides the mean value of $y$ for a given value of $x$.

## 14.2 Least Squares Method

The **least squares method** is a procedure for using sample data to find the estimated regression equation. To illustrate the least squares method, suppose data were collected from a sample of 10 Armand's Pizza Parlor restaurants located near college campuses. For the $i$th observation or restaurant in the sample, $x_i$ is the size of the student population (in thousands) and $y_i$ is the quarterly sales (in thousands of dollars). The values of $x_i$ and $y_i$ for the 10 restaurants in the sample are summarized in Table 14.1. We see that restaurant 1, with $x_1 = 2$ and $y_1 = 58$, is near a campus with 2000 students and has quarterly sales of $58,000. Restaurant 2, with $x_2 = 6$ and $y_2 = 105$, is near a campus with 6000 students and has quarterly sales of $105,000. The largest sales value is for restaurant 10, which is near a campus with 26,000 students and has quarterly sales of $202,000.

**Table 14.1: Student Population and Quarterly Sales Data for 10 Armand's Pizza Parlors**

| Restaurant $i$ | Student Population (1000s) $x_i$ | Quarterly Sales (\$1000s) $y_i$ |
|----------------|----------------------------------|----------------------------------|
| 1 | 2 | 58 |
| 2 | 6 | 105 |
| 3 | 8 | 88 |
| 4 | 8 | 118 |
| 5 | 12 | 117 |
| 6 | 16 | 137 |
| 7 | 20 | 157 |
| 8 | 20 | 169 |
| 9 | 22 | 149 |
| 10 | 26 | 202 |

Figure 14.3 is a scatter diagram of the data in Table 14.1. Student population is shown on the horizontal axis and quarterly sales is shown on the vertical axis. Scatter diagrams for regression analysis are constructed with the independent variable $x$ on the horizontal axis and the dependent variable $y$ on the vertical axis. The scatter diagram enables us to observe the data graphically and to draw preliminary conclusions about the possible relationship between the variables.

What preliminary conclusions can be drawn from Figure 14.3? Quarterly sales appear to be higher at campuses with larger student populations. In addition, for these data the relationship between the size of the student population and quarterly sales appears to be approximated by a straight line; indeed, a positive linear relationship is indicated between $x$ and $y$. We therefore choose the simple linear regression model to represent the relationship between quarterly sales and student population. Given that choice, our next task is to use the sample data in Table 14.1 to determine the values of $b_0$ and $b_1$ in the estimated simple linear regression equation. For the $i$th restaurant, the estimated regression equation provides

$$\hat{y}_i = b_0 + b_1 x_i \tag{14.4}$$

where:
- $\hat{y}_i$ = predicted value of quarterly sales (\$1000s) for the $i$th restaurant
- $b_0$ = the y-intercept of the estimated regression line
- $b_1$ = the slope of the estimated regression line
- $x_i$ = size of the student population (1000s) for the $i$th restaurant

With $y_i$ denoting the observed (actual) sales for restaurant $i$ and $\hat{y}_i$ in equation (14.4) representing the predicted value of sales for restaurant $i$, every restaurant in the sample will have an observed value of sales $y_i$ and a predicted value of sales $\hat{y}_i$. For the estimated regression line to provide a good fit to the data, we want the differences between the observed sales values and the predicted sales values to be small.

The least squares method uses the sample data to provide the values of $b_0$ and $b_1$ that minimize the sum of the squares of the deviations between the observed values of the dependent variable $y_i$ and the predicted values of the dependent variable $\hat{y}_i$. The criterion for the least squares method is given by expression (14.5).

> **Least Squares Criterion**
> $$\min \sum (y_i - \hat{y}_i)^2 \tag{14.5}$$
> 
> where:
> - $y_i$ = observed value of the dependent variable for the $i$th observation
> - $\hat{y}_i$ = predicted value of the dependent variable for the $i$th observation

Differential calculus can be used to show (see Appendix 14.1) that the values of $b_0$ and $b_1$ that minimize expression (14.5) can be found by using equations (14.6) and (14.7).

> **Slope and y-Intercept for the Estimated Regression Equation**
> $$b_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} \tag{14.6}$$
> 
> $$b_0 = \bar{y} - b_1 \bar{x} \tag{14.7}$$
> 
> where:
> - $x_i$ = value of the independent variable for the $i$th observation
> - $y_i$ = value of the dependent variable for the $i$th observation
> - $\bar{x}$ = mean value for the independent variable
> - $\bar{y}$ = mean value for the dependent variable
> - $n$ = total number of observations

An alternate formula for $b_1$ is:
$$b_1 = \frac{\sum x_i y_i - (\sum x_i \sum y_i)/n}{\sum x_i^2 - (\sum x_i)^2/n}$$

This form of equation (14.6) is often recommended when using a calculator to compute $b_1$.

Some of the calculations necessary to develop the least squares estimated regression equation for Armand's Pizza Parlors are shown in Table 14.2. With the sample of 10 restaurants, we have $n = 10$ observations. Because equations (14.6) and (14.7) require $\bar{x}$ and $\bar{y}$, we begin the calculations by computing $\bar{x}$ and $\bar{y}$.

$$\bar{x} = \frac{\sum x_i}{n} = \frac{140}{10} = 14$$

$$\bar{y} = \frac{\sum y_i}{n} = \frac{1300}{10} = 130$$

**Table 14.2: Calculations for the Least Squares Estimated Regression Equation for Armand's Pizza Parlors**

| Restaurant $i$ | $x_i$ | $y_i$ | $x_i - \bar{x}$ | $y_i - \bar{y}$ | $(x_i - \bar{x})(y_i - \bar{y})$ | $(x_i - \bar{x})^2$ |
|----------------|-------|-------|-----------------|-----------------|----------------------------------|---------------------|
| 1 | 2 | 58 | −12 | −72 | 864 | 144 |
| 2 | 6 | 105 | −8 | −25 | 200 | 64 |
| 3 | 8 | 88 | −6 | −42 | 252 | 36 |
| 4 | 8 | 118 | −6 | −12 | 72 | 36 |
| 5 | 12 | 117 | −2 | −13 | 26 | 4 |
| 6 | 16 | 137 | 2 | 7 | 14 | 4 |
| 7 | 20 | 157 | 6 | 27 | 162 | 36 |
| 8 | 20 | 169 | 6 | 39 | 234 | 36 |
| 9 | 22 | 149 | 8 | 19 | 152 | 64 |
| 10 | 26 | 202 | 12 | 72 | 864 | 144 |
| **Totals** | 140 | 1300 | | | 2840 | 568 |

Using equations (14.6) and (14.7) and the information in Table 14.2, we can compute the slope and intercept of the estimated regression equation for Armand's Pizza Parlors. The calculation of the slope ($b_1$) proceeds as follows.

$$b_1 = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2} = \frac{2840}{568} = 5$$

The calculation of the y-intercept ($b_0$) follows.

$$b_0 = \bar{y} - b_1 \bar{x} = 130 - 5(14) = 60$$

Thus, the estimated regression equation is

$$\hat{y} = 60 + 5x$$

Figure 14.4 shows the graph of this equation on the scatter diagram.

The slope of the estimated regression equation ($b_1 = 5$) is positive, implying that as student population increases, sales increase. In fact, we can conclude (based on sales measured in \$1000s and student population in 1000s) that an increase in the student population of 1000 is associated with an increase of \$5000 in expected sales; that is, quarterly sales are expected to increase by \$5 per student.

If we believe the least squares estimated regression equation adequately describes the relationship between $x$ and $y$, it would seem reasonable to use the estimated regression equation to predict the value of $y$ for a given value of $x$. For example, if we wanted to predict quarterly sales for a restaurant to be located near a campus with 16,000 students, we would compute

$$\hat{y} = 60 + 5(16) = 140$$

Hence, we would predict quarterly sales of \$140,000 for this restaurant. In the following sections we will discuss methods for assessing the appropriateness of using the estimated regression equation for estimation and prediction.

> Using the estimated regression equation to make predictions outside the range of the values of the independent variable should be done with caution because outside that range we cannot be sure that the same relationship is valid.

> In computing $b_1$ with a calculator, carry as many significant digits as possible in the intermediate calculations. We recommend carrying at least four significant digits.

**Notes and Comments:**

The least squares method provides an estimated regression equation that minimizes the sum of squared deviations between the observed values of the dependent variable $y_i$ and the predicted values of the dependent variable $\hat{y}_i$. This least squares criterion is used to choose the equation that provides the best fit. If some other criterion were used, such as minimizing the sum of the absolute deviations between $y_i$ and $\hat{y}_i$, a different equation would be obtained. In practice, the least squares method is the most widely used.

## 14.3 Coefficient of Determination

For the Armand's Pizza Parlors example, we developed the estimated regression equation $\hat{y} = 60 + 5x$ to approximate the linear relationship between the size of the student population $x$ and quarterly sales $y$. A question now is: How well does the estimated regression equation fit the data? In this section, we show that the **coefficient of determination** provides a measure of the goodness of fit for the estimated regression equation.

For the $i$th observation, the difference between the observed value of the dependent variable, $y_i$, and the predicted value of the dependent variable, $\hat{y}_i$, is called the $i$th **residual**. The $i$th residual represents the error in using $\hat{y}_i$ to estimate $y_i$. Thus, for the $i$th observation, the residual is $y_i - \hat{y}_i$. The sum of squares of these residuals or errors is the quantity that is minimized by the least squares method. This quantity, also known as the **sum of squares due to error**, is denoted by SSE.

> **Sum of Squares Due to Error**
> $$SSE = \sum (y_i - \hat{y}_i)^2 \tag{14.8}$$

The value of SSE is a measure of the error in using the estimated regression equation to predict the values of the dependent variable in the sample.

In Table 14.3 we show the calculations required to compute the sum of squares due to error for the Armand's Pizza Parlors example. For instance, for restaurant 1 the values of the independent and dependent variables are $x_1 = 2$ and $y_1 = 58$. Using the estimated regression equation, we find that the predicted value of quarterly sales for restaurant 1 is $\hat{y}_1 = 60 + 5(2) = 70$. Thus, the error in using $\hat{y}_1$ to predict $y_1$ for restaurant 1 is $y_1 - \hat{y}_1 = 58 - 70 = -12$. The squared error, $(-12)^2 = 144$, is shown in the last column of Table 14.3. After computing and squaring the residuals for each restaurant in the sample, we sum them to obtain SSE = 1530. Thus, SSE = 1530 measures the error in using the estimated regression equation $\hat{y} = 60 + 5x$ to predict sales.

**Table 14.3: Calculation of SSE for Armand's Pizza Parlors**

| Restaurant $i$ | $x_i$ (Student Pop. 1000s) | $y_i$ (Quarterly Sales \$1000s) | $\hat{y}_i = 60 + 5x_i$ | $y_i - \hat{y}_i$ | $(y_i - \hat{y}_i)^2$ |
|----------------|----------------------------|----------------------------------|-------------------------|-------------------|------------------------|
| 1 | 2 | 58 | 70 | −12 | 144 |
| 2 | 6 | 105 | 90 | 15 | 225 |
| 3 | 8 | 88 | 100 | −12 | 144 |
| 4 | 8 | 118 | 100 | 18 | 324 |
| 5 | 12 | 117 | 120 | −3 | 9 |
| 6 | 16 | 137 | 140 | −3 | 9 |
| 7 | 20 | 157 | 160 | −3 | 9 |
| 8 | 20 | 169 | 160 | 9 | 81 |
| 9 | 22 | 149 | 170 | −21 | 441 |
| 10 | 26 | 202 | 190 | 12 | 144 |
| | | | | | **SSE = 1530** |

Now suppose we are asked to develop an estimate of quarterly sales without knowledge of the size of the student population. Without knowledge of any related variables, we would use the sample mean as an estimate of quarterly sales at any given restaurant. Table 14.2 showed that for the sales data, $\sum y_i = 1300$. Hence, the mean value of quarterly sales for the sample of 10 Armand's restaurants is $\bar{y} = \sum y_i / n = 1300/10 = 130$. In Table 14.4 we show the sum of squared deviations obtained by using the sample mean $\bar{y} = 130$ to predict the value of quarterly sales for each restaurant in the sample. For the $i$th restaurant in the sample, the difference $y_i - \bar{y}$ provides a measure of the error involved in using $\bar{y}$ to predict sales. The corresponding sum of squares, called the **total sum of squares**, is denoted SST.

> **Total Sum of Squares**
> $$SST = \sum (y_i - \bar{y})^2 \tag{14.9}$$

**Table 14.4: Computation of the Total Sum of Squares for Armand's Pizza Parlors**

| Restaurant $i$ | $x_i$ (Student Pop. 1000s) | $y_i$ (Quarterly Sales \$1000s) | $y_i - \bar{y}$ | $(y_i - \bar{y})^2$ |
|----------------|----------------------------|----------------------------------|-----------------|---------------------|
| 1 | 2 | 58 | −72 | 5184 |
| 2 | 6 | 105 | −25 | 625 |
| 3 | 8 | 88 | −42 | 1764 |
| 4 | 8 | 118 | −12 | 144 |
| 5 | 12 | 117 | −13 | 169 |
| 6 | 16 | 137 | 7 | 49 |
| 7 | 20 | 157 | 27 | 729 |
| 8 | 20 | 169 | 39 | 1521 |
| 9 | 22 | 149 | 19 | 361 |
| 10 | 26 | 202 | 72 | 5184 |
| | | | | **SST = 15,730** |

The sum at the bottom of the last column in Table 14.4 is the total sum of squares for Armand's Pizza Parlors; it is SST = 15,730.

In Figure 14.5 we show the estimated regression line $\hat{y} = 60 + 5x$ and the line corresponding to $\bar{y} = 130$. Note that the points cluster more closely around the estimated regression line than they do about the line $\bar{y} = 130$. For example, for the 10th restaurant in the sample we see that the error is much larger when $\bar{y} = 130$ is used to predict $y_{10}$ than when $\hat{y}_{10} = 60 + 5(26) = 190$ is used. We can think of SST as a measure of how well the observations cluster about the $\bar{y}$ line and SSE as a measure of how well the observations cluster about the $\hat{y}$ line.

To measure how much the $\hat{y}$ values on the estimated regression line deviate from $\bar{y}$, another sum of squares is computed. This sum of squares, called the **sum of squares due to regression**, is denoted SSR.

> **Sum of Squares Due to Regression**
> $$SSR = \sum (\hat{y}_i - \bar{y})^2 \tag{14.10}$$

From the preceding discussion, we should expect that SST, SSR, and SSE are related. Indeed, the relationship among these three sums of squares provides one of the most important results in statistics.

> **Relationship Among SST, SSR, and SSE**
> $$SST = SSR + SSE \tag{14.11}$$
> 
> where:
> - SST = total sum of squares
> - SSR = sum of squares due to regression
> - SSE = sum of squares due to error

> SSR can be thought of as the explained portion of SST, and SSE can be thought of as the unexplained portion of SST.

Equation (14.11) shows that the total sum of squares can be partitioned into two components, the sum of squares due to regression and the sum of squares due to error. Hence, if the values of any two of these sum of squares are known, the third sum of squares can be computed easily. For instance, in the Armand's Pizza Parlors example, we already know that SSE = 1530 and SST = 15,730; therefore, solving for SSR in equation (14.11), we find that the sum of squares due to regression is

$$SSR = SST - SSE = 15,730 - 1530 = 14,200$$

Now let us see how the three sums of squares, SST, SSR, and SSE, can be used to provide a measure of the goodness of fit for the estimated regression equation. The estimated regression equation would provide a perfect fit if every value of the dependent variable $y_i$ happened to lie on the estimated regression line. In this case, $y_i - \hat{y}_i$ would be zero for each observation, resulting in SSE = 0. Because SST = SSR + SSE, we see that for a perfect fit SSR must equal SST, and the ratio (SSR/SST) must equal one. Poorer fits will result in larger values for SSE. Solving for SSE in equation (14.11), we see that SSE = SST − SSR. Hence, the largest value for SSE (and hence the poorest fit) occurs when SSR = 0 and SSE = SST.

The ratio SSR/SST, which will take values between zero and one, is used to evaluate the goodness of fit for the estimated regression equation. This ratio is called the **coefficient of determination** and is denoted by $r^2$.

> **Coefficient of Determination**
> $$r^2 = \frac{SSR}{SST} \tag{14.12}$$

For the Armand's Pizza Parlors example, the value of the coefficient of determination is

$$r^2 = \frac{SSR}{SST} = \frac{14,200}{15,730} = .9027$$

When we express the coefficient of determination as a percentage, $r^2

## Exercises continued

The regression equation is
Y = 6.1092 + .8951 X

| Predictor | Coef | SE Coef |
|---|---|---|
| Constant | 6.1092 | 0.9361 |
| X | 0.8951 | 0.1490 |

**Analysis of Variance**

| SOURCE | DF | SS | MS |
|---|---|---|---|
| Regression | 1 | 1575.76 | 1575.76 |
| Residual Error | 8 | 349.14 | 43.64 |
| Total | 9 | 1924.90 | |

a. Write the estimated regression equation.
b. Use a t test to determine whether monthly maintenance expense is related to usage at the .05 level of significance.
c. Use the estimated regression equation to predict monthly maintenance expense for any terminal that is used 25 hours per week.

42. A regression model relating x, number of salespersons at a branch office, to y, annual sales at the office (in thousands of dollars) provided the following computer output from a regression analysis of the data.

The regression equation is
Y = 80.0 + 50.00 X

| Predictor | Coef | SE Coef | T | p |
|---|---|---|---|---|
| Constant | 80.0 | 11.333 | 7.06 | 0.000 |
| X | 50.00 | 5.482 | 9.12 | 0.000 |

**Analysis of Variance**

| SOURCE | DF | SS | MS |
|---|---|---|---|
| Regression | 1 | 6828.6 | 6828.6 |
| Residual Error | 28 | 2298.8 | 82.1 |
| Total | 29 | 9127.4 | |

43. U.S. News & World Report's "America's Best Graduate Schools" listed the following information regarding applicants to top-rated business schools.

| School | Tuition & Fees ($1000s) | Salary & Bonus ($1000s) |
|---|---|---|
| Arizona State University | 28 | 98 |
| Babson College | 35 | 94 |
| Cornell University | 44 | 119 |
| Georgetown University | 40 | 109 |
| Georgia Institute of Technology | 30 | 88 |
| Indiana University—Bloomington | 35 | 105 |
| Michigan State University | 26 | 99 |
| Northwestern University | 44 | 123 |
| Ohio State University | 35 | 97 |
| Purdue University—West Lafayette | 33 | 96 |
| Rice University | 36 | 102 |
| Stanford University | 46 | 135 |
| University of California—Davis | 35 | 89 |
| University of Florida | 23 | 71 |
| University of Iowa | 25 | 78 |
| University of Minnesota—Twin Cities | 37 | 100 |
| University of Notre Dame | 36 | 95 |
| University of Rochester | 38 | 99 |
| University of Washington | 30 | 94 |
| University of Wisconsin—Madison | 27 | 93 |

a. Develop a scatter diagram with salary and bonus as the dependent variable.
b. Does there appear to be any relationship between these variables? Explain.
c. Develop an estimated regression equation that can be used to predict the starting salary and bonus paid to graduates given the cost of out-of-state tuition and fees at the school.
d. Test for a significant relationship at the .05 level of significance. What is your conclusion?
e. Did the estimated regression equation provide a good fit? Explain.
f. Suppose that we randomly select a recent graduate of the University of Virginia graduate school of business. The school has an out-of-state tuition and fees of $43,000. Predict the starting salary and bonus for this graduate.

44. Automobile racing, high-performance driving schools, and driver education programs run by automobile clubs continue to grow in popularity. All these activities require the participant to wear a helmet that is certified by the Snell Memorial Foundation, a not-for-profit organization dedicated to research, education, testing, and development of helmet safety standards. Snell "SA" (Sports Application) rated professional helmets are designed for auto racing and provide extreme impact resistance and high fire protection. One of the key factors in selecting a helmet is weight, since lower weight helmets tend to place less stress on the neck. The following data show the weight and price for 18 SA helmets (SoloRacer website, April 20, 2008).

| Helmet | Weight (oz) | Price ($) |
|---|---|---|
| Pyrotect Pro Airflow | 64 | 248 |
| Pyrotect Pro Airflow Graphics | 64 | 278 |
| RCi Full Face | 64 | 200 |
| RaceQuip RidgeLine | 64 | 200 |
| HJC AR-10 | 58 | 300 |
| HJC Si-12 | 47 | 700 |
| HJC HX-10 | 49 | 900 |
| Impact Racing Super Sport | 59 | 340 |
| Zamp FSA-1 | 66 | 199 |
| Zamp RZ-2 | 58 | 299 |
| Zamp RZ-2 Ferrari | 58 | 299 |
| Zamp RZ-3 Sport | 52 | 479 |
| Zamp RZ-3 Sport Painted | 52 | 479 |
| Bell M2 | 63 | 369 |
| Bell M4 | 62 | 369 |
| Bell M4 Pro | 54 | 559 |
| G Force Pro Force 1 | 63 | 250 |
| G Force Pro Force 1 Grafx | 63 | 280 |

a. Develop a scatter diagram with weight as the independent variable.
b. Does there appear to be any relationship between these two variables?
c. Develop the estimated regression equation that could be used to predict the price given the weight.
d. Test for the significance of the relationship at the .05 level of significance.
e. Did the estimated regression equation provide a good fit? Explain.

---

## 14.8 Residual Analysis: Validating Model Assumptions

As we noted previously, the residual for observation i is the difference between the observed value of the dependent variable ($y_i$) and the predicted value of the dependent variable ($\hat{y}_i$).

> Residual analysis is the primary tool for determining whether the assumed regression model is appropriate.

### Residual for Observation i

$$y_i - \hat{y}_i \tag{14.28}$$

where
- $y_i$ is the observed value of the dependent variable
- $\hat{y}_i$ is the predicted value of the dependent variable

In other words, the ith residual is the error resulting from using the estimated regression equation to predict the value of the dependent variable. The residuals for the Armand's Pizza Parlors example are computed in Table 14.7. The observed values of the dependent variable are in the second column and the predicted values of the dependent variable, obtained using the estimated regression equation $\hat{y} = 60 + 5x$, are in the third column. An analysis of the corresponding residuals in the fourth column will help determine whether the assumptions made about the regression model are appropriate.

Let us now review the regression assumptions for the Armand's Pizza Parlors example. A simple linear regression model was assumed.

$$y = \beta_0 + \beta_1 x + \varepsilon \tag{14.29}$$

This model indicates that we assumed quarterly sales (y) to be a linear function of the size of the student population (x) plus an error term ε. In Section 14.4 we made the following assumptions about the error term ε.

1. E(ε) = 0.
2. The variance of ε, denoted by σ², is the same for all values of x.
3. The values of ε are independent.
4. The error term ε has a normal distribution.

These assumptions provide the theoretical basis for the t test and the F test used to determine whether the relationship between x and y is significant, and for the confidence and prediction interval estimates presented in Section 14.6. If the assumptions about the error term ε appear questionable, the hypothesis tests about the significance of the regression relationship and the interval estimation results may not be valid.

The residuals provide the best information about ε; hence an analysis of the residuals is an important step in determining whether the assumptions for ε are appropriate. Much of residual analysis is based on an examination of graphical plots. In this section, we discuss the following residual plots.

1. A plot of the residuals against values of the independent variable x
2. A plot of residuals against the predicted values of the dependent variable $\hat{y}$
3. A standardized residual plot
4. A normal probability plot

**Table 14.7: Residuals for Armand's Pizza Parlors**

| Student Population $x_i$ | Sales $y_i$ | Predicted Sales $\hat{y}_i = 60 + 5x_i$ | Residuals $y_i - \hat{y}_i$ |
|---|---|---|---|
| 2 | 58 | 70 | −12 |
| 6 | 105 | 90 | 15 |
| 8 | 88 | 100 | −12 |
| 8 | 118 | 100 | 18 |
| 12 | 117 | 120 | −3 |
| 16 | 137 | 140 | −3 |
| 20 | 157 | 160 | −3 |
| 20 | 169 | 160 | 9 |
| 22 | 149 | 170 | −21 |
| 26 | 202 | 190 | 12 |

### Residual Plot Against x

A residual plot against the independent variable x is a graph in which the values of the independent variable are represented by the horizontal axis and the corresponding residual values are represented by the vertical axis. A point is plotted for each residual. The first coordinate for each point is given by the value of $x_i$ and the second coordinate is given by the corresponding value of the residual $y_i - \hat{y}_i$. For a residual plot against x with the Armand's Pizza Parlors data from Table 14.7, the coordinates of the first point are (2, −12), corresponding to $x_1 = 2$ and $y_1 - \hat{y}_1 = -12$; the coordinates of the second point are (6, 15), corresponding to $x_2 = 6$ and $y_2 - \hat{y}_2 = 15$; and so on. Figure 14.11 shows the resulting residual plot.

Before interpreting the results for this residual plot, let us consider some general patterns that might be observed in any residual plot. Three examples appear in Figure 14.12.

If the assumption that the variance of ε is the same for all values of x and the assumed regression model is an adequate representation of the relationship between the variables, the residual plot should give an overall impression of a horizontal band of points such as the one in Panel A of Figure 14.12. However, if the variance of ε is not the same for all values of x—for example, if variability about the regression line is greater for larger values of x—a pattern such as the one in Panel B of Figure 14.12 could be observed. In this case, the assumption of a constant variance of ε is violated. Another possible residual plot is shown in Panel C. In this case, we would conclude that the assumed regression model is not an adequate representation of the relationship between the variables. A curvilinear regression model or multiple regression model should be considered.

Now let us return to the residual plot for Armand's Pizza Parlors shown in Figure 14.11. The residuals appear to approximate the horizontal pattern in Panel A of Figure 14.12. Hence, we conclude that the residual plot does not provide evidence that the assumptions made for Armand's regression model should be challenged. At this point, we are confident in the conclusion that Armand's simple linear regression model is valid.

Experience and good judgment are always factors in the effective interpretation of residual plots. Seldom does a residual plot conform precisely to one of the patterns in Figure 14.12. Yet analysts who frequently conduct regression studies and frequently review residual plots become adept at understanding the differences between patterns that are reasonable and patterns that indicate the assumptions of the model should be questioned. A residual plot provides one technique to assess the validity of the assumptions for a regression model.

### Residual Plot Against $\hat{y}$

Another residual plot represents the predicted value of the dependent variable on the horizontal axis and the residual values on the vertical axis. A point is plotted for each residual. The first coordinate for each point is given by $\hat{y}_i$ and the second coordinate is given by the corresponding value of the ith residual $y_i - \hat{y}_i$. With the Armand's data from Table 14.7, the coordinates of the first point are (70, −12), corresponding to $\hat{y}_1 = 70$ and $y_1 - \hat{y}_1 = -12$; the coordinates of the second point are (90, 15); and so on. Figure 14.13 provides the residual plot.

Note that the pattern of this residual plot is the same as the pattern of the residual plot against the independent variable x. It is not a pattern that would lead us to question the model assumptions. For simple linear regression, both the residual plot against x and the residual plot against $\hat{y}$ provide the same pattern. For multiple regression analysis, the residual plot against $\hat{y}$ is more widely used because of the presence of more than one independent variable.

### Standardized Residuals

Many of the residual plots provided by computer software packages use a standardized version of the residuals. As demonstrated in preceding chapters, a random variable is standardized by subtracting its mean and dividing the result by its standard deviation. With the least squares method, the mean of the residuals is zero. Thus, simply dividing each residual by its standard deviation provides the standardized residual.

It can be shown that the standard deviation of residual i depends on the standard error of the estimate s and the corresponding value of the independent variable $x_i$.

#### Standard Deviation of the ith Residual

$$s_{y_i - \hat{y}_i} = s\sqrt{1 - h_i} \tag{14.30}$$

Note that equation (14.30) shows that the standard deviation of the ith residual depends on $x_i$ because of the presence of $h_i$ in the formula.

where

$$h_i = \frac{1}{n} + \frac{(x_i - \bar{x})^2}{\sum(x_i - \bar{x})^2} \tag{14.31}$$

- s = the standard error of the estimate
- $s_{y_i - \hat{y}_i}$ = the standard deviation of residual i

Once the standard deviation of each residual is calculated, we can compute the standardized residual by dividing each residual by its corresponding standard deviation.

#### Standardized Residual for Observation i

$$\frac{y_i - \hat{y}_i}{s_{y_i - \hat{y}_i}} \tag{14.32}$$

> Small departures from normality do not have a great effect on the statistical tests used in regression analysis.

Table 14.8 shows the calculation of the standardized residuals for Armand's Pizza Parlors. Recall that previous calculations showed s = 13.829. Figure 14.14 is the plot of the standardized residuals against the independent variable x.

**Table 14.8: Computation of Standardized Residuals for Armand's Pizza Parlors**

| Restaurant i | $x_i$ | $x_i - \bar{x}$ | $(x_i - \bar{x})^2$ | $\frac{(x_i - \bar{x})^2}{\sum(x_i - \bar{x})^2}$ | $h_i$ | $s_{y_i - \hat{y}_i}$ | Residual $y_i - \hat{y}_i$ | Standardized Residual |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 | −12 | 144 | .2535 | .3535 | 11.1193 | −12 | −1.0792 |
| 2 | 6 | −8 | 64 | .1127 | .2127 | 12.2709 | 15 | 1.2224 |
| 3 | 8 | −6 | 36 | .0634 | .1634 | 12.6493 | −12 | −.9487 |
| 4 | 8 | −6 | 36 | .0634 | .1634 | 12.6493 | 18 | 1.4230 |
| 5 | 12 | −2 | 4 | .0070 | .1070 | 13.0682 | −3 | −.2296 |
| 6 | 16 | 2 | 4 | .0070 | .1070 | 13.0682 | −3 | −.2296 |
| 7 | 20 | 6 | 36 | .0634 | .1634 | 12.6493 | −3 | −.2372 |
| 8 | 20 | 6 | 36 | .0634 | .1634 | 12.6493 | 9 | .7115 |
| 9 | 22 | 8 | 64 | .1127 | .2127 | 12.2709 | −21 | −1.7114 |
| 10 | 26 | 12 | 144 | .2535 | .3535 | 11.1193 | 12 | 1.0792 |
| Total | | | 568 | | | | | |

*Note: The values of the residuals were computed in Table 14.7.*

The standardized residual plot can provide insight about the assumption that the error term ε has a normal distribution. If this assumption is satisfied, the distribution of the standardized residuals should appear to come from a standard normal probability distribution. Thus, when looking at a standardized residual plot, we should expect to see approximately 95% of the standardized residuals between −2 and +2. We see in Figure 14.14 that for the Armand's example all standardized residuals are between −2 and +2. Therefore, on the basis of the standardized residuals, this plot gives us no reason to question the assumption that ε has a normal distribution.

Because of the effort required to compute the estimated values of $\hat{y}$, the residuals, and the standardized residuals, most statistical packages provide these values as optional regression output. Hence, residual plots can be easily obtained. For large problems computer packages are the only practical means for developing the residual plots discussed in this section.

### Normal Probability Plot

Another approach for determining the validity of the assumption that the error term has a normal distribution is the normal probability plot. To show how a normal probability plot is developed, we introduce the concept of normal scores.

Suppose 10 values are selected randomly from a normal probability distribution with a mean of zero and a standard deviation of one, and that the sampling process is repeated over and over with the values in each sample of 10 ordered from smallest to largest. For now, let us consider only the smallest value in each sample. The random variable representing the smallest value obtained in repeated sampling is called the first-order statistic.

Statisticians show that for samples of size 10 from a standard normal probability distribution, the expected value of the first-order statistic is −1.55. This expected value is called a normal score. For the case with a sample of size n = 10, there are 10 order statistics and 10 normal scores (see Table 14.9). In general, a data set consisting of n observations will have n order statistics and hence n normal scores.

**Table 14.9: Normal Scores for n = 10**

| Order Statistic | Normal Score |
|---|---|
| 1 | −1.55 |
| 2 | −1.00 |
| 3 | −.65 |
| 4 | −.37 |
| 5 | −.12 |
| 6 | .12 |
| 7 | .37 |
| 8 | .65 |
| 9 | 1.00 |
| 10 | 1.55 |

Let us now show how the 10 normal scores can be used to determine whether the standardized residuals for Armand's Pizza Parlors appear to come from a standard normal probability distribution. We begin by ordering the 10 standardized residuals from Table 14.8. The 10 normal scores and the ordered standardized residuals are shown together in Table 14.10. If the normality assumption is satisfied, the smallest standardized residual should be close to the smallest normal score, the next smallest standardized residual should be close to the next smallest normal score, and so on. If we were to develop a plot with the normal scores on the horizontal axis and the corresponding standardized residuals on the vertical axis, the plotted points should cluster closely around a 45-degree line passing through the origin if the standardized residuals are approximately normally distributed. Such a plot is referred to as a normal probability plot.

**Table 14.10: Normal Scores and Ordered Standardized Residuals for Armand's Pizza Parlors**

| Normal Scores | Ordered Standardized Residuals |
|---|---|
| −1.55 | −1.7114 |
| −1.00 | −1.0792 |
| −.65 | −.9487 |
| −.37 | −.2372 |
| −.12 | −.2296 |
| .12 | −.2296 |
| .37 | .7115 |
| .65 | 1.0792 |
| 1.00 | 1.2224 |
| 1.55 | 1.4230 |

Figure 14.15 is the normal probability plot for the Armand's Pizza Parlors example. Judgment is used to determine whether the pattern observed deviates from the line enough to conclude that the standardized residuals are not from a standard normal probability distribution. In Figure 14.15, we see that the points are grouped closely about the line. We therefore conclude that the assumption of the error term having a normal probability distribution is reasonable. In general, the more closely the points are clustered about the 45-degree line, the stronger the evidence supporting the normality assumption. Any substantial curvature in the normal probability plot is evidence that the residuals have not come from a normal distribution. Normal scores and the associated normal probability plot can be obtained easily from statistical packages such as Minitab.

> **Notes and Comments**
> 
> 1. We use residual and normal probability plots to validate the assumptions of a regression model. If our review indicates that one or more assumptions are questionable, a different regression model or a transformation of the data should be considered. The appropriate corrective action when the assumptions are violated must be based on good judgment; recommendations from an experienced statistician can be valuable.
> 
> 2. Analysis of residuals is the primary method statisticians use to verify that the assumptions associated with a regression model are valid. Even if no violations are found, it does not necessarily follow that the model will yield good predictions. However, if additional statistical tests support the conclusion of significance and the coefficient of determination is large, we should be able to develop good estimates and predictions using the estimated regression equation.

---

## Exercises

### Methods

45. Given are data for two variables, x and y.

| $x_i$ | 6 | 11 | 15 | 18 | 20 |
|---|---|---|---|---|---|
| $y_i$ | 6 | 8 | 12 | 20 | 30 |

a. Develop an estimated regression equation for these data.
b. Compute the residuals.
c. Develop a plot of the residuals against the independent variable x. Do the assumptions about the error terms seem to be satisfied?
d. Compute the standardized residuals.
e. Develop a plot of the standardized residuals against $\hat{y}$. What conclusions can you draw from this plot?

46. The following data were used in a regression study.

| Observation | $x_i$ | $y_i$ | Observation | $x_i$ | $y_i$ |
|---|---|---|---|---|---|
| 1 | 2 | 4 | 6 | 7 | 6 |
| 2 | 3 | 5 | 7 | 7 | 9 |
| 3 | 4 | 4 | 8 | 8 | 5 |
| 4 | 5 | 6 | 9 | 9 | 11 |
| 5 | 7 | 4 | | | |

a. Develop an estimated regression equation for these data.
b. Construct a plot of the residuals. Do the assumptions about the error term seem to be satisfied?

### Applications

47. Data on advertising expenditures and revenue (in thousands of dollars) for the Four Seasons Restaurant follow.

| Advertising Expenditures | Revenue |
|---|---|
| 1 | 19 |
| 2 | 32 |
| 4 | 44 |
| 6 | 40 |
| 10 | 52 |
| 14 | 53 |
| 20 | 54 |

a. Let x equal advertising expenditures and y equal revenue. Use the method of least squares to develop a straight line approximation of the relationship between the two variables.
b. Test whether revenue and advertising expenditures are related at a .05 level of significance.
c. Prepare a residual plot of $y - \hat{y}$ versus $\hat{y}$. Use the result from part (a) to obtain the values of $\hat{y}$.
d. What conclusions can you draw from residual analysis? Should this model be used, or should we look for a better one?

48. Refer to exercise 7, where an estimated regression equation relating years of experience and annual sales was developed.

a. Compute the residuals and construct a residual plot for this problem.
b. Do the assumptions about the error terms seem reasonable in light of the residual plot?

49. Recent family home sales in San Antonio provided the following data (San Antonio Realty Watch website, November 2008).

| Square Footage | Price ($) |
|---|---|
| 1580 | 142,500 |
| 1572 | 145,000 |
| 1352 | 115,000 |
| 2224 | 155,900 |
| 1556 | 95,000 |
| 1435 | 128,000 |
| 1438 | 100,000 |
| 1089 | 55,000 |
| 1941 | 142,000 |
| 1698 | 115,000 |
| 1539 | 115,000 |
| 1364 | 105,000 |
| 1979 | 155,000 |
| 2183 | 132,000 |
| 2096 | 140,000 |
| 1400 | 85,000 |
| 2372 | 145,000 |
| 1752 | 155,000 |
| 1386 | 80,000 |
| 1163 | 100,000 |

a. Develop the estimated regression equation that can be used to predict the sales prices given the square footage.
b. Construct a residual plot of the standardized residuals against the independent variable.
c. Do the assumptions about the error term and model form seem reasonable in light of the residual plot?

---

## 14.9 Residual Analysis: Outliers and Influential Observations

In Section 14.8 we showed how residual analysis could be used to determine when violations of assumptions about the regression model occur. In this section, we discuss how residual analysis can be used to identify observations that can be classified as outliers or as being especially influential in determining the estimated regression equation. Some steps that should be taken when such observations occur are discussed.

### Detecting Outliers

Figure 14.16 is a scatter diagram for a data set that contains an outlier, a data point (observation) that does not fit the trend shown by the remaining data. Outliers represent observations that are suspect and warrant careful examination. They may represent erroneous data; if so, the data should be corrected. They may signal a violation of model assumptions; if so, another model should be considered. Finally, they may simply be unusual values that occurred by chance. In this case, they should be retained.

To illustrate the process of detecting outliers, consider the data set in Table 14.11; Figure 14.17 is a scatter diagram. Except for observation 4 ($x_4 = 3$, $y_4 = 75$), a pattern suggesting a negative linear relationship is apparent. Indeed, given the pattern of the rest of the data, we would expect $y_4$ to be much smaller and hence would identify the corresponding observation as an outlier. For the case of simple linear regression, one can often detect outliers by simply examining the scatter diagram.

**Table 14.11: Data Set Illustrating the Effect of an Outlier**

| $x_i$ | $y_i$ |
|---|---|
| 1 | 45 |
| 1 | 55 |
| 2 | 50 |
| 3 | 75 |
| 3 | 40 |
| 3 | 45 |
| 4 | 30 |
| 4 | 35 |
| 5 | 25 |
| 6 | 15 |

The standardized residuals can also be used to identify outliers. If an observation deviates greatly from the pattern of the rest of the data (e.g., the outlier in Figure 14.16), the corresponding standardized residual will be large in absolute value. Many computer packages automatically identify observations with standardized residuals that are large in absolute value. In Figure 14.18 we show the Minitab output from a regression analysis of the data in Table 14.11. The next to last line of the output shows that the standardized residual for observation 4 is 2.67. Minitab provides a list of each observation with a standardized residual of less than −2 or greater than +2 in the Unusual Observation section of the output; in such cases, the observation is printed on a separate line with an R next to the standardized residual, as shown in Figure 14.18. With normally distributed errors, standardized residuals should be outside these limits approximately 5% of the time.

**Figure 14.18: Minitab Output for Regression Analysis of the Outlier Data Set**

```
The regression equation is
y = 65.0 - 7.33 x

Predictor    Coef  SE Coef      T      p
Constant   64.958    9.258   7.02  0.000
X          -7.331    2.608  -2.81  0.023

S = 12.6704   R-Sq = 49.7%   R-Sq(adj) = 43.4%

Analysis of Variance
SOURCE          DF      SS      MS     F      p
Regression       1  1268.2  1268.2  7.90  0.023
Residual Error   8  1284.3   160.5
Total            9  2552.5

Unusual Observations
Obs     x      y    Fit  SE Fit  Residual  St Resid
4  3.00  75.00  42.97    4.04     32.03      2.67R

R denotes an observation with a large standardized residual.
```

In deciding how to handle an outlier, we should first check to see whether it is a valid observation. Perhaps an error was made in initially recording the data or in entering the data into the computer file. For example, suppose that in checking the data for the outlier in Table 14.17, we find an error; the correct value for observation 4 is $x_4 = 3$, $y_4 = 30$. Figure 14.19 is the