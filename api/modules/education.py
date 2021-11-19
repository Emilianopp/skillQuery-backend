from flask import Blueprint, session
import json
import re
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
education = Blueprint('education', __name__)


@education.route('/education', methods=['GET'])
def get_education():
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
                {'$match': {"role_info.country": country ,
                "role_info.title": role}},
                   {"$group" : {"_id":"$degrees",
                       "count" : {'$sum' : 1}
                   
                   
                   }}
            ]

            query = client.prod.education.aggregate(pipeline=pipe)
            embedded_list = [{"degrees" : x.get("_id"),"count" : x.get("count")} for x in query]
            print(embedded_list)
            return json.dumps(embedded_list)

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
            embedded_list = [{"degrees" : x.get("_id"),"count" : x.get("count")} for x in query]
            print(embedded_list)
            return json.dumps(embedded_list)

    else: 
        return '200'
