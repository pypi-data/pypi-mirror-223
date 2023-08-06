# newpychromedriver

fork [pychromedriver](https://github.com/parklam/pychromedriver), 
but support chrome 115.0 or newer versions

update: every day 00:00:00

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
