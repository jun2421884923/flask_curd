from flask import Blueprint
from flask import jsonify,request,current_app


hour_adx_buyer_position = Blueprint('hour_adx_buyer_position', __name__)
app=current_app

from . import views

