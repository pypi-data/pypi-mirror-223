from setuptools import setup

setup(
    name='simple_ts',
    version='0.9.1',
    description='A simple time series analysis package',
    readme = "README.md",
    author='Alisson Louly',
    packages=['simplets'],
    install_requires=['statsmodels', 'matplotlib','pmdarima'],
    long_description="""
                    simple_ts package
                    A simple package for analyze and check time series stationarity.

    Installation

    pip install simple_ts

    Quick Start
    import simplets
    simplets.simple_ts(x, plot= True)
    
    Parameters
    x: array-like
    The time series data.

    plot: bool, default False
    if true, plots the decomposition of the time series.

    *Returns*
    0riginal plot, trend plot, seasonal plot and resid plot for the time series: (optional)
    Summary of Augmented Dickey-Fuller unit root test.
    Summary of Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
    Best ARIMA model for the time series""",
    long_description_content_type='text/markdown'
)