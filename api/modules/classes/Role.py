#=====================Class Role, allows to search and filter out roles we want from those we aren't interested in=====================#
import re
class Role:
    def __init__(self, title:str, thresh:int =2,alternate_tittles:str = None) -> None:
        self.title = title
        self.score = 0
        self.thresh = thresh
        self.alternate_tittles = alternate_tittles
        if self.alternate_tittles != None:
            self.rank_list = self.title.split(" ") + self.alternate_tittles.split(" ")
        else:
            self.rank_list = self.title.split(" ")
    def check_role(self, role:str) -> int:
        regex_expressions = [fr"(?=.*\b{i.lower()}\b)" for i in self.rank_list]
        self.score = sum([bool(re.search(m, role)) for m in regex_expressions])
        return self.score