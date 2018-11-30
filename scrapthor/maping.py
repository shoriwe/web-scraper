from os import mkdir, chdir, getcwd
from os.path import join
from asyncio import get_event_loop,ProtoactorEventLoop
from sys import platform
from .criptografia import fingerprint
from .descargar import _extraer_links,aio_descargar,filtro,_guardar_hashes,_guardar_links,_crear_archivo

if platform == 'win32':
    _loop = ProtoactorEventLoop()
else:
    _loop = get_event_loop()

###Crea un directorio y luego cd en el
def crear_mantener_directorio(directorio):
    try:
        mkdir(directorio)
    except Exception as e:
        print(e)
    try:
        chdir(directorio)
    except Exception as e:
        print(e)

###Funcion que crea una ruta a un directorio de una carpeta
def conseguir_directorio(archivo):
    return join(getcwd(),archivo)

###Funcion que fuciona la creacion de un hash con la descarga de un archivo
def hash_y_archivo(hashes,nombre,contenido,parametros,descargar_archivos,guardar_hashes):
    if not filtro(nombre, contenido, parametros):
        if descargar_archivos:
            try:
                _crear_archivo(nombre, contenido)
                print('Descargardo {}'.format(nombre))
            except Exception as e:
                print(e,23)
        if guardar_hashes:
            try:
                hashes[nombre] = fingerprint(nombre, contenido)
            except Exception as e:
                print(e)
    return hashes

###Funcion que analiza un link para luego extraerle el hash,, descargarlo o determinar los links que tiene
async def mapear(url, profundidad, parametros, descargar_archivos, guardar_links, guardar_hashes,informacion=None):
    hashes={}
    try:
        if profundidad>0:
            if informacion == None:
                informacion= await aio_descargar(url)
            directorio = conseguir_directorio(informacion[0])
            crear_mantener_directorio(directorio)
            links=_extraer_links(informacion[2])
            hashes = hash_y_archivo(hashes,informacion[1],informacion[2],parametros,descargar_archivos,guardar_hashes)
            if guardar_links:
                _guardar_links(links)
            for link in links:
                chdir(directorio)
                try:
                    if link != url:
                        
                        informacion = await aio_descargar(link)
                        hashes = hash_y_archivo(hashes, informacion[1], informacion[2], parametros,descargar_archivos, guardar_hashes)
                        _loop.create_task(mapear(link,profundidad-1,parametros,descargar_archivos,guardar_links,guardar_hashes,informacion))
                except:
                    pass
            _guardar_hashes(hashes)
    except Exception as e:
        print(e)
        _guardar_hashes(hashes)

###Funcion final que se utiliza para hacer el analisis de un url, (esta es la que debe usarce para el scraping)
def scrap(url, profundidad=2, parametros={}, descargar_archivos=True, guardar_links=True, guardar_hashes=True):
    _loop.run_until_complete(mapear(url, profundidad, parametros, descargar_archivos, guardar_links, guardar_hashes))
