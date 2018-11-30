from requests import get
from bs4 import BeautifulSoup
from re import compile

###Clase  filtros que ayuda a crear un diccionario para la parte de parametros
class  filtros(dict):
    def __init__(self):
        pass
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
def __filtro(nombre, contenido, ignorar: dict,filter=filtros__):
    n = []
    for valor in ignorar.keys():
        n.append(getattr(filter, valor)(nombre, contenido, ignorar[valor]))
    if len(n) == 0:
        return False
    else:
        return any(n)

###funcion que ayuda a la funcion de _sacar_nombre_y_contenido para quee asi se pueda determinar que la extension no es
###un dominio web
def __dominios(nombre: str, dominios='org,com,co,net,gov,edu,info,xyz,ly'.split(',')):
    for dominio in dominios:
        if dominio == nombre.split('.')[-1]:
            return False
    return True

###Funcion que se utiliza para sacar el nombre de la carpeta en donde se guardaran los archivos si el resultado del
###archivo es .html, para sacar el nombre y formato del archivo, para sacar el contenido del archivo en si
def _sacar_nombre_y_contenido(url):
    try:
        data = get(url)
        if '.' in url.split('/')[-1] and __dominios(url.split('/')[-1]):
            nombre = _formato(url.split('/')[-1])

            return [None, nombre, data.content]
        else:
            nombre = ''.join(caracter if caracter not in ['.', ':', '/', '?'] else '_' for caracter in url)
            archivo = nombre + '.html'
            if 'json' in url:
                archivo = nombre + '.json'
            return [nombre, archivo, data.content]
    except Exception as e:
        print(e)
        return None

###Funcion creada debido a la poca eficiencia de str.split(), esta version esta optimizada para urls
def __split(s, *quitar):
    for caracter in quitar:
        s = s.replace(caracter, ' ')
    return [x for x in s.split(' ') if x != '']


###Funcion para extraeer todos los links de un archivo html
def _extraer_links(contenido):
    patron = r'"[(http),(www)]s?\.?(.*)"'
    s = BeautifulSoup(contenido, features='html.parser')
    r = compile(patron)
    links = []
    for linea in __split(s.prettify(), *[',', ' ', ';', '\n']):
        linea = linea.replace('\\', '')
        x = r.search(linea)
        if x != None:
            if '.' in x.group():
                if ':' in x.group() and 'http' not in x.group()[:5]:
                    pass
                else:
                    link = x.group().replace('"', '')
                    if '/' not in link:
                        link += '/'
                    links.append(link)
    return links

###Funcion para descargar un archivo
###Esta fucionada con la de filtros para que de esta forma se pueda determinar de una vez si el archivo debe descargarse
def _descargar_archivo(nombre, contenido, ignorar):
    if not __filtro(nombre, contenido, ignorar):
        with open(nombre, 'wb') as file:
            file.write(contenido)
            file.close()
        del file