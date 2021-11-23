from flask import Blueprint,session
import json
import re
from flask.globals import current_app
from pymongo import ASCENDING, MongoClient

'''
Primary get method for location and regions
'''

client = MongoClient()
db = client.prod
location = Blueprint('location',__name__)

def suitable_regions(country):

    pipe = [{
                    '$lookup':
                    {
                        'from': "Scraped_Data",
                        'localField': "url",
                        
                        'foreignField': "url",
                        'as': "role_info"
                    }
                },
                {"$match": {"role_info.country": country}}
                
                ,

                    {"$group": {"_id": "$role_info.region", 'count': { "$sum":1 } }}
                ]
                

    query = client.prod.techs.aggregate(pipeline=pipe)
    acceptable = [x for x in query if x.get('count') > 5  ]
    return acceptable



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
    print(session.get('country'),'set')
    return ('200')

'''
region GET
if a region is fed we do a mongodb aggregation in order to retrieve 

'''
@location.route('/region/<country>',methods = ['POST'])
def get_region(country):

    if country != "Select%Country":
            
        pipe = [{
                        '$lookup':
                        {
                            'from': "Scraped_Data",
                            'localField': "url",
                            
                            'foreignField': "url",
                            'as': "role_info"
                        }
                    },
                    {"$match": {"role_info.country": country}}
                    
                    ,

                        {"$group": {"_id": "$role_info.region", 'count': { "$sum":1 } }}
                    ]
                    

        query = client.prod.techs.aggregate(pipeline=pipe)
        acceptable = [x for x in query if x.get('count') > 5  ]
        out = [x.get("_id") for x in acceptable]
        out = sum(out,[])
        out = sorted(out)
        if "All"  in out:
            out.remove("All")
            out.insert(0,"All")
        elif "All" not in out:
            out.insert(0,"All")
        
        print(out)
        return json.dumps(out)
    return json.dumps([])


'''
Post request to set region
sets session region ready for interaction 
'''
@location.route('/set_region/<region>',methods = ["POST"])
def set_region(region):
    if region != None:
        session['region'] = region
    return ('200')


'''
Get country api request
simply returns country to enable more dynamic jsx code
'''
@location.route('/get_country',methods = ["GET"])
def get_country():
    return (json.dumps([session["country"]]))
