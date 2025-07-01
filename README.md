# Beibo, predict the stock market 💸

<br/>
<br/>

<p align="center">
  <img height="200" src="https://user-images.githubusercontent.com/61618641/147752368-7488930a-49d7-42ae-b14f-50555c5a721e.png" alt="Beibo logo")
</p>

 <br/>
  
<div align="center">
  
![](https://img.shields.io/badge/license-MIT-orange)
![](https://img.shields.io/badge/version-0.1.1-blueviolet)
![](https://img.shields.io/badge/language-python🐍-blue)
![](https://img.shields.io/badge/Open%20source-💜-white)	
[![Quickstart](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dn-JklrtCmALfWYz7uVWywVT4breQxm_?usp=sharing)
  
</div>

<br/>
<br/>

This is a **fork** of the original [Beibo](https://github.com/ssantoshp/Beibo) project by Santosh Passoubady.
  
**Beibo** is a **Python** library that uses several **AI prediction models** to predict **stocks returns** over a defined period of time. 

It was firstly introduced in one of my previous package called [**Empyrial**](https://github.com/ssantoshp/Empyrial). 
  
_Disclaimer: Information is provided 'as is' and solely for informational purposes, not for trading purposes or advice._

---

## What’s new in this fork

This fork includes **bug fixes and improvements** to:

- Fix prediction value extraction and rounding issues  
- Handle yfinance data multi-index column structures  
- Improve compatibility with latest Darts and pandas versions  
- Fix some edge cases causing runtime errors

---

## How to install 📥

```py
pip install yfinance pandas darts matplotlib scikit-learn pmdarima prophet --quiet
```
  
## How to use 💻

  
```py
# Step 2: Download the Beibo fork Python script from GitHub

!wget -q https://raw.githubusercontent.com/iNANOV/Beibo/main/src/beibo.py

# Import the 'oracle' function from the downloaded script dynamically
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("beibo", "./beibo.py")
beibo = importlib.util.module_from_spec(spec)
sys.modules["beibo"] = beibo
spec.loader.exec_module(beibo)

beibo.oracle(
    portfolio=["TSLA", "AAPL", "NVDA", "NFLX"],
    start_date="2020-01-01",
    weights=[0.3, 0.2, 0.3, 0.2],
    prediction_days=30
)
  
```
<br/>

**Output**

<br/>

<p align="center">
  <img height="600" src="https://user-images.githubusercontent.com/61618641/147704638-8713f729-c196-4f13-b9f3-b57709ad7e65.png" alt="Beibo output")
</p>

<br/>

**About Accuracy**
<div align="center">
   
| MAPE  | Interpretation |
| ------------- | ------------- |
| <10  | Highly accurate forecasting 👌  |
| 10-20  | Good forecasting 🆗  |
| 20-50  | Reasonable forecasting 😔  |
| >50  | Inaccurate forecasting 👎 |
	
</div>

 <br/>

**Models available**
  
<div align="center">
   
| Models  | Availability |
| ------------- | ------------- |
| ```Exponential Smoothing```  |  ✅  |
| [```Facebook Prophet```](https://github.com/facebook/prophet)  |  ✅  |
| ```ARIMA```  |  ✅  |
| ```AutoARIMA```  |  ✅  |
| [```Theta```](https://robjhyndman.com/papers/Theta.pdf) |  ✅  |
| [```4 Theta```](https://github.com/Mcompetitions/M4-methods/blob/master/4Theta%20method.R)  |  ✅  |
| ```Fast Fourier Transform``` (FFT)  |  ✅  |
| ```Naive Drift```  |  ✅  |
| ```Naive Mean```  |  ✅  |
| ```Naive Seasonal```  |  ✅  |
	
</div>

  
## Stargazers over time

<div align="center">
	
![追星族的时间](https://starchart.cc/ssantoshp/Beibo.svg)
	
</div>

## Contribution and Issues

Beibo uses GitHub to host its source code.  *Learn more about the [Github flow](https://docs.github.com/en/get-started/quickstart/github-flow).*  

For larger changes (e.g., new feature request, large refactoring), please open an issue to discuss first.  

* If you wish to create a new Issue, then [click here to create a new issue](https://github.com/ssantoshp/Beibo/issues/new/choose).  

Smaller improvements (e.g., document improvements, bugfixes) can be handled by the Pull Request process of GitHub: [pull requests](https://github.com/ssantoshp/Beibo/pulls).  

* To contribute to the code, you will need to do the following:  

 * [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo#forking-a-repository) [Beibo](https://github.com/ssantoshp/Beibo) - Click the **Fork** button at the upper right corner of this page. 
 * [Clone your own fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository).  E.g., ```git clone https://github.com/ssantoshp/Beibo.git```  
  *If your fork is out of date, then will you need to manually sync your fork: [Synchronization method](https://help.github.com/articles/syncing-a-fork/)*
 * [Create a Pull Request](https://github.com/ssantoshp/Beibo/pulls) using **your fork** as the `compare head repository`. 

You contributions will be reviewed, potentially modified, and hopefully merged into Beibo.  

**Contributions of any kind are welcome!**

## Acknowledgments

- [Unit8](https://github.com/unit8co) for [Darts](https://github.com/unit8co/darts)
- [@ranroussi](https://github.com/ranaroussi) for [yfinance](https://github.com/ranaroussi/yfinance) 
- This random guy on Python's Discord server who helped me 
- @devnull10 on Reddit who warned me when I called the package The Oracle

## Contact

You are welcome to contact us by email at **santoshpassoubady@gmail.com** or in Beibo's [discussion space](https://github.com/ssantoshp/Beibo/discussions)

## License

MIT
