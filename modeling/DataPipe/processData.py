import sys 
sys.path.append("../../scraping")
from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
from preprocessor.preprocessor import *
from datetime import datetime
from pymongo.errors import BulkWriteError
import argparse
import yaml
def main(date,role,country)->None:
    client = MongoClient()
    db = Mongo(client,col = 'Scraped_Data')
    pre = Preprocessor( db = db,date = date,role = role ,country = country)
    pre.get_data()
    records = pre.process()
    try:
         db.db.model_inputs.insert_many(records)
    except BulkWriteError as e:
        print(e)
        pass
   
    print("Processed")
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                     type=str)
    args = parser.parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    date = datetime.strptime(config['Date'], "%m/%Y")
    role = config["Role"]['title']
    country = config['Scraping']['Query']['location']
    main(date,role,country)