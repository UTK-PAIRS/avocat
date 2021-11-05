import requests
import urllib.parse
import avocat.db.apikey as apikey

QSITE = "askubuntu"

def extract_code(body):
    out = []
    for c in body.split("<code>")[1:]:
        out += [*[s.rstrip() for s in c.split("</code>")[0].split("\n") if s != '']]

    return out

class question:
    def __init__(self, body, answers, id):
        self.body = body
        self.answers = answers
        self.id = id

    def __str__(self):
        return self.body

    def __repr__(self):
        answers = '\n'.join([repr(r) for r in self.answers])
        return f"QID {self.id}:\n{self.body}\n\n{answers}"

class answer:
    def __init__(self, body, id, score):
        self.body = body
        self.id = id
        self.score = score
        self.code = extract_code(body)

    def __str__(self):
        return self.body

    def __repr__(self):
        return f"AID {self.id}:\n{self.body}"

def querySO(query:str="", tags:list=[], n:int=1, apikey:str=apikey.so) -> dict:
    """
        Queries StackOverflow to resolve an issue with cli execution
        of a program according to the parameters.

        query: str
            The query to be resolved.

        tags: list
            The tags to be used to filter the results.

        n: int
            The number of results to be returned.

        apikey: str
            The StackOverflow API key.
    """

    """
    Query request -- what questions will we target?
    """
    # encode query string into url safe format
    query = urllib.parse.quote_plus(query)

    # make request
    req = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q={query}{'&tagged=' + ';'.join(tags) if tags else ''}&site={QSITE}&answers={n}&filter=withbody{'&key=' + apikey if apikey else ''}"
    
    # DEBUG
    print(req)

    # get result
    r = requests.get(req)

    # parse result
    q_resp = dict(r.json())
    remaining = q_resp["quota_remaining"]

    if not len(q_resp['items']):
        raise Exception("Got no results from query request")

    questions = {q['question_id']: question(q['body'], [], q['question_id']) for q in q_resp['items']}

    return questions


def getAnswers(questions:dict, apikey=apikey.so) -> dict:
    """
    Answers request -- get answers from selected questions
    """
    # make request
    ids = [q for q in questions]
    req = f"https://api.stackexchange.com/2.3/questions/{';'.join(map(str, ids))}/answers?order=desc&sort=activity&site={QSITE}&filter=withbody{'&key=' + apikey if apikey else ''}"

    # DEBUG
    print(req)
    
    # get result
    r = requests.get(req)

    # parse result
    a_resp = dict(r.json())

    remaining = a_resp["quota_remaining"]

    if not len(a_resp['items']):
        raise Exception("Got no results from answers request")

    for i in a_resp['items']:
        questions[i['question_id']].answers.append(answer(i['body'], i['answer_id'], i['score']))

    return questions
