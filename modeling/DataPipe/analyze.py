from pymongo.errors import BulkWriteError
from analysis.analysis import Analysis_Processing
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
from datetime import datetime
from pymongo import MongoClient
import argparse
import yaml



def main(analysis_to_do,date,country,role:str)->None:
    client = MongoClient('mongodb+srv://emilianopp:Jonsnow1@cluster0.2p4zi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
    db = Mongo(client)
    analysis = Analysis_Processing(db,Role(role) ,date,country)
    for topic in analysis_to_do.keys():
        inserts = analysis.do_analysis(fr"{analysis_to_do.get(topic)}" ,col = 'model_outputs')
        try:
            client.prod[topic].insert_many(inserts)
        except BulkWriteError as e:
            pass
        print(f'successfully inserted into {topic}')
    education = analysis.education('model_outputs')
    try:
        client.prod['education'].insert_many(education)
    except BulkWriteError as e:
        pass
    print("succesfully insterted into education")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    analysis_to_do = config["Analysis"]["analysisFiles"]
    country = config['Scraping']['Query']['location']
    date = datetime.strptime(config['Date'],"%m/%Y")
    role = config["Role"]["title"]
    main(analysis_to_do,date,country,role)