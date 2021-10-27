""" avocat/act/__init__.py - initialization for avocat.act, which are action trees

basically, this module is the meat of the solver/helper functionality


SEE:
  * https://stackoverflow.com/questions/45022566/create-python-cli-with-select-interface
  * https://stackoverflow.com/questions/31642940/finding-if-two-strings-are-almost-similar


@author: Cade Brown <cade@cade.utk>
"""

import os


class Tree:
    """ action tree, which is an abstract action that can be evaluated by an 'Actor' """

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
        ind = '  '
        def _str(node, dep=0):
            
            r = f'{ind * dep}<{type(node).__name__}'
            for k, v in node.kwargs.items():
                r += f' {k}={v!r}'

            if node.args:
                yield r
                for sub in node.args:
                    for r in _str(sub, dep + 1):
                        yield ind + r

                yield f'{ind * dep}>'
            
            else:
                yield r + '>'

        return '\n'.join(_str(self))

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

class Const(Tree):
    """ represents a constant value """

    def run(self, actor):
        return self['data']

class Message(Tree):
    """ reprents a message, which should display something to the user """

    def run(self, actor):
        # run all sub arguments and print them out
        print(*[actor.run(arg) for arg in self.args], sep=self.get("sep", ''))

class Choice(Tree):
    """ prompts the user for a choice, and yields the data associated with it 

    example:
    Choice(Q="which do you prefer?", choices=["abc", "xyz"])
    
    """

    def run(self, actor):
        return actor.choice(self["Q"], self["data"])

class Find(Tree):
    """ attempts to locate a file/directory by name

    example:
    Find(name"myfile.c", req=True)
    
    """

    def run(self, actor):
        return actor.find(self["name"], self.get("req", False))

class FindClose(Tree):
    """ attempts to locate a file/directory by name, using fuzzy/close search logic """

    def run(self, actor):
        return actor.find_close(self["name"], self.get("req", False))

class Shell(Tree):
    """ runs a shell command """

    def run(self, actor):
        # dump arguments
        args = [actor.run(arg) for arg in self.args]
        return actor.shell(args)

class InstallPackage(Tree):
    """ installs a package, with a list of valid choices """

    def run(self, actor):
        # dump arguments
        args = [actor.run(arg) for arg in self.args]
        return actor.shell(args)


