from hashlib import sha3_256


# Funcion para crear el finger print de un archivo sha3-256(contenido_archivo).hexdigest()

# This function creates a fingerprint for a file (sha3-256sum)
def fingerprint(btes):
    return sha3_256(btes).hexdigest()
