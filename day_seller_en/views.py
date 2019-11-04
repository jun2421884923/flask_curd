# -*- coding: utf-8 -*-

from . import day_seller_en
from util.dbutil import MysqlUtil
from util.decorator import jsonp,json_response
from flask import jsonify,request,current_app
import collections
from util.common import conver_type,convert_object
import json
from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate,Length

from util.result import *
@day_seller_en.route('/', methods=['GET', 'POST'])
def _day_seller_en():
    current_app.logger.info("_day_seller_en /")
    return "day_seller_en "
@day_seller_en.route('/get', methods=['GET', 'POST'])
@jsonp
def _day_seller_en_get():
    current_app.logger.info(request.url)
    current_app.logger.info("current_app  _day_seller_en_get  get")

    rules = {
        "startdate": [Required, Length(8, 8)],
        "enddate": [Required, Length(8, 8)]
    }
    valid, errors = validate(rules, request.args)  #
    current_app.logger.info(str(valid) + str(errors))

    result = results()
    # 参数校验
    if not valid:
        result.set_statuscode(1)
        result.set_data(str(errors))
        return jsonify(json.loads(str(result)))

    conn = MysqlUtil("adver")
    sql = """select   day,en,terminal,sum(oreq) as oreq ,sum(sreq) as sreq,sum(sres) as sres,sum(sans) as sans,
sum(request)
 as request,sum(start) as start,sum(imp) as imp,sum(click) as click,sum(repository) as repository,
 sum(repository_max) as repository_max,sum(repository_30max) as repository_30max
from day_sellerid_en 
where day>=%s and day<=%s
        """ % (request.args.get('startdate', None), request.args.get('enddate', None))
    if request.args.get('en', None):
        sql = sql + "  and  en in ( '%s') " % (request.args.get('en', None))
    sql = sql + """
          group by day,en,terminal """
    current_app.logger.info(sql)
    print  sql
    flag, res = conn.excute(sql)
    if flag:
        data = []
        for row in res:
            list_col=['day','en','terminal','oreq','sreq','sres','sans',
                        'request','start','imp','click','repository',
                        'repository_max','repository_30max']
            dict_tmp=convert_object(list_col,row)
            #判断列数是否一致
            if dict_tmp ==1:
                data.append({"error":'序列化列数不一致'})
                result.set_data(data)
                result.set_statuscode(1)
                return jsonify(json.loads(str(result)))
            for k, v in dict_tmp.items():
                dict_tmp[k] = conver_type(v)
            data.append(dict_tmp)
        print "取出的条数=" + str(len(data))
        current_app.logger.info("取出的条数=" + str(len(data)))
        result.set_statuscode(0)
        result.set_data(data)

    else:
        result.set_statuscode(1)
        result.set_resultMsg(res + ":sql exec  fail！！！")
    return jsonify(json.loads(str(result)))
