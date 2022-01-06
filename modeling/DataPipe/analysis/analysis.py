import pymongo 
import pandas as pd 
import numpy as np 
import sys
import pymongo
from pymongo import MongoClient 
import re
import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
from collections import Counter
sys.path.append("../DataPipe/")
from scraping.classes.DataBase.Mongo import *
from scraping.classes.Role import *


class Analysis_Processing:
    def __init__(self,db,role:Role,date,country:str):
        self.db = db
        self.role = role
        self.date = date
        self.country = country
        self.date = date
    '''
    if a pipeline is given, returns a dataframe with the pipeline query
    if none is given, returns all model outputs as a dataframe 
    '''
    def get_data(self,col,pipe=None) -> pd.DataFrame:
        if pipe != None:
            query_cursor = self.db[col].aggregate(pipe)
        else:
            query_cursor = self.db[col].find({"date":self.date,"Country":self.country,'role':self.role.title},{"_id":0,"text":1})
            query_cursor = {"text":[x.get("text") for x in query_cursor]}
        out = pd.DataFrame(query_cursor)
        if ( out.empty):
            raise Exception("DATA FRAME EMPTY")
        return out


    '''
   cleanse_sentence and strip_digits_from_corpus 
    you can play around with they were both experimental
    
    '''
    '''
    Strips symbols from sentence 
    still does not strip "," <- to fix
    '''
    def cleanse_sentence(self,sentence:str):
        stop = stopwords.words('english')
        sentence_clean = sentence.replace("-", " ")
        sentence_clean = sentence.replace(",", "")
        sentence_clean = re.sub("[\n]", " ",sentence_clean)
        sentence_clean = re.sub("[.!?/\()-,:]", "",sentence_clean)
        sentence_clean = sentence_clean.lower()
        sentence_clean = " ".join([word for word in sentence_clean.split(" ") if word not in stop])
        return sentence_clean

    '''
    Strips digits from sentence
    mostly used for bigram stuff
    '''
    def strip_digits_from_corpus(self,text):
        subs = re.sub("[\d+][+-]", "",text)
        subs = re.sub("[’']", "",subs)
        return(subs)

    '''
    finds keywords in model outputs
    filters model outputs by url
    this way we do not count repeats of words in a single posting
    can do analysis with any txt file as long as the format is correct
    '''
    def do_analysis(self,keyword_path,col = None ):
        urls = []
        urls_used = []
        #load tech lists
        tech_list = list(pd.read_csv(keyword_path).iloc[:,0].str.lower())
        #load all text 
        # model_outs = self.db[col].find({},{"text":1, "_id":0,'urls':1 })
        model_outs = self.db[col].find({"country":self.country,'role':self.role.title,"date":self.date},{"text":1, "_id":0,'urls':1 })
        #iterate through text, for items in list
        for text_dict in model_outs:
            found = []
            text = text_dict.get("text")
            text = self.cleanse_sentence(text)
            url = text_dict.get('urls')
            for word in text.split(" "):
                if word in tech_list:
                   found.append(word)
            if url not in urls_used and found:
                metaData = self.db.Scraped_Data.find_one({"url":url},{"country":1, "_id":0,'title':1,"date":1 ,'region':1})               
                urls.append({'url':url,"date" :metaData.get("date"),"role":metaData.get('title'),"Country":metaData.get("country"), 'region':metaData.get('region'),'found_list': found})
                urls_used.append(url)
            elif found:
                target = [x for x in urls if x.get("url") == url][0]
                if target['found_list']:
                    target['found_list'] = list(set(found + target['found_list']))
        return urls

    def education(self,col = None):
        model_outs = self.db[col].find({"country":self.country,'role':self.role.title,"date":self.date},{"text":1, "_id":0,'urls':1 })
        # model_outs = self.db[col].find({},{"text":1, "_id":0,'urls':1 })
        
        bachelor = ["bachelor","bsc","ba","bachelors","bs","undergraduate"]
        masters = ["masters","msc","ma"]
        phd = ["phd","doctorate"]
        out = []
        for text_dict in model_outs:
            text = text_dict.get("text")
            text = self.cleanse_sentence(text)
            url = text_dict.get('urls')
            
            for word in text.split(" "):
                degrees = {}
                educs = {}
                if word in bachelor:
                    educs.update({"Bachelors":1})
                if word in masters:
                    educs.update({"Masters":1})
                if word in phd:
                    educs.update({"PHD":1})
                if educs: 
                    metaData = self.db.Scraped_Data.find_one({"url":url},{"country":1, "_id":0,'title':1,"date":1,'region':1 })
                    degrees.update({'url':url,"date" :metaData.get("date"),"role":metaData.get("title"),"Country":metaData.get("country"), 'region':metaData.get('region'),"degrees":educs})
                    out.append(degrees)
        return out 




    '''
    
    #======================================================================#
    #=====================================BIGRAMS==========================#
    #======================================================================#
    
    '''
    '''
    Bigram analysis still need to fix and touch up
    '''
    def bigram_analysis(self,df,thresh = 5):
        bigram_measures = nltk.collocations.BigramAssocMeasures()
        corpus_list = [self.cleanse_sentence(self.strip_digits_from_corpus(sentence)) for sentence in df.text]
        corpus = ' '.join(corpus_list)
        finder = BigramCollocationFinder.from_words(corpus.lower().split(" "),window_size=2)
        finder.apply_freq_filter(thresh)
        bigram_results = finder.score_ngrams(bigram_measures.pmi)
        return bigram_results 

