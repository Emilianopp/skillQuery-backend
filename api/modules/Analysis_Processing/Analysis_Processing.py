import pymongo 
import pandas as pd 
import plotly as px 
import numpy as np 
import sys
import pymongo
from pymongo import MongoClient 
import re
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from collections import Counter
from ..classes.Mongo import *
from ..classes.Role import *

class Analysis_Processing:
    def __init__(self,db:Mongo,role:Role):
        self.db = db
        self.role = role

    def get_data(self) -> pd.DataFrame:
        query_cursor = self.db.query({"role":self.role.title},{"_id":0},col = "model_outputs")
        out = pd.DataFrame(query_cursor)
        if ( out.empty):
            raise Exception("DATA FRAME EMPTY")
        return out

    def cleanse_sentence(self,sentence:str):
        stop = stopwords.words('english')
        sentence_clean = sentence.replace("-", " ")
        sentence_clean = re.sub("[\n]", " ",sentence_clean)
        sentence_clean = re.sub("[.!?/\()-,:]", "",sentence_clean)
        sentence_clean = sentence_clean.lower()
        sentence_clean = " ".join([word for word in sentence_clean.split(" ") if word not in stop])
        return sentence_clean

    def word_count(self, text:pd.Series):
        return Counter(self.cleanse_sentence(" ".join(text)).split(" "))

    def text_count(self,query_df):
        urls = query_df.urls.unique()
        count_arr = np.empty(shape = (len(urls)),dtype = Counter)
        for i,url in enumerate(urls):
            count_arr[i] = self.word_count(query_df[query_df.urls == url].text)
        return count_arr 

    def per_role_analysis(self,keyword_path,insert = False,col = None,insert_key = None ):
        tech_count = {}
        tech_list = pd.read_csv(keyword_path ,index_col=[0]).iloc[:,0].str.lower()
        for dicts in counters:
            for word in dicts.keys():
                if word in list(tech_list): 
                    if word not in tech_count.keys():
                        tech_count.update({word:1})
                    else:
                        tech_count[word] += 1
        if insert == True: 
            requests = [InsertOne({f"{insert_key}":tech_count,'role':self.role.title})]
            self.db.db[col].bulk_write(requests)
            print('successful insertion')
        else: 
            return tech_count

    def strip_digits_from_corupus(self,text):
        subs = re.sub("[\d+][+-]", "",text)
        subs = re.sub("[’']", "",subs)
        return(subs)
        
    def bigram_analysis(self,df,thresh = 5,insert = False,col = "bigrams"):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        corpus_list = [self.strip_digits_from_corupus(sentence) for sentence in df.text]
        corpus = ' '.join(corpus_list)
        finder = BigramCollocationFinder.from_words(corpus.lower().split(" "),window_size=2)
        finder.apply_freq_filter(thresh)
        bigram_results = finder.score_ngrams(bigram_measures.pmi)
        if insert == True: 
            requests =  [InsertOne({"bigram":x[0],"pmi":x[1],'role':self.role.title}) for x in bigram_results]
            self.db.db[col].write(requests)
            print("successful insertion")
        else: 
            return bigram_results 

    def store_analysis(self,db,data:dict):
        [{"bigram":x[0],"pmi":x[1]} for x in analysis.bigram_analysis(df = query_df)]
        requests = [InsertOne(x) for x in data]
        scrape_table.collection.bulk_write(requests)
        return None