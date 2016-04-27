from Term import *
import re
import socket
import gc

timeout = 30
socket.setdefaulttimeout(timeout)

latin = (
'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö'
, 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î'
, 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ')

list = ('&#192;', '&#193;', '&#194;', '&#195;', '&#196;', '&#197;', '&#198;', '&#199;', '&#200;', '&#201;', '&#202;', '&#203;',
        '&#204;', '&#205;', '&#206;', '&#207;', '&#208;', '&#209;', '&#210;', '&#211;', '&#212;', '&#213;', '&#214;',
        '&#216;', '&#217;', '&#218;', '&#219;', '&#220;', '&#221;', '&#222;', '&#223;', '&#224;', '&#225;', '&#226;', '&#227;',
        '&#228;', '&#229;', '&#230;', '&#231;', '&#232;', '&#233;', '&#234;', '&#235;', '&#236;', '&#237;', '&#238;', '&#239;',
        '&#240;', '&#241;', '&#242;', '&#243;', '&#244;', '&#245;', '&#246;', '&#248;', '&#249;', '&#250;', '&#251;',
        '&#252;', '&#253;', '&#254;', '&#255;')

proc = re.compile('<r>(.+)<\r>', re.M)
authorc = re.compile('<author>(.+)</author>')
titlec = re.compile('<title>(.+)</title>')
yearc = re.compile('<year>(.+)</year>')
volumec = re.compile('<volume>(.+)</volume>')
journalc = re.compile('<journal>(.+)</journal>')
pagec = re.compile('<pages>(.+)</pages>')
booktitlec = re.compile('<booktitle>(.+)</booktitle>')

def ContentModify(content, d_data, value):
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

def AddTerm(list, addterm, docID, term_position):
    a = 0
    for i in range(len(list)):
        if list[i].term == addterm:  # an old term
            a = 1
            samedoc = 0
            for x in list[i].postinglist:
                if x.doc_ID == docID:  # in the same doc
                    x.AddTermPosition(term_position)
                    samedoc = 1
                    break
            if samedoc == 0:  # new doc
                list[i].AddElementToPostingList(docID, term_position)
                list[i].DFValueIncreaseOne()
            break
    if a == 0:   #new term
        newdoc = TermList(addterm)
        newdoc.AddElementToPostingList(docID, term_position)
        list.append(newdoc)
    return list

def SaveDocTale(doclist):
    DocumentList = open("DocData.txt", 'w')  # 存储 postinglist Doc 文件
    for i in range(len(doclist)):
        try:
            DocumentList.write(str(doclist[i].doc_ID) + "\t" + str(doclist[i].term_count) + "\t" + doclist[i].url +"\t"+ doclist[i].content+"\n")
        except :
            print("wrong")
    DocumentList.close()
    return

def SaveTable(list):
    termPostList = open("TermPostingList.txt", 'wb')  # 存储 postinglist Doc 文件
    for i in list:
        post_str = ""
        post_str = i.GetPostString(post_str)
        try:
            termPostList.write(i.term.encode('utf-8')+"\t".encode('utf-8') + post_str.encode('utf-8') + "\r\n".encode('utf-8'))
        except:
            print("something wrong in" + i.term)
    termPostList.close()
    return

def DocIDModify(doc_id):
    prefix = "myDocID_"
    doc_id = prefix + str(doc_id)
    return str(doc_id)

def GetDocumentString(insertstring, data):
    authordata = authorc.findall(data)
    titledata = titlec.findall(data)
    yeardata = yearc.findall(data)
    volumndata = volumec.findall(data)
    journaldata = journalc.findall(data)
    pagedata = pagec.findall(data)
    booktitledata = booktitlec.findall(data)

    insertstring = ContentModify(insertstring, authordata[1:], 1)
    insertstring = ContentModify(insertstring, titledata, 1)
    insertstring = ContentModify(insertstring, booktitledata, 1)
    insertstring = ContentModify(insertstring, pagedata, 0)
    insertstring = ContentModify(insertstring, volumndata, 0)
    insertstring = ContentModify(insertstring, journaldata, 0)
    insertstring = ContentModify(insertstring, yeardata, 0)

    insertstring = insertstring.replace('\\', ' ').replace('-', ' ').replace('<i>', '').replace('</i>', '').replace('<sup>', '').replace('</sup>', '')
    insertstring = insertstring.replace(',', '').replace('(', '').replace(')', '').replace('$', '').replace('.', '').replace('\'', '').replace(';', '; ').replace('/', ' ')
    insertstring = ContentStringModify(insertstring)
    return insertstring

def RedisInsert(key, value):
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
    except redis.ConnectionError:
        print("Error: Failed to connect server")
        return False
    try:
        r.set(key, value)
    except redis.RedisError as e:
        print(e)
        return False
    print("add success")
    return True

def InsertDataToRedis(Tlist):
    for i in Tlist:
        value = i.ValueString()
        if not RedisInsert(i.term, value):
            return False
    del Tlist
    gc.collect()
    return True

def InsertDocDetailToRedis(doclist):
    for i in doclist:
        value = i.GetString()
        if not RedisInsert(i.doc_ID, value):
            return False
    del doclist
    gc.collect()
    return True

def InsertDBdata(total_word,doc_count,ava_doclength):
    name = "myDocID_0"
    value = str(total_word) + "," + str(doc_count) +","+str(ava_doclength)
    if not RedisInsert(name, value):
        return False
    return True

def CheckKeyExist(key):
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
    except redis.ConnectionError:
        print("Error: Failed to connect server")
        return 0
    if r.exists(key):
        return 1
    else:
        return 2

def ContentStringModify(substring):
    content = [""]
    a = substring.split(" ")
    for i in a:
        if i != ' ' and i != "":
            content[0] += (i+" ")
    end = len(content[0])
    return content[0][:end-1]
