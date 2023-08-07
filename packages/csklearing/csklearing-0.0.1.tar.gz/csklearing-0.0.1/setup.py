from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = """
自己平时会使用的一些统计学和数学模型
"""
LONG_DESCRIPTION = """
目前有两个改进的朴素贝叶斯算法和一个TOPSIS
"""


setup(
    name='csklearing',
    version=VERSION,
    author='Checkey01',
    author_email='Chiaki2048@outlook.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'scikit-learn'],
    keywords=['Machine Learning', 'Python']
)
