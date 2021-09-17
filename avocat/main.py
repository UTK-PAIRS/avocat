#!/usr/bin/env python3

"""
main.py

Author: Gregory Croisdale
"""

import sys
import selectors
from subprocess import Popen, PIPE
from io import BytesIO
import urllib.parse
import requests
import re

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

# https://stackoverflow.com/a/58780542
def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

# https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def menu() -> "sel":
    print("s: view url source; c: view code snippets; q: change query; e: execute command")
    return 

def main():
    """ 
        open subprocess with pipes
    """

    p = Popen(sys.argv[1:], stdout=PIPE, stderr=PIPE)

    """
        create buffers
    """
    stdoutb = BytesIO()
    stderrb = BytesIO()

    # https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order/32741930
    """
        use selector to listen simultaneously and add to buffer
    """
    sel = selectors.DefaultSelector()
    sel.register(p.stdout, selectors.EVENT_READ)
    sel.register(p.stderr, selectors.EVENT_READ)

    while p.poll() is None:
        for key, _ in sel.select():
            data = key.fileobj.read1()
            if data:
                if key.fileobj is p.stdout:
                    stdoutb.write(data)
                    print(data.decode(), end='')
                else:
                    stderrb.write(data)
                    print(bcolors.FAIL + data.decode() + bcolors.ENDC, file=sys.stderr, end='')

    """
        At this point, the process has finished running. Now, we can figure out if we need to diagnose it.
    """

    ret = p.poll()
    
    """
        upon nonzero return value, diagnose with server
    """
    if ret:
        print("\n=== AVOCAT ===")
        print(f"'{' '.join(sys.argv[1:])}' ended with error code {ret}!")
        print("Diagnosing...")
        
        enc = urllib.parse.quote_plus

        # process bytestreams
        sout = ' '.join(stdoutb.getvalue().decode().split())
        serr = ' '.join(stderrb.getvalue().decode().split())

        # generate and send request
        #req = f'http://localhost:5000/req?argv={",".join(map(enc, sys.argv[1:]))}&stdout={enc(sout)}&stderr={enc(serr)}&r={ret}'
        req = 'http://localhost:5000/req?argv=dummy'

        r = None
        try:
            r = requests.get(req)
        except:
            print(bcolors.FAIL + "Unable to complete request with server -- all hope is lost." + bcolors.ENDC)
        
        # we got a response from the server! triage
        if r:
            d = r.json()

            # check for code
            if "code" in d:
                print(f"Try code snippet `{c[-1]}`.")
            if "questions" in d:
                normalize = lambda body, w: cleanhtml('\n'.join(["\n".join([line[start:start + w] for start in range(0, len(line), w)]) for line in body.split('\n')]))
                print_msg_box(normalize(d["questions"][0]["body"], 80))
                print_msg_box(normalize(d["questions"][0]["answers"][0], 80))
            else:
                print(bcolors.FAIL + "Unable to diagnose -- got no matching posts" + bcolors.ENDC)
        else:
            print("Got nothing back from the server... Darn you, cats!")
    
    stdoutb.close()
    stderrb.close()

if __name__ == "__main__":
    main()
