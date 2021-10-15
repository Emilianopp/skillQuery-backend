#=====================Class Role, allows to search and filter out roles we want from those we aren't interested in=====================#
import re
class Role:
    def __init__(self, must, thresh):
        self.must = must
        self.score = 0
        self.thresh = thresh

    def check_role(self, role):
        regex_expressions = [fr"(?=.*\b{i.lower()}\b)" for i in self.must]
        self.score = sum([bool(re.search(m, role)) for m in regex_expressions])
        return self.score