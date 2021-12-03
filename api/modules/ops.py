from flask import Blueprint, session,request
import json
import re
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter
from  flask_cors import CORS, cross_origin
client = MongoClient("mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
ops = Blueprint('ops', __name__)

'''

Ops joins on scraped_data in order to return subset of postings
returns dict in the form 
{"counts" :sorted_out,"numRoles":count }

where numRoles are the total amount of roles the query recieved
counts is a sorted dictionary of ops and their respective counts

'''
@ops.route('/ops', methods=['GET'])
@cross_origin(supports_credentials = True)
def get_ops():
    check_key = lambda x: not request.cookies.get(x) is None
    #if region is NOT set 
    if check_key("country") and check_key("role") and check_key('region'):
        if(request.cookies.get('region') == "All"):
            country = request.cookies['country']
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
            count = client.prod.Scraped_Data.count( {"country": country ,
                "title": role}) 
            query = client.prod.ops.aggregate(pipeline=pipe)
            embedded_list = [x.get("_id") for x in query]
            ops_list = sum(embedded_list,[])
            counts = Counter(ops_list)
            formated_return = [{"label":x,"value":counts.get(x)} for x in counts]
            sorted_out = sorted(formated_return, key=lambda d: d['value'],reverse= True) 
            out = {"counts" :sorted_out,"numRoles":count }
            return json.dumps(out)
        #if region is set
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
            query = client.prod.ops.aggregate(pipeline=pipe)
            embedded_list = [x.get("_id") for x in query]
            ops_list = sum(embedded_list,[])

            counts = Counter(ops_list)
            formated_return = [{"label":x,"value":counts.get(x)} for x in counts]
            sorted_out = sorted(formated_return, key=lambda d: d['value'],reverse= True) 
            out = {"counts" :sorted_out,"numRoles":count }
            return json.dumps(out)
    else: 
        return '200'
