from flask import Blueprint,session
import json
import re
import flask
from flask.globals import current_app
from flask.wrappers import Request
from pymongo import ASCENDING, MongoClient
from  flask_cors import CORS, cross_origin
from flask import Flask, make_response, request
'''
Primary get method for location and regions
'''

client = MongoClient("mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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
@cross_origin( supports_credentials = True)
def select_country():
    country = db.Scraped_Data
    country_query = country.distinct('country')
    response = flask.jsonify(country_query)

    return response


'''
POST method for country
sets the country for session
allows us to access country variable in other blueprint files
'''
@location.route('/set_country/<country>',methods = ["POST"])
@cross_origin(supports_credentials = True)
def set_country(country):
    if country != None:
        response = flask.jsonify('200')
        response.set_cookie("country",country,secure=True,samesite= "None",domain= "skillquery.herokuapp.com")
       
        return response

    return (flask.jsonify('200'))

'''
region GET
if a region is fed we do a mongodb aggregation in order to retrieve 

'''
@location.route('/region/<country>',methods = ['POST'])
@cross_origin(supports_credentials = True)
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
        
        response = flask.jsonify(out)
 

        return response
    return flask.jsonify([])


'''
Post request to set region
sets session region ready for interaction 
'''
@location.route('/set_region/<region>',methods = ["POST"])
@cross_origin(supports_credentials = True)
def set_region(region):
    if region != None:
        response = flask.jsonify("200")
        response.set_cookie("region",region,secure=True,samesite= "None",domain= "skillquery.herokuapp.com")
        return response

    return ('200')


'''
Get country api request
simply returns country to enable more dynamic jsx code
'''
@location.route('/get_country',methods = ["GET"])
@cross_origin( supports_credentials = True)
def get_country():
    country = request.cookies.get("country")

    response = flask.jsonify(country)

    return (response)

# @cross_origin( supports_credentials = True)
# def select_country():
#     country = db.Scraped_Data
#     country_query = country.distinct('country')
#     response = flask.jsonify(country_query)
#     return response