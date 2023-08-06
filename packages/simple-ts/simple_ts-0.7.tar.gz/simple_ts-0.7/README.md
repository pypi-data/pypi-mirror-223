simple\_ts package

--------------How to install:

pip install simple\_ts

---------------How to use:

simple\_ts(x, plot=False)

A simple package for analyze and check time series stationarity.

Parameters

x: array\_like

The time series data.

plot: bool, default False

if true, plots the decomposition of the time series.

Returns

- original plot, trend plot, seasonal plot and resid plot for the time series: (optional)
- summary of Augmented Dickey-Fuller unit root test.
- summary of Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
- best ARIMA model for the time series
