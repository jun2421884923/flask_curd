# -*- coding: utf-8 -*-
import sys
from util.dbutil import MysqlUtil
import time
reload(sys)
sys.setdefaultencoding('utf-8')
"""
flask获取参数方式：

request.form.get("key", type=str, default=None) 获取表单数据

request.args.get("key") 获取get请求参数

request.values.get("key") 获取所有参数
"""
from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate,Length

def test_valid():
    rules = {
        "foo": [Required, Length(8,8)],  # foo must be exactly equal to 123
        "bar": [Required, Truthy()],  # bar must be equivalent to True
        "baz": [In(["spam", "eggs", "bacon"])],  # baz must be one of these options
        "qux": [Not(Range(1, 100))]  # qux must not be a number between 1 and 100 inclusive
    }
    # then this following dict would pass:
    passes = {
        "foo": '20191027',
        "bar": True,  # or a non-empty string, or a non-zero int, etc...
        "baz": "sp2am",
        "qux": 101
    }
    valid,errors = validate(rules,passes)  # 姿势 2
    print  valid
    print errors
    print type(valid)
    print type(errors)
def test(x):
    sp = float(x) * 100
    if sp < 0:
        sp = 0
    print str(sp)
if __name__ == '__main__':
    test(3.079352)
    # test_valid()
    # conn=MysqlUtil("local1")
    # print conn.executeone("insert into user1 (name)values('user1')")


