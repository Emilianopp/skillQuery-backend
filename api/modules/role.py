from flask import Flask,make_response, app,jsonify,Blueprint,session
import sys
import json

from bson.objectid import ObjectId
from pymongo import MongoClient

#=================== Role http request===================#
'''
select role:
    Allows for selection of role request, fetches data from Mongo and returns available roles

set_role:
    modifies current app configs to be set as 

'''
client = MongoClient()
db = client.prod
roles = Blueprint('roles',__name__)
@roles.route('/role_dropdown',methods = ['GET'])
def select_role():
    out = db.Roles.find({},{"role":1,"_id":0})
    return json.dumps([x['role'] for x in out])

@roles.route('/role/<selection>',methods = ['POST'])
def set_role(selection):
    session['role'] = selection
    return('200')
