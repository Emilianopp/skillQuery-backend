from scraping.classes.Role import *
from scraping.classes.DataBase.Mongo import *
class Preprocessor: 
    def __init__(self, db:Mongo)-> None:
        self.db = db
    def process_item(self,x:dict)->list:
        desc = x.get('description')
        if desc != None :
            return({'urls': x.get('url'), 'inputs':[x for x in desc.split("\n") if x != ""]})
        else:
            return(False)
    def process(self) -> list:
        return([self.process_item(x) for x in self.descriptions if self.process_item(x)])


    def get_data(self) -> None:
        self.descriptions = self.db.query({},{'description':1,'_id':0,'url':1})


