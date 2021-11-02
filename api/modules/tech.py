from flask import Blueprint,session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient

from api.modules.Analysis_Processing.Analysis_Processing import Analysis_Processing
from api.modules.classes.Role import Role

client = MongoClient()
db = client.prod
tech = Blueprint('tech',__name__)
@tech.route('/tech',methods = ['GET'])
def get_tech():
    country = session['country']
    region = session['region']
    role = session['role']
    analysis = Analysis_Processing(db,role = Role(role))
    
