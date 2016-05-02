from inner_kernel.Document import *
from inner_kernel.TypeEnum import WSMEnum
class TermList:

    def __init__(self, termName):
        self.term = termName
        self.df_value = 1
        self.postinglist = []

    def AddElementToPostingList(self, docID, term_position):
        element = DocDetail()
        element.SetDocID(docID)
        element.AddTermPosition(term_position)
        self.postinglist.append(element)

    def AddDocument(self, doc):
        self.postinglist.append(doc)

    def DFValueIncreaseOne(self):
        self.df_value += 1

    def SetDFValue(self, df):
        self.df_value = df

    def MergePostingList(self, NewTermList):
        '''
           used in the big data insert(not complete)
           merge two TermList obj which share the same term and is different in postinglist
           add two seperate df value together and union two postinglist
        '''
        if self.term != NewTermList.term:
            return False
        else:
            for i in NewTermList.postinglist:
                self.postinglist.append(i)
                self.DFValueIncreaseOne()
            return True

    def SearchTerm(self, tname, docID, position):
        if self.term != tname:
            return 0
        else:
            for x in self.postinglist:
                if x.doc_ID == docID:
                    x.AddTermPosition(position)
                    return 1
            self.AddElementToPostingList(docID, position)
            self.DFValueIncreaseOne()
            return 1

    def GetPostString(self, post_str):
        '''
           used in function SaveTable() in invert_index_fun.py file, to formulate the relationship of term
           with its private variable such as dfvalue and postinglist
        '''
        post_str = str(self.df_value) + "\t"
        for x in self.postinglist:
            post_str = x.PostStringDetial(post_str)
        return post_str

    def ValueString(self):
        '''
            used in function InsertDataToRedis() in RedisInnerLink.py file, to formulate the content of term
            as well as  its private variable such as dfvalue and postinglist in one string with some spilt symbol
         '''
        value = [""]
        value[0] = "{" + str(self.df_value)
        for x in self.postinglist:
            value[0] = value[0] + x.GetSubString()
        value[0] += "}"
        return value[0]

    def GetPositonInDoc(self,docID):
        '''
            used by query.py, and outer interface with search engine, return the position
            that the term appear in specific document, if the term is null(eg: search a
            term which can't in DB), return null list[]
         '''
        nulllist = []
        if len(self.postinglist) == 0:
            return nulllist
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetIntPositionList()
        return nulllist

    def GetPositionInDoc(self,docID):
        if not docID.isdigit():
            print("Error, document ID must be integer")
            return []
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetIntPositionList()  # return the postion of a term in specific document
        return []

    def GetTFValueInDoc(self, docID):
        '''
            used by query.py, and outer interface with search engine, return the raw TFvalue
            of a term (the number of times the term appear in a specific document),
            if the term is null(eg: search a term which can't in DB), return 0
         '''
        if not docID.isdigit():
            print("Error, document ID must be integer")
            return 0
        if len(self.postinglist) == 0:
            return 0
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetTFValue()
        print("document "+str(docID)+" doesn't exist")
        return 0


    def GetDocAndTFValueList(self, value= WSMEnum.DOC_TF_LIST, sort=True, order=True):   # default in reverse order sorted
        '''
             used by query.py, and outer interface with search engine, return the document list,
             TFvalue list or both of them according to the parameter

             value: (Default WSMEnum.DOC_TF_LIST)
             WSMEnum.DOC_TF_LIST : return a relation union list with Doclist and TFlist
             WSMEnum.DOC_TF_LIST : return Doclist
             WSMEnum.TFLIST : return TFlist

             sort: (Default True)
             True: return a sorted list
             False: return a arbitrary list

             order (Default True)
             True: rank from high to low
             False: rank from low to high

            if the term is null(eg: search a term which can't in DB), return null list []
         '''
        docdict={}
        if len(self.postinglist) == 0:
            return list(docdict)
        for i in self.postinglist:
            docdict[i.doc_ID] = i.GetTFValue()
        if sort:
            if value == WSMEnum.DOC_TF_LIST:
                a = sorted(docdict.items(), key = lambda d: d[1], reverse=order)  # return sorted nest list
                return a
            elif value == WSMEnum.DOCLIST:
                b = list(docdict.keys())
                b.sort(reverse=order)
                return b
            elif value == WSMEnum.TFLIST:
                c = list(docdict.values())
                c.sort(reverse=order)
                return c
            else:
                print("Error, the number of value must be DOC_TF_LIST,WSMEnum.DOCLIST,WSMEnum.TFLIST")
                return ""
        else:
            if value == WSMEnum.DOC_TF_LIST:
                return list(docdict)
            elif value == WSMEnum.DOCLIST:
                return list(docdict.keys())
            elif value == WSMEnum.TFLIST:
                return list(docdict.values())
            else:
                print("Error, the number of value must be DOC_TF_LIST,WSMEnum.DOCLIST,WSMEnum.TFLIST")
                return ""

