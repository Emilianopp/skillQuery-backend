from flask import Blueprint
import json
import re
from pymongo import MongoClient
from .Analysis_Processing.Analysis_Processing import *

# sys.path.append("../modeling/DataPipe/")
# from modeling.DataPipe.scraping.classes.DataBase.Mongo import *

client = MongoClient()
db = client.prod
analysis = Analysis_Processing(db,role = )
software = Blueprint('software',__name__)
@software.route('/software',methods = ['GET'])
def select_country():
