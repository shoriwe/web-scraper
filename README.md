# Scrapthor

This is a python module to speed up and simplify the web scraping, it can be used to map a web site or to extrack all the information it's
filters can get

## #Quick start

This is one way you can use it
```python
from scrapthor import scrap

url = 'https://en.wikipedia.org/wiki/Conor_McGregor'  # The url to scrap
speed = 3  # The speed of asyncio (lower = more ssecure for crash) 6 <= hight speed
debug = True  # Debug the operations
debug_file = 'my_debug.txt'  # Out put of the debug, None for print
parameters = {'formato': ['html', 'css']}  # Parameters for the filter, in this case only download if the file format == .html
deep = 2  # The max deep of the scraping
download_files = True  # Download files found, if the return of the filter funtion is download, and this is == True,
#  the scrap funtion is going to donwload the file
scrap(url, velocidad=speed, debug=debug, debug_file=debug_file, parametros=parameters, profundidad=deep,
      descargar_archivos=download_files)

```
### #Prerequisites

#### ##You need to install
##### python 3.7.1
##### beautifulsoup4
##### aiohttp

```
pip3 install beautifulsoup4 aiohttp
```

### #Installation

```
git clone <clone_url>
cd web_scrap & python3 setup.py install
```

Also you can copy the scrapthor folder to your site-packages

