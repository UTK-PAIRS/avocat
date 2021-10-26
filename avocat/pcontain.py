#!/usr/bin/env python3

import selectors
from subprocess import Popen, PIPE
from io import BytesIO

"""
    Holds a process and synchronously captures stdout / stderr
"""
class PContain:
    def __init__(self, argv, callbackstd=print, callbackerr=print):
        """ 
            open subprocess with pipes
        """
        p = Popen(argv, stdout=PIPE, stderr=PIPE)

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
                        callbackstd(data.decode())
                    else:
                        stderrb.write(data)
                        callbackerr(data.decode())

        self.ret = p.poll()
        self.stdout = stdoutb.getvalue().decode()
        self.stderr = stderrb.getvalue().decode()