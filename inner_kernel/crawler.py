import re
import urllib.request
import urllib
import socket
from urllib.error import URLError, HTTPError
from collections import deque
timeout = 30
socket.setdefaulttimeout(timeout)

queue = deque()  # the search queue
xmlqueue = deque() # target xml
xmlsourcequeue=deque() # the link point to target xml
visited = set()

pagenum = 10
url = 'http://dblp.uni-trier.de/pers?pos=1'  # A开头的作者pages
queue.append(url)
url_count = 0
author_count = 0
linkre = re.compile('href=\"(.+?)\"')
def duplicate(q, s): # 不能重复遍历
    if q.count(s) > 0:
        return 0
    return 1
xmlfile = open("dblpxml1000.txt", 'wb+')  # 存储xml path txt文件
xmlsourcefile = open("dblpxmlsource1000.txt", 'wb+')  # 存储link point to xml path txt文件
old_ulr = [""]
while queue:
    if author_count >= pagenum:
        print("xmlqueue is full of " + str(pagenum))
        break

    url0 = queue[url_count]  # 队首元素出队
    if old_ulr[0] != url0:
         old_ulr[0] = url0
    else:
        url_count += 1
        queue.append("http://dblp.uni-trier.de/pers?pos="+str(300*url_count+1))
        print("add another url " + str(author_count))
        continue
    visited |= {url0}  # 标记为已访问
    #print('抓取: ' + str(url_count) + '   正在抓取 <---  ' + url0)
    #print(author_count)
    try:
        urlop0 = urllib.request.urlopen(url0)
    except HTTPError as e:
        print(url0 + "is wrong and " + e.reason)
        continue
    except URLError as e:
        print(url0 + "is wrong and " + e.reason)
    if 'html' not in urlop0.getheader('Content-Type'):  # 避免抓到 .jpg 等资源图片文件
        continue
    # 避免程序异常中止, 用try..catch处理异常
    try:
        data0 = urlop0.read().decode('utf-8')
    except:
        continue
    perslimit = re.compile(r'http://dblp.uni-trier.de/pers/hd/a/')  # link point to xml path
    for x in linkre.findall(data0):
        if author_count >= pagenum:
            #print("xmlqueue is full of "+str(pagenum))
            break
        if 'http' in x and x not in visited:
            match = re.search(perslimit, x)
            if match:  # 访问队列
                if duplicate(xmlsourcequeue, x) == 1:
                    xmlsourcequeue.append(x)
                    print('加入队列 --->  ' + x)
                    author_count += 1

xml_count = 0
while xmlsourcequeue:
    path = xmlsourcequeue.popleft()
    visited |= {path}
    print('   正在抓取 <---  ' + path)
    try:
        urlop = urllib.request.urlopen(path)
    except HTTPError as e:
        print(path+"is wrong and "+e.reason)
        continue
    except URLError as e:
        print(path+"is wrong and "+e.reason)
    if 'html' not in urlop.getheader('Content-Type'):  # 避免抓到 .jpg 等资源图片文件
        continue
    # 避免程序异常中止, 用try..catch处理异常
    try:
        data = urlop.read().decode('utf-8')
    except:
        continue
    xxlimtit = re.compile(r'http://dblp.uni-trier.de/pers/xx')  # xml path
    for xml in linkre.findall(data):
        if 'http' in xml and xml not in visited:
            match2 = re.search(xxlimtit, xml)
            if match2:  # 输出文件
                if duplicate(xmlqueue, xml) == 1:
                    xmlqueue.append(xml)
                    xmlfile.write(bytes(xml, 'utf-8'))
                    xmlfile.write(bytes('\r\n', 'utf-8'))
                    xmlsourcefile.write(bytes(path, 'utf-8'))
                    xmlsourcefile.write(bytes('\r\n', 'utf-8'))
                    print("actual xml add " + str(xml_count) + "--->" + xml)
                    #print("the xml is under this ulr:" + path)
                    xml_count += 1
xmlfile.close()
xmlsourcefile.close()
