from Document import *


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

    def SetDFvalue(self, df):
        self.df_value = df

    def GetPostString(self, post_str):
        post_str = str(self.df_value) + "\t"
        for x in self.postinglist:
            post_str = x.PostStringDetial(post_str)
        return post_str

    def ValueString(self):
        value = [""]
        value[0] = "{" + str(self.df_value)
        for x in self.postinglist:
            value[0] = value[0] + x.GetSubString()
        value[0] += "}"
        return value[0]

    def GetPositonInDoc(self,docID):
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetPositionList()  # return the postion of a term in specific document
        return ""

    def GetTFValueInDoc(self, docID):
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetTFValue()      #return the raw tfvalue of a term in sepcific document
        print("document "+str(docID)+" doesn't exist")
        return 0


    def GetDocAndTFValueList(self, value=0, sort=True, order=True):   # default in reverse order sorted
        docdict={}
        for i in self.postinglist:
            docdict[i.doc_ID] = i.GetTFValue()
        if sort:
            if value == 0:
                a = sorted(docdict.items(), key = lambda d: d[1], reverse=order)  # return sorted nest list
                return a
            elif value == 1:
                b = list(docdict.keys())
                b.sort(reverse=order)
                return b                       # return sorted doclist
            elif value == 2:
                c = list(docdict.values())
                c.sort(reverse=order)
                return c                       # return sorted tfvaluelist
            else:
                print("Error, the number of value must be 0,1,2")
                return ""
        else:
            if value == 0:
                return list(docdict)           # return dictionary of pairs(doc_ID,tfvalue) in arbitrary order
            elif value == 1:
                return list(docdict.keys())    # return document list in arbitrary order
            elif value == 2:
                return list(docdict.values())  # return tfvalue list in arbitrary order
            else:
                print("Error, the number of value must be 0,1,2")
                return ""