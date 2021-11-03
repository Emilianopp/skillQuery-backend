from pymongo.errors import BulkWriteError
from analysis.analysis import Analysis_Processing
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
from pymongo import MongoClient
import argparse
import yaml


def main(analysis_to_do)->None:
    client = MongoClient()
    db = Mongo(client)
    analysis = Analysis_Processing(db,Role("Data Science") )
    for topic in analysis_to_do.keys():
        inserts = analysis.do_analysis(fr"{analysis_to_do.get(topic)}" ,col = 'model_outputs')
        try:
            client.prod[topic].insert_many(inserts)
        except BulkWriteError as e:
            pass
        print(f'successfully into {topic}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="yaml config file for query",
                        type=str)
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    analysis_to_do = config["Analysis"]["analysisFiles"]
    main(analysis_to_do)