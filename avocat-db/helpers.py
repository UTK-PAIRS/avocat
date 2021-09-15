"""
    Author: Gregory Croisdale
"""

import requests
import urllib.parse

# https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

METHOD = "STACK"

def querySO(argv:list=[], stdout:str="", stderr:str="", r:int=None, n:int=1, apikey=None) -> dict:
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

    """
        Query questions request
    """
    # construct query string based on provided params
    query = ""
    if len(argv): query += argv[0]
    if stderr not in {"", "stderr"}: query += " " + stderr
    #elif stdout not in {"", "stdout"}: query += " " + stdout
    if r != 0: query += f" error code {r}"
    query = urllib.parse.quote_plus(query)

    if METHOD == "STACK":
        # make request
        req = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q={query}{'&tagged=' + argv[0] if argv else ''}&site=stackoverflow&answers={n}&filter=withbody{'&key=' + apikey if apikey else ''}"
        print(req)

        r = None
        try:
            r = requests.get(req)
        except:
            print(bcolors.FAIL + "Unable to complete request with server -- all hope is lost." + bcolors.ENDC)
            return {"Unable to communicate with stackexchange!"}

        q_resp = dict(r.json())
        remaining = q_resp["quota_remaining"]
        if not len(q_resp['items']): return {"error": "Got no results from query...", "remaining": remaining}
        question_id = q_resp['items'][0]['question_id']
        question = q_resp['items'][0]['body']
    elif METHOD == "GOOGLE":
        print("NOT IMPLEMENTED")

    """
        Get answers request
    """
    # make request
    req = f"https://api.stackexchange.com/2.3/questions/{';'.join(map(str, [question_id]))}/answers?order=desc&sort=activity&site=stackoverflow&filter=withbody{'&key=' + apikey if apikey else ''}"
    print(req)
    
    r = None
    try:
        r = requests.get(req)
    except:
        print(bcolors.FAIL + "Unable to complete request with server -- all hope is lost." + bcolors.ENDC)
        return {"Unable to communicate with stackexchange!"}

    a_resp = dict(r.json())
    remaining = a_resp["quota_remaining"]
    if not len(a_resp['items']): return {"error": "Got no results from query...", "remaining": remaining}
    answer_id = a_resp['items'][0]['question_id']
    answer = a_resp['items'][0]['body']

    return {
        'questions':
            [
                {
                    'body': question,
                    'url': f'https://stackoverflow.com/questions/{question_id}/',
                    'answers': [answer]
                },
            ],
        'remaining': remaining
    }