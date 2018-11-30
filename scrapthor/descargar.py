from requests import get
from bs4 import BeautifulSoup
from re import compile
from aiohttp import ClientSession
from asyncio import sleep
from json import dumps

###Clase  filtros que ayuda a crear un diccionario para la parte de parametros
class  filtros(dict):
    def ig_formato(self,valores:list):
        self['ig_formato']=valores

    def formato(self,valores: list):
        self['formato'] = valores

    def ig_nombre(self,valores: list):
        self['ig_nombre'] = valores

    def nombre(self,valores: list):
        self['nombre'] = valores

    def ig_contenido(self, valores: list):
        self['ig_contenido'] = valores

    def contenido(self,valores: list):
        self['contenido'] = valores

    def ig_todo(self, valores: list):
        self['ig_todo'] = valores

    def todo(self, valores: list):
        self['toddo'] = valores
###Clase con un conjunto de funciones que en si son las encargadas de determinar si un archivo cumple con los requisitos
###del filtro para empezar a ser procesado; True = ignorar ; False = no ignorar
class filtros__:
    def ig_formato(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in nombre.split('.')[-1]:
                return True
        return False

    def formato(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in nombre.split('.')[-1]:
                return False
        return True

    def ig_nombre(nombre:str, contenido, valores: list):
        for valor in valores:
            for parte in nombre.split('.')[:-1]:
                if valor in parte:
                    return True
        return False

    def nombre(nombre:str, contenido, valores: list):
        for valor in valores:
            for parte in nombre.split('.')[:-1]:
                if valor in parte:
                    return False
        return True

    def ig_contenido(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in contenido:
                return True
        return False

    def contenido(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in contenido:
                return False
        return True

    def ig_todo(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in nombre or valor in contenido:
                return True
        return False

    def todo(nombre:str, contenido, valores: list):
        for valor in valores:
            if valor in nombre or valor in contenido:
                return False
        return True

##Funcion
def _formato(x):
    patron = r'(.*)\.\w{2,5}\??'
    r = compile(patron)
    return r.search(x).group().replace('?', '')

###Funcion de filtro (determinar si un archivo se puede procesar o no)
def filtro(nombre, contenido, ignorar: dict,filter=filtros__):
    n = []
    for valor in ignorar.keys():
        n.append(getattr(filter, valor)(nombre, contenido, ignorar[valor]))
    if len(n) == 0:
        return False
    else:
        return any(n)

###funcion que ayuda a la funcion de extraer_nombre para quee asi se pueda determinar que la extension no es
###un dominio web
def __dominios(nombre: str, dominios='org,com,co,net,gov,edu,info,xyz,ly'):
    dominios=dominios.split(',')
    for dominio in dominios:
        if dominio == nombre.split('.')[-1]:
            return False
    return True

###Funcion que se utiliza para sacar el nombre de la carpeta en donde se guardaran los archivos si el resultado del
###archivo es .html, para sacar el nombre y formato del archivo, para sacar el contenido del archivo en si
async def extraer_nombre(url):
    if '.' in url.split('/')[-1] and __dominios(url.split('/')[-1]):
        nombre = _formato(url.split('/')[-1])

        return [None, nombre]
    else:
        await sleep(0.0001)
        nombre = ''.join(caracter if caracter not in ['.', ':', '/', '?'] else '_' for caracter in url)
        archivo = nombre + '.html'
        if 'json' in url:
            archivo = nombre + '.json'
        return [nombre, archivo]

###Funcion creada debido a la poca eficiencia de str.split(), esta version esta optimizada para urls
def __split(s, *quitar):
    for caracter in quitar:
        s = s.replace(caracter, ' ')
    return [x for x in s.split(' ') if x != '']

###Extraer el un link de una linea de texto como entrada
def _sacar_link(linea,r):
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

###Funcion para extraeer todos los links de un archivo html
def _extraer_links(contenido):
    try:
        patron = r'"[(http),(www)]s?\.?(.*)"'
        r= compile(patron)
        links=[]
        soup= BeautifulSoup(contenido,features='html.parser')
        for linea in __split(soup.prettify(),*[',', ' ', ';', '\n']):
            link= _sacar_link(linea,r)
            if link is not None:
                links.append(link)
        return links
    except:
        return []

###Funcion para crear un archivo con el contenido proporcionado por el link
def _crear_archivo(nombre,contenido):
    try:
        with open(nombre,'wb') as archivo:
            archivo.write(contenido)
            archivo.close()
    except Exception as e:
        print(e)

###Funcion para descargar el contenido de un archivo
async def aio_descargar(url):
    try:
        async with ClientSession() as sesion:
            async with sesion.get(url) as data:
                salida= await extraer_nombre(url)
                salida.append(await data.read())
                return salida
    except Exception as e:
        print(e,2)
###Funcion para guardar los links econtrados en un archivo  txt
def _guardar_links(links):
    links='\n'.join(link for link in links)
    with open('lista_links.txt','w') as archivo:
        archivo.write(links)
        archivo.close()
###Funcion para guardar los hashes generados en un archivo json
def _guardar_hashes(hashes):
    hashes=dumps(hashes)
    with open('lista_links.txt','w') as archivo:
        archivo.write(hashes)
        archivo.close()
