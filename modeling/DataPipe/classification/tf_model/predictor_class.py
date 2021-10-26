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

  def __init__(self,path_tokenizer,path_model,db:Mongo,role:Role):
    self.tokenizer = DistilBertTokenizer.from_pretrained(path_tokenizer)
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
    df['text'] = sum(series_inputs.inputs,[])
    df["out"] = list(map(self.pred_vectorized,df.text))
    df['urls'] = sum([x * [m] for x,m in zip(lengths,series_inputs.urls)],[])
    df["role"] = [self.role.title for x in range(len(df.out))]
    return df[df.out == 1].drop(['out'],axis = 1)

  def save_df(self,path):
    self.prod_predict.to_csv(path)


