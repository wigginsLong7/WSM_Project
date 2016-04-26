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

    def GetDocIDList(self):
        docID = []
        for i in self.postinglist:
            docID.append(i.doc_ID)
        return docID   # return all the doc_ID under the term

    def GetPositonInDoc(self,docID):
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetPositionList()  # return the postion of a term in specific document
        return ""

    def GetTFValueInDoc(self, docID):
        for i in self.postinglist:
            if docID == i.doc_ID:
                return i.GetTFValue()  #return the raw tfvalue of a term in sepcific document
        print("document "+str(docID)+" doesn't exist")
        return 0

    def GetTFValueList(self):
        TFlist = []
        for i in self.postinglist:
            a = self.GetTFValueInDoc(i.doc_ID)
            if a != 0:
                TFlist.append(a)
            else:
                return 0
        return TFlist  # all the doc_ID under term