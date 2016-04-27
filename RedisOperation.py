import redis
from Term import *

class RedisHandler:

   def __init__(self,h='localhost', p=6379, d=0):
        try:
            self.pool= redis.ConnectionPool(host=h, port=p, db=d)
            self.r = redis.Redis(connection_pool=self.pool)
        except redis.ConnectionError as e:
            print(e)

   def FetchData(self, key):
        try:
            value = self.r.get(key).decode('utf-8')
        except redis.RedisError as e:
            print(e)
            return ""
        return value

   def GetDFValue(self, term):
        if not self.ExistKey(term):
            return 0
        a = self.FetchData(term)
        if a == "":
            return 0
        try:
            df = a.split('[')
            df_value = int(df[0][1:])
        except TypeError as e:
            print(e)
            return 0
        return df_value  # return df_value of term

   def GetDocTermCount(self, docname):
        if not self.ExistKey(docname):
            return 0
        a = self.FetchData(docname)
        if a == "":
            return 0
        t = a[1:].split(',')
        try:
            count = int(t[0])
        except:
            return 0
        return count  # return the number of word of specific document

   def GetDocUrl(self, docname):
       if not self.ExistKey(docname):
           return ""
       a = self.FetchData(docname)
       if a == "":
           return ""
       t = a.split(',')
       return t[1]  # return the actual url link to document

   def GetDocFullContent(self,docname):
        if not self.ExistKey(docname):
           return ""
        a = self.FetchData(docname)
        if a == "":
            return ""
        t = a.split('[')
        length = len(t[1])
        c = t[1][:length-2].split(' ')
        return c    # return the actual string of document content

   def GetDBHeaderData(self):
       key = 'myDocID_0'
       if not self.ExistKey(key):
           return ""
       a = self.FetchData(key)
       if a == "":
           return ""
       datalist= []
       for i in a.split(","):
           datalist.append(i)
       return datalist       # first element is total words of DB, second element is number of all doc, third element is avaDoclength


   def GetTermPostingList(self, term):
        if not self.ExistKey(term):
            return ""
        a = self.FetchData(term)
        if a == "":
            return ""
        new_term = TermList(term)
        t = a.split(':')
        df = a.split('[')                    #{xx[
        df_v = int(df[0][1:])
        new_term.SetDFvalue(df_v)
        pos = t[0].find('[')                #{xx[doc_ID,tf_value;(x,x,x,)]
        new_term = self.AddDocToTermList(new_term,t[0][pos:])
        end = len(t)
        if end > 2:
            for i in range(1, end-1):
                new_term = self.AddDocToTermList(new_term, t[i])
        return new_term   # return structure TermList

   def AddDocToTermList(self, Tlist, data):   # [doc_ID,tf_value;(x,x,x,)]
        Document = DocDetail()
        t = data.split(';')
        docID = t[0].split(',')                    # [doc_ID,tf_value
        Document.SetDocID(docID[0][1:])
        end = len(t[1])-3                        # reduce  ,) from (x,x,x,)
        for i in t[1][1:end].split(','):        # x,x,x -> x x x
            Document.AddTermPosition(i)
        Tlist.AddDocument(Document)
        return Tlist

   def ExistKey(self, key):
        if not self.r.exists(key):
            print("Error,"+ key + " doesn't exist")
            return False
        else:
            return True