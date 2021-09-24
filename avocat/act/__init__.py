""" avocat/act/__init__.py - initialization for avocat.act, which are action trees and actors

basically, this module is the meat of the solver/helper functionality



SEE:
  * https://stackoverflow.com/questions/45022566/create-python-cli-with-select-interface
  * https://stackoverflow.com/questions/31642940/finding-if-two-strings-are-almost-similar


@author: Cade Brown <cade@cade.utk>
"""

import os

# for choices in the terminal
import inquirer

# for loose string matching
from fuzzywuzzy import fuzz




# check whether 'A' and 'B' are close, return 0.0 to 1.0
def text_close(actor, A, B):
    # ratio of closeness [0.0,1.0]
    return fuzz.partial_ratio(A, B) / 100.0

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
        if isinstance(tree, Tree):
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
        if isinstance(res, Tree):
            res = self.run(res)

        return res


""" avocat.act.Tree - represents an action tree, which is an abstract action that can be evaluated by an 'Actor'


{
    "type": "Choice",
    "Q": "what do you enter",
    "choices": ["abc", "xyz"],
}

"""
class Tree:

    # create with 'args' being sub-nodes of this tree, and 'kwargs' being the attributes of this tree node
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
    def __repr__(self) -> str:
        at = ', '.join(repr(v) for v in self.args)
        kwt = ', '.join(str(k) + '=' + repr(v) for k, v in self.kwargs.items())
        if not self.args and not self.kwargs:
            return f"{type(self).__name__}()"
        elif not self.kwargs:
            return f"{type(self).__name__}({at})"
        elif not self.args:
            return f"{type(self).__name__}({kwt})"
        else:
            return f"{type(self).__name__}({at}, {kwt})"
        
    def __str__(self) -> str:
        return repr(self)

    def __iter__(self):
        return iter(self.args)

    def __getitem__(self, key):
        if isinstance(key, int):
            # return subnode
            return self.args[key]
        else:
            # return attr
            return self.kwargs[key]

    def __setitem__(self, key, val):
        if isinstance(key, int):
            # set subnode
            self.args[key] = val
        else:
            # set attr
            self.kwargs[key] = val

    def get(self, key, defa=None):
        return self.kwargs.get(key, defa)


    # run the tree (i.e. actually do the action) on a given actor
    # NOTE: override this!
    def run(self, actor):
        raise NotImplementedError

""" avocat.act.Const - action tree that just yields a constant value (give 'data=' to constructor)


"""
class Const(Tree):

    def run(self, actor):
        return self['data']

""" avocat.act.Print - action tree that just prints out its argument


"""
class Print(Tree):

    def run(self, actor):
        # run all sub arguments and print them out
        print(*[actor.run(arg) for arg in self.args], sep=self.get("sep", ''))

""" avocat.act.Choice - action tree that prompts the user for a choice, and yields it


"""
class Choice(Tree):

    def run(self, actor):
        return actor.choice(self["Q"], self["data"])


""" avocat.act.Find - action tree that finds a file/directory


"""
class Find(Tree):

    def run(self, actor):
        return actor.find(self["name"], self.get("req", False))

""" avocat.act.FindClose - action tree that finds a file/directory, using fuzzy logic


"""
class FindClose(Tree):

    def run(self, actor):
        return actor.find_close(self["name"], self.get("req", False))


