#!/usr/local/bin/python
#coding=utf-8

import os
import sys
import time
import datetime
import pymysql as MySQLdb

class MysqlUtil:
    def __init__(self):
        self.conn = None

    def connect(self,hst,prt,usr,pwd,db,chst='utf8'):
        try:
            self.conn = MySQLdb.connect(host = hst\
                ,user = usr\
                ,passwd = pwd\
                ,db = db\
                ,port = prt\
                ,charset = chst\
                )
        except MySQLdb.Error as e:
            print (e)
        if self.conn: return True
        return False

    def disconnect(self):
        if self.conn:
            self.conn.close()


    def excute(self,sql_cmd):
        results = []
        try:
            if sql_cmd:
                cur = self.conn.cursor()
                cur.execute(sql_cmd) 
                results=cur.fetchall()
                cur.close()
                return True,results
        except Exception as e:
            print (e)
        return False,results

    def excute_with_field(self,sql_cmd):
        results = []
        try:
            if sql_cmd:
                cur = self.conn.cursor()
                cur.execute(sql_cmd) 
                indexs = cur.description
                result=cur.fetchall()
                cur.close()
                #print indexs
                for row in result:
                    data = {}
                    for i in range(len(indexs)):
                        data[indexs[i][0]] = row[i]
                    results.append(data)

                return True,results
        except Exception as e:
            print(e)
        return False,results
    def executeone(self,sql):
        try:
            if sql:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
                cur.close()
            return True
        except Exception as e:
            print (e)
        return False

    def executemany(self,sql,data_list):
        try:
            if sql:
                cur = self.conn.cursor()
                cur.executemany(sql,data_list)
                self.conn.commit()                                                                                              
                cur.close()
            return True
        except Exception as e:
            print (e)
            return False
        return False


if __name__=="__main__":

    conn=MysqlUtil()
    conn.connect('localhost',3306,'root','root','test')
    sql="show tables;"
    flag,res=conn.excute(sql)
    print(flag)
    print(res)


    #______________
    # conn=MysqlUtil()
    # conn.connect('localhost',33063,'vid_w','Ci4EY5','video_adver')
    # adver_sql="insert into hour_adver_tmp(`day`,`hour`,`a`,`impid`,`materialid`,`dealid`,`b`,`imp`,`click`,`request`,`start`,`vshow`,`vdMid`) "
    # value_sql="values (20181112,12,1,123,9575,312,'b',5123,51251,512341,5123,513,51);"
    # sql=adver_sql+value_sql
    # print(sql)
    # flag=conn.executeone(sql)
    # print(flag)


 
