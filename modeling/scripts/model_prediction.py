from pymongo.mongo_client import MongoClient
from classification import  *
from classification.tf_model.predictor_class import Predictor
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
client = MongoClient()
db = Mongo(client,col = "model_inputs")
predictor = Predictor(path_tokinizer="./classification/tf_model/tokenizer",
path_model="./classification/tf_model/model_BERT",
db = db,
role = Role('Software Engineer'))
out = predictor.predict_prod()
db.db.model_outputs.insert_many(out.to_dict('records'))