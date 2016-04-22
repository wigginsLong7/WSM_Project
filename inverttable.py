import socket
import urllib.request
import re
import math
from urllib.error import URLError, HTTPError
timeout = 30
socket.setdefaulttimeout(timeout)

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
           list[i].idf_value= math.log(doc_count/a)
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

Linkurlset = []
linkfile = open('dblpxmlsource1000.txt', 'r')
linklines = linkfile.readlines()
for line in linklines:
    Linkurlset.append(line)

# ------------------------read the xml file----------------------------
inputfile = open('test.txt', 'r')
lines = inputfile.readlines()
# --------------------------ISO-8859-1 code change--------------------------- Latin chacracter is hard to change to unicode?
latin=('À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö'
       , 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î'
       , 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ')
list=('&#192', '&#193', '&#194', '&#195', '&#196', '&#197', '&#198', '&#199', '&#200', '&#201', '&#202', '&#203',
      '&#204', '&#205',	'&#206', '&#207', '&#208', '&#209',	'&#210', '&#211', '&#212', '&#213', '&#214',
      '&#216', '&#217', '&#218', '&#219', '&#220', '&#221', '&#222', '&#223', '&#224', '&#225', '&#226', '&#227',
      '&#228', '&#229', '&#230', '&#231', '&#232', '&#233',	'&#234', '&#235', '&#236', '&#237',	'&#238', '&#239',
      '&#240', '&#241',	'&#242', '&#243', '&#244', '&#245', '&#246', '&#248', '&#249', '&#250', '&#251',
      '&#252', '&#253', '&#254', '&#255')


 #--------------------the regular expression--------------------------
proc = re.compile('<r>(.+)<\r>', re.M)
authorc = re.compile('<author>(.+)</author>')
titlec = re.compile('<title>(.+)</title>')
yearc = re.compile('<year>(.+)</year>')
volumec = re.compile('<volume>(.+)</volume>')
journalc = re.compile('<journal>(.+)</journal>')
urlc = re.compile('<ee>(.+)</ee>')
pagec = re.compile('<pages>(.+)</pages>')
booktitlec = re.compile('<booktitle>(.+)</booktitle>')
crossrefc = re.compile('<crossref>(.+)</crossref>')
Doccount = 1
TermTable = []
DocContent = []
url_count = 0
true_doc_count = 0
for line in lines:
    url_count += 1
    # read xml path
    url= line
    try:
      urlop = urllib.request.urlopen(url)
    except HTTPError as e:
      print(e.reason)
      continue
    except URLError as e:
        print(e.reason)
    data = urlop.read().decode('utf-8')

    # ---------------get detail data from the html-----------------------
    authordata = authorc.findall(data)
    titledata = titlec.findall(data)
    yeardata = yearc.findall(data)
    volumndata = volumec.findall(data)
    journaldata = journalc.findall(data)
    urldata = urlc.findall(data)
    pagedata = pagec.findall(data)
    booktitledata = booktitlec.findall(data)
    crossrefdata = crossrefc.findall(data)
    insertstring=[""]

    #-----------------imply the insert sql string-------------------
    insertstring[0]= contentmodify(insertstring, authordata, 1)
    insertstring[0] = contentmodify(insertstring, titledata, 1)
    insertstring[0] = contentmodify(insertstring, booktitledata, 1)
    insertstring[0]= contentmodify(insertstring, pagedata, 0)
    insertstring[0] = contentmodify(insertstring, volumndata, 0)
    insertstring[0] = contentmodify(insertstring, journaldata, 0)
    insertstring[0] = contentmodify(insertstring, yeardata, 0)
    #insertstring[0] = contentmodify(insertstring, crossrefdata, 0)

    insertstring[0] = insertstring[0].replace('.', '')
    insertstring[0] = insertstring[0].replace('&#34', '\" ')
    insertstring[0] = insertstring[0].replace('-', ' ')
    insertstring[0] = insertstring[0].replace('$', '')
    #print("content "+str(Doccount)+" is:  "+insertstring[0])
    a = insertstring[0].split(' ')
    doc_c = 0
    for x in a:
        if x != ' ' and x != '\,' and x != "":
            doc_c += 1
    #print("the length of doc_c"+str(Doccount)+" is: "+str(doc_c)+" and its url is "+str(url_count))
    true_doc_count += 1
    e = DocData(true_doc_count, doc_c, Linkurlset[url_count-1])
    DocContent.append(e)
    while a:
        b = a.pop()
        if b != ' ' and b != '\,' and b != "":
           TermTable = AddTerm(TermTable, b, Doccount, doc_c)
    Doccount += 1

SaveDocTale(DocContent)
CalculateDFvalue(TermTable, Doccount)
TermTable.sort(key=lambda TermList:TermList.term)
SaveTable(TermTable)



