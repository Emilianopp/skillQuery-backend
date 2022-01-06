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
        # self.descriptions = self.db.Scraped_Data.find({},{'description':1,'_id':0,'url':1})

        self.descriptions = self.db.Scraped_Data.find({'title':self.role,"country":self.country,'date':self.date},{'description':1,'_id':0,'url':1})
     


