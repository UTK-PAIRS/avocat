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
    req = f'http://localhost:5000/req?{",".join(map(enc, sys.argv[1:]))};stdout={enc(sout)};stderr={enc(serr)};r={ret}'
    print(req)

    r = None
    try:
        r = requests.get(req)
    except:
        print(bcolors.FAIL + "Unable to complete request with server -- all hope is lost." + bcolors.ENDC)

stdoutb.close()
stderrb.close()