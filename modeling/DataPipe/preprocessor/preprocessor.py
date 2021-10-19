from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
class Preprocessor: 
    def __init__(self,role:Role, db:Mongo)-> None:
        self.db = db
        self.role = role
    def process_item(self,x:dict)->list:
        desc = x.get('description')
        return({'urls': x.get('url'), 'inputs':[x for x in desc.split("\n") if x != "" ],"role":self.role.title})

    def process(self) -> list:
        return([self.process_item(x) for x in self.descriptions])


    def get_data(self) -> None:
        self.descriptions = self.db.query({"title":self.role.title},{'description':1,'_id':0,'url':1})


