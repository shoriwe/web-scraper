from os.path import abspath, dirname

from setuptools import setup, find_packages

here = abspath(dirname(__file__))
setup(
    name='Scrapthor',
    version='0.4.0',
    author='Antonio Jose Donis Hung',
    author_email='antoniojosedonishung@gmail.com',
    packages=find_packages(),
    scripts=['bin/ejemplo.py'],
    url='https://github.com/walogo/web_scrap',
    license='LICENSE.txt',
    description='Simplificacion de web-scraping\nrequiere beautifulsoup4 y aiohttp\n\nSimple web scraping module to speed up it',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 >= 4.6.3",
        "aiohttp >= 3.4.4"
    ],
)
