from outer_interface.RedisOperation import *

""" initialize """
handle =RedisHandler()

""" get dfvalue of a term, if not exists return 0 """
print(handle.GetDFValue('based'))

""" get the number of words in a document, if not exists return 0 """
print(handle.GetDocTermCount('myDocID_5'))

""" get the URL of a document, if not exists return null string """
print(handle.GetDocUrl('myDocID_5'))

""" get the content in a document, if not exists return null string """
print(handle.GetDocFullContent('myDocID_5'))

""" get [total words; doc_num ; avarage length of document ] of a term, if not exists return null string """
print(handle.GetDBHeaderData())

"""  get the TermList """
term = handle.GetTermPostingList('for')

if isinstance(term, TermList):

    """  get the Positonlist of term in specific document,if not exist return null string """
    print(term.GetPositonInDoc('myDocID_7'))

    """  get the TFvalue of term in specific document,if not exist return 0 """
    print(term.GetTFValueInDoc('myDocID_7'))

    """  get the TFvaluelist and doclist of term in all document,if not exist return null string"""
    print(term.GetDocAndTFValueList(WSMEnum.DOCLIST))
