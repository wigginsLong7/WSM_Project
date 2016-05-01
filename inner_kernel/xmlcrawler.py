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
        self.xmlpath = "dblpxmlconf.txt"
        self.linkpath = "dblpxmlsourceconf.txt"

    def CheckCrawlType(self):
        if self.url.find('http://dblp.uni-trier.de/pers?') != -1 and self.crawltype != 0:
            print("Error, start url is the author page type, please check the inpurt crawl type")
            return False
        elif self.url.find('http://dblp.uni-trier.de/db/journals/') != -1 and self.crawltype != 1:
            print("Error, start url is the journal page type,please check the inpurt crawl type")
            return False
        elif self.url.find('http://dblp.uni-trier.de/db/conf/') != -1 and self.crawltype != 2:
            print("Error, start url is the conference page type,please check the inpurt crawl type")
            return False
        if self.crawltype < 0 or self.crawltype > 2:
            return False
        return True


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
            if self.crawltype == 0:
                self.url = "http://dblp.uni-trier.de/pers?pos=" + str(300 * url_count[0] + 1)
            elif self.crawltype == 1:
                self.url = "http://dblp.uni-trier.de/db/journals/?pos=" + str(100 * url_count[0] + 1)
            elif self.crawltype == 2:
                self.url = "http://dblp.uni-trier.de/db/conf/?pos=" + str(100 * url_count[0] + 1)
            print("add another url " + str(author_count[0]))
        return

    def AddElementToQueue(self,data,author_count,pattern,queue,Qtype,xmlfile= ""):
        flag = [0]
        for x in linkre.findall(data):
            if Qtype == 1 and author_count[0] >= self.pagenum:
                break
            if 'http' in x and x not in self.Visited:
                match = re.search(pattern, x)
                if match:  # 访问队列
                    dup = False
                    if self.Duplicate(queue, x) == 1:
                        dup = True
                    if Qtype == 1 or Qtype == 2:
                        if dup:
                            queue.append(x)
                            print('加入队列 --->  ' + x)
                            author_count[0] += 1
                    elif Qtype == 0:
                        if (self.crawltype == 0 and dup) or (self.crawltype == 1 or self.crawltype == 2):
                            queue.append(x)
                            xmlfile.write(bytes(x+",", 'utf-8'))
                            flag[0] = 1
                            print("actual xml add " + str(author_count[0]) + "--->" + x)
                            author_count[0] += 1
                    else:
                        print("input type Error")
                        return False
        if Qtype == 0 and flag[0] == 0:
            return False
        else:
            return True

    def FindLinkSet(self,linkpattern):
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
            self.AddElementToQueue(data, author_count, linkpattern, self.linkqueue, 1)
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

    def FindXmlSet(self,xmlpattern):
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
            if self.AddElementToQueue(data, xml_count, xmlpattern, self.linkqueue, 0, xmlfile):
                xmlfile.write(bytes('\r\n', 'utf-8'))
                xmlsourcefile.write(bytes(path, 'utf-8'))
                xmlsourcefile.write(bytes('\r\n', 'utf-8'))
        xmlfile.close()
        xmlsourcefile.close()

    def MediumnJumpForLinkQueue(self):
        count = [len(self.linkqueue)]
        link_num = [0]
        while self.linkqueue:
            if count[0] <= 0:
                break
            path = self.linkqueue.popleft()
            self.Visited |= {path}
            data = self.Catchdata(path)
            if data == "":
                continue
            pattern_j = re.compile(path)
            self.AddElementToQueue(data, link_num, pattern_j, self.linkqueue, 2)
            count[0] += -1
        return

    def StartCrawl(self):

        authorlink = re.compile(r'http://dblp.uni-trier.de/pers/hd/a/')  # link point to xml path
        authorxml = re.compile(r'http://dblp.uni-trier.de/pers/xx')  # xml path
        journallink =re.compile(r'http://dblp.uni-trier.de/db/journals/')
        journalxml= re.compile(r'http://dblp.uni-trier.de/rec/xml/journals/')
        conferencelink= re.compile(r'http://dblp.uni-trier.de/db/conf/')
        conferencexml=re.compile(r'http://dblp.uni-trier.de/rec/xml/conf/')
        linkpatternlist= []
        xmlpatternlist = []
        linkpatternlist.append(authorlink)
        linkpatternlist.append(journallink)
        linkpatternlist.append(conferencelink)
        xmlpatternlist.append(authorxml)
        xmlpatternlist.append(journalxml)
        xmlpatternlist.append(conferencexml)

        if not self.CheckCrawlType():
            return False
        self.FindLinkSet(linkpatternlist[self.crawltype])
        if self.crawltype == 1:
            self.MediumnJumpForLinkQueue()
        self.FindXmlSet(xmlpatternlist[self.crawltype])
        return True
