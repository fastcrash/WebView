from lxml import etree


class Device(object):


    def __init__(self, n, a, i, t):
        self.__name = n
        self.__address = a
        self.__ise_id = i
        self.__channels = {}
        self.__type = t

    def add_channel(self, i, c):

        self.__channels[i] = c


class Channel(object):


    def __init__(self, n, i, p, v, t, index):
        self.__name = n
        self.__ise_id = i
        self.__parent_id = p
        self.__visible = v
        self.__type = t
        self.__index = index
        self.__statelist = {}


class Sysvar(object):


    def __init__(self, n, va, v, vl, i, u, t, st, vis):
        self.__name = n
        self.__variable = va
        self.__value = v
        self.__value_list = vl
        self.__ise_id = i
        self.__unit = u
        self.__type = t
        self.__subtype = st
        self.__visible = vis


class Program(object):

    def __init__(self, i, a, n, vis, o):
        self.__id = i
        self.__active = a
        self.__name = n
        self.__visible = vis
        self.__operate = o

class Wrapper(object):

    def __init__(self):
        self.__Devices = {}
        self.__Sysvars = {}
        self.__Programs = {}


    def getDevicebyname(self, name):
        return none

    def getDevicebyid(self, id):
        return self.__Devices[id]

