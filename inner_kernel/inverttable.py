import urllib
import urllib.request
from inner_kernel.invert_index_fun import *
from urllib.error import URLError, HTTPError
import socket

timeout = 30
socket.setdefaulttimeout(timeout)

linker = RedisLinker()
linker.RefreshDB()
Linkurlset = []
linkfile = open('dblpxmlsource.txt', 'r')
linklines = linkfile.readlines()
for line in linklines:
    Linkurlset.append(line)

inputfile = open('dblpxml.txt', 'r')
lines = inputfile.readlines()
TermTable = []
DocContent = []
url_count = 0
true_doc_count = 1
total_word = 0
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
        continue
    except TimeoutError as e:
        print(e)
        continue
    data = urlop.read().decode('utf-8')
    insertstring = ""
    pos = [0]
    replace_str = [""]

    insertstring = GetDocString(insertstring, TermTable, true_doc_count, data, pos)
    print(pos[0])
    print("content "+str(true_doc_count)+" is:  "+insertstring)
    e = DocData(true_doc_count)
    e.SetDocCount(pos[0])
    e.SetUrl(Linkurlset[url_count - 1])
    e.SetDocContent(insertstring)
    DocContent.append(e)
    true_doc_count += 1
    total_word += pos[0]

print(total_word)
SaveDocTable(DocContent)
TermTable.sort(key=lambda TermList : TermList.term)
SaveTable(TermTable)

InsertDBdata(total_word, true_doc_count-1, int(total_word/(true_doc_count-1)), linker)
linker.InsertDataToRedis(TermTable)
linker.InsertDataToRedis(DocContent)
linker.SaveData()





