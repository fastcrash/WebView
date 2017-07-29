import os
import json
from lxml import etree
from collections import OrderedDict
from collections import OrderedDict


class Import(object):

    def __init__(self, ip):
        self.__ccuip =ip
        self.__devicelisturl="http://"+self.__ccuip+"/config/xmlapi/devicelist.cgi?show_internal=1"
        self.__sysvarlisturl = "http://"+self.__ccuip+"/config/xmlapi/sysvarlist.cgi"
        self.__programlisturl = "http://"+self.__ccuip+"/config/xmlapi/programlist.cgi"
        self.__importfile = "./config/import.json"

    def importfromccu(self):
        """ Connect to XML-Api, fetch devices, sysvars and programs and write
            them to import.json
        """
        imp = {} #
        devicelist = [] #list of all devices
        sysvarslist = [] #list of all sysvars
        progslist = [] #list of all programms

        # fetch devices
        root = etree.parse(self.__devicelisturl) #read xml data from api
        devices = root.findall("device") #select all devices

        for device in devices:
            tmp = {} # temporary representation of one device
            for attrib in device.attrib: # get all attributes of one device
                tmp[attrib] = device.get(attrib) # add attributes to tmp
            devicelist.append(tmp) # add device to list

        # fetch sysvars
        root = etree.parse(self.__sysvarlisturl) #read xml data from api
        sysvars = root.findall("systemVariable") #select all sysvars

        for sysvar in sysvars:
            tmp = {} # temporary representation of one sysvar
            for attrib in sysvar.attrib: # get all attributes of one sysvar
                tmp[attrib] = sysvar.get(attrib) # add attributes to tmp
            sysvarslist.append(tmp) # add sysvar to list

        # fetch programs
        root = etree.parse(self.__programlisturl) #read xml data from api
        progs = root.findall("program") #select all progs

        for prog in progs:
            tmp = {} # temporary representation of one program
            for attrib in prog.attrib: # get all attributes of one program
                tmp[attrib] = prog.get(attrib) # add attributes to tmp
            progslist.append(tmp) # add program to list

        imp["devices"] = devicelist
        imp["sysvars"] = sysvarslist
        imp["progs"] = progslist

        # write data to .json file
        with open(self.__importfile, 'w') as impfile:
            json.dump(imp, impfile, indent=2, sort_keys=False) # make it look pretty ;)

class Config(object):

    def __init__(self):
        self.__categorieslist = []
        self.__componentslist = []
        self.__subcategorieslist = {}
        self.__config = {}
        self.__categoriefile = "./config/categories.json"
        self.__componentsfile = "./config/components.json"
        self.__configfile = "./config/config.json"

    @property
    def configlist(self):
        return self.__configlist

    @property
    def categorielist(self):
        """getter for categorielist
        """
        return self.__categorieslist

    @property
    def componentslist(self):
        """ getter for componentslist
        """
        return self.__componentslist

    @property
    def subcategorieslist(self):
        """ getter for subcategorieslist
        """
        return self.__subcategorieslist

    def loadconfig(self):
        """ Load config from .json files"""

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
            categorie = self.__categorieslist[c]
            if "subcategories" in categorie:
                self.__subcategorieslist[c] = categorie["subcategories"]




class Homematic(object):

    def __init__(self, conf):
        if conf:
            self.__config = conf
        else:
            self.__config = Config()

        print(self.__config.configlist)
        self.__stateurl = "http://" + self.__config.configlist["ccuip"] + "/config/xmlapi/state.cgi?device_id="

    def getcomponents(self, cat):
        components = []
        complist = self.__config.componentslist
        for c in complist:
            if c == cat:
                print(c)
                components.append(complist[c])
        return components

    def getdatapoints(self, compid):

        datapoints = []
        url = self.__stateurl + compid

        # fetch datapoints
        root = etree.parse(url) #read xml data from api

        for dp in root.iter("datapoint"):
            tmp ={}
            for attrib in dp.attrib:
                tmp[attrib] = dp.get(attrib)
            datapoints.append(tmp)

        return datapoints

if __name__ == '__main__':
    #imp = Import("192.168.1.6")
    #imp.importfromccu()
    conf = Config()
    conf.loadconfig()
    hm = Homematic(conf)
    print(hm.getdatapoints("4619"))
