""" avocat/db/stackexchange.py - StackExchange API wrapper


"""

import functools

import requests
import urllib.parse

# API key for stack exchange (i believe this is Greg's)
apikey_ = "d3qKMek1GCXs8ED6ee6ANA(("

# what StackExchange site should we use?
site_ = "askubuntu"

class Post:
    """ Represents either a question or an answer. Provides utilities """

    @functools.cached_property
    def codes(self):
        """ Return a list of all code elements """
        res = []
        for c in self.body.split("<code>")[1:]:
            res += [*[s.rstrip() for s in c.split("</code>")[0].split("\n") if s != '']]
        return res


class Q(Post):
    """ Represents a question on some site """
    def __init__(self, id, title, body, score, As_=None):
        self.id = id
        self.title = title
        self.body = body
        self.score = score
        self.As_ = As_

    def __repr__(self) -> str:
        return f"Q({self.id}, {self.body})"

    def __str__(self) -> str:
        return repr(self)

    # cache '.As' to be a list of answers, calculated lazily
    @property
    def As(self):
        if self.As_ is not None:
            return self.As_

        assert False and "shouldn't be lazyily computing... internal error"
        # otherwise, we need to makea request
        req_url = f"https://api.stackexchange.com/2.3/questions/{self.id}/answers?order=desc&sort=activity&site={site_}&filter=withbody{'&key=' + apikey_ if apikey_ else ''}"
        
        # get result
        resp = requests.get(req_url)

        resp_data = dict(resp.json())
        if not len(resp_data['items']):
            raise Exception(f"failed to get any results from: {req_url}")

        # now, save it for next time
        self.As_ = [A(a['answer_id'], a['body'], a['score']) for a in resp_data['items']]
        return self.As_

class A(Post):
    """ Represents an answer on some site """
    def __init__(self, id, body, score):
        self.id = id
        self.body = body
        self.score = score

    def __repr__(self) -> str:
        return f"A({self.id}, {self.body}, {self.score})"

    def __str__(self) -> str:
        return repr(self)
        
def find_Qs(query, num=1, tags=[]):
    """ Returns a list of questions that is relevant to the given query """
    # encode query string into url safe format
    query = urllib.parse.quote_plus(query)

    # generate request URL
    req_url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q={query}{'&tagged=' + ';'.join(tags) if tags else ''}&site={site_}&answers={num}&filter=withbody{'&key=' + apikey_ if apikey_ else ''}"

    # get response object
    resp = requests.get(req_url)

    # convert to raw data
    resp_data = dict(resp.json())

    if not len(resp_data['items']):
        raise Exception(f"failed to get any results from request: {req_url}")

    # map of qid: []As
    qas = {q["question_id"]: [] for q in resp_data["items"]}

    # make a request for all answers
    areq_url = f"https://api.stackexchange.com/2.3/questions/{';'.join(map(str, qas.keys()))}/answers?order=desc&sort=activity&site={site_}&filter=withbody{'&key=' + apikey_ if apikey_ else ''}"

    areq = requests.get(areq_url)
    aresp_data = dict(areq.json())

    # generate results
    for a in aresp_data["items"]:
        qas[a["question_id"]].append(A(a["answer_id"], a["body"], a["score"]))

    # give 'As_' for precomputation
    return [Q(q["question_id"], q["title"], q["body"], q["score"], As_=qas[q["question_id"]]) for q in resp_data['items']]

