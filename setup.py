from distutils.core import setup

setup(
    name='Scrapthor',
    version='0.1.0',
    author='Antonio Jose Donis Hung',
    author_email='antoniojosedonishung@gmail.com.com',
    packages=['scrapthor'],
    scripts=['bin/ejemplo.py'],
    url='https://github.com/walogo/web_scrap',
    license='LICENSE.txt',
    description='Simplificacion de web-scraping\nrequiere beautifulsoup4 y aiohttp',
    long_description=open('README.txt').read(),
    install_requires=[
        "beautifulsoup4 >= 4.6.3",
        "aiohttp >= 3.4.4"
    ],
)