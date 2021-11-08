from flask import Blueprint,session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient

client = MongoClient()
db = client.prod
location = Blueprint('location',__name__)
@location.route('/country',methods = ['GET'])
def select_country():
    country = db.Scraped_Data
    country_query = country.distinct('country')
    return json.dumps(country_query)

@location.route('/set_country/<country>',methods = ["POST"])
def set_country(country):
    if country != None:
        session['country'] = country
    return ('200')

@location.route('/region/',methods = ['GET'])
def select_location():
    if not session.get("country") is None:
        country = session['country']
        pipe = [{
                '$lookup': {
                    'from': "Scraped_Data",
                    'localField': "url",
                    'foreignField': "url",
                    'as': "role_info"
                }
            }, {
                '$match': {
                    "role_info.region": {

                        "$exists": 'true',
                        "$ne": 'null'
                    }
                }

            }, {
                '$group': {
                    '_id': 'null',
                    'uniqueValues': {
                        '$addToSet': "$role_info.region"
                    }
                }
            }
            ]

        query = client.prod.techs.aggregate(pipeline=pipe)   
        regions = sum(list(query)[0].get("uniqueValues"),[])
        print(regions)
        # regions = db.techs.find({"country":country},{"region":-1,"_id":0}).distinct("region")
        out_regions = [re.sub(r"(\w)([A-Z])", r"\1 \2", x) for x in regions]
        out = sorted([x for x in out_regions if x != "All"])
        out.insert(0,"All")
        return json.dumps(out)
    return json.dumps([])

@location.route('/set_region/<region>',methods = ["POST"])
def set_region(region):
    if region != None:
        session['region'] = region
    return ('200')
