from outer_interface.RedisOperation import *
from inner_kernel.Tokenizer import Tokenizer
from collections import defaultdict
import operator
import math


class BM25:

    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b

    def __calc_TF__(self, tf, l_d, l_avg):
        return tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * l_d / l_avg))

    def __calc_IDF__(self, N, df):
        return math.log((N - df + 0.5) / (df + 0.5))

    def get_score(self, N, df, tf, l_d, l_avg):
        IDF = self.__calc_IDF__(N, df)
        TF = self.__calc_TF__(tf, l_d, l_avg)

        return IDF * TF


class Query:

    def __init__(self, query):
        self.db = RedisHandler()
        self.tokenizer = Tokenizer()
        self.tokens = self.__filter_query__(query)
        self.docIDs = []
        self.positions = defaultdict(list)

    def __filter_query__(self, query):
        words = query.split(' ')
        tokens = []

        for word in words:
            word = self.tokenizer.tokenize(word)
            if word != '':
                tokens.append(word)

        return tokens

    def __get_top_docIDs__(self, K):
        scores = defaultdict(float)
        positions = defaultdict(set)
        col_data = self.db.GetDBHeaderData()

        if not col_data:
            return [], []

        N = col_data[1]                        # total number of docs in the collection
        l_avg = col_data[2]                    # avg length of doc
        bm25 = BM25()

        for token in self.tokens:
            Nt = self.db.GetDFValue(token)                  # doc frequency
            term_obj = self.db.GetTermPostingList(token)
            doc_data = term_obj.GetDocAndTFValueList(0)       # doc Id list

            for (docID, tf) in doc_data:
                doc_len = self.db.GetDocTermCount(docID)
                score = bm25.get_score(N, Nt, tf, doc_len, l_avg)
                scores[docID] += score

                pos = term_obj.GetPositionInDoc(docID)
                positions[docID] = positions[docID].union(set(pos))

        sorted_scores = sorted(scores.items(), key = operator.itemgetter(1), reverse=True)
        docIDs = []

        for docID, score in sorted_scores:
            docIDs.append(docID)

        if K <= len(docIDs):
            docIDs_K = docIDs[0:K]
            positions_K = defaultdict(list)
            for docID in docIDs_K:
                positions_K[docID] = positions[docID]
            return docIDs_K, positions_K
        else:
            return docIDs, positions

    def retrieve_top_docs(self, st, end):
        if len(self.docIDs) == 0:
            self.docIDs, self.positions = self.__get_top_docIDs__(1000)

        if st >= len(self.docIDs):
            return []
        if end > len(self.docIDs):
            end = len(self.docIDs)

        docIDs = self.docIDs[st:end]
        docs = []
        for docID in docIDs:
            url = self.db.GetDocUrl(docID)
            content = self.db.GetDocFullContent(docID)
            title = self.db.GetDocTitle(docID)
            pos = self.positions[docID]
            docs.append({"url": url, "title": title, "content": content, "position": pos})

        return docs

    def get_rel_doc_counts(self):
        return len(self.docIDs)


class FieldSearch:
    def __init__(self, year, title, journal, author):
        self.db = RedisHandler()
        self.tokenizer = Tokenizer()
        self.year = year
        self.title_tokens = self.__filter_query__(title)
        self.journal_tokens = self.__filter_query__(journal)
        self.author_tokens = self.__filter_query__(author)
        self.docIDs = []
        self.positions = defaultdict(list)

    def __filter_query__(self, query):
        words = query.split(' ')
        tokens = []

        for word in words:
            word = self.tokenizer.tokenize(word)
            if word != '':
                tokens.append(word)

        return tokens

    def __get_top_docIDs__(self, K):
        scores = defaultdict(float)
        positions = defaultdict(set)
        col_data = self.db.GetDBHeaderData()

        if not col_data:
            return [], []

        N = col_data[1]                        # total number of docs in the collection
        l_avg = col_data[2]                    # avg length of doc
        bm25 = BM25()

        Nt = self.db.GetDFValue(self.year, WSMEnum.YEAR_FIELD)                  # doc frequency
        term_obj = self.db.GetTermPostingList(self.year, WSMEnum.YEAR_FIELD)
        doc_data = term_obj.GetDocAndTFValueList(0)       # doc Id list

        for (docID, tf) in doc_data:
            doc_len = self.db.GetDocTermCount(docID)
            score = bm25.get_score(N, Nt, tf, doc_len, l_avg)
            scores[docID] += score

            pos = term_obj.GetPositionInDoc(docID)
            positions[docID] = positions[docID].union(set(pos))

        for token in self.title_tokens:
            Nt = self.db.GetDFValue(token, WSMEnum.TITLE_FIELD)                  # doc frequency
            term_obj = self.db.GetTermPostingList(token, WSMEnum.TITLE_FIELD)
            doc_data = term_obj.GetDocAndTFValueList(0)       # doc Id list

            for (docID, tf) in doc_data:
                doc_len = self.db.GetDocTermCount(docID)
                score = bm25.get_score(N, Nt, tf, doc_len, l_avg)
                scores[docID] += score

                pos = term_obj.GetPositionInDoc(docID)
                positions[docID] = positions[docID].union(set(pos))

        for token in self.journal_tokens:
            Nt = self.db.GetDFValue(token, WSMEnum.JOURNAL_FIELD)                  # doc frequency
            term_obj = self.db.GetTermPostingList(token, WSMEnum.JOURNAL_FIELD)
            doc_data = term_obj.GetDocAndTFValueList(0)       # doc Id list

            for (docID, tf) in doc_data:
                doc_len = self.db.GetDocTermCount(docID)
                score = bm25.get_score(N, Nt, tf, doc_len, l_avg)
                scores[docID] += score

                pos = term_obj.GetPositionInDoc(docID)
                positions[docID] = positions[docID].union(set(pos))

        for token in self.author_tokens:
            Nt = self.db.GetDFValue(token, WSMEnum.AUTHOR_FIELD)                  # doc frequency
            term_obj = self.db.GetTermPostingList(token, WSMEnum.AUTHOR_FIELD)
            doc_data = term_obj.GetDocAndTFValueList(0)       # doc Id list

            for (docID, tf) in doc_data:
                doc_len = self.db.GetDocTermCount(docID)
                score = bm25.get_score(N, Nt, tf, doc_len, l_avg)
                scores[docID] += score

                pos = term_obj.GetPositionInDoc(docID)
                positions[docID] = positions[docID].union(set(pos))


        sorted_scores = sorted(scores.items(), key = operator.itemgetter(1), reverse=True)
        docIDs = []

        for docID, score in sorted_scores:
            docIDs.append(docID)

        if K <= len(docIDs):
            docIDs_K = docIDs[0:K]
            positions_K = defaultdict(list)
            for docID in docIDs_K:
                positions_K[docID] = positions[docID]
            return docIDs_K, positions_K
        else:
            return docIDs, positions

    def retrieve_top_docs(self, st, end):
        if len(self.docIDs) == 0:
            self.docIDs, self.positions = self.__get_top_docIDs__(1000)

        if st >= len(self.docIDs):
            return []
        if end > len(self.docIDs):
            end = len(self.docIDs)

        #print(st, end)
        docIDs = self.docIDs[st:end]
        docs = []
        for docID in docIDs:
            url = self.db.GetDocUrl(docID)
            content = self.db.GetDocFullContent(docID)
            title = self.db.GetDocTitle(docID)
            pos = self.positions[docID]
            docs.append({"url": url, "title": title, "content": content, "position": pos})

        return docs

    def get_rel_doc_counts(self):
        return len(self.docIDs)

# test
if __name__ == 'main':
    query = Query('James')
    print(query.retrieve_top_docs(0,20))

