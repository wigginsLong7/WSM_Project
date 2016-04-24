import socket
import urllib.request
from invert_index_fun import *
from urllib.error import URLError, HTTPError

<<<<<<< HEAD
=======

"""
TODO:
1. add tokenization part
2. restructure codes
3. I don't know what else > <
"""


>>>>>>> origin/master
timeout = 30

socket.setdefaulttimeout(timeout)

<<<<<<< HEAD
=======

class DocData:
    def __init__(self, docID, tcount,urlpath):
        self.doc_ID = docID
        self.term_count = tcount
        self.url = urlpath


class DocDetail:
    def __init__(self, docID, tfvalue):
        self.doc_ID = docID
        self.tf = tfvalue

class TermList:
    def __init__(self, termName):
        self.term = termName
        self.idf_value = 1
        self.postinglist = []


def contentmodify(content, d_data, value):
    d_str= [""]
    if value==0 :
        while d_data:
            a = d_data.pop()
            content[0] = content[0] + a + " "
    else:
        while d_data:
            a = d_data.pop()
            d_str[0] = d_str[0] + a + " "
        for i in range(0, 62):
            d_str[0] = d_str[0].replace(list[i], latin[i])
            d_str[0] = d_str[0].replace(';', '')
        content[0] = content[0] + d_str[0] + " "
    return content[0]

def AddTerm(list, addterm, docID, doc_c):
    a = 0
    for i in range(len(list)):
        if list[i].term == addterm:  # an old term
            a = 1
            samedoc = 0
            for x in list[i].postinglist:
                if x.doc_ID == docID:  # in the same doc
                    x.tf += 1/doc_c
                    samedoc = 1
                    break
            if samedoc == 0:  # new doc
                element = DocDetail(docID, (1/doc_c))
                list[i].postinglist.append(element)
                list[i].idf_value += 1
            break
    if a == 0:  #new term
        newdoc = TermList(addterm)
        element = DocDetail(docID, (1 / doc_c))
        newdoc.postinglist.append(element)
        list.append(newdoc)
    return list

def CalculateDFvalue(list,doc_count):
    for i in range(len(list)):
        a = list[i].idf_value
        if a>=1:
           list[i].idf_value = math.log(doc_count/a)
    return

def PrintTermTable(list):
    for i in list:
        print("term is: "+i.term+" idf is: "+str(i.idf_value))
        doc_str = [""]
        for x in i.postinglist:
            doc_str[0] = doc_str[0]+"["+str(x.doc_ID)+"( "+str(x.tf)+")]"+","
        print(doc_str[0])
    return
def PrintDocTable(list):
    for i in range(len(list)):
        print("the doc"+str(list[i].doc_ID) + " and its capacity is " + str(list[i].term_count)+" and its url is" + list[i].url)
    return
def SaveDocTale(list):
    DocList = open("DocData.txt", 'w')  # 存储 postinglist Doc 文件
    for i in range(len(list)):
        try:
           DocList.write(str(list[i].doc_ID) + "\t" + str(list[i].term_count) + "\t" + list[i].url + "\n")
        except:
           print("wrong")
    DocList.close()
    return
def SaveTable(list):
    DocPostList = open("dbl.txt", 'wb')  # 存储 postinglist Doc 文件
    TFvalue = open("TFvalue.txt", 'wb')  # 存储postinglist tfvalue文件
    IDFvalue = open("IDFvalue.txt", 'wb')  # 存储 term IDF value文件
    for i in list:
        try:
            IDFvalue.write(i.term.encode('utf-8')+"\t".encode('utf-8') + str(i.idf_value).encode('utf-8') + "\r\n".encode('utf-8'))
        except:
            print("something wrong in" + str(i.term))
        doc_str = [""]
        tf_str = [""]
        for x in i.postinglist:
            tf_str[0] = tf_str[0]+str(x.tf)+"\t"
            doc_str[0] = doc_str[0]+str(x.doc_ID) + "\t"
        try:
            TFvalue.write(i.term.encode('utf-8') + "\t".encode('utf-8') + tf_str[0].encode('utf-8') + "\r\n".encode('utf-8'))
            DocPostList.write(i.term.encode('utf-8')+"\t".encode('utf-8') + doc_str[0].encode('utf-8') + "\r\n".encode('utf-8'))
        except:
            print("something wrong in" + str(i.term))
    IDFvalue.close()
    DocPostList.close()
    TFvalue.close()
    return

>>>>>>> origin/master
Linkurlset = []
linkfile = open('dblpxmlsource.txt', 'r')
linklines = linkfile.readlines()
for line in linklines:
    Linkurlset.append(line)

# ------------------------read the xml file----------------------------
<<<<<<< HEAD
inputfile = open('dblpxml.txt', 'r')
=======
inputfile = open('dblpxml1000.txt', 'r')
>>>>>>> origin/master
lines = inputfile.readlines()
TermTable = []
DocContent = []
DocText = []
url_count = 0
true_doc_count = 1
for line in lines:
    url_count += 1
    # read xml path
    url = line
    try:
        urlop = urllib.request.urlopen(url)
    except HTTPError as e:
        print(e.reason)
        continue
    except URLError as e:
        print(e.reason)
    data = urlop.read().decode('utf-8')
    insertstring = ""
    insertstring = GetDocumentString(insertstring, data)
    print("content "+str(true_doc_count)+" is:  "+insertstring)
    a = insertstring.split(' ')
    doc_c = 0
    for x in a:
        if x != ' ' and x != '\,' and x != "":
            doc_c += 1
    pos = 0
    while a:
        b = a.pop()
        if b != ' ' and b != '\,' and b != "":
            if RemoveSingleCharacter(str(b)) == 1:
                TermTable = AddTerm(TermTable, b, DocIDModify(true_doc_count), doc_c, pos)
            pos += 1
    doc_e = DocFullData(DocIDModify(true_doc_count), insertstring)
    DocText.append(doc_e)
    e = DocData(DocIDModify(true_doc_count), doc_c, Linkurlset[url_count - 1])
    DocContent.append(e)
    true_doc_count += 1

SaveDocTale(DocContent)
TermTable.sort(key=lambda TermList : TermList.term)
SaveTable(TermTable)
<<<<<<< HEAD
SaveDocAllData(DocText)

=======
>>>>>>> origin/master

