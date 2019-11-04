# -*- coding: utf-8 -*-
import  decimal
import collections
def conver_type(x):
    """
    把结果中的decical类型转给float，解决json dumps的错误
    :param x:
    :return:
    """
    if isinstance(x,decimal.Decimal):
        return float(x)
    else:
        return x
def convert_object(list_col,row):
    """
    把数据库的结果集转为字典
    :param list_col:
    :return:
    """
    dict_tmp = collections.defaultdict()

    if len(row)==0:
        print "convert_object   row len=0"
        return dict_tmp
    if len(list_col) != len(row):
        print "convert_object  len  list_col != row !!!"
        return 1
    for i,k in enumerate(list_col):
        dict_tmp[k] = row[i]
    return dict_tmp

if __name__ == '__main__':
    print convert_object(['qwe','rqweq'],(123,"data"))

