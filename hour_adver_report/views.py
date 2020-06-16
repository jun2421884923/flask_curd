# -*- coding: utf-8 -*-

from . import hour_adver_report,logger
from util.dbutil import MysqlUtil
from util.decorator import jsonp,json_response
from util.common import conver_type
from flask import jsonify,request,current_app
import collections
import json
from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate,Length

from util.result import *
@hour_adver_report.route('/', methods=['GET', 'POST'])
def _hour_adver_report():
    current_app.logger.info("_hour_adver_report /")
    return "hour_adver_report "
@hour_adver_report.route('/get', methods=['GET', 'POST'])
@jsonp
def _hour_adver_report_get():
    current_app.logger.info(request.url)
    current_app.logger.info("current_app  _hour_adver_report  get")

    rules = {
        "startdate": [Required, Length(8, 8)],
        "enddate": [Required, Length(8, 8)]
    }
    valid, errors = validate(rules, request.args)  #
    current_app.logger.info(str(valid)+str(errors))

    result = results()
    # 参数校验
    if not valid:
        result.set_statuscode(1)
        result.set_data(str(errors))
        return jsonify(json.loads(str(result)))


    conn = MysqlUtil("adver")
    sql = """select day<=%s
    """ % (request.args.get('startdate', None), request.args.get('enddate', None))
    if request.args.get('b', None):
        sql = sql + "  and  b in (%s)" % (request.args.get('b', None))
    sql = sql + """
      group by day,hour,b,impid,a
) as t left join adx_ssp_adposition b on b.id=t.impid
left join(
select * from adver_ssp_strategy  union all select * from adver_ssp_strategy_sp)e on e.id=t.a  """
    current_app.logger.info(sql)
    print  sql
    flag, res = conn.excute(sql)
    if flag:
        data = []
        for row in res:
            dict_tmp = collections.defaultdict()
            dict_tmp['day'] = row[0]
            dict_tmp['hour'] = row[1]
            dict_tmp['b'] = row[2]
            dict_tmp['impid'] = row[3]
            dict_tmp['impidname'] = row[4]
            dict_tmp['strategyid'] = row[5]
            dict_tmp['strategyname'] = row[6]
            dict_tmp['request'] = row[7]
            dict_tmp['start'] = row[8]
            dict_tmp['imp'] = row[9]
            dict_tmp['click'] = row[10]
            dict_tmp['clickrate'] = row[11]
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
