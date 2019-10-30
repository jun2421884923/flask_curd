from . import hour_adx_buyer_position
from util.dbutil import MysqlUtil
from util.decorator import jsonp,json_response
from flask import jsonify,request,current_app
import collections
import json
from util.result import *
@hour_adx_buyer_position.route('/', methods=['GET', 'POST'])
def _hour_adx_buyer_position():
    current_app.logger.info("_hour_adx_buyer_position_t //")
    print "day get/"
    return "hour_adx_buyer_position "
@hour_adx_buyer_position.route('/get', methods=['GET', 'POST'])
@jsonp
def _hour_adx_buyer_position_test():
    # print request.form["en"]
    print request.args.keys()
    current_app.logger.info(request.url)

    current_app.logger.info("_hour_adx_buyer_position_test")
    print "day get"
    conn=MysqlUtil("adver")
    result=results()
    flag,res= conn.excute("select day,en,rp,imp,click,repository from day_sellerid_en where day=20191020 limit 5")
    if flag:
        data=[]
        for row in res:
            dict_tmp=collections.defaultdict()
            dict_tmp['day']  = row[0]
            dict_tmp['en']   = row[1]
            dict_tmp['rp']   = row[2]
            dict_tmp['imp']  = row[3]
            dict_tmp['click']= row[4]
            dict_tmp['repository'] = row[5]
            data.append(dict_tmp)
        result.set_statuscode(0)
        result.set_data(data)

    else:
        result.set_statuscode(1)
    current_app.logger.info("current_app"+str(result))
    return jsonify(json.loads(str(result)))
