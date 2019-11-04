from flask import Blueprint
from flask import jsonify,request
from flask import current_app
from werkzeug.local import LocalProxy
logger = LocalProxy(lambda: current_app.logger)
hour_adx_buyer_position = Blueprint('hour_adx_buyer_position', __name__)
from . import views

