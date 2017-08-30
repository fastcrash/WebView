import os
import json
import requests
from Config import Config
from lxml import etree
from collections import OrderedDict



class xmlapi(object):

    def __init__(self):

        self.__config = Config()
        self.__baseurl = "http://"+self.__config.ccuip + "/config/xmlapi/"
        self.__cgis = ["devicelist", "functionlist", "sysvarlist", "sysvar",
                       "state", "statelist", "statechange", "programlist",
                       "runprogram"]
        self.__urls = {k: self.__baseurl + k + ".cgi" for k in self.__cgis}

        self.__importfile = "./config/import.json" # file to store imported data


    def callapi(self, cgi, **kwargs):
        """
        Calls the given cgi script an returns an etree._ElementTree
        If kwargs a given, thy will be appended to rhe url.

        e.g. callapi(stechange, ise_id="1234", new_value="56 returns
        http://ccuip/config/xmlapi/statechange.cgi?ise_id="1234"&new_value="56"
        """

        if kwargs:
            url = self.__urls[cgi] + "?"
            if len(kwargs) > 1:
                for k, v in kwargs.items():
                    url += k+"="+v+"&"
                url = url[:-1]
            else:
                for k, v in kwargs.items():
                    url += k+"="+v
        else:
            url = self.__urls[cgi]
        return etree.parse(url)

    def statechange(self, iseid, value):
        url = self.__urls["statechange"]
        payload = {'ise_id': iseid, 'new_value': value}
        r = requests.get(url, params=payload)

    def importfromccu(self):
        """ Connect to XML-Api, fetch devices, sysvars and programs and write
            them to import.json
        """
        imp = [] #
        devicelist = [] #list of all devices
        sysvarslist = [] #list of all sysvars
        progslist = [] #list of all programms

        # fetch devices
        devicelist = self.callapi("devicelist") #read xml data from api
        statelist = self.callapi("statelist")
        devices = devicelist.findall(".//device") #select all devices

        for device in devices:
            tmp = {k: v for k, v in device.items()} # temporary representation of one device
            channels = device.findall(".//channel")
            chans = []
            for chan in channels:
                dplist = []
                i = chan.get("ise_id")
                c = {k: v for k, v in chan.items()}
                #TODO: for dp in channel ...
                points = statelist.findall(".//channel[@ise_id='"+i+"']/datapoint")
                for point in points:
                    p = {k: v for k, v in point.items()}
                    dplist.append(p)
                c["datapoints"] = dplist
                chans.append(c)
            tmp["channels"] = chans
            tmp["comptype"] = "device"
            imp.append(tmp) # add device to list


        sysvars = self.callapi("sysvarlist").findall(".//systemVariable")

        for s in sysvars:
            tmp = {k:v for k,v in s.items()}
            tmp["comptype"] = "sysvar"
            imp.append(tmp)

        programs = self.callapi("programlist").findall(".//program")

        for p in programs:
            tmp = {k:v for k, v in p.items()}
            tmp["comptype"] = "prog"
            imp.append(tmp)


        # write data to .json file
        with open(self.__importfile, 'w') as impfile:
            json.dump(imp, impfile, indent=2, sort_keys=False) # make it look pretty ;)

    def openimport(self):
        with open(self.__importfile) as impfile:
            return json.load(impfile)

    def dpvalue(self, iseid):
        root = self.callapi("state", datapoint_id=iseid)
        return root.find(".//datapoint").get("value")

    def idbyname(self, name):
        imp = self.openimport()
        try:
            comp = next(c for c in imp if c["name"] == name)
            return(comp["ise_id"])
        except:
            return None

    
    def gettype(self, ise_id):
        imp = self.openimport()
        try:
            comp = next(c for c in imp if c["ise_id"] == ise_id)
            return(comp["comptype"])
        except:
            return None



if __name__ == "__main__":
    x = xmlapi()
    x.importfromccu()
