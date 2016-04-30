
from inner_kernel.TypeEnum import WSMEnum
from inner_kernel.Tokenizer import *
from inner_kernel.RedisInnerLink import *

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

proc = re.compile('<r>(\n|(.+\n))((.+)\n)+</r>', re.M)
authorc = re.compile('<author>(.+)</author>')
titlec = re.compile('<title>(.+)</title>')
yearc = re.compile('<year>(.+)</year>')
volumec = re.compile('<volume>(.+)</volume>')
journalc = re.compile('<journal>(.+)</journal>')
pagec = re.compile('<pages>(.+)</pages>')
booktitlec = re.compile('<booktitle>(.+)</booktitle>')

def TermModify(a, value):
    '''
       called by function ContentModify(), if the value is digit ,add the prefix 'D_' to
       distinct the difference of term and the doc_ID
    '''
    if a.isdigit():
        return "D_" + str(a)
    else:
        return a
    '''
    ma = [""]
    if value == WSMEnum.AUTHOR:
        ma[0] = 'A_' + str(a)
    elif value == WSMEnum.TITLE:
        ma[0] = 'T_' + str(a)
    elif value == WSMEnum.BOOKTITLE:
        ma[0] = 'BT_' + str(a)
    elif value == WSMEnum.YEAR:
        ma[0] = 'Y_' + str(a)
    elif value == WSMEnum.PAGE:
        ma[0] = 'P_' + str(a)
    elif value == WSMEnum.VOLUMN:
        ma[0] = 'V_' + str(a)
    elif value == WSMEnum.JOURNAL:
        ma[0] = 'J_' + str(a)
    return ma[0]
'''
def ContentModify(content, TermTable, doccount, d_data, value, pos):
    '''
       call by function SingleDocString(),  seperate the term in the the data segment and add it in the TermTable list
    '''
    term_name = [""]
    while d_data:
        a = d_data.pop()
        a = a.replace('/', ' / ')
        sub_a = a.split(' ')
        for i in sub_a:
            if i != ' ' and i != '':
                content = content + i + " "
                t = Tokenizer()
                t.set_num_del(False)
                b = t.tokenize(i)
                if b != "":
                    term_name[0] = TermModify(b, value)
                    AddTerm(TermTable, term_name[0], str(doccount), pos[0])
                pos[0] += 1
    return content

def AddTerm(list, addterm, docID, term_position):
    '''
       call by function SingleDocString ContentModify(),
    '''
    for i in list:
        if i.SearchTerm(addterm, docID, term_position) == 1:
            return list
    newdoc = TermList(addterm)
    newdoc.AddElementToPostingList(docID, term_position)
    list.append(newdoc)
    return True

def SaveDocTable(doclist):
    DocumentList = open("DocData.txt", 'wb')  # 存储 postinglist Doc 文件
    for i in range(len(doclist)):
        try:
            DocumentList.write(
                str(doclist[i].doc_ID).encode('utf-8') + "\t".encode('utf-8') + str(doclist[i].term_count).encode(
                    'utf-8') + "\t".encode('utf-8') + doclist[i].url.encode('utf-8') + "\t".encode('utf-8') + doclist[
                    i].content.encode('utf-8') + "\n".encode('utf-8'))
        except:
            print("wrong in save documentdata in txt")

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

def InsertDBdata(total_word,doc_count,ava_doclength,l):
    name = "0"
    value = str(total_word) + "," + str(doc_count) +","+str(ava_doclength)
    if not l.RedisInsert(name, value):
        return False
    return True

def SingleDocString(substring, TermTable, doccount, data, pos):
    authordata = authorc.findall(data)
    titledata = titlec.findall(data)
    yeardata = yearc.findall(data)
    volumndata = volumec.findall(data)
    journaldata = journalc.findall(data)
    pagedata = pagec.findall(data)
    booktitledata = booktitlec.findall(data)

    substring = ContentModify(substring, TermTable, doccount, authordata, WSMEnum.AUTHOR, pos)
    substring = ContentModify(substring, TermTable, doccount, titledata, WSMEnum.TITLE, pos)
    substring = ContentModify(substring, TermTable, doccount,  booktitledata, WSMEnum.BOOKTITLE, pos)
    substring = ContentModify(substring, TermTable, doccount, pagedata, WSMEnum.PAGE, pos)
    substring = ContentModify(substring, TermTable, doccount, volumndata, WSMEnum.VOLUMN, pos)
    substring = ContentModify(substring, TermTable, doccount, journaldata, WSMEnum.JOURNAL, pos)
    substring = ContentModify(substring, TermTable, doccount, yeardata, WSMEnum.YEAR, pos)
    return substring

def GetDocString(datastr, TermTable, doccount, data, pos):
    data_sub = data.split('\n')
    record = False
    datastring = [""]
    for i in data_sub:
        if len(i) >= 3:
            a = i[0:3]
            if a == '<r>':
                record = True
        if len(i) >= 4:
            b = i[0:4]
            if b == '</r>':
                record = False
                datastr = SingleDocString(datastr, TermTable, doccount, StringReplaceModify(datastring[0]), pos)
                datastring[0] = ""
        if record:
            datastring[0] += (i + '\n')
    '''
    s = linker.CheckMergeInRedis(TermTable)
    if s == WSMEnum.TERM_INSERT_SUCCESS:
        print("len is " + str(len(TermTable)))
        flag = 1
    elif s == WSMEnum.TERM_INSERT_FAIL:
        return ""
    '''
    length = len(datastr)
    return datastr[:length-1]

def StringReplaceModify(datastring):
    """ replace Latin 1 character  and deal with the specific character"""
    for i in range(0, 62):
        datastring = datastring.replace(list[i], latin[i])
    datastring = datastring.replace('<i>', '').replace('</i>', '').replace('<sup>', '').replace('</sup>', '').replace('(', ' ( ').replace(')', ' ) ')
    datastring = datastring.replace(',', ' , ').replace('$', ' $ ').replace('.', ' . ').replace('\'', ' \' ').replace(';', '; ').replace('\\', ' \\  ').replace('-', ' -  ').replace(':', ' : ')
    return datastring




