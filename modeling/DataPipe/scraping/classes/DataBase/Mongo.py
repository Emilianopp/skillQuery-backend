import pymongo
from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne

class Mongo:

    def __init__(self,client:MongoClient,test_mode:bool = False,col = 'Scraped_Data')->None:
        self.client = client
        if(test_mode):
             self.db = self.client['test_db']
        else:
            self.db = self.client['prod']
        self.collection = self.db[col]

    def get_database(self,database:str)->None:
        return self.client[f'{database}']
    def make_index(self,index:str) -> None:
        self.collection.create_index(index, unique = True)
    def insert_document(self,doc:dict)->bool:
        self.collection.insert_one(doc)
    def query(self,condition:dict,select:dict):
        return(self.collection.find(condition,select))
    