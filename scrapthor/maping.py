from asyncio import get_event_loop, ProactorEventLoop, sleep
from os import mkdir, getcwd
from os.path import join
from sys import platform
from .logger import logger
from .criptografia import fingerprint
from .descargar import _extraer_links, aio_descargar, filtro, _crear_archivo, Reglas
from csv import writer

# Crear loop paraa async
# Create loop for async
if platform == 'win32':
    _loop = ProactorEventLoop()
else:
    _loop = get_event_loop()


# ESPANOL
# Funcion para guardar los links encontrados en un archivo .txt

# ENGLISH
# Function to save all links founded in a .txt file
def _guardar_links(directorio, links):
    with open(join(directorio, 'lista_links.txt'), 'w') as archivo:
        archivo.write('\n'.join(x for x in links))
        archivo.close()


# ESPANOL
# Funcion para guardar hashes en un archivo .csv

# ENGLISH
# Funtion to create a .csv file and save hashes in there
def _guardar_hashes(directorio, hashes):
    with open(join(directorio, 'hashes.csv'), 'w') as archivo:
        escritor = writer(archivo)
        escritor.writerow(['Archivo', 'Hash'])
        for hash in hashes:
            escritor.writerow(hash)
        archivo.close()


###Crea un directorio y luego cd en el
def crear_mantener_directorio(directorio, loger):
    try:
        mkdir(directorio)
    except Exception as e:
        loger.logear(e)


# ESPANOL#
###Funcion que crea una ruta a un directorio de una carpeta

# ENGLISH#
###This function found the directory to work
def conseguir_directorio(directorio, archivo):
    if directorio != None:
        return join(directorio, archivo)


# ESPANOL#
###Funcion que fuciona la creacion de un hash con la descarga de un archivo

# ENGLISH#
###This function create a file with the  bytes recieved and calculate the hash for fingerprint, them that hash is
###Inserted into a the hash list that the user have, them return it [name_of file,hash]
def hash_y_archivo(hashes, nombre, contenido, directorio, parametros, descargar_archivos, guardar_hashes, loger,
                   reglas):
    try:
        if not filtro(nombre, contenido, parametros, reglas):
            if descargar_archivos:
                _crear_archivo(join(directorio, nombre), contenido, logger=loger)

            if guardar_hashes:
                try:
                    hashes.append([nombre, fingerprint(contenido)])
                except Exception as e:
                    loger.logear(e)
    except:
        print('error en hashyarchivo')
    return hashes


# ESPANOL
# Funcion que analiza un link para luego extraerle el hash,, descargarlo o determinar los links que tiene

# ENGLISH
# This function realize all the scraping process
async def mapear(url, profundidad, parametros, descargar_archivos, guardar_links, guardar_hashes, loger, reglas,
                 velocidad,
                 informacion=None, directorio_a=getcwd()):
    hashes = []  # This variable store all the hashes found
    try:
        if profundidad > 0:
            ###This is only used after the first link is used
            if informacion == None:
                informacion = await aio_descargar(url, logger=loger)
            # Get the directory to work
            directorio = conseguir_directorio(directorio_a, informacion[0])
            # Try to create a directory and cd into it
            crear_mantener_directorio(directorio, loger)
            # Extrack all the links of html bytes
            links = _extraer_links(informacion[2])
            # Try to download the file and extrack the hash
            hashes = hash_y_archivo(hashes, informacion[1], informacion[2], directorio, parametros, descargar_archivos,
                                    guardar_hashes, loger, reglas)
            # Continue if someone wants to save all the linkss found in a file ('lista_links.txt')
            if guardar_links:
                _guardar_links(directorio, links)
            # Work with all  links in the links list
            for numero, link in enumerate(links):
                try:
                    # This statement because sometimes without it the program make duplications or use unnecesary resources
                    if link != url:
                        # Get information to mapear function
                        informacion = await aio_descargar(link, logger=loger)
                        await sleep(profundidad / velocidad)  # Go to other process in this time

                        # Extract the hash and download the file
                        hashes = hash_y_archivo(hashes, informacion[1], informacion[2], directorio, parametros,
                                                descargar_archivos,
                                                guardar_hashes, loger, reglas)

                        # Start maping the link
                        _loop.create_task(
                            mapear(link, profundidad - 1, parametros, descargar_archivos, guardar_links, guardar_hashes,
                                   loger, reglas, velocidad=velocidad,
                                   informacion=informacion, directorio_a=directorio))
                except:
                    pass
                # This is the progress of analysis in the current 'url'
                loger.logear('{}% en {}'.format(100 * (numero + 1) / len(links), url))

            # Save all the hashes found in a .csv file
            _guardar_hashes(directorio, hashes)
    except Exception as e:

        # Exception debuging
        loger.logear(e)
        try:
            # Try to create the file
            _guardar_hashes(directorio, hashes)
        except Exception as e:
            # Debuging
            loger.logear('[ERROR] Se re-intento es cribir el hash pero no se logro')


# ESPANOL
# Funcion final que se utiliza para hacer el analisis de un url, (esta es la que debe usarce para el scraping)

# ENGLISH
# This function is the only that can be used from this file, it is the implementation of mapear
def scrap(url, debug_file=None, debug=True, profundidad=2, parametros={}, descargar_archivos=True, guardar_links=True,
          guardar_hashes=True, reglas=Reglas, velocidad=3):
    loger = logger(debug_file, debug)
    _loop.run_until_complete(
        mapear(url, profundidad, parametros, descargar_archivos, guardar_links, guardar_hashes, loger, reglas,
               velocidad=velocidad))
