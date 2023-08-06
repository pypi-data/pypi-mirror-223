# newpychromedriver
## Installation:
```
# From PyPI
pip install newpychromedriver
```
## Usage:
```
from selenium import webdriver
from newpychromedriver import chromedriver_path

bs = webdriver.Chrome(executable_path=chromedriver_path)
bs.get('https://www.pypi.org')
```
