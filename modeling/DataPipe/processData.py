import sys 
# sys.path.append("../scraping/classes/Database")
sys.path.append("../../scraping")
# from ....scripts.scraping.classes.Role import *
from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
from preprocessor.preprocessor import *
import argparse
import yaml
def main(role:str)->None:
    role = Role(role)
    client = MongoClient()
    db = Mongo(client)
    test = Preprocessor(role = role, db = db)
    test.get_data()
    records = test.process()
    db.db.model_inputs.bulk_write([InsertOne(x) for x in records])
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    role = config['Role']["title"]
    main(role = role)