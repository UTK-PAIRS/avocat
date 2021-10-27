""" avocat/__init__.py - initialization for avocat


@author: Cade Brown <cade@cade.utk>
@author: Gregory Croisdale <>
"""


import os
import subprocess

# for choices in the terminal
import inquirer

# for loose string matching
from fuzzywuzzy import fuzz


from . import act

### UTILS ###

# check whether 'A' and 'B' are close, return 0.0 to 1.0
def text_close(actor, A, B):
    # ratio of closeness [0.0,1.0]
    return fuzz.partial_ratio(A, B) / 100.0

def msg(*args):
    print('avocat>', *args)



""" avocat.act.Actor - represents a virtual user (i.e. personifying the avocat process itself), with permissions, and
                       help messages, and allows users to control what is executed automatically

"""
class Actor:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
        
    def __str__(self) -> str:
        return repr(self)

    def get(self, key, defa=None):
        return self.kwargs.get(key, defa)

    # run a decision tree
    def run(self, tree):
        if isinstance(tree, act.Tree):
            # execute the tree
            return tree.run(self)
        else:
            raise Exception(f"unexpected type for action tree (got object of type {type(tree)})")

    # find a file, return a path to it
    def find(self, name, req=False, paths=[]):
        # add paths
        paths = self.kwargs.get('paths', ['.']) + paths

        # search through
        rpath = None
        for path in paths:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    for fullname in map(lambda x: os.path.join(root, x), files):
                        if fullname.endswith(name):
                            rpath = fullname

        # not found, but required
        if req and rpath is None: raise Exception(f'failed to find file {repr(name)} (looked: {paths})')

        return rpath
        

    # find a file (using fuzzy logic)
    # NOTE: if give 'closefn', accept (actor, A, B) and return whether 'A' and 'B' are close (0.0 to 1.0 scale)
    def find_close(self, name, req=False, paths=[], closefn=text_close):
        # add paths
        paths = self.kwargs.get('paths', ['.']) + paths

        # search through
        rpath = None
        rclose = None
        for path in paths:
            for root, dirs, files in os.walk(path):
                for fullname in map(lambda x: os.path.join(root, x), files):
                    close = closefn(self, name, fullname)
                    if close > 0.5:
                        # (' ', fullname, close)
                        # possible result
                        if rpath is None or close > rclose:
                            rpath = fullname
                            rclose = close

        # not found, but required
        if req and rpath is None: raise Exception(f'failed to find file {repr(name)} (looked: {paths})')

        return rpath

    # perform a single choice
    def choice(self, Q, mapping, force=False):
        res = None
        # make dict
        if isinstance(mapping, list):
            mapping = { v: v for v in mapping }

        # now, seeif it should be interactive
        if not force and self.kwargs.get('auto', False):
            # run automatically
            res = next(iter(mapping.values()))
            print('(auto) ', Q, ' -> ', res, ' (from: ', list(mapping.keys()), ')', sep='')
        else:
            # run manually
            Qs = [
                inquirer.List(
                    "res",
                    message=Q,
                    choices=mapping,
                ),
            ]

            # get answer
            As = inquirer.prompt(Qs)
            res = As["res"]

        # now, check if it needs to be evaluated
        if isinstance(res, act.Tree):
            res = self.run(res)

        return res

    def shell(self, args):
        print('$', *args)
        # run shell command

        res = subprocess.run(args, check=True)

        return res


def find_sol(err, out):
    """ find a solution tree for the given stderr/stdout """
    return act.Shell(
        act.Const(data="apt"), 
        act.Const(data="install"),
        act.Const(data="some-package-name"),
    )  
    #act.Choice(Q="which looks right?", choices=["abc", "xyz"])
    #return act.Tree()

