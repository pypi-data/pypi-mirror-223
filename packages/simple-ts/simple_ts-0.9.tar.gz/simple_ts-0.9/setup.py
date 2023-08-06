from setuptools import setup

setup(
    name='simple_ts',
    version='0.9',
    description='A simple time series analysis package',
    readme = "README.md",
    author='Alisson Louly',
    packages=['simplets'],
    install_requires=['statsmodels', 'matplotlib','pmdarima'],
    long_description="""
                        simple\_ts package

    **Installation**

    pip install simple\_ts

    **Quick Start**
    ```
    simple\_ts(x, plot=False)
    ```

    A simple package for analyze and check time series stationarity.

    *Parameters*

    *x:* array\_like

    The time series data.

    *plot:* bool, default False

    if true, plots the decomposition of the time series.

    *Returns*

    - original plot, trend plot, seasonal plot and resid plot for the time series: (optional)
    - summary of Augmented Dickey-Fuller unit root test.
    - summary of Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
    - best ARIMA model for the time series""",
    long_description_content_type='text/markdown'
)