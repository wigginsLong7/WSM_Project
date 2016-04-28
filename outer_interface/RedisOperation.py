import redis
from inner_kernel.Term import *
from inner_kernel.TypeEnum import WSMEnum

class RedisHandler:

   def __init__(self, h='localhost', p=6379, d=0):
        try:
            self.pool = redis.ConnectionPool(host=h, port=p, db=d)
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
        key = '0'
        if not self.ExistKey(key):
            return ""
        a = self.FetchData(key)
        if a == "":
           return ""
        datalist= []
        for i in a.split(","):
            try:
                datalist.append(int(i))
            except TypeError as e:
                print(e)
                return ""
        return datalist       # first element is total words of DB, second element is number of all doc, third element is avaDoclength


   def GetTermPostingList(self, term):
        cterm = ""
        if term.isdigit():
            cterm = "D_"+str(term)
        else:
            cterm = term
        if not self.ExistKey(cterm):
            return ""
        a = self.FetchData(cterm)
        if a == "":
            return ""
        new_term = TermList(cterm)
        t = a.split(':')
        df = a.split('[')                    #{xx[
        df_v = int(df[0][1:])
        new_term.SetDFValue(df_v)
        pos = t[0].find('[')                #{xx[doc_ID,tf_value;(x,x,x,)]
        new_term = self.AddDocToTermList(new_term, t[0][pos:])
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
             print("Error," + key + " doesn't exist")
             return False
        else:
             return True


'''
   def KeyModify(self, key, value):
        ma = [""]
        if value == WSMEnum.AUTHOR:
            ma[0] = 'A_' + str(key)
        elif value == WSMEnum.TITLE:
            ma[0] = 'T_' + str(key)
        elif value == WSMEnum.BOOKTITLE:
            ma[0] = 'BT_' + str(key)
        elif value == WSMEnum.YEAR:
            ma[0] = 'Y_' + str(key)
        elif value == WSMEnum.PAGE:
            ma[0] = 'P_' + str(key)
        elif value == WSMEnum.VOLUMN:
            ma[0] = 'V_' + str(key)
        elif value == WSMEnum.JOURNAL:
            ma[0] = 'J_' + str(key)
        else:
            print("Error,wrong type")
            return ""
        return ma[0]

   def GetTermPostingList2(self, term, value=WSMEnum.ALLTYPES):
        tlist = []
        if value in range(10, 17):
            return self.GetTermPostingList(self.KeyModify(term, value))
        elif value == WSMEnum.ALLTYPES:
            for i in range(10, 17):
                newtermlist = self.GetTermPostingList(self.KeyModify(term, i))
                if newtermlist != "":
                    tlist.append(newtermlist)
            if len(tlist) <= 1:
                return tlist
            else:
                return self.UnityTerm(tlist, term)
        else:
            return ""
   def UnityTerm(self, Tlist, termname):
       return
'''