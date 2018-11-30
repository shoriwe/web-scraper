from hashlib import sha3_256

###Funcion para crear el finger print de un archivo sha(nombre_archivo+contenido_archivo).digest()
def fingerprint(nombre,btes,string=False):
    if not isinstance(nombre,bytes):
        nombre=bytes(nombre,'utf-8')

    if not string:
        return sha3_256(nombre+btes).digest()
    else:
        return str(sha3_256(nombre+btes).digest())