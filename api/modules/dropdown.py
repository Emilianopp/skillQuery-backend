from flask import Flask,jsonify,Blueprint
import sys
import json
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient()
db = client.prod
roles = Blueprint('roles',__name__)
@roles.route('/role_dropdown',methods = ['GET'])
def select_role():
    out = db.Roles.find({},{"role":1,"_id":0})
    return json.dumps([x['role'] for x in out])
