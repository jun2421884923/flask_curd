# -*- coding: utf-8 -*-
import sys
from util.dbutil import MysqlUtil
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == '__main__':
    conn=MysqlUtil("local1")
    print conn.executeone("insert into user1 (name)values('user1')")


