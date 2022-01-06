from datetime import datetime
import enum
import tensorflow as tf
import numpy as np
from transformers import DistilBertTokenizer
import sys
sys.path.append("../../scraping")
from scraping.classes.DataBase.Mongo import Mongo
from scraping.classes.Role import Role
from transformers import TFAutoModelForSequenceClassification
import pandas as pd


'''
Predictor class 
Allows to create an object to run new data on 
path to pretrained tokenizers and model are required
'''
class Predictor:

  def __init__(self,path_tokenizer,path_model,db,role:Role,date,country:str):
    self.model = TFAutoModelForSequenceClassification.from_pretrained(path_model)
    self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    self.db = db
    self.role = role
    self.date = date
    self.country = country

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
  
    inputs = self.db.model_inputs.find({'role':self.role.title,"date":self.date,"Country":self.country},{"urls":1,"_id":0,"inputs":1})

    # inputs = self.db.model_inputs.find({},{"urls":1,"_id":0,"inputs":1})
  
    series_inputs = pd.DataFrame(inputs)
    series_inputs['inputs'].replace('empty', np.nan, inplace=True)
    series_inputs.dropna(subset=['inputs'], inplace=True)
    lengths = [len(x) for x in series_inputs.inputs]
    df = pd.DataFrame()
    df['text'] = sum(series_inputs.inputs,[])
    res = []
    print(f"Starting predictions of {len(df.text)} lines")
    for i,line in enumerate(df.text):
      res.append(self.pred_vectorized(line))
      if i % 100 == 0: 
        print(f'checkpoint index at {i} of {len(df.text)}')
    df["out"] = res
    df['urls'] = sum([x * [m] for x,m in zip(lengths,series_inputs.urls)],[])
    df["role"] = [self.role.title for x in range(len(df.out))]
    df["date"] = [self.date for x in range(len(df.out))]
    df["country"] = [self.country for x in range(len(df.out))]
    return df[df.out == 1].drop(['out'],axis = 1)

  def save_df(self,path):
    self.prod_predict.to_csv(path)


