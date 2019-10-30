from flask import Blueprint
from flask import jsonify,request
from flask import current_app
from werkzeug.local import LocalProxy
logger = LocalProxy(lambda: current_app.logger)
hour_adver_report = Blueprint('hour_adver_report', __name__)
from . import views

