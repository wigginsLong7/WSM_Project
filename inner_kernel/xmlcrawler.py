import re
import urllib.request
import urllib
import socket
from urllib.error import URLError, HTTPError
from collections import deque

timeout = 30
socket.setdefaulttimeout(timeout)

linkre = re.compile('href=\"(.+?)\"')
class crawler:

    def __init__(self, starturl,pnum=1000, type=0):
        self.crawltype = type
        self.xmlqueue = deque()
        self.Visited = set()
        self.linkqueue = deque()
        self.pagenum = pnum
        self.url = starturl
        self.xmlpath = "dblpxml.txt"
        self.linkpath = "dblpxmlsource.txt"

    def ResetURL(self, newurl):
        self.url = newurl

    def ResetCrawlType(self, newtype):
        self.crawltype = newtype

    def ResetCrawlPagenum(self, num):
        self.pagenum = num

    def ModifyXmlPath(self, path):
        self.xmlpath = path

    def ModifyLinkPath(self, path):
        self.linkpath = path

    def Duplicate(self, q, s):  # 不能重复遍历
        if q.count(s) > 0:
            return 0
        return 1

    def PageUp(self, old_ulr,url_count, author_count):
        if old_ulr[0] != self.url:
            old_ulr[0] = self.url
        else:
            url_count[0] += 1
            self.url = "http://dblp.uni-trier.de/pers?pos=" + str(300 * url_count[0] + 1)
            print("add another url " + str(author_count[0]))
        return

    def AddElementToQueue(self,data,author_count,pattern,queue,Qtype, xmlfile= "", xmlsourcefile= "",path=""):
        for x in linkre.findall(data):
            if Qtype and author_count[0] >= self.pagenum:
                break
            if 'http' in x and x not in self.Visited:
                match = re.search(pattern, x)
                if match:  # 访问队列
                    if self.Duplicate(queue, x) == 1:
                        queue.append(x)
                        if Qtype:
                            print('加入队列 --->  ' + x)
                        else:
                            xmlfile.write(bytes(x, 'utf-8'))
                            xmlfile.write(bytes('\r\n', 'utf-8'))
                            xmlsourcefile.write(bytes(path, 'utf-8'))
                            xmlsourcefile.write(bytes('\r\n', 'utf-8'))
                            print("actual xml add " + str(author_count[0]) + "--->" + x)
                        author_count[0] += 1
        return

    def FindLinkSet(self):
        author_count = [0]
        old_ulr = [""]
        url_count = [0]
        while True:
            if author_count[0] >= self.pagenum:
                print("xmlqueue is full of " + str(self.pagenum))
                break
            self.PageUp(old_ulr,url_count,author_count)
            self.Visited |= {self.url}  # 标记为已访问
            data = self.Catchdata(self.url)
            if data == "":
                continue
            perslimit = re.compile(r'http://dblp.uni-trier.de/pers/hd/a/')  # link point to xml path
            self.AddElementToQueue(data, author_count, perslimit, self.linkqueue, True)
        return

    def Catchdata(self,fetchurl):
        try:
            urlop = urllib.request.urlopen(fetchurl)
        except HTTPError as e:
            print(self.url + "is wrong and " + e.reason)
            return ""
        except URLError as e:
            print(self.url + "is wrong and " + e.reason)
            return ""
        except TimeoutError as e:
            print(e.reason)
            return ""

        if 'html' not in urlop.getheader('Content-Type'):
            return ""
        try:
            data = urlop.read().decode('utf-8')
        except:
            return ""
        return data

    def FindXmlSet(self):
        xml_count = [0]
        xmlfile = open(self.xmlpath, 'wb+')  # 存储xml path txt文件
        xmlsourcefile = open(self.linkpath, 'wb+')  # 存储link point to xml path txt文件
        while self.linkqueue:
            path = self.linkqueue.popleft()
            self.Visited |= {path}
            #print('   正在抓取 <---  ' + path)
            data = self.Catchdata(path)
            if data == "":
                continue
            xxlimtit = re.compile(r'http://dblp.uni-trier.de/pers/xx')  # xml path
            self.AddElementToQueue(data, xml_count, xxlimtit, self.linkqueue, False, xmlfile, xmlsourcefile, path)
        xmlfile.close()
        xmlsourcefile.close()

    def StartCrawl(self):
        self.FindLinkSet()
        self.FindXmlSet()
