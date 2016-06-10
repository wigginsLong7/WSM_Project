from outer_interface.RedisOperation import *
from inner_kernel.TypeEnum import WSMEnum
""" initialize """
handle =RedisHandler()

""" get dfvalue of a term, if not exists return 0 """
print(handle.GetDFValue('based'))

""" get the number of words in a document, if not exists return 0 """
print(handle.GetDocTermCount('1'))

""" get the URL of a document, if not exists return null string """
print(handle.GetDocUrl('95'))

""" get the content in a document, if not exists return null string """
print(handle.GetDocFullContent('95'))

print(handle.GetDocTitle('95'))

""" get [total words; doc_num ; avarage length of document ] of a term, if not exists return null string """
print(handle.GetDBHeaderData())

"""  get the TermList """
term = handle.GetTermPostingList('networks',WSMEnum.JOURNAL_FIELD)

if isinstance(term, TermList):

    """  get the Positonlist of term in specific document,if not exist return null string """
    print(term.GetPositonInDoc('95'))

    """  get the TFvalue of term in specific document,if not exist return 0 """
    print(term.GetTFValueInDoc('95'))

    """  get the TFvaluelist and doclist of term in all document,if not exist return null string"""
    print(term.GetDocAndTFValueList(WSMEnum.DOC_TF_LIST))
