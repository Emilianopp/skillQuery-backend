from flask import Blueprint,request
import json
import re
from flask.globals import current_app
from flask.json import jsonify
from pymongo import MongoClient
from  flask_cors import CORS, cross_origin
'''
Primary get method for map and regions
'''

client = MongoClient("mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.prod
map = Blueprint('map',__name__)

'''
checks if all values for submit 
'''



@map.route('/submit',methods = ['GET'])
@cross_origin(supports_credentials = True)
def get_map():


    return '200'
