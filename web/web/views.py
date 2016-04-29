from pyramid.view import view_config

import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))

from outer_interface.Query import Query

@view_config(route_name='home', renderer='templates/home.pt')
def my_view(request):
    query_terms = request.params.get('query', '')

    docs = []
    """
    if query_terms:
        query = Query(query_terms)
        docs = query.retrieve_top_docs(20)
    """
    # doc {"url": url, "content": content, "position": pos}
    docs = [{"url":"http://something.com", "content": "OIO", "position": [1,2,3,4]},
            {"url":"http://nothing.com", "content": "IOI", "position": [5,6,7,8]}]
    return {'project': 'web', 'docs': docs}
