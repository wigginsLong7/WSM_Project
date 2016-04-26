import re
from PorterStemmer import PorterStemmer


class Tokenizer:

    def __init__(self):
        self.is_stemming = False            # whether stemming is applied
        self.is_stopping = False            # whether stop words is removed
        self.is_entity_del = True           # whether entity is removed
        self.is_num_del = True              # whether number is removed (only remove when the whole token is a number)
        self.is_single_letter_del = True    # whether a single letter is removed

    def set_stemming(self, option):
        self.is_stemming = option

    def set_stopping(self, option):
        self.is_stopping = option

    def set_entity_del(self, option):
        self.is_entity_del = option

    def set_num_del(self, option):
        self.is_num_del = option

    def set_single_letter_del(self, option):
        self.is_single_letter_del = option

    def __del_single_letter__(self, token):
        if len(token) <= 1:
            return ""
        return token

    def __del_num__(self, token):
        if re.search(r'^[0-9]+$', token):
            return ""
        return token

    def __del_entity__(self, token):
        entity_ref = re.compile(r"""
             &[#]                # Start of a numeric entity reference
             (
                 0[0-7]+         # Octal form
               | [0-9]+          # Decimal form
               | x[0-9a-fA-F]+   # Hexadecimal form
             )
             ;                   # Trailing semicolon
            """, re.VERBOSE)

        token = re.sub(entity_ref, "", token)
        return token

    def __del_stop_word__(self, token):
        stop_words = [
            "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
            "any", "are", "aren't", "as", "at",
            "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
            "can't", "cannot", "could", "couldn't",
            "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
            "each", "few", "for", "from", "further",
            "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll",
            "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
            "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
            "let's", "me", "more", "most", "mustn't", "my", "myself",
            "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our","ours",
            "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should",
            "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
            "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
            "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're",
            "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who",
            "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
            "you're", "you've", "your", "yours", "yourself", "yourselves"
        ]

        for word in stop_words:
            if word == token:
                return ""

        return token

    def __del_non_alphanumeric__(self, token):
        pattern = re.compile('[\W_]+')
        token = re.sub(pattern, '', token)
        return token

    def __apply_porter_stemming__(self, token):
        porter_stemmer = PorterStemmer()
        token = porter_stemmer.stem(token, 0, len(token)-1)
        return token

    def __apply_lower_case__(self, token):
        return token.lower()

    def tokenize(self, token):
        if self.is_entity_del:
            token = self.__del_entity__(token)
        token = self.__apply_lower_case__(token)
        token = self.__del_non_alphanumeric__(token)

        if self.is_num_del and token:
            token = self.__del_num__(token)
        if self.is_stopping and token:
            token = self.__del_stop_word__(token)
        if self.is_stemming and token:
            token = self.__apply_porter_stemming__(token)
        if self.is_single_letter_del and token:
            token = self.__del_single_letter__(token)

        return token