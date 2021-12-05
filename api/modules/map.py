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
get country method
queries through mongo db scraped_data collection to count occurance of DISTINCT regions in dataset

'''



@map.route('/map',methods = ['GET'])
@cross_origin(supports_credentials = True)
def get_map():
    check_key = lambda x: not request.cookies.get(x) is None
    if check_key("country") and check_key("role") and check_key('region'):
            
            country = request.cookies['country']
            role = request.cookies['role'] 

            pipe = [{
                    "$match": {
                            "country": country,
                            "title" : role
                        }
                    },
                    {
                        "$group": {
                                "_id": "$region",
                                "count": {
                                '$sum': 1
                            }
                        }
                    }
                    ]
            count = client.prod.Scraped_Data.aggregate(pipeline = pipe )
            #format out dict ei: {'region':'Ontario' , 'count': 'N'}
            if country == "Canada":
                province_mapper = {
                    'AB':'01',
                    'BC':'02',
                    'MB':'03',
                    'NB':'04',
                    'NL':'05',
                    'NT':'13',	
                    'NS':'07',
                    'NU':'14',
                    'ON':'08',
                    'PE':'09',	
                    'QC':'10',	
                    'SK':'11',
                    'YT':'12'
                    }
                formatted_dict = [{"id":  province_mapper.get(x.get("_id")), "value": x.get("count"),"showLabel" : "1" } for x in list(count) if x.get("_id") in province_mapper.keys() ]  
            elif country == "US":
                
                formatted_dict = [{"id":  x.get("_id"), "value": x.get("count"),"showLabel" : "1" } for x in list(count) if type(x.get("_id") ) == str ]  
        
            return json.dumps('formatted_dict')         
    else :
        return json.dumps('200')
