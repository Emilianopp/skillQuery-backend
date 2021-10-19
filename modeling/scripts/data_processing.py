import sys 
# sys.path.append("../scraping/classes/Database")
sys.path.append("../../scraping")
# from ....scripts.scraping.classes.Role import *
from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
from preprocessor.preprocessor import *

role = Role('Software Engineer',2)
client = MongoClient()
db = Mongo(client)
test = Preprocessor(role = role, db = db)
test.get_data()
records = test.process()
db.db.model_inputs.bulk_write([InsertOne(x) for x in records])