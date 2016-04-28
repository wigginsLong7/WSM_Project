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
        N = int(col_data[1] )                        # total number of docs in the collection
        l_avg = int(col_data[2])                     # avg length of doc
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
            return (docIDs[0:K], positions[docIDs[0:K]])
        else:
            return (docIDs, positions)

    def retrieve_top_docs(self, K=20):
        docIDs, positions = self.__get_top_docIDs__(K)
        docs = []

        for docID in docIDs:
            url = self.db.GetDocUrl(docID)
            content = self.db.GetDocFullContent(docID)
            pos = positions[docID]
            docs.append({"url": url, "content": content, "position": pos})

        return docs

# test
query = Query('and')
print(query.retrieve_top_docs())

