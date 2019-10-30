# -*- coding: utf-8 -*-
import json
dict_result={
    0:"success",
    1:"error"
}
class results(object):
    def __init__(self, statuscode=0,data=None):
        self.__statuscode = statuscode
        self.__data= data
        self.__resultMsg = dict_result[self.__statuscode]

    def set_statuscode(self, statuscode):
        self.__statuscode = statuscode
        self.__resultMsg = dict_result[self.__statuscode]
    def set_data(self,data):
        self.__data=data

    def get_statuscode(self):
        return self.__statuscode
    def get_resultMsg(self):
        return self.__resultMsg

    def get_data(self):
        return self.__data
    def __str__(self):
        return json.dumps({"statuscode":self.__statuscode,"data":self.__data,"msg":self.__resultMsg})