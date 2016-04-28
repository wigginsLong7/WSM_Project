import urllib
import urllib.request
from inner_kernel.invert_index_fun import *
from urllib.error import URLError, HTTPError

import sys
import psutil


Linkurlset = []
linkfile = open('dblpxmlsource.txt', 'r')
linklines = linkfile.readlines()
for line in linklines:
    Linkurlset.append(line)

inputfile = open('test.txt', 'r')
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
    data = urlop.read().decode('utf-8')
    insertstring = ""
    pos = [0]
    replace_str = [""]
    #insertstring = GetDocumentString(insertstring, data)
    insertstring = GetDocString(insertstring, TermTable, true_doc_count, data, pos)
    print(pos[0])
    print("content "+str(true_doc_count)+" is:  "+insertstring)
    '''
    a = insertstring.split(' ')
    tokenizer = Tokenizer()
    tokenizer.set_num_del(False)
    for b in a:
        if b != ' ' and b != '\,' and b != "":
            replace_str[0] = tokenizer.tokenize(b)
            if replace_str[0] != "":
                AddTerm(TermTable, replace_str[0], DocIDModify(true_doc_count), pos)
            pos += 1
    '''
    e = DocData(true_doc_count)
    e.SetDocCount(pos[0])
    e.SetUrl(Linkurlset[url_count - 1])
    e.SetDocContent(insertstring)
    DocContent.append(e)
    true_doc_count += 1
    total_word += pos[0]

print(total_word)
print(psutil.cpu_percent())
print(int(psutil.virtual_memory().total / (1027 * 1024)))
print(psutil.virtual_memory().percent)
SaveDocTale(DocContent)
TermTable.sort(key=lambda TermList : TermList.term)
SaveTable(TermTable)
print(sys.getsizeof(TermTable))


try:
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    r.flushall()
except redis.ConnectionError as e:
    print(e)
    exit(1)
InsertDBdata(total_word, true_doc_count-1, int(total_word/(true_doc_count-1)))
InsertDataToRedis(TermTable)
InsertDocDetailToRedis(DocContent)





