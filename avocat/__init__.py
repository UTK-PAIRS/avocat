""" avocat/__init__.py - avocat initialization/setup


@author: Cade Brown <me@cade.site>
@author: Gregory Croisdale <gcroisda@vols.utk.edu>
"""


import os
import subprocess
import threading

# for choices in the terminal
import inquirer


# for loose string matching
# from fuzzywuzzy import fuzz

import avocat.tree as tree
import avocat.db as db

### UTILS ###

# check whether 'A' and 'B' are close, return 0.0 to 1.0
def text_close(actor, A, B):
    return 1.0
    # ratio of closeness [0.0,1.0]
    # return fuzz.partial_ratio(A, B) / 100.0


def display(*args, prefix='avocat>'):
    print(prefix, *args)

def section(title):
    """ Print section header """
    print()
    lx = 48
    print('-' * lx)
    print(title)
    print('-' * lx)
    print()



def shell(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.stdout, proc.stderr

    def run(res, fp, prefix):
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.decode('utf-8')
            res.append(line)
            print(prefix + line.strip())
    # content of each
    rout = []
    rerr = []


    # launch threads to display in real time
    tout = threading.Thread(target=run, args=(rout, out, 'out> '))
    terr = threading.Thread(target=run, args=(rerr, err, 'err> '))

    tout.start()
    terr.start()

    proc.wait()

    tout.join()
    terr.join()

    # return success, stdout, stderr
    return proc.returncode == 0, "".join(rout), "".join(rerr)

class ActorError(Exception):
    """ An error from an actor """
    pass

"""
    avocat.act.Actor - represents a virtual user (i.e. personifying the avocat process itself), with permissions, and
                       help messages, and allows users to control what is executed automatically
"""
class Actor:
    """ An actor/user abstraction that can perform actions, and evaluate trees (see avocat.tree) """
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
        
    def __str__(self) -> str:
        return repr(self)

    def get(self, key, defa=None):
        return self.kwargs.get(key, defa)
        
    def __call__(self, node: tree.Node):
        """ Call 'actor(node)' to run a tree node """
        if isinstance(node, tree.Node):
            return node.run(self)
        elif isinstance(node, list):
            return list(map(lambda x: self(x), node))
        elif isinstance(node, (str, int, float)):
            return node
        else:
            return node
        #    raise Exception(f"unexpected type for action tree (got object of type {type(node)})")

    ### UTILS ###

    def print(self, *args):
        r = []
        for a in args:
            while isinstance(a, (tree.Node, list)):
                a = self(a)
            r.append(a)

        display(*r)

    def error(self, *args):
        r = []
        for a in args:
            while isinstance(a, tree.Node):
                a = self(a)
            r.append(a)

        # raise an error
        raise ActorError(' '.join(map(str, r)))

    def choose(self, prompt: str, keys: list, vals: list, multi=False, default=None):
        """ Perform a choice with 'keys' being the display values, and 'vals' being the result values 
        
        Give 'multi=True' to allow multiple choices
        """
        if multi:
            Qs = [
                inquirer.Checkbox("res", message=prompt, choices=dict(zip(keys, vals)), default=default),
            ]

            As = inquirer.prompt(Qs)
            try:
                res = []
                for v in As['res']:
                    res.append(vals[keys.index(v)])
            except KeyboardInterrupt:
                display("exiting, because user hit CTRL+C")
                exit(0)

            # convert to constant
            while isinstance(res, (tree.Node, list)):
                res = self(res)

            return res

        else:
            Qs = [
                inquirer.List("res", message=prompt, choices=dict(zip(keys, vals)), default=default),
            ]

            As = inquirer.prompt(Qs)
            try:
                res = vals[keys.index(As["res"])]
            except KeyboardInterrupt:
                display("exiting, because user hit CTRL+C")
                exit(0)

            # convert to constant
            while isinstance(res, (tree.Node, list)):
                res = self(res)

            return res

    def shell(self, args):
        # print that we are running it
        args = [self(a) for a in args]
        display(*args, prefix='$')

        # now, run it
        proc = subprocess.run(args, capture_output=True, text=True, shell=True)
        out, err = proc.stdout, proc.stderr
            
        if proc.returncode != 0:
            section("While Solving An Error, Another Occured...")

            # display
            for line in out.split('\n'):
                display(line, prefix='out>')
            for line in err.split('\n'):
                display(line, prefix='err>')

            section("Finding Solution...")

            # try to find solution
            sol = db.find_sol(out, err)

            # find solution tree
            display("Found solutions from StackOverflow")
            #sol = avocat.db.find_sol(out, err, args.command)
            #print(sol)

            section("Running Solution...")

            # run solution
            self(sol)

            return proc

        else:
            # display
            for line in out.split('\n'):
                display(line, prefix='out>')
            for line in err.split('\n'):
                display(line, prefix='err>')

            return proc
