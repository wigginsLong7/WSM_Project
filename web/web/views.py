from pyramid.view import view_config

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from outer_interface.Query import Query
from outer_interface.Query import FieldSearch

query = None
fieldsearch = None

@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    query_terms = request.params.get('query', '')
    page_id = int(request.params.get('page', '0'))
    if query_terms == '':
        return {'docs': [], 'page_class': 'page-index', 'query_terms': query_terms, 'page_counts': 0, 'tot_docs':0}

    if page_id == 0:
        global query
        query = Query(query_terms) #TODO: %20 and '+' encoding problem
        page_id += 1

    docs = query.retrieve_top_docs(20 * (page_id-1), 20 * page_id)
    tot_docs = query.get_rel_doc_counts()
    page_cnt = int((tot_docs-1) / 20) + 1

    # doc {"url": url, "content": content, "position": pos, "title": title}
    ret_docs = []
    for doc in docs:
        if not doc['url']:
            continue

        # add red marks to query terms in the snippets
        position = sorted(doc['position'])
        for pos in position:
            try:
                doc['content'][pos] = '<span class="term-red">' + doc['content'][pos] + '</span>'
            except IndexError:
                #print(position)
                print("document length:", len(doc['content']))
                print("maximal position:",max(position))


        # grab snippets
        content_list = []
        prev_pos = 0
        for i in range(len(position)):
            if position[i] > prev_pos + 20:
                st = prev_pos - 5
                en = prev_pos + 5
                if st < 0:
                    st = 0

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)

                st = position[i] - 5
                en = position[i] + 5
                if en > len(doc['content']):
                    en = len(doc['content'])

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)
                prev_pos = en
            else:
                st = prev_pos - 5
                if st < 0:
                    st = 0
                en = position[i] + 5
                if en > len(doc['content']):
                    en = len(doc['content'])

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)
                prev_pos = en

        # truncate snippet size
        if len(content_list) > 5:
            content_list = content_list[0:10]

        doc['content'] = '...'.join(content_list) + '...'
        ret_docs.append(doc)

    return {'docs': ret_docs, 'page_class': 'page-results',
            'query_terms': query_terms, 'page_counts': page_cnt,
            'cur_page': page_id, 'tot_docs': tot_docs}

@view_config(route_name='fieldsearch', renderer='templates/fieldsearch.pt')
def field_view(request):
    query_journal = request.params.get('journal', '')
    query_year = request.params.get('year', '')
    query_title = request.params.get('title', '')
    query_author = request.params.get('author', '')

    page_id = int(request.params.get('page', '0'))
    if query_journal == '' and query_year == '' and query_title == '' and query_author == '':
        return {'docs': [], 'page_class': 'page-index',
                'query_journal': query_journal,
                'query_year': query_year,
                'query_title': query_title,
                'query_author': query_author,
                'page_counts': 0, 'tot_docs':0}

    if page_id == 0:
        global fieldsearch
        fieldsearch = FieldSearch(query_year, query_title, query_journal, query_author) #TODO: %20 and '+' encoding problem
        page_id += 1

    docs = fieldsearch.retrieve_top_docs(20 * (page_id-1), 20 * page_id)
    tot_docs = fieldsearch.get_rel_doc_counts()
    page_cnt = int((tot_docs-1) / 20) + 1

    # doc {"url": url, "content": content, "position": pos, "title": title}
    ret_docs = []
    for doc in docs:
        if not doc['url']:
            continue

        # add red marks to query terms in the snippets
        position = sorted(doc['position'])
        for pos in position:
            try:
                doc['content'][pos] = '<span class="term-red">' + doc['content'][pos] + '</span>'
            except IndexError:
                #print(position)
                print("document length:", len(doc['content']))
                print("maximal position:",max(position))


        # grab snippets
        content_list = []
        prev_pos = 0
        for i in range(len(position)):
            if position[i] > prev_pos + 20:
                st = prev_pos - 5
                en = prev_pos + 5
                if st < 0:
                    st = 0

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)

                st = position[i] - 5
                en = position[i] + 5
                if en > len(doc['content']):
                    en = len(doc['content'])

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)
                prev_pos = en
            else:
                st = prev_pos - 5
                if st < 0:
                    st = 0
                en = position[i] + 5
                if en > len(doc['content']):
                    en = len(doc['content'])

                snippets = ' '.join(doc['content'][st:en])
                content_list.append(snippets)
                prev_pos = en

        # truncate snippet size
        if len(content_list) > 5:
            content_list = content_list[0:10]

        doc['content'] = '...'.join(content_list) + '...'
        ret_docs.append(doc)

    return {'docs': ret_docs, 'page_class': 'page-results',
            'query_year': query_year, 'query_journal': query_journal, 'query_title': query_title,
            'query_author': query_author, 'page_counts': page_cnt,
            'cur_page': page_id, 'tot_docs': tot_docs}
