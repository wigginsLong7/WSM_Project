import socket
import urllib.request
from invert_index_fun import *
from urllib.error import URLError, HTTPError

timeout = 30
socket.setdefaulttimeout(timeout)

Linkurlset = []
linkfile = open('dblpxmlsource.txt', 'r')
linklines = linkfile.readlines()
for line in linklines:
    Linkurlset.append(line)

# ------------------------read the xml file----------------------------
inputfile = open('dblpxml.txt', 'r')
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
SaveDocAllData(DocText)


