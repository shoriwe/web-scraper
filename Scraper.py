##Funciones Experimentales (aun no son aptas para usarse  ya que pueden generar  errores)
###-hw
###-multiProcesos

# La funcion 'lineal' es la que debe usarse
# log_file = archivo en donde se podran registrar las cosas que sucedan, None para que la salida se  imprima
# descargar = True para que descarge todos los archivos
# profundidad = la profundidad en la que puede indagar de un sitio web
# archivo = archivo .json donde se guardara el dicionario del mapeo, '' para no escribir ningun archivo

##EJEMPLO##

# url = 'https://en.wikipedia.org/wiki/Roy_Clark'
# descargar = True
# profundidad = 2
# archivo = clark.json
# s = Scraper()
# s.lineal(url,profundidad,descargar,archivo)

import requests
from os import mkdir, getcwd, chdir, listdir
from os.path import join
import bs4
from threading import Thread
from json import dumps
from re import search
from hashlib import sha3_256
from time import sleep


class Scraper:
    def __init__(self, log_file=None):
        # Mapa de el excraping salida
        self.salida = {}
        self.memoria = []
        # logear es un archivo es  posible, solo hace falta poner la ruta de uno txt
        self.log = log_file
        if type(self.log) == str:
            if '/' not in log_file:
                self.log = join(getcwd(), log_file)

    def archivo_repetido(self, nombre):
        memoria = nombre.split('.')
        return '{}_.{}'.format(memoria[0], memoria[1])

    def obtener_nombre_de_url(self, url):
        salida = ''
        for caracter in url:
            if caracter in ['/', ':', '.', '\\']:
                salida += '-'
            else:
                salida += caracter
        return salida

    # Extrae todos los urls del contenido de un html
    def fingerprint(self, nombre, contenido):
        if type(contenido) != bytes:
            contenido = bytes(contenido, 'utf-8')
        return str(sha3_256(bytes(nombre, 'utf-8') + contenido).digest())

    def obtener_links(self, contenido):
        links = []
        for linea in contenido.split('\n'):
            link = self.extraer_url(linea)
            if link != '':
                links.append(link)
        return links

    # Extrae el url de una determinada linea
    def extraer_url(self, linea):
        patron_http = r'https?(://)(.*)'
        extraccion = search(patron_http, linea)
        if extraccion == None:
            patron_www = r'www.(.*)'
            extraccion = search(patron_www, linea)
        salida = ''
        if extraccion != None:
            for caracter in extraccion.group(0):
                if caracter != '"':
                    salida += caracter
                else:
                    return ''.join(x for x in salida if x not in ['\\', '(', ')'])
        return ''

    # Extrae url, nombre, contenido, tipo, links
    def extraeccion(self, url):
        r = requests.get(url)
        tipo = r.headers['Content-Type']
        nombre = '{}.html'.format(self.obtener_nombre_de_url(url))
        links = []
        if 'html' in tipo:
            contenido = bs4.BeautifulSoup(r.content, features='html.parser').prettify()
            links = self.obtener_links(contenido)

        else:
            contenido = r.content
            nombre = url.split('/')[-1]
        return [url, nombre, contenido, tipo, links]

    def descargar(self, nombre, contenido, activado):
        if activado:
            if '?' in nombre:
                nombre = nombre[:list(nombre).index('?')]
            if type(contenido) != bytes:
                contenido = bytes(contenido, 'utf-8')
            try:
                with open(nombre, 'wb') as archivo:
                    archivo.write(contenido)
                    archivo.close()
                salida = '{} descargado\n'.format(nombre)
                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{} descargado\n'.format(nombre))
                    archivo.close()
                else:
                    print(salida, end='')
            except Exception as e:
                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{}\n'.format(e))
                    archivo.close()
                else:
                    print(e, end='')

    # Esta funcion almacena los links extraidos en un diccionario {link_inicial:[tipo,{segundo_link:[tipo,{...:...}],...}
    def mapear(self, data, salida=None, profundidad=2, descargar=True):
        if profundidad > 0:
            ###Archivo para guardar los hash de verificacion
            hash = {}
            archivo = False
            ##Definir el directorio en el que se va a trabajar
            directorio = getcwd()
            if salida == None:
                salida = [data[3], {}]
            if data[1] in listdir(directorio):
                data[1] = self.archivo_repetido(data[1])
            ##Se intenta crear el nuevo directorio con el nombre de la url
            try:
                if data[1].split('.')[-1] == 'html':
                    mkdir(join(directorio, self.obtener_nombre_de_url(data[0])))
                    salida = 'Carpeta {} creada\n'.format(data[0])
                    if type(self.log) == str:
                        archivo = open(self.log, 'a')
                        archivo.write('Carpeta {} creada\n'.format(data[0]))
                        archivo.close()
                    else:
                        print(salida, end='')
            except Exception as e:

                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{}\n'.format(e))
                    archivo.close()
                else:
                    print(e)

            try:
                chdir(join(directorio, self.obtener_nombre_de_url(data[0])))
                directorio_hash = getcwd()
                archivo = open(join(directorio_hash, 'hash.json'), 'w')
            except Exception as e:

                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{}\n'.format(e))
                    archivo.close()
                else:
                    print(e)
            self.descargar(data[1], data[2], descargar)
            hash[data[1]] = self.fingerprint(data[1], data[2])
            if data[1].split('.')[-1] == 'html':
                for url in data[4]:
                    if url != data[0]:
                        try:
                            chdir(join(directorio, self.obtener_nombre_de_url(data[0])))
                        except:
                            pass
                        try:
                            data1 = self.extraeccion(url)
                            self.descargar(data1[1], data1[2], descargar)
                            hash[data1[1]] = self.fingerprint(data1[1], data1[2])
                            memoria = self.mapear(data1, [data1[3], {}], profundidad=profundidad - 1,
                                                  descargar=descargar)
                            salida[1][url] = memoria
                        except Exception as e:

                            if type(self.log) == str:
                                archivo = open(self.log, 'a')
                                archivo.write('{} {}'.format(e, url))
                                archivo.close()
                            else:
                                e = '{} {}'.format(e, url)
                                print(e)
            try:
                archivo.write(dumps(hash))
                archivo.close()
                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{}\n'.format('Hash escrito'))
                    archivo.close()
                else:
                    print('Hash escrito')
            except Exception as e:
                if type(self.log) == str:
                    archivo = open(self.log, 'a')
                    archivo.write('{}\n'.format(e))
                    archivo.close()
                else:
                    print(e)
            return salida

    def lineal(self, url, profundidad, descargar, archivo=''):
        directorio = getcwd()
        data = self.extraeccion(url)
        self.salida[url] = self.mapear(data, profundidad=profundidad, descargar=descargar)
        if archivo != '':
            with open(join(directorio, archivo), 'w') as out:
                out.write(dumps(self.salida))
                out.close()
        return self.salida

    # Estas funciones servirian para mapear el sitio web con la funcion de threading con la cual se analizaria cada
    ##sitio web por separado

    # def  hw(self,url,profundidad,descargar):
    #    #####EXPERIMENTAL
    #    data=self.extraeccion(url)
    #    self.memoria.append([url,self.mapear(data,profundidad=profundidad,descargar=descargar)])
    #
    # def multiProcesos(self, url, profundidad, descarga, archivo=''):
    #    #####EXPERIMENTAL
    #    print('Esto sigue ejecutandose de  forma lineal')
    #    if input('Esto es experimental, quieres seguir "no"')=='':
    #        data=self.extraeccion(url)
    #        salida={url:[data[3],{}]}
    #        for link in data[-1]:
    #            Thread(self.hw(link,profundidad,descarga)).start()
    #        while len(self.memoria) == len(data[-1]):
    #            sleep(1)
    #            print(1)
    #    return self.salida
