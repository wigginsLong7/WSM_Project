import redis
from inner_kernel.Term import *
import gc

class RedisLinker:
    '''
       inherited by the child class in outer interface named RedisHandler
    '''
    def __init__(self, h='localhost', p=6379, d=0):
        try:
            self.pool = redis.ConnectionPool(host=h, port=p, db=d)
            self.r = redis.Redis(connection_pool=self.pool)
        except redis.ConnectionError as e:
            print(e)
        self.pipenum = 100
        #self.insertnum = 100

    def GetTermPostingList(self, term):
        '''
            decode the string from the redis DataBase and construct it into the TermList obj
            if the term is in DB, return the actual Termlist obj ,else return the
            null Termlist obj which postinglist is the null list[]
        '''
        cterm = ""
        if term.isdigit():
            cterm = "D_" + str(term)
        else:
            cterm = term
        if not self.ExistKey(cterm):
            return TermList(cterm)
        a = self.FetchData(cterm)
        if a == "":
            return ""
        new_term = TermList(cterm)
        t = a.split(':')
        df = a.split('[')  # {xx[
        df_v = int(df[0][1:])
        new_term.SetDFValue(df_v)
        pos = t[0].find('[')  # {xx[doc_ID,tf_value;(x,x,x,)]
        new_term = self.AddDocToTermList(new_term, t[0][pos:])
        end = len(t)
        if end > 2:
            for i in range(1, end - 1):
                new_term = self.AddDocToTermList(new_term, t[i])
        return new_term  # return structure TermList

    def AddDocToTermList(self, Tlist, data):  # [doc_ID,tf_value;(x,x,x,)]
        '''
            called by the same class fucntion GetTermPostingList(), a part of job in decoding
        '''
        Document = DocDetail()
        t = data.split(';')
        docID = t[0].split(',')  # [doc_ID,tf_value
        Document.SetDocID(docID[0][1:])
        end = len(t[1]) - 3  # reduce  ,) from (x,x,x,)
        for i in t[1][1:end].split(','):  # x,x,x -> x x x
            Document.AddTermPosition(i)
        Tlist.AddDocument(Document)
        return Tlist

    def ExistKey(self, key, p=True):
        '''
           judge whether the search term exists in DB or not
        '''
        if not self.r.exists(key):
            if p:
                print("key: " + key + " doesn't exist")
            return False
        else:
            return True

    def RedisInsert(self, key, value):
        '''
            Insert the key-value pair into the redis DB ,if the key already exits,
            this function will modify the new value to replace the old one
         '''
        try:
            self.r.set(key, value)
        except redis.RedisError as e:
            print(e)
            return False
        print("add success")
        return True
    '''
    def CheckMergeInRedis(self, TermTable):
        if len(TermTable) >= self.insertnum:
            TermTable.sort(key=lambda TermList: TermList.term)
            if self.r.dbsize() == 0:
                if not self.InsertDataToRedis(TermTable):
                    return WSMEnum.TERM_INSERT_FAIL
            else:
                if not self.MergeInRedis(TermTable):
                    return WSMEnum.TERM_INSERT_FAIL
            return WSMEnum.TERM_INSERT_SUCCESS
        else:
            return WSMEnum.TERM_NOT_ENOUGTH
    '''
    def InsertDataToRedis(self, Tlist):
        '''
           called by inverttable.py, this function is used to insert all the key-value pair in redis DB
            use the pipeline to accelerate the insert speed and at last "delete" the reference Tlist, If
            Insert Data into Redis successfully, return True, else return False
        '''
        p = self.r.pipeline()
        count = [0]
        for i in Tlist:
            if isinstance(i, TermList):
                p.set(i.term, i.ValueString())
            elif isinstance(i, DocData):
                p.set(i.doc_ID, i.GetString())
            if not self.PiplineInsertCheck(count, p):
                return False
            count[0] += 1
        if count[0] > 1 and not self.RedisPiplineInsert(p):
            return False
        p.reset()
        del Tlist
        gc.collect()
        return True

    def RedisPiplineInsert(self, p):
        '''
            called by Same class function InsertDataToRedis() and PiplineInsertCheck(), this function is used to execute
            the actual insert command, if execute successfully return True, else return False
         '''
        try:
            p.execute()
        except redis.RedisError as e:
            print(e)
            return False
        p.reset()
        print("pipeline add success")
        return True
    '''
    def MergeInRedis(self, TermTable):
        p = self.r.pipeline()
        count = [0]
        for i in TermTable:
            if self.ExistKey(i.term, False):
                old_term = self.GetTermPostingList(i.term)
                if old_term != "":
                    old_term.MergePostingList(i)
                    p.set(old_term.term, old_term.ValueString())
                else:
                    return False
            else:
                p.set(i.term, i.ValueString())
            if not self.PiplineInsertCheck(count, p):
                return False
            count[0] += 1
        if count[0] > 1 and not self.RedisPiplineInsert(p):
            return False
        p.reset()
        return True
    '''
    def PiplineInsertCheck(self, time, p):
        '''
            called by Same class function InsertDataToRedis(), this function is used to check the number
            of insert command of pipeline and if it reach the upper bound and call the fucntion RedisPiplineInsert() to
            execute it. Finally, reset the number of count
         '''
        if time[0] >= self.pipenum:
            if not self.RedisPiplineInsert(p):
                return False
            time[0] = 0
        return True

    def RefreshDB(self):
        '''
           called by inverttable.py ,clear all the key-value data of the whole redis DB(from 0 - n DB)
        '''
        try:
            self.r.flushall()
        except redis.ConnectionError as e:
            print(e)
            return False
        return True

    def FetchData(self, key):
        '''
           get the value of key , if not success, return null string
        '''
        try:
            value = self.r.get(key).decode('utf-8')
        except redis.RedisError as e:
            print(e)
            return ""
        return value

    def SaveData(self):
        '''
            called by inverttable.py ,save the redis DB data from memory to hard disk with the  dump.rbd file
        '''
        try:
            self.r.save()
        except redis.RedisError as e:
            print(e)
        return True
