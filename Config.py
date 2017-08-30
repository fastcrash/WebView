import os
import json
from lxml import etree
from collections import OrderedDict

class Config(object):
    ''' Class for handling the .json config-files and accessing the Config'''

    def __init__(self):
        self.__configlist = {}  # the whole config

        # the .json-files
        self.__categoriefile = "./config/categories.json"
        self.__componentsfile = "./config/components.json"
        self.__configfile = "./config/config.json"
        self.__importfile = "./config/import.json"

        self.__categorieslist = []  # list of maincategories
        self.__componentslist = []  # dict of components, key = subcategorie
        self.__subcategorieslist = {}   # dict of subcategories by maincategories


        self.loadconfig() # load config from files


    def __getattr__(self, name):
        return self.__configlist.get(name, None)

    @property
    def categories(self):
        """getter for categorielist
        """
        return self.__categorieslist

    @property
    def components(self):
        """ getter for componentslist
        """
        return self.__componentslist

    @property
    def subcategories(self):
        """ getter for subcategorieslist
        """
        return self.__subcategorieslist


    def loadconfig(self):
        """ Load config from .json files"""

        # open the main config file
        with open(self.__configfile, "r") as cf:
            self.__configlist = json.load(cf)

        # load categorie.json
        with open(self.__categoriefile, "r") as cf:
            self.__categorieslist = json.load(cf, object_pairs_hook=OrderedDict)

        # load components.json
        with open(self.__componentsfile, "r") as cf:
            self.__componentslist = json.load(cf)
            
        # extract subcategories
        for c in self.__categorieslist:
            self.__subcategorieslist[c] = self.__categorieslist[c]["subcategories"]


if __name__ == '__main__':
    c = Config()
    #print(c.categories)
