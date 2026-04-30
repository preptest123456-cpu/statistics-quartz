---
title: Time Series Analysis and Forecasting
chapter: 17
tags:
  - statistics
  - time_series
  - forecasting
  - trend_analysis
  - seasonality
  - moving_averages
  - exponential_smoothing
  - decomposition
---

# Time Series Analysis and Forecasting

This chapter introduces the fundamental methods of **time series analysis** and **forecasting**. A [[time_series]] is a sequence of observations measured at successive points in time, and the goal is to identify patterns in historical data and extrapolate them into the future.

## 17.1 Time Series Patterns

A [[time_series_plot]] is essential for identifying the underlying pattern in data. The common patterns include:

### Horizontal Pattern

> [!definition]
> A **horizontal pattern** exists when data fluctuate around a constant mean with no systematic increase or decrease over time. Also called a **stationary time series**.

Key characteristics of a stationary time series:
1. The process has a constant mean
2. The variability is constant over time

### Trend Pattern

> [!definition]
> A **trend pattern** shows gradual shifts or movements to relatively higher or lower values over a longer period of time. Usually results from factors like population changes, technology, or consumer preferences.

Trends can be:
- **Linear**: Constant rate of change
- **Nonlinear/Curvilinear**: Rate of change varies (e.g., exponential growth)

### Seasonal Pattern

> [!definition]
> A **seasonal pattern** is a repeating pattern over successive periods of time (typically within one year). Examples include quarterly or monthly fluctuations.

### Trend and Seasonal Pattern

Some time series exhibit both a long-term trend and seasonal fluctuations simultaneously, requiring forecasting methods that handle both components.

### Cyclical Pattern

> [!definition]
> A **cyclical pattern** shows alternating sequences of points below and above the trend line lasting more than one year, often due to business cycles.

---

## 17.2 Forecast Accuracy

### Forecast Error

$$\text{Forecast Error} = \text{Actual Value} - \text{Forecast}$$

### Measures of Forecast Accuracy

1. **Mean Absolute Error (MAE)**
$$\text{MAE} = \frac{\sum_{t=1}^{n} |\text{Forecast Error}_t|}{n}$$

2. **Mean Squared Error (MSE)**
$$\text{MSE} = \frac{\sum_{t=1}^{n} (\text{Forecast Error}_t)^2}{n}$$

3. **Mean Absolute Percentage Error (MAPE)**
$$\text{MAPE} = \frac{\sum_{t=1}^{n} \left|\frac{\text{Forecast Error}_t}{\text{Actual Value}_t}\right| \times 100}{n}$$

> [!definition]
> **MAPE** is preferred when comparing forecasting methods across different time intervals or different time series because it provides a relative measure.

---

## 17.3 Moving Averages and Exponential Smoothing

These are **smoothing methods** appropriate for time series with a horizontal pattern.

### Moving Averages

> [!definition]
> The **moving average** method uses the average of the most recent $k$ data values as the forecast for the next period.

$$F_{t+1} = \frac{Y_t + Y_{t-1} + \cdots + Y_{t-k+1}}{k}$$

where:
- $F_{t+1}$ = forecast for period $t+1$
- $Y_t$ = actual value in period $t$
- $k$ = number of periods in the moving average

### Weighted Moving Averages

Each observation receives a different weight, with more recent observations typically receiving larger weights. The sum of all weights must equal 1.

### Exponential Smoothing

> [!definition]
> **Exponential smoothing** uses a weighted average of past values where weights decrease exponentially for older observations.

$$F_{t+1} = \alpha Y_t + (1 - \alpha) F_t$$

where:
- $\alpha$ = smoothing constant $(0 < \alpha < 1)$
- $F_t$ = forecast for period $t$

Alternative form showing adjustment:
$$F_{t+1} = F_t + \alpha(Y_t - F_t)$$

Key considerations:
- Small $\alpha$: More smoothing, slower response to changes
- Large $\alpha$: Less smoothing, faster response to changes

---

## 17.4 Trend Projection

### Linear Trend Regression

For time series with a linear trend:

$$T_t = b_0 + b_1 t$$

where:
- $T_t$ = trend forecast in period $t$
- $b_0$ = intercept
- $b_1$ = slope
- $t$ = time period

The slope and intercept are computed using:

$$b_1 = \frac{\sum_{t=1}^{n}(t - \bar{t})(Y_t - \bar{Y})}{\sum_{t=1}^{n}(t - \bar{t})^2}$$

$$b_0 = \bar{Y} - b_1 \bar{t}$$

### Holt's Linear Exponential Smoothing

> [!definition]
> **Holt's method** (double exponential smoothing) uses two smoothing constants to handle both level and trend.

$$L_t = \alpha Y_t + (1 - \alpha)(L_{t-1} + b_{t-1})$$
$$b_t = \beta(L_t - L_{t-1}) + (1 - \beta)b_{t-1}$$
$$F_{t+k} = L_t + b_t \cdot k$$

where:
- $\alpha$ = smoothing constant for level
- $\beta$ = smoothing constant for trend
- $L_t$ = estimate of level at period $t$
- $b_t$ = estimate of slope at period $t$

### Nonlinear Trend Regression

**Quadratic Trend:**
$$T_t = b_0 + b_1 t + b_2 t^2$$

**Exponential Trend:**
$$T_t = b_0 (b_1)^t$$

---

## 17.5 Seasonality and Trend

### Seasonality Without Trend

Use [[dummy_variables]] to model seasonal effects:
- For $k$ seasons, use $k-1$ dummy variables
- For quarterly data: 3 dummy variables

$$\hat{Y} = b_0 + b_1 \text{Qtr1} + b_2 \text{Qtr2} + b_3 \text{Qtr3}$$

### Seasonality and Trend

Combine dummy variables with time period:

$$\hat{Y}_t = b_0 + b_1 \text{Qtr1} + b_2 \text{Qtr2} + b_3 \text{Qtr3} + b_4 t$$

For monthly data, 11 dummy variables are needed to represent the 12 months.

---

## 17.6 Time Series Decomposition

> [!definition]
> **Time series decomposition** separates a time series into its trend, seasonal, and irregular components.

### Multiplicative Model

$$Y_t = \text{Trend}_t \times \text{Seasonal}_t \times \text{Irregular}_t$$

### Additive Model

$$Y_t = \text{Trend}_t + \text{Seasonal}_t + \text{Irregular}_t$$

### Calculating Seasonal Indexes

1. Compute **centered moving averages** to identify trend
2. Calculate **seasonal-irregular values**: $\frac{Y_t}{\text{Centered MA}}$
3. Average seasonal-irregular values for each season to get **seasonal indexes**
4. Adjust indexes so they average to 1.00

### Deseasonalizing the Time Series

$$\text{Deseasonalized Value} = \frac{Y_t}{\text{Seasonal Index}}$$

### Forecasting with Decomposition

1. Fit a trend equation to deseasonalized data
2. Compute trend forecasts for future periods
3. Multiply trend forecasts by appropriate seasonal indexes

$$\text{Forecast} = \text{Trend Forecast} \times \text{Seasonal Index}$$

---

## Key Takeaways

- A **time series plot** is the essential first step for identifying patterns (horizontal, trend, seasonal, cyclical)
- **Moving averages** and **exponential smoothing** are effective for horizontal patterns and adapt to level shifts
- **Forecast accuracy** is measured using MAE, MSE, or MAPE; choose the method that minimizes these errors
- **Linear trend regression** fits a straight line when data show consistent growth or decline
- **Holt's linear exponential smoothing** handles both level and trend with two smoothing constants
- **Quadratic** or **exponential** models capture nonlinear trends
- **Dummy variables** in regression handle seasonal effects; use $k-1$ dummies for $k$ seasons
- **Time series decomposition** separates data into trend, seasonal, and irregular components
- **Seasonal indexes** allow deseasonalizing data and making seasonally adjusted forecasts
- The **multiplicative model** is most common in practice when seasonal fluctuations grow with the trend