# noinspection PyUnresolvedReferences
from scrapthor import scrap

url = 'https://en.wikipedia.org/wiki/Conor_McGregor'  # The url to scrap
speed = 3  # The speed of asyncio (lower = more ssecure for crash) 6 <= hight speed
debug = True  # Debug the operations
debug_file = 'my_debug.txt'  # Out put of the debug, None for print
parameters = {
    'formato': ['html', 'css']}  # Parameters for the filter, in this case only download if the file format == .html
deep = 2  # The max deep of the scraping
download_files = True  # Download files found, if the return of the filter funtion is download, and this is == True,
#  the scrap funtion is going to donwload the file
scrap(url, velocidad=speed, debug=debug, debug_file=debug_file, parametros=parameters, profundidad=deep,
      descargar_archivos=download_files)
