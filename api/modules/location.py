from flask import Flask,jsonify,Blueprint
import sys
import json
from pymongo import MongoClient

# sys.path.append("../modeling/DataPipe/")
# from modeling.DataPipe.scraping.classes.DataBase.Mongo import *

client = MongoClient()
db = client.prod
location = Blueprint('location',__name__)
@location.route('/location',methods = ['GET'])
def select_location():
    locations = db.Scraped_Data
    location_query = locations.distinct('location')
    return json.dumps(location_query)