from pymongo.errors import BulkWriteError, DuplicateKeyError
from analysis.analysis import Analysis_Processing
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
from datetime import datetime
from pymongo import MongoClient
import argparse
import yaml



def main(analysis_to_do,date,country,role:str)->None:
    mdb = open(r"./mongo.txt", "r").read()
    client = MongoClient(mdb)
    db = client.prod
    analysis = Analysis_Processing(db,Role(role) ,date,country)
    for topic in analysis_to_do.keys():
        inserts = analysis.do_analysis(fr"{analysis_to_do.get(topic)}" ,col = 'model_outputs')
        try:
            res = client.prod[topic].insert_many(inserts)
            print(f'successfully inserted into {topic} {len(res.inserted_ids)} documents')
        except BulkWriteError as e:
            print(f"duplicate key entries at {topic}")
        print(f'successfully inserted into {topic} ')
    education = analysis.education('model_outputs')
    dups = 0
    inserts = 0
    for i in education:
        try:
            
            client.prod['education'].insert_one(i)
            inserts += 1
            # print(f'successfully inserted into education {len(res.inserted_ids)} documents')

        except DuplicateKeyError as e:
            dups +=1
    print(f"Inserted {inserts} into Education with {dups} duplicates")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    analysis_to_do = config["Analysis"]["analysisFiles"]
    country = config['Scraping']['Query']['location']
    dates = datetime.today().strftime('%m/%Y')
    date = datetime.strptime(dates, "%m/%Y")
    role = config["Role"]["title"]
    main(analysis_to_do,date,country,role)