# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,flash,redirect,url_for
import logging,os,sys,json
from flask import current_app
from flask import jsonify
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
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

#实现mvc  url和函数分离
#app.add_url_rule('/foo', view_func=login_required(views.foo))

# @app.errorhandler(404)
# def not_fond(e):
#     return render_template("404.html")
if __name__ == '__main__':
    currentdir = os.path.abspath(os.path.dirname(__file__))
    data_dir=os.path.join(currentdir,'data')
    app.run(host='0.0.0.0',port=5001,debug=True,use_reloader=False)
