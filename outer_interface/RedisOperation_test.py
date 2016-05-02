from outer_interface.RedisOperation import *
from inner_kernel.TypeEnum import WSMEnum
""" initialize """
handle =RedisHandler()

""" get dfvalue of a term, if not exists return 0 """
print(handle.GetDFValue('abdul'))

""" get the number of words in a document, if not exists return 0 """
print(handle.GetDocTermCount('3'))

""" get the URL of a document, if not exists return null string """
print(handle.GetDocUrl('3'))

""" get the content in a document, if not exists return null string """
print(handle.GetDocFullContent('3'))

print(handle.GetDocTitle('1'))

""" get [total words; doc_num ; avarage length of document ] of a term, if not exists return null string """
print(handle.GetDBHeaderData())

"""  get the TermList """
term = handle.GetTermPostingList('2030')

if isinstance(term, TermList):

    """  get the Positonlist of term in specific document,if not exist return null string """
    print(term.GetPositonInDoc('3'))

    """  get the TFvalue of term in specific document,if not exist return 0 """
    print(term.GetTFValueInDoc('3'))

    """  get the TFvaluelist and doclist of term in all document,if not exist return null string"""
    print(term.GetDocAndTFValueList(WSMEnum.DOC_TF_LIST))
