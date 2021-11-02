from pymongo import MongoClient
import pandas as pd 

client = MongoClient()
data_col = client.prod.model_inputs
col = data_col.find({},{"inputs":1,"_id":0})
records = pd.DataFrame(col)
records.to_csv("../model_in.csv")
records.sample(.2).to_csv('../sample.csv')