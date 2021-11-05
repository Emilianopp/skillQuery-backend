from flask import Blueprint, session
import json
from flask.globals import current_app
from pymongo import MongoClient
from collections import Counter

client = MongoClient()
packages = Blueprint('packages', __name__)


@packages.route('/packages', methods=['GET'])
def get_packages():
    check_key = lambda x: not session.get(x) is None
    if check_key("country") and check_key("role") and check_key('region'):
        country = session['country']
        region = session['region']
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
            "role_info.region": region,
            "role_info.title": role}},
            {"$group": {"_id": "$found_list"}}
        ]
        count = client.prod.Scraped_Data.count( {"country": country ,
            "region": region,
            "title": role}) 
        query = client.prod.packages.aggregate(pipeline=pipe)
        embedded_list = [x.get("_id") for x in query]
        packages_list = sum(embedded_list,[])
        counts = Counter(packages_list)
        formated_return = [{"label":x,"value":counts.get(x)} for x in counts]
        sorted_out = sorted(formated_return, key=lambda d: d['value'],reverse= True) 
        out = {"counts" :sorted_out,"numRoles":count }


        return json.dumps(out)
    else: 
        return '200'
