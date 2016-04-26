from RedisOperation import *

""" initialize """
redispool = redis.ConnectionPool(host='localhost', port=6379, db=0)
handle =RedisHandler(redispool)

""" get dfvalue of a term, if not exists return 0 """
print(handle.GetDFValue('based'))

""" get the number of words in a document, if not exists return null string """
print(handle.GetDocTermCount('myDocID_5'))

""" get the URL of a document, if not exists return null string """
print(handle.GetDocUrl('myDocID_5'))

""" get the content in a document, if not exists return null string """
print(handle.GetDocFullContent('myDocID_5'))

""" get [total words; doc_num ; avarage length of document ] of a term, if not exists return null string """
print(handle.GetDBHeaderData())

"""  get the TermList """
term = handle.GetTermPostingList('in')

if isinstance(term, TermList):

    """  get the Doclist of term in all document,if not exist return null string"""
    print(term.GetDocIDList())

    """  get the Positonlist of term in specific document,if not exist return null string """
    print(term.GetPositonInDoc('myDocID_4'))

    """  get the TFvalue of term in specific document,if not exist return 0 """
    print(term.GetTFValueInDoc('myDocID_4'))

    """  get the TFvaluelist of term in all document,if not exist return null string"""
    print(term.GetTFValueList())

