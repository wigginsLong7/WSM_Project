
from inner_kernel.Tokenizer import *
from inner_kernel.RedisInnerLink import *
latin = (
'À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö'
, 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î'
, 'ï', 'ð', 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ')

list = ('&#192;', '&#193;', '&#194;', '&#195;', '&#196;', '&#197;', '&#198;', '&#199;', '&#200;', '&#201;', '&#202;', '&#203;',
        '&#204;', '&#205;', '&#206;', '&#207;', '&#208;', '&#209;', '&#210;', '&#211;', '&#212;', '&#213;', '&#214;',
        '&#216;', '&#217;', '&#218;', '&#219;', '&#220;', '&#221;', '&#222;', '&#223;', '&#224;', '&#225;', '&#226;', '&#227;',
        '&#228;', '&#229;', '&#230;', '&#231;', '&#232;', '&#233;', '&#234;', '&#235;', '&#236;', '&#237;', '&#238;', '&#239;',
        '&#240;', '&#241;', '&#242;', '&#243;', '&#244;', '&#245;', '&#246;', '&#248;', '&#249;', '&#250;', '&#251;',
        '&#252;', '&#253;', '&#254;', '&#255;')

class DocHandler:
    def __init__(self):
        self.patternlist = []
        self.PatternListInital()

    def PatternListInital(self):
        '''
           initial all the regular pattern
        '''
        authorc = re.compile('<author>(.+)</author>')
        titlec = re.compile('<title>(.+)</title>')
        yearc = re.compile('<year>(.+)</year>')
        volumec = re.compile('<volume>(.+)</volume>')
        journalc = re.compile('<journal>(.+)</journal>')
        pagec = re.compile('<pages>(.+)</pages>')
        booktitlec = re.compile('<booktitle>(.+)</booktitle>')
        numberc =re.compile('<number>(.+)</number>')
        editorc = re.compile('<editor>(.+)</editor>')
        isbnc = re.compile('<isbn>(.+)</isbn>')
        publisherc =re.compile('<publisher>(.+)</publisher>')
        seriesc=re.compile('[^<series(.+)>](.+)</series>')

        self.patternlist.append(authorc)
        self.patternlist.append(editorc)
        self.patternlist.append(titlec)
        self.patternlist.append(booktitlec)
        self.patternlist.append(publisherc)
        self.patternlist.append(pagec)
        self.patternlist.append(yearc)
        self.patternlist.append(volumec)
        self.patternlist.append(journalc)
        self.patternlist.append(numberc)
        self.patternlist.append(isbnc)
        self.patternlist.append(seriesc)

    def TermModify(self, a):
        '''
           called by function ContentModify(), if the value is digit ,add the prefix 'D_' to
           distinct the difference of term and the doc_ID
        '''
        if a.isdigit():
            return "D_" + str(a)
        else:
            return a

    def ContentModify(self, content, TermTable, doccount, d_data, pos):
        '''
           call by function SingleDocString(),  seperate the term in the the data segment and add it in the TermTable list
        '''
        term_name = [""]
        while d_data:
            a = d_data.pop()
            a = a.replace('/', ' / ')
            sub_a = a.split(' ')
            for i in sub_a:
                if i != ' ' and i != '':
                    content = content + i + " "
                    t = Tokenizer()
                    t.set_num_del(False)
                    b = t.tokenize(i)
                    if b != "":
                        term_name[0] = self.TermModify(b)
                        self.AddTerm(TermTable, term_name[0], str(doccount), pos[0])
                    pos[0] += 1
        return content

    def AddTerm(self, list, addterm, docID, term_position):
        '''
           call by function SingleDocString ContentModify(),
        '''
        for i in list:
            if i.SearchTerm(addterm, docID, term_position) == 1:
                return list
        newdoc = TermList(addterm)
        newdoc.AddElementToPostingList(docID, term_position)
        list.append(newdoc)
        return True

    def SingleDocString(self, substring, TermTable, doccount, data, pos):
        subdata = []
        for i in self.patternlist:
            s = i.findall(data)
            if i == re.compile('[^<series(.+)>](.+)</series>') and s != []:
                st = s[0].find('>')
                t = [s[0][st+1:]]
                subdata.append(t)
            else:
                subdata.append(s)
        for x in subdata:
            substring = self.ContentModify(substring, TermTable, doccount, x, pos)
        return substring

    def GetDocString(self, datastr, TermTable, doccount, data, pos):
        '''
           main function  entrance
        '''
        datastring = [""]
        record = False
        data_sub = data.split('\n')
        ''' seperate the single document'''
        for i in data_sub:
            if len(i) >= 3:
                a = i[0:3]
                if a == '<r>':
                    record = True
            if len(i) >= 4:
                b = i[0:4]
                if b == '</r>':
                    record = False
                    datastr = self.SingleDocString(datastr, TermTable, doccount, self.StringReplaceModify(datastring[0]),pos)
                    datastring[0] = ""
            if record:
                datastring[0] += (i + '\n')
        length = len(datastr)
        if length == 0:
            return ""
        return datastr[:length - 1]

    def StringReplaceModify(self, datastring):
        """ replace Latin 1 character  and deal with the specific character"""
        for i in range(0, 62):
            datastring = datastring.replace(list[i], latin[i])
        datastring = datastring.replace('<i>', '').replace('</i>', '').replace('<sup>', '').replace('</sup>', '').replace('(', ' ( ').replace(')', ' ) ')
        datastring = datastring.replace(',', ' , ').replace('$', ' $ ').replace('.', ' . ').replace('\'', ' \' ').replace(';', '; ').replace('\\', ' \\  ').replace('-', ' -  ').replace(':', ' : ')
        return datastring

    def FindDocTitle(self, data):
        '''
           get the title of the document
        '''
        if data == "":
            return ""
        titlepattern = re.compile('<h1>(.+)</h1>')
        a = titlepattern.findall(data)[0]
        end = a.find('</span>')
        if end != -1:
            st = a.find('>')
            return a[st+1:end-1]
        return a
    '''
        if data == "":
            return ""
        st = data.find('<author>')
        end = data.find('</author>')
        if st == -1 or end == -1 or end-st <= 9:
            return ""
        titlestring = data[st + 8:end - 1]
        for i in range(0, 62):
            titlestring = titlestring.replace(list[i], latin[i])
        return titlestring +" Personal Homepage"
        '''


    def GetSingleDocString(self, datastr, TermTable, doccount, data, pos):
        datastr = self.SingleDocString(datastr, TermTable, doccount, self.StringReplaceModify(data), pos)
        return datastr