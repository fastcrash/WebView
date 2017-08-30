from lxml import etree
from Config import Config
from xmlapi import xmlapi
import requests


class Components(object):
    """ Container for all types of Components
    """

    def __init__(self, categorie):

        self.__config = Config()
        self.__categorie = categorie
        self.__api = xmlapi()
        self.__components = {}

        self.load()

    def __getattr__(self, name):
        if name in self.__components:
            return self.__components.get(name, None)

    def __iter__(self):
        return iter(self.__components)

    @property
    def components(self):
        return self.__components

    def load(self):
        for cat in self.__config.categories:
            for sub in self.__config.subcategories[cat]:
                try:
                    for comp in self.__config.components[sub]:
                        i = comp["ise_id"]
                        t = self.__api.gettype(i)
                        if t == "sysvar":
                            self.__components[i] = SysVar(i)
                        if t == "device":
                            self.__components[i] = Device(i)
                        if t == "prog":
                            self.__components[i] = Program(i)
                except:
                    pass



class SysVar(object):
    """ This Class represents an HM-SysVar.
    """
    def __init__(self, iseid, root=None):
        self.__api = xmlapi()
        self.__iseid = iseid
        self.__attribs = {}

        # check if xml tree is given as root
        if isinstance(root, etree._ElementTree):
            self.__root = root
        else:
            self.__root = self.__api.callapi("sysvar", ise_id=iseid)

        # load attribs from xml
        self.loadsysvar()

    def __getattr__(self, name):
        """
        Makes the attribs available
        """
        if name in self.__attribs:
            return self.__attribs.get(name, None)

    def __setattr__(self, name, value):
        if name == "value":
            self.__api.statechange(self.__iseid, value)
            self.loadsysvar()
        super(SysVar, self).__setattr__(name, value)

    def loadsysvar(self):
        # load the xml-data
        sysvar = self.__root.find(".//systemVariable[@ise_id='"+self.__iseid+"']")
        # extract  values
        self.__attribs = {k: v for k,v in sysvar.items()}


class Device(object):

    def __init__(self, iseid):
        self.__iseid = iseid
        self.__attribs = {}
        self.__channels = []
        self.__datapoints = []
        self.__import = xmlapi().openimport()

        self.loaddevice()

    def __iter__(self):
        return iter(self.__channels)

    def __getattr__(self, name):
        if name in self.__attribs:
            return self.__attribs.get(name, None)

    @property
    def channels(self):
        return self.__channels

    def loaddevice(self):
        device = next(d for d in self.__import if d["ise_id"] == self.__iseid)
        self.__attribs = {k: v for k, v in device.items()}
        self.__channels = [Channel(c) for c in device["channels"]]
        for c in self.__channels:
            self.__datapoints.extend([Datapoint(dp) for dp in c.datapoints])


    def actdp(self):
        for dp in self.__datapoints:
            iseid = dp["ise_id"]
            dp["value"] = xmlapi().dpvalue(iseid)

    @property
    def datapoints(self):
        return self.__datapoints


class Channel(object):

    def __init__(self, *args):
        for c in args:
            self.__attribs = {k: v for k, v in c.items()}

    def __getattr__(self, name):
        if name in self.__attribs:
            return self.__attribs.get(name, None)


class Datapoint(object):

    def __init__(self, *args):
        for arg in args:
            self.__attribs = {k: v for k, v in arg.items()}

    def __getattr__(self, name):
        if name in self.__attribs:
            return self.__attribs.get(name, None)

    def actvalue(self):
        self.__attribs["value"] = xmlapi().dpvalue(self.__attribs["ise_id"])
        print(self.value)


class Program(object):
    pass

if __name__ == "__main__":
    c = Components("Home")
    print(c.components)
    for k, v in c.components.items():
        print(xmlapi().gettype(v.ise_id))
