from os import getcwd
from os.path import join


# Logger para dirigir un debug al programa
# Logger to have a debug mode in the program
class logger:
    def __init__(self, archivo=None, log=True):
        if isinstance(archivo, str):
            self.nombre = join(getcwd(), archivo)
        else:
            self.nombre = None
        self.log = log

    def logear(self, mensage):
        if self.log:
            if isinstance(self.nombre, str):
                with open(self.nombre, 'a')  as file:
                    file.write('{}\n'.format(str(mensage)))
                    file.close()
            else:
                print(mensage)
