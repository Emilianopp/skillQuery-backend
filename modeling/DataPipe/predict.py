from pymongo.mongo_client import MongoClient
from classification import  *
from classification.tf_model.predictor_class import Predictor
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
import argparse
import yaml
def main(path_model:str,path_tokenizer:str,role:str)->None:
            client = MongoClient()
            db = Mongo(client,col = "model_inputs")
            predictor = Predictor(path_tokenizer=path_tokenizer,
            path_model=path_model,
            db = db,
            role = Role(role))
            out = predictor.predict_prod()
            db.db.model_outputs.insert_many(out.to_dict('records')
        )
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
    main(path_model = path_model,role = role,path_tokenizer = path_tokenizer)