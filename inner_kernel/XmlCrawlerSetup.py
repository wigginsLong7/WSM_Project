from inner_kernel.xmlcrawler import *

url ='http://dblp.uni-trier.de/pers?pos=1'
#url = 'http://dblp.uni-trier.de/db/conf/?pos=1'
#url = 'http://dblp.uni-trier.de/db/journals/?pos=1'
a = crawler(url, 5, 0)
if a.StartCrawl():
    print("Crawl Success")
else:
    print("Crawl fail")