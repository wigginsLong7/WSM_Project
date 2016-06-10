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

