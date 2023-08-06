from setuptools import setup

setup(
    name='simple_ts',
    version='0.0.9',
    description='A simple time series analysis package',
    readme = "README",
    author='Alisson Louly',
    packages=['simplets'],
    install_requires=['statsmodels', 'matplotlib','pmdarima']
)