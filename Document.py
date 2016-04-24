
class DocFullData:
    def __init__(self, docID, content):
        self.doc_ID = docID
        self.doctext = content

class DocData:
    def __init__(self, docID, tcount, urlpath):
        self.doc_ID = docID
        self.term_count = tcount
        self.url = urlpath

class DocDetail:
    def __init__(self, docID, tfvalue):
        self.doc_ID = docID
        self.positionlist = []
        self.positionlist.append(tfvalue)
    def poststringdetial(self, post_str):
        post_str = post_str + "(" + str(self.doc_ID) + "," + str(len(self.positionlist)) + " "
        post_str += "["
        for y in self.positionlist:
            post_str = post_str + str(y) + " "
        post_str += "])\t"
        return post_str