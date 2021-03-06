
class DocData:
    def __init__(self, docID):
        self.doc_ID = docID
        self.term_count = 0
        self.url = ""
        self.content = ""
        self.title = ""

    def SetDocCount(self, tcount):
        self.term_count = tcount
        return

    def SetUrl(self, urlpath):
        self.url = urlpath
        return

    def SetDocContent(self, insertcontent):
        self.content = insertcontent
        return

    def GetString(self):
        sub = [""]
        sub[0] = "{" + str(self.term_count)+ ","+self.url +","+self.title+","+"["+self.content+"]}"
        return sub[0]

    def SetTitle(self,tstring):
        self.title = tstring

class DocDetail:
    def __init__(self):
        self.doc_ID = 0
        self.positionlist = []

    def SetDocID(self, docID):
        self.doc_ID = docID

    def AddTermPosition(self, pos_i):
        self.positionlist.append(pos_i)

    def GetPositionList(self):
        return self.positionlist

    def GetIntPositionList(self):
        plist = []
        for i in self.positionlist:
            try:
                plist.append(int(i))
            except TypeError as e:
                print(e)
                return ""
        return plist

    def GetTFValue(self):
        return len(self.positionlist)

    def PostStringDetial(self, post_str):
        post_str = post_str + "(" + str(self.doc_ID) + " "+"tf_"+str(len(self.positionlist))+" "
        post_str += "["
        for y in self.positionlist:
            post_str = post_str + str(self.doc_ID)+"-"+str(y) + " "
        post_str += "])\t"
        return post_str

    def GetSubString(self):
        sub = [""]
        sub[0] = "[" + str(self.doc_ID)+","+str(len(self.positionlist))+";("
        for i in self.positionlist:
            sub[0] += (str(i)+",")
        sub[0] += ")]:"
        return sub[0]


