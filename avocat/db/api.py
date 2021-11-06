import requests
import urllib.parse
import apikey

class question:
    def __init__(self, question, answers, id):
        self.question = question
        self.answers = answers
        self.id = id

class answer:
    def __init__(self, body, id, score):
        self.body = body
        self.id = id
        self.score = score

def querySO(argv:list=[], stdout:str="", stderr:str="", r:int=None, n:int=1, apikey=apikey.so) -> dict:
    """
        Queries StackOverflow to resolve an issue with cli execution
        of a program according to the parameters.

        argv -> List of program arguments. argv[0] should be the name
        of the errored process.

        stdout -> String representing standard output stream
        of the program after execution. Generally not necessary
        for good results.

        stderr -> String representing standard error stream of the
        program after execution.

        r -> integer indicating the return value of the errored program.

        n -> integer indicating the maximum number of stack overflow
        answers to return.
    
        ===========

        returns a list of stack overflow answers in PUT THE FORMAT
        HERE WHEN YOU FIGURE IT OUT
    """
    def query():

    """
        Query request -- what questions will we target?
    """
    # construct query string based on provided params
    query = argv[0]
    """if len(argv): query += argv[0]
    if stderr not in {"", "stderr", None}: query += " " + stderr
    #elif stdout not in {"", "stdout"}: query += " " + stdout
    if r != 0: query += f" error code {r}"
    """
    # encode query string into url safe format
    query = urllib.parse.quote_plus(query)

    # make request
    req = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q={query}{'&tagged=' + argv[0] if argv else ''}&site=stackoverflow&answers={n}&filter=withbody{'&key=' + apikey if apikey else ''}"
    
    # DEBUG
    print(req)

    # get result
    r = requests.get(req)

    # parse result
    q_resp = dict(r.json())
    remaining = q_resp["quota_remaining"]
    if not len(q_resp['items']): return {"error": "Got no results from query...", "remaining": remaining}

    questions = {q['question_id']: question(q['body'], [], q['question_id']) for q in q_resp['items']}
    ids = [q['id'] for q in questions]

    """
        Answers request -- get answers from selected questions
    """
    # make request
    req = f"https://api.stackexchange.com/2.3/questions/{';'.join(map(str, ids))}/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody{'&key=' + apikey if apikey else ''}"
    print(req)
    
    # get result
    r = requests.get(req)

    # parse result
    a_resp = dict(r.json())
    remaining = a_resp["quota_remaining"]
    if not len(a_resp['items']): return {"error": "Got no results from query...", "remaining": remaining}
    answer_id = a_resp['items'][0]['question_id']
    answer = a_resp['items'][0]['body']

    #code = [answer[s+len('<code>'):e] for s, e in zip([m.start() for m in re.finditer('<code>', answer)], [m.start() for m in re.finditer('</code>', answer)])]

    return {
        'questions': [
            {
                'body': question,
                'url': f'https://stackoverflow.com/questions/{question_id}/',
                'answers': [answer]
            },
        ],
        'code': "code",
        'remaining': remaining
    }

def dummyError():
    print("DUMMY")
    return {
        'questions': [
            {
                'body': 'Dummy question',
                'url': 'https://en.wikipedia.org/wiki/Newtons_(cookie)',
                'answers': ['Dummy answer']
            }
        ],
        'code': [
            'echo meow'
        ],
        'remaining': float('inf')
    }
