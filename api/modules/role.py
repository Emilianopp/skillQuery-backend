from flask import Flask,make_response, app,jsonify,Blueprint,session
import sys
import json
from  flask_cors import CORS, cross_origin
from bson.objectid import ObjectId
from pymongo import MongoClient

#=================== Role http request===================#
'''
select role:
    Allows for selection of role request, fetches data from Mongo and returns available roles

set_role:
    modifies current app configs to be set as 

'''
client = MongoClient("mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.prod
roles = Blueprint('roles',__name__)
@roles.route('/role_dropdown',methods = ['GET'])
@cross_origin(supports_credentials = True)
def select_role():
    out = db.Roles.find({},{"role":1,"_id":0})
    response = jsonify([x['role'] for x in out])
    return response

@roles.route('/role/<selection>',methods = ['POST'])
@cross_origin(supports_credentials = True)
def set_role(selection):
    out =  jsonify('200')
    out.set_cookie("role",selection,secure=True,samesite= "None",domain= "skillquery.herokuapp.com")

    return(out)
