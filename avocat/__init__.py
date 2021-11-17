""" avocat/__init__.py - avocat initialization/setup


@author: Cade Brown <me@cade.site>
@author: Gregory Croisdale <gcroisda@vols.utk.edu>
"""


import os
import subprocess

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
        elif isinstance(node, (str, int, float)):
            return node
        else:
            raise Exception(f"unexpected type for action tree (got object of type {type(node)})")

    ### UTILS ###

    def choose(self, prompt: str, keys: list, vals: list):
        """ Perform a choice with 'keys' being the display values, and 'vals' being the result values """
        Qs = [
            inquirer.List("res", message=prompt, choices=dict(zip(keys, vals))),
        ]

        As = inquirer.prompt(Qs)
        try:
            res = vals[keys.index(As["res"])]
        except:
            display("exiting, because user hit CTRL+C")
            exit(0)

        # convert to constant
        while isinstance(res, tree.Node):
            res = self(res)

        return res

    def shell(self, args):
        # print that we are running it
        args = [self(a) for a in args]
        display(*args, prefix='$')

        # now, run it
        proc = subprocess.run(args, capture_output=True, text=True)
        out, err = proc.stdout, proc.stderr

        # display
        for line in out.split('\n'):
            display(line, prefix='out>')
        for line in err.split('\n'):
            display(line, prefix='err>')

        return proc
