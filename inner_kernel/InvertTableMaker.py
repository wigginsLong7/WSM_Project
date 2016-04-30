import urllib
import urllib.request
from urllib.error import URLError, HTTPError
import socket
from inner_kernel.DocHandler import *
timeout = 30
socket.setdefaulttimeout(timeout)

class InvertTableMaker:
    def __init__(self, xpath ,lpath,plistpath,docpath,txtSave=True,DBSave=True):
        self.xmlpath = xpath
        self.linkpath = lpath
        self.documentpath = docpath
        self.postinglistpath = plistpath
        self.TermTable = []
        self.DocContent = []
        self.url_count = 0
        self.true_doc_count = 1
        self.total_word = 0
        self.save_data_to_txt = txtSave
        self.save_data_to_redis = DBSave

    def ResetSaveTxt(self, flag):
        self.save_data_to_txt = flag

    def ResetSaveDB(self, flag):
        self.save_data_to_redis = flag

    def LinkListInital(self):
        '''
           store the link url which the search engine return
        '''
        Linkurlset = []
        try:
            linkfile = open(self.linkpath, 'r')
            linklines = linkfile.readlines()
        except :
            print("the linkpath file doesn't exist")
            return Linkurlset
        for line in linklines:
            Linkurlset.append(line)
        return Linkurlset

    def RefreshRedisDB(self):
        '''
            clear all the data in redis DB
        '''
        linker = RedisLinker()
        if linker.RefreshDB():
            return True
        else:
            return False

    def StartBuild(self):
        '''
           main process of getting the invert_index_table
        '''
        linklist = self.LinkListInital()
        if len(linklist) == 0:
            print("Error, the number of linkpath is 0")
            return False
        inputfile = open(self.xmlpath, 'r')
        lines = inputfile.readlines()
        for line in lines:
            self.url_count += 1
            insertstring = ""
            pos = [0]
            dh = DocHandler()
            insertstring = dh.GetDocString(insertstring, self.TermTable, self.true_doc_count, self.GetUrlData(line), pos)
            if insertstring == "":
                print("the inserting in "+str(self.true_doc_count)+" is null")
                continue
            print(pos[0])
            print("content " + str(self.true_doc_count) + " is:  " + insertstring)
            self.DocumentDataBuild(linklist, insertstring, pos)
        print(self.total_word)
        self.TermTable.sort(key=lambda TermList: TermList.term)
        if self.SaveDataToHardDisk():
            return True
        else:
            return False

    def GetUrlData(self, url):
        '''
           get the data content in the xml url
         '''
        try:
            urlop = urllib.request.urlopen(url)
            data = urlop.read().decode('utf-8')
        except HTTPError as e:
            print(e.reason)
            return ""
        except URLError as e:
            print(e.reason)
            return ""
        except TimeoutError as e:
            print(e)
            return ""
        except:
            return ""
        return data

    def DocumentDataBuild(self, Linkurlset, insertstring, pos):
        '''
            get the data content in the xml url
          '''
        e = DocData(self.true_doc_count)
        e.SetDocCount(pos[0])
        e.SetUrl(Linkurlset[self.url_count - 1])
        e.SetDocContent(insertstring)
        self.DocContent.append(e)
        self.true_doc_count += 1
        self.total_word += pos[0]

    def SaveTable(self):
        '''
            save the postinglist
          '''
        termPostList = open(self.postinglistpath, 'wb')  # 存储 postinglist Doc 文件
        for i in self.TermTable:
            post_str = ""
            post_str = i.GetPostString(post_str)
            try:
                termPostList.write(
                    i.term.encode('utf-8') + "\t".encode('utf-8') + post_str.encode('utf-8') + "\r\n".encode('utf-8'))
            except:
                print("something wrong in" + i.term)
                return False
        termPostList.close()
        return True

    def SaveDocTable(self):
        '''
            save the documentlist
          '''
        DocumentList = open(self.documentpath, 'wb')  # 存储 postinglist Doc 文件
        for i in range(len(self.DocContent)):
            try:
                DocumentList.write(
                    str(self.DocContent[i].doc_ID).encode('utf-8') + "\t".encode('utf-8') + str(self.DocContent[i].term_count).encode(
                        'utf-8') + "\t".encode('utf-8') + self.DocContent[i].url.encode('utf-8') + "\t".encode('utf-8') +
                    self.DocContent[i].content.encode('utf-8') + "\n".encode('utf-8'))
            except:
                print("wrong in save documentdata in txt")
                return False
        DocumentList.close()
        return True

    def SaveDataToHardDisk(self):
        '''
           all the save work job are completed in here
        '''
        linker = RedisLinker()
        if self.save_data_to_txt:
            if self.SaveTable() and self.SaveDocTable():
                if not self.save_data_to_redis:
                    return True
            else:
                return False
        if self.save_data_to_redis:
            self.RefreshRedisDB()
            value = str(self.total_word) + "," + str(self.true_doc_count-1) + "," + str(int(self.total_word/(self.true_doc_count-1)))
            if not linker.RedisInsert("0", value):
                print("Error, insert headerData failed'")
                return False
            if linker.RefreshDB():
                if linker.InsertDataToRedis(self.TermTable) and linker.InsertDataToRedis(self.DocContent):
                    if linker.SaveData():
                        return True
            return False
        return True








