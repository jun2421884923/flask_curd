from flask import Blueprint
from flask import jsonify,request,current_app


day_seller_en = Blueprint('day_seller_en', __name__)
app=current_app

from . import views

