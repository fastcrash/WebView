from Config import Config
from Components import *

class Homematic(object):
    """ THE backend """
    def __init__(self, categorie="Home"):

        self.__categorie = categorie # categorie from flask route
        self.__components = Components(categorie).components

    @property
    def components(self):
        return self.__components

if __name__ == '__main__':
    #imp = Import()
    #imp.importfromccu()

    hm = Homematic("Heizung")
