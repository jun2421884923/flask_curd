# -*- coding: utf-8 -*-

from . import hour_adx_buyer_position,logger
from util.dbutil import MysqlUtil
from util.decorator import jsonp,json_response
from util.common import conver_type
from flask import jsonify,request,current_app
import collections
import json
from validator import Required, Not, Truthy, Blank, Range, Equals, In, validate,Length

from util.result import *
@hour_adx_buyer_position.route('/', methods=['GET', 'POST'])
def _hour_adx_buyer_position():
    current_app.logger.info("_hour_adx_buyer_position /")
    return "hour_adx_buyer_position "
@hour_adx_buyer_position.route('/get', methods=['GET', 'POST'])
@jsonp
def _hour_adx_buyer_position_get():
    current_app.logger.info(request.url)
    current_app.logger.info("current_app  hour_adx_buyer_position  get")

    rules = {
        "startdate": [Required, Length(8,8)],
        "enddate": [Required,  Length(8,8)]
    }
    valid,errors = validate(rules,request.args)  #
    result=results()
    current_app.logger.info(str(valid)+str(errors))
    #参数校验
    if  not valid:
        result.set_statuscode(1)
        result.set_data(str(errors))
        return jsonify(json.loads(str(result)))

    conn=MysqlUtil("adver")
    sql="""SELECT hab.buyerid,hab.day,hab.hour,hab.impid,asa.name,sum(hab.effective_imp) as imp,
sum(hab.effective_click) as click,sum(effective_income) as effectincome,sum(position_request) as position_request,sum(position_bid) as position_bid ,sum(win) as win,CONCAT(format(sum(hab.timeout)/sum(hab.position_request)*100,2),"%%") as 'timeoutrate'
FROM `hour_adx_buyer_position` hab
left join adx_ssp_adposition   asa 
on hab.impid=asa.id 
where 
day>=%s  and day<=%s
"""%(request.args.get('startdate',None),request.args.get('enddate',None))
    if request.args.get('b',None):
        sql=sql+"  and buyerid in (%s)"%(request.args.get('b',None))
    sql=sql+"""
 group by hab.buyerid,hab.day,hab.hour,hab.impid,asa.name"""
    current_app.logger.info(sql)
    print  sql
    flag,res= conn.excute(sql)
    if flag:
        data=[]
        for row in res:
            dict_tmp=collections.defaultdict()
            dict_tmp['buyerid']    = row[0]
            dict_tmp['day']        = row[1]
            dict_tmp['hour']       = row[2]
            dict_tmp['impid']      = row[3]
            dict_tmp['impidname']  = row[4]
            dict_tmp['imp']        = row[5]
            dict_tmp['click']      = row[6]
            dict_tmp['effectincome']         = row[7]
            dict_tmp['position_request']     =row[8]
            dict_tmp['position_bid']         = row[9]
            dict_tmp['win']         = row[10]
            dict_tmp['timeoutrate'] = row[11]
            for k,v in dict_tmp.items():
                dict_tmp[k]=conver_type(v)
            data.append(dict_tmp)
        print "取出的条数="+str(len(data))
        current_app.logger.info("取出的条数="+str(len(data)))
        result.set_statuscode(0)
        result.set_data(data)

    else:
        result.set_statuscode(1)
        result.set_resultMsg(res+":sql exec  fail！！！")
    return jsonify(json.loads(str(result)))
