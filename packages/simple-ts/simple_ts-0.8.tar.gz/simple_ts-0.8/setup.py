from setuptools import setup

setup(
    name='simple_ts',
    version='0.8',
    description='A simple time series analysis package',
    readme = "README.md",
    author='Alisson Louly',
    packages=['simplets'],
    install_requires=['statsmodels', 'matplotlib','pmdarima']
)