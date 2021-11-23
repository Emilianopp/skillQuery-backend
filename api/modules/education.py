from flask import Blueprint, session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
education = Blueprint('education', __name__)

'''
Education api call
joins on scraped_data to determine subset of required positions
returns counts of degrees in below format
{"label" : <degree> , "value" : <count>}

'''
@education.route('/education', methods=['GET'])
def get_education():

    #Return ALL regions
    check_key = lambda x: not session.get(x) is None
    if check_key("country") and check_key("role") and check_key('region'):
        if(session.get('region') == "All"):
            country = session['country']
            role = session['role'] 
            pipe = [{
                '$lookup':
                {
                    'from': "Scraped_Data",
                    'localField': "url",
                    'foreignField': "url",
                    'as': "role_info"
                }
            },
                {'$match': {"role_info.country": country,
                "role_info.title": role
                }},
                   {"$group" : {"_id":"$degrees",
                       "count" : {'$sum' : 1}
                   
                   
                   }}
            ]

            query = client.prod.education.aggregate(pipeline=pipe)
            embedded_list = [{"label" : list(x.get("_id").keys())[0],"value" : x.get("count")} for x in query]
            print(embedded_list)
            return json.dumps(embedded_list)
        #Return specific region
        else:
            country = session['country']
            role = session['role'] 
            region = session['region'].replace(" ","")
            pipe = [{
                '$lookup':
                {
                    'from': "Scraped_Data",
                    'localField': "url",
                    'foreignField': "url",
                    'as': "role_info"
                }
            },
                {'$match': {"role_info.country": country,
                "role_info.title": role,
                "role_info.region": region,
                }},
                   {"$group" : {"_id":"$degrees",
                       "count" : {'$sum' : 1}
                   
                   
                   }}
            ]

            query = client.prod.education.aggregate(pipeline=pipe)
            embedded_list = [{"label" : x.get("_id"),"value" : x.get("count")} for x in query]
            print(embedded_list)
            return json.dumps(embedded_list)

    else: 
        return '200'
