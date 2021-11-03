import pymongo
from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne
from pymongo import collection
#=====================PRIMARY WAY TO INTERACT WITH MONGO=====================#
class Mongo:
    
    def __init__(self,client:MongoClient,test_mode:bool = False,col = 'Scraped_Data')->None:
        self.client = client
        if(test_mode):
             self.db = self.client['test_db']
        else:
            self.db = self.client['prod']
        self.collection = self.db[col]
    #returns the current database 
    def get_database(self,database:str)->None:
        return self.client[f'{database}']
    #makes an index for the collection
    def make_index(self,index:str) -> None:
        self.collection.create_index(index, unique = True)
    #inserts document into database
    def insert_document(self,doc:dict,col = None)->bool:
        if col == None: 
            in_collection = self.collection
        else: 
            in_collection = col
        in_collection.insert_one(doc)
    #Queries the database based on conditions selected
    def query(self,condition:dict,select:dict,col =None ):
        if col == None:
            collection = self.collection
        else: 
            collection = self.db[col]
        return(collection.find(condition,select))
