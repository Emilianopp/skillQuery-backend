
from pandas.core import series
import tensorflow as tf
import numpy as np
from datasets import load_dataset
from transformers import DistilBertTokenizer
import sys
sys.path.append("../../scraping")
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
from transformers import TFAutoModelForSequenceClassification
import pandas as pd
from itertools import cycle, islice

'''
Predictor class 
Allows to create an object to run new data on 
path to pretrained tokinizers and model are required
'''
class Predictor:

  def __init__(self,path_tokinizer,path_model,db:Mongo,role:Role):
    self.tokenizer = DistilBertTokenizer.from_pretrained(path_tokinizer)
    self.model = TFAutoModelForSequenceClassification.from_pretrained(path_model)
    self.db = db
    self.role = role

  '''
  runs predictions for a given sentance
  '''
  def pred_vectorized(self,text,max_length = 150):
      preds = self.tokenizer.encode(text,truncation=True,padding=True,max_length=max_length,return_tensors="tf")
      pred =  self.model.predict(preds)[0]
      softed = tf.nn.softmax(pred).numpy()[0]
      out = np.where( np.round(softed) ==1)[0][0]
      return out

  '''
  Predicts and runs a list comprehension to predict values

  +++++++++++++++++++++++++++++
  Find a way to do this with numpy vectorization
  +++++++++++++++++++++++++++++
  
  '''
  def predict_prod(self) -> pd.DataFrame:

    inputs = self.db.query({"role":self.role.title},{"urls":1,"_id":0,"inputs":1})
    series_inputs = pd.DataFrame(inputs)
    lengths = [len(x) for x in series_inputs.inputs]
    df = pd.DataFrame()
    df['inputs'] = sum(series_inputs.inputs,[])
    df["out"] = list(map(self.pred_vectorized,df.inputs))
    df['urls'] = sum([x * [m] for x,m in zip(lengths,series_inputs.urls)],[])
    return df

  def save_df(self,path):
    self.prod_predict.to_csv(path)


