
from tensorflow import keras
import tensorflow as tf
import numpy as np
from datasets import load_dataset
from sklearn.metrics import accuracy_score
from transformers import TFDistilBertForSequenceClassification, DistilBertConfig




'''
Predictor class 
Allows to create an object to run new data on 
path to pretrained tokinizers and model are required
'''
class Predictor:

  def __init__(self,path_tokinizer,path_model):
    self.tokenizer = DistilBertTokenizer.from_pretrained(path_tokinizer)
    self.model = tf.saved_model.load(path_model)

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
  def predict_prod(self,path):

    prod_data = load_dataset('csv', data_files=path)
    prod_txt = prod_data['train']['0']
    preds_prod = [self.pred_vectorized(x) for x in prod_txt] 
    df = pd.read_csv('/content/prod_data.csv',index_col = [0])
    df['out'] = pd.Series(preds_prod).values
    self.prod_predict = df 
    return df 

  def save_df(self,path):
    self.prod_predict.to_csv(path)


