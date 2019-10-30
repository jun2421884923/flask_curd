from . import hour_adver_report,logger
from util.dbutil import MysqlUtil
from util.decorator import jsonp,json_response
from util.common import conver_type
from flask import jsonify,request,current_app
import collections
import json
from util.result import *
@hour_adver_report.route('/', methods=['GET', 'POST'])
def _hour_adver_report():
    current_app.logger.info("_hour_adver_report_t //")
    return "hour_adver_report "
@hour_adver_report.route('/get', methods=['GET', 'POST'])
@jsonp
def _hour_adver_report_test():
    # print request.form["en"]
    print request.args.keys()
    current_app.logger.info(request.url)
    print current_app._get_current_object()
    current_app.logger.info("current_app  _hour_adver_report_test")
    logger.info(" logger  _hour_adver_report_test")
    print "day get"
    conn=MysqlUtil("adver")
    result=results()
    flag,res= conn.excute("""SELECT hab.buyerid,hab.day,hab.hour,hab.impid,asa.name,sum(hab.effective_imp) as imp,
sum(hab.effective_click) as click,sum(effective_income) as effectincome,sum(position_request) as position_request,sum(position_bid) as position_bid ,sum(win) as win,CONCAT(format(sum(hab.timeout)/sum(hab.position_request)*100,2),"%") as 'timeoutrate'
FROM `hour_adx_buyer_position` hab
left join adx_ssp_adposition   asa 
on hab.impid=asa.id 
where 
#day>=20190916
 buyerid in (1001)
 and day in (20191015)
#buyerid in (1023,1066,1071,1003,1094)
group by hab.buyerid,hab.day,hab.hour,hab.impid,asa.name""")
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
        result.set_statuscode(0)
        result.set_data(data)

    else:
        result.set_statuscode(1)

    current_app.logger.info("current_app"+str(result))
    return jsonify(json.loads(str(result)))
