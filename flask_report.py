# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,flash,redirect,url_for
import logging,os,sys,json
from flask import current_app
from flask import jsonify
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__,static_folder="templates")
app.secret_key = b"qweq#.??daddadaqqe"
# 获取logger实例，如果参数为空则返回root logger
print __name__
logger = logging.getLogger(__name__)
currentdir = os.path.abspath(os.path.dirname(__file__))
LOG_PATH = os.path.join(currentdir,'logs')
LOG_FILE = 'flask_curd.log'
data_dir=os.path.join(currentdir,'data')
'''
abort(401)
redirect(url_for('login'))
'''
def config():
    print("config start")
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # 文件日志
    file_handler = logging.FileHandler("%s%s%s" % (LOG_PATH,os.sep,LOG_FILE))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.DEBUG)
config()
@app.route('/test')
def hello_world():
    logger.info("hello")
    logger.info(str(os.pathsep))
    app.logger.warn("warn")
    # return render_template('upload.html')
    return "hello"


#蓝图
from day_seller_en import day_seller_en as day_seller_en_blueprint
app.register_blueprint(day_seller_en_blueprint,url_prefix='/day_seller_en')
from hour_adver_report import hour_adver_report as hour_adver_report_blueprint
app.register_blueprint(hour_adver_report_blueprint,url_prefix='/hour_adver_report')
from hour_adx_buyer_position import hour_adx_buyer_position as hour_adx_buyer_position_blueprint
app.register_blueprint(hour_adx_buyer_position_blueprint,url_prefix='/hour_adx_buyer_position')
#实现mvc  url和函数分离
#app.add_url_rule('/foo', view_func=login_required(views.foo))

from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))
from pyecharts import options as opts
from pyecharts.charts import Bar
def bar_base() :
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c
@app.route("/")
def index():
    c = bar_base()
    return Markup(c.render_embed())





@app.errorhandler(404)
def not_fond(e):
    return render_template("404.html")
if __name__ == '__main__':
    currentdir = os.path.abspath(os.path.dirname(__file__))
    data_dir=os.path.join(currentdir,'data')
    app.run(host='0.0.0.0',port=5001,debug=True,use_reloader=False)
