from inner_kernel.InvertTableMaker import *

xmlpath = 'dblpxmlconf.txt'
linkpath = 'dblpxmlsourceconf.txt'
docpath = 'DocData.txt'
postinglistpath = 'TermPostingList.txt'
a = InvertTableMaker(xmlpath, linkpath, postinglistpath, docpath)
if a.StartBuild():
    print("Build Sccuess")
else:
    print("Build Failed")