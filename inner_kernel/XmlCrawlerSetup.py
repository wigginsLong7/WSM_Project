from inner_kernel.xmlcrawler import *

url ='http://dblp.uni-trier.de/pers?pos=1'
a = crawler(url, 300)
a.StartCrawl()