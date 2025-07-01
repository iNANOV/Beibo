from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='beibo-fix', 
    version='0.1.3-fix',
    description='🤖 Fork of Beibo: Predict the stock market with AI (includes bug fixes and improvements)',
    py_modules=['beibo'],
    package_dir={'': 'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/iNANOV/Beibo',  
    author="iNANOV",
    author_email="nanov.iliya@gmail.com",
    license='MIT',
    install_requires=[
        'darts',
        'yfinance'
    ],
)
