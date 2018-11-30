from os import mkdir, chdir, getcwd, listdir
from os.path import join
from asyncio import get_event_loop, sleep, wait
from .criptografia import fingerprint
from .descargar import _extraer_links,__filtro,_descargar_archivo,_sacar_nombre_y_contenido
from json import dumps

###Funcion para escribir hash en un archivo
def _escribir_hash(hashes, directorio):
    chdir(directorio)
    archivo = open(join(directorio, 'hashes.json'), 'w')
    archivo.write(dumps(hashes))
    archivo.close()

###Funcion para escribir los links que se hayan encontrado en un archivo txt
def _guardar_links(links):
    with open('__links__locales.txt', 'w') as archivo:
        try:
            archivo.write('\n'.join(link for link in links))
            archivo.close()
        except:
            archivo.close()

###Funcion que analiza un link para luego extraerle el hash,, descargarlo o determinar los links que tiene
async def mapear(url, informacion, profundidad, parametros, download, guardar_links, guardar_hashes):
    hashes = {}
    try:
        if profundidad > 0:
            directorio = join(getcwd(), informacion[0])
            try:
                mkdir(directorio)
            except Exception as e:
                print(e)
            try:
                chdir(directorio)
            except Exception as e:
                print(e)
            try:
                links = _extraer_links(informacion[2])
            except:
                links = []
            try:
                if guardar_hashes and __filtro(informacion[1], informacion[2], parametros):
                    hashes[informacion[1]] = fingerprint(informacion[1], informacion[2], True)
            except:
                pass
            try:
                if download and informacion[1] not in listdir(getcwd()):
                    _descargar_archivo(informacion[1], informacion[2], parametros)
            except:
                pass
            if guardar_links:
                _guardar_links(links)
            for link in links:
                if link != url:
                    chdir(directorio)
                    informacion = _sacar_nombre_y_contenido(link)
                    try:
                        hashes[informacion[1]] = fingerprint(informacion[1], informacion[2], True)
                    except Exception as e:
                        print(e)
                    if informacion == None:
                        print('Intentanto {}'.format('{}/{}'.format(url, link.replace('/', ''))))
                        informacion = _sacar_nombre_y_contenido('{}/{}'.format(url, link.replace('/', '')))
                    await sleep(0.001)
                    try:

                        if download and (informacion[1] not in listdir(getcwd())):
                            _descargar_archivo(informacion[1], informacion[2], parametros)
                    except:
                        pass
                    try:
                        await mapear(link, informacion, profundidad - 1, parametros, download, guardar_links,
                                     guardar_hashes)
                    except:
                        pass
            _escribir_hash(hashes, directorio)
    except:
        try:
            directorio = join(getcwd(), informacion[0])
            _escribir_hash(hashes, directorio)
        except Exception as e:
            print(e)
            print(url)

###Funcion que organiza la funcion "mapear" para poderla utilizarr con asyncio
async def _mapear(url, profundidad, parametros, download, guardar_links, guardar_hashes):
    informacion = _sacar_nombre_y_contenido(url)
    await wait([mapear(url, informacion, profundidad, parametros, download, guardar_links, guardar_hashes)])

###Funcion final que se utiliza para hacer el analisis de un url, (esta es la que debe usarce para el scraping)
def scrap(url, profundidad=1, parametros={}, download=True, guardar_links=True, guardar_hashes=True):
    _loop = get_event_loop()
    _loop.run_until_complete(_mapear(url, profundidad, parametros, download, guardar_links, guardar_hashes))