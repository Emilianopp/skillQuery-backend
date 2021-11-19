from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
class Preprocessor: 
    def __init__(self, db:Mongo,date,role:str,country :str)-> None:
        self.db = db
        self.date = date
        self.role = role
        self.country = country
        
    def process_item(self,x:dict)->list:
        desc = x.get('description')
        if desc != None :
            return({'urls': x.get('url'), 'Country' : self.country,'role':self.role,'date':self.date,'inputs':[x for x in desc.split("\n") if x != ""]})
        else:
            return(False)
    def process(self) -> list:
        return([self.process_item(x) for x in self.descriptions if self.process_item(x)])


    def get_data(self) -> None:
        self.descriptions = self.db.query({"date":self.date,"country":self.country},{'description':1,'_id':0,'url':1})


