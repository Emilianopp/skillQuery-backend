import pymongo
from pymongo import MongoClient
from pymongo import InsertOne, DeleteOne, ReplaceOne

class Scraped_Data:

    def __init__(self,client:MongoClient,test_mode:bool = False)->None:
        self.client = client
        if(test_mode):
             self.db = self.client['test_db']
        else:
            self.db = self.client['prod']
        self.collection = self.db['Scraped_Data']

    def get_database(self,database:str)->None:
        return self.client[f'{database}']
    def make_index(self,index:str) -> None:
        self.collection.create_index(index, unique = True)
    def insert_document(self,doc:dict)->bool:
        self.collection.insert_one(doc)





# test = Scraped_Data(client)
# # test.make_index("url")
# test.instert_document({"url_1":"https://www.emilianopp.com","company":"company",'location':"location",'role':"role"})

