from flask import Blueprint,session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient

'''
Primary get method for location and regions
'''

client = MongoClient()
db = client.prod
location = Blueprint('location',__name__)

'''
get country method
queries through mongo db scraped_data collection to obtain DISTINCT countries in dataset

'''
@location.route('/country',methods = ['GET'])
def select_country():
    country = db.Scraped_Data
    country_query = country.distinct('country')
    return json.dumps(country_query)


'''
POST method for country
sets the country for session
allos us to access country variable in other blueprint files
'''
@location.route('/set_country/<country>',methods = ["POST"])
def set_country(country):
    if country != None:
        session['country'] = country
    return ('200')

'''
region GET
if a region is fed we do a mongodb aggregation in order to retrieve 

'''
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
        out = sorted([x for x in regions if x != "All"])
        out.insert(0,"All")
        return json.dumps(out)
    return json.dumps([])

@location.route('/set_region/<region>',methods = ["POST"])
def set_region(region):
    if region != None:
        session['region'] = region
    return ('200')
