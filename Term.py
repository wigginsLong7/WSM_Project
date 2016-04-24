from Document import *

class TermList:
    def __init__(self, termName, docID, term_position):
        self.term = termName
        self.idf_value = 1
        self.postinglist = []
        element = DocDetail(docID, term_position)
        self.postinglist.append(element)

    def getpoststring(self, post_str):
        post_str = str(self.idf_value) + "\t"
        for x in self.postinglist:
            post_str = x.poststringdetial(post_str)
        return post_str