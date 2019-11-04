
#coding=utf-8
import pymysql
from settings import  dbconfig
import threading
from flask import current_app
from DBUtils.PooledDB import PooledDB, SharedDBConnection

class MysqlUtil(object):
    # 连接池对象
    __pool = None
    _instance_lock = threading.Lock()
    def __init__(self,bind="local"):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._bind = bind
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()
    #单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(MysqlUtil, "_instance"):
            with MysqlUtil._instance_lock:
                if not hasattr(MysqlUtil, "_instance"):
                    MysqlUtil._instance = object.__new__(cls)
        return MysqlUtil._instance

    def __getConn(self):
        """
        @summary:
        @return MySQLdb.connection
        """
        if MysqlUtil.__pool is None:
            MysqlUtil.__pool = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=30,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=3,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=30,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host=dbconfig[self._bind]["host"],
        port=dbconfig[self._bind]["port"],
        user=dbconfig[self._bind]["user"],
        password=dbconfig[self._bind]["password"],
        database=dbconfig[self._bind]["database"],#链接的数据库的名字
        charset='utf8'
    )
        return MysqlUtil.__pool.connection()
    def excute(self,sql_cmd):
        results = []
        try:
            if sql_cmd:
                self._cursor.execute(sql_cmd)
                results=self._cursor.fetchall()
                self._cursor.close()
                return True,results
        except Exception as e:
            print (e)
            return False, str(e)
        return False,results
    def executeone(self,sql):
        try:
            if sql:
                self._cursor.execute(sql)
                self._conn.commit()
                self._cursor.close()
            return True
        except Exception as e:
            print (e)
        return False

    def executemany(self,sql,data_list):
        try:
            if sql:
                self._cursor.executemany(sql,data_list)
                self._conn.commit()
                self._cursor.close()
            return True
        except Exception as e:
            print (e)
            return False
    def disconnect(self):
        if self._conn:
            self._conn.close()












