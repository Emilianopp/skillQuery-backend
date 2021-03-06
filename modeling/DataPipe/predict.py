from datetime import datetime
from pymongo.mongo_client import MongoClient
from classification import *
from classification.tf_model.predictor_class import Predictor
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
import argparse
import yaml


def main(path_model: str, path_tokenizer: str, role: str, date, country: str) -> None:

    '''DATABASE CONFIGS'''
    mdb = open(r"./mongo.txt", "r").read()
    client = MongoClient(mdb)
    db = client.prod
    '''=============='''

    '''PREICTOR OBJECT'''
    predictor = Predictor(
        path_tokenizer=path_tokenizer,
        path_model=path_model,
        db=db,
        role=Role(role),
        date=date,
        country=country)
    '''=============='''

    '''PREDICTION'''
    out = predictor.predict_prod()
    print("Done classifying")
    db.model_outputs.insert_many(out.to_dict('records'))
    print("Model run comleted")
    '''=============='''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    role = config['Role']['title']
    path_model = config["Predict"]["path_model"]
    path_tokenizer = config['Predict']['path_tokenizer']
    country = config['Scraping']['Query']['location']
    dates = datetime.today().strftime('%m/%Y')
    date = datetime.strptime(dates, "%m/%Y")
    main(path_model=path_model, role=role,
         path_tokenizer=path_tokenizer, date=date, country=country)
