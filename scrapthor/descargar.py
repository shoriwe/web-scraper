from asyncio import sleep
from re import compile
from aiohttp import ClientSession
from bs4 import BeautifulSoup


# Clase  filtros que ayuda a crear un diccionario para la parte de parametros

# This class help with the creation of the  default dictionary to make a filtering in the scraping
class Parametros(dict):
    # Ignorar el url si 'x'  esta en su formato
    # Ignore url if 'x' in its file format
    def ig_formato(self, valores: list):
        self['ig_formato'] = valores

    # No ignorar el url si 'x' esta en el formato del archivo
    # Do not ignore url if 'x' in file format
    def formato(self, valores: list):
        self['formato'] = valores

    # Ignorar url si 'x' esta en el nombre del archivo
    # Ignore url if 'x' in file name
    def ig_nombre(self, valores: list):
        self['ig_nombre'] = valores

    # No ignorar el url si 'x' esta dentro del nombre
    # Do not ignore the url if 'x' in the file name
    def nombre(self, valores: list):
        self['nombre'] = valores

    # Ignorar url si 'x' esta en el contenido
    # Ignore url if 'x' in content
    def ig_contenido(self, valores: list):
        self['ig_contenido'] = valores

    # No ignorar el url si 'x' esta en el contenido
    # Do not ignorethe url if 'x' in the content
    def contenido(self, valores: list):
        self['contenido'] = valores

    # Ignorar url si 'x'  esta tanto en el nombre como en el contenido del archivo
    # Ignore url if 'x' in the name  or in the content
    def ig_todo(self, valores: list):
        self['ig_todo'] = valores

    # No ignorar url si 'x'  esta nombre o el contendio
    # Do not ignore url if 'x' in the name or the content
    def todo(self, valores: list):
        self['toddo'] = valores


# Clase con un conjunto de funciones que en si son las encargadas de determinar si un archivo cumple con los requisitos
# del filtro para empezar a ser procesado; True = ignorar ; False = no ignorar

# Default class that is used to take all the rules to process the filter statements
class Reglas:
    def ig_formato(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in nombre.split('.')[-1]:
                return True
        return False

    def formato(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in nombre.split('.')[-1]:
                return False
        return True

    def ig_nombre(nombre: str, contenido, valores: list):
        for valor in valores:
            for parte in nombre.split('.')[:-1]:
                if valor in parte:
                    return True
        return False

    def nombre(nombre: str, contenido, valores: list):
        for valor in valores:
            for parte in nombre.split('.')[:-1]:
                if valor in parte:
                    return False
        return True

    def ig_contenido(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in contenido:
                return True
        return False

    def contenido(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in contenido:
                return False
        return True

    def ig_todo(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in nombre or valor in contenido:
                return True
        return False

    def todo(nombre: str, contenido, valores: list):
        for valor in valores:
            if valor in nombre or valor in contenido:
                return False
        return True


##Funcion
def _formato(x):
    patron = r'(.*)\.\w{2,5}\??'
    r = compile(patron)
    return r.search(x).group().replace('?', '')


# Funtion used as filter, anyone can change its default rules
# Funcion de filtro (determinar si un archivo se puede procesar o no)
def filtro(nombre, contenido, parametros: dict, reglas: classmethod):
    n = []
    for valor in parametros.keys():
        n.append(getattr(reglas, valor)(nombre, contenido, parametros[valor]))
    if len(n) == 0:
        return False
    else:
        return any(n)


# This function is used to identify when a url haves at last word a domain
# funcion que ayuda a la funcion de extraer_nombre para quee asi se pueda determinar que la extension no es
# un dominio web
def __dominios(nombre: str, dominios='org,com,co,net,gov,edu,info,xyz,ly'):
    dominios = dominios.split(',')
    for dominio in dominios:
        if dominio == nombre.split('.')[-1]:
            return False
    return True


# This function have the funtion to extract the file_name of a url
# Funcion que se utiliza para sacar el nombre de la carpeta en donde se guardaran los archivos si el resultado del
# archivo es .html, para sacar el nombre y formato del archivo, para sacar el contenido del archivo en si
async def extraer_nombre(url):
    # Identify if the file is html
    if '.' in url.split('/')[-1] and __dominios(url.split('/')[-1]):
        if '?' in url.split('/')[-1]:
            nombre = _formato(url.split('/')[-1])
        else:
            nombre = url.split('/')[-1]

        return [None, nombre]
    # This if the file isn't .html
    else:
        await sleep(0.0001)
        nombre = ''.join(caracter if caracter not in ['.', ':', '/', '?'] else '_' for caracter in url)
        archivo = nombre + '.html'
        if 'json' in url:
            archivo = nombre + '.json'
        return [nombre, archivo]


# Funtion similar to split but better for this program
# Funcion creada debido a la poca eficiencia de str.split(), esta version esta optimizada para urls
def __split(s, *quitar):
    for caracter in quitar:
        s = s.replace(caracter, ' ')
    return [x for x in s.split(' ') if x != '']


# Funtion to extract the link from a line
# Extraer el un link de una linea de texto como entrada
def _sacar_link(linea, r):
    linea = linea.replace('\\', '')
    busqueda = r.search(linea)
    if busqueda != None:
        if '.' in busqueda.group():
            if ':' in busqueda.group() and 'http' not in busqueda.group()[:5]:
                pass
            else:
                link = busqueda.group().replace('"', '')
                if '/' not in link:
                    link += '/'
                return link


# Funtion to extract all the links of a html file
# Funcion para extraeer todos los links de un archivo html
def _extraer_links(contenido):
    try:
        patron = r'"[(http),(www)]s?\.?(.*)"'
        r = compile(patron)
        links = []
        soup = BeautifulSoup(contenido, features='html.parser')
        for linea in __split(soup.prettify(), *[',', ' ', ';', '\n']):
            link = _sacar_link(linea, r)
            if link is not None:
                links.append(link)
        return links
    except:
        return []


# Funtion to make a file with it's content and the name of the function 'extraer_nombre'
# Funcion para crear un archivo con el contenido proporcionado por el link
def _crear_archivo(nombre, contenido, logger):
    try:
        with open(nombre, 'wb') as archivo:
            archivo.write(contenido)
            archivo.close()
        logger.logear('Descargardo {}'.format(__split(nombre, '/', '\\')[-1]))
    except Exception as e:
        logger.logear(e)


# Async funtion to download a url content
# Funcion para descargar el contenido de un archivo
async def aio_descargar(url, logger):
    try:
        async with ClientSession() as sesion:
            async with sesion.get(url) as data:
                salida = await extraer_nombre(url)
                salida.append(await data.read())
                return salida
    except Exception as e:
        logger.logear(e)
