from pyramid.view import view_config

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from outer_interface.Query import Query

query = None

@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    query_terms = request.params.get('query', '')
    page_id = int(request.params.get('page', '0'))
    if query_terms == '':
        return {'docs': [], 'page_class': 'page-index', 'query_terms': query_terms, 'page_counts': 0, 'tot_docs':0}

    if page_id == 0:
        global query
        query = Query(query_terms)
        page_id += 1

    docs = query.retrieve_top_docs(20 * (page_id-1), 20 * page_id)
    tot_docs = query.get_rel_doc_counts()
    page_cnt = int((tot_docs-1) / 20) + 1

    # doc {"url": url, "content": content, "position": pos}
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
