from Term import *
import re

latin = (
'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö'
, 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î'
, 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ')

list = ('&#192', '&#193', '&#194', '&#195', '&#196', '&#197', '&#198', '&#199', '&#200', '&#201', '&#202', '&#203',
        '&#204', '&#205', '&#206', '&#207', '&#208', '&#209', '&#210', '&#211', '&#212', '&#213', '&#214',
        '&#216', '&#217', '&#218', '&#219', '&#220', '&#221', '&#222', '&#223', '&#224', '&#225', '&#226', '&#227',
        '&#228', '&#229', '&#230', '&#231', '&#232', '&#233', '&#234', '&#235', '&#236', '&#237', '&#238', '&#239',
        '&#240', '&#241', '&#242', '&#243', '&#244', '&#245', '&#246', '&#248', '&#249', '&#250', '&#251',
        '&#252', '&#253', '&#254', '&#255')

proc = re.compile('<r>(.+)<\r>', re.M)
authorc = re.compile('<author>(.+)</author>')
titlec = re.compile('<title>(.+)</title>')
yearc = re.compile('<year>(.+)</year>')
volumec = re.compile('<volume>(.+)</volume>')
journalc = re.compile('<journal>(.+)</journal>')
pagec = re.compile('<pages>(.+)</pages>')
booktitlec = re.compile('<booktitle>(.+)</booktitle>')

def contentmodify(content, d_data, value):
    d_str = " "
    if value == 0:
        while d_data:
            a = d_data.pop()
            content = content + a + " "
    else:
        while d_data:
            a = d_data.pop()
            d_str = d_str + a + " "
        for i in range(0, 62):
            d_str = d_str.replace(list[i], latin[i])
        content = content + d_str + " "
    return content

def AddTerm(list, addterm, docID, doc_c, term_position):
    a = 0
    for i in range(len(list)):
        if list[i].term == addterm:  # an old term
            a = 1
            samedoc = 0
            for x in list[i].postinglist:
                if x.doc_ID == docID:  # in the same doc
                    x.positionlist.append(term_position)
                    samedoc = 1
                    break
            if samedoc == 0:  # new doc
                element = DocDetail(docID, term_position)
                list[i].postinglist.append(element)
                list[i].idf_value += 1
            break
    if a == 0:   #new term
        newdoc = TermList(addterm, docID, term_position)
        list.append(newdoc)
    return list

def SaveDocTale(list):
    DocList = open("DocData2.txt", 'w')  # 存储 postinglist Doc 文件
    for i in range(len(list)):
        try:
            DocList.write(str(list[i].doc_ID) + "\t" + str(list[i].term_count) + "\t" + list[i].url + "\n")
        except :
            print("wrong")
    DocList.close()
    return

def SaveTable(list):
    termPostList = open("TermPostingList2.txt", 'wb')  # 存储 postinglist Doc 文件
    for i in list:
        post_str = ""
        post_str = i.getpoststring(post_str)
        try:
            termPostList.write(i.term.encode('utf-8')+"\t".encode('utf-8') + post_str.encode('utf-8') + "\r\n".encode('utf-8'))
        except:
            print("something wrong in" + i.term)
    termPostList.close()
    return

def SaveDocAllData(listdoc):
    docdata = open("DocContent2.txt", 'wb')
    for i in listdoc:
        try:
            docdata.write(i.doc_ID.encode('utf-8')+"\t".encode('utf-8')+i.doctext.encode('utf-8')+'\r\n'.encode('utf-8'))
        except:
            print("wrong")
    docdata.close()
    return

def DocIDModify(doc_id):
    prefix = "Mdoc_"
    doc_id = prefix + str(doc_id)
    return str(doc_id)

def RemoveSingleCharacter(a):
    if len(a) == 1:
        if a.isdigit():
            return 1
        else:
            return 0
    else:
        return 1
def GetDocumentString(insertstring, data):
    authordata = authorc.findall(data)
    titledata = titlec.findall(data)
    yeardata = yearc.findall(data)
    volumndata = volumec.findall(data)
    journaldata = journalc.findall(data)
    pagedata = pagec.findall(data)
    booktitledata = booktitlec.findall(data)
    insertstring = contentmodify(insertstring, authordata, 1)
    insertstring = contentmodify(insertstring, titledata, 1)
    insertstring = contentmodify(insertstring, booktitledata, 1)
    insertstring = contentmodify(insertstring, pagedata, 0)
    insertstring = contentmodify(insertstring, volumndata, 0)
    insertstring = contentmodify(insertstring, journaldata, 0)
    insertstring = contentmodify(insertstring, yeardata, 0)
    insertstring = insertstring.replace('&#38', '&').replace('\\', ' ').replace('-', ' ').replace('<i>', '').replace('</i>', '').replace('<sup>', '').replace('</sup>', '')
    insertstring = insertstring.replace(',', '').replace('(', '').replace(')', '').replace('$', '').replace('.', '').replace('\'', '').replace(';', '').replace('&#34', '')
    return insertstring