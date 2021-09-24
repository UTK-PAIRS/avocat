""" avocat/act/__init__.py - initialization for avocat.act, which are action trees and actors

basically, this module is the meat of the solver/helper functionality



SEE: https://stackoverflow.com/questions/45022566/create-python-cli-with-select-interface

@author: Cade Brown <cade@cade.utk>
"""

# for choices in the terminal
import inquirer

""" avocat.act.Actor - represents a virtual user (i.e. personifying the avocat process itself), with permissions, and
                       help messages, and allows users to control what is executed automatically

"""
class Actor:

    def __init__(self):
        pass
        
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
        
    def __str__(self) -> str:
        return repr(self)



    # run a decision tree
    def run(self, tree):
        if isinstance(tree, Tree):
            # execute the tree
            return tree.run(self)
        else:
            raise Exception(f"unexpected type for action tree (got object of type {type(tree)})")


""" avocat.act.Tree - represents an action tree, which is an abstract action that can be evaluated by an 'Actor'


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
        print(*[actor.run(arg) for arg in self.args], sep='')

""" avocat.act.Choice - action tree that prompts the user for a choice, and yields it


"""
class Choice(Tree):

    def run(self, actor):
        # produce questions
        Qs = [
            inquirer.List(
                "res",
                message=self["Q"],
                choices=self["choices"],
            ),
        ]

        # get answers
        As = inquirer.prompt(Qs)

        # return result
        return As["res"]
