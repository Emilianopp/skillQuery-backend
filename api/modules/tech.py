from flask import Blueprint, session,request
import json
import re
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter
from  flask_cors import CORS, cross_origin
client = MongoClient("mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
tech = Blueprint('tech', __name__)

'''

Techs joins on scraped_data in order to return subset of postings
returns dict in the form 
{"counts" :sorted_out,"numRoles":count }

where numRoles are the total amount of roles the query recieved
counts is a sorted dictionary of techs and their respective counts

'''

@tech.route('/tech', methods=['GET'])
@cross_origin(supports_credentials = True)
def get_tech():
    check_key = lambda x: not request.cookies.get(x) is None
#ONLY COUNTRY SET  ============================
    if check_key("country") and check_key("role") and check_key('region'):
        if(request.cookies.get('region') == "All"):
            country = request.cookies['country']
            'Machine Learning'
            role = request.cookies['role'] 
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
                {"$group": {"_id": "$found_list"}}
            ]
            count = client.prod.Scraped_Data.count({"country": country ,
                "title": role}) 
            query = client.prod.techs.aggregate(pipeline=pipe)

            embedded_list = [x.get("_id") for x in query]
            print([x for x in query])
            tech_list = sum(embedded_list,[])
            counts = Counter(tech_list)
            formated_return = [{"label":x,"value":counts.get(x)} for x in counts]
            sorted_out = sorted(formated_return, key=lambda d: d['value'],reverse= True) 
            out = {"counts" :sorted_out,"numRoles":count }
            return json.dumps(out)
#REGION SET  ============================
        else:
            country = request.cookies['country']
            region = request.cookies['region'].replace(" ","")
            role = request.cookies['role'] 
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
                "role_info.region": region,
                "role_info.title": role}},
                {"$group": {"_id": "$found_list"}}
            ]
            count = client.prod.Scraped_Data.count( {"country": country ,
                "region": region,
                "title": role}) 
            query = client.prod.techs.aggregate(pipeline=pipe)
            embedded_list = [x.get("_id") for x in query]
            tech_list = sum(embedded_list,[])

            counts = Counter(tech_list)
            formated_return = [{"label":x,"value":counts.get(x)} for x in counts]
            sorted_out = sorted(formated_return, key=lambda d: d['value'],reverse= True) 
            out = {"counts" :sorted_out,"numRoles":count }
            return json.dumps(out)
    else: 
        return '200'
