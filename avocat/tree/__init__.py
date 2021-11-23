""" avocat/tree/__init__.py - avocat tree setup/definitions

In avocat, solutions/actions are organized in a tree structure, which can be evaluated by
  an actor (see avocat.Actor()). Trees can run shell commands, install packages, send messages,
  or even prompt the user for input.

SEE:
  * https://stackoverflow.com/questions/45022566/create-python-cli-with-select-interface
  * https://stackoverflow.com/questions/31642940/finding-if-two-strings-are-almost-similar

@author: Cade Brown <me@cade.site>
"""

def pretty(node):
    """ Make a pretty-printable string for a tree """
    def gen(node, dep):
        yield dep, type(node).__name__
        for s in node.sub:
            for d, l in gen(s, dep+1):
                yield d+1, l
    return '\n'.join(map(lambda d, l: '  '*d + l, gen(node, 0)))

class Node:
    """ Base class of all tree nodes """

    def __init__(self, *sub, **kwargs):
        self.sub = list(sub)
        self.kwargs = kwargs

    def __repr__(self) -> str:
        args = [self.sub]
        for key, val in self.kwargs.items():
            args.append(f"{key}={val!r}")
        return type(self).__name__ + "(" + ", ".join(map(repr, args)) + ")"

    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.sub)

    def __getitem__(self, key):
        return self.kwargs[key]

    def get(self, key, defa=None):
        return self.kwargs.get(key, defa)

    # run the tree (i.e. actually do the action) on a given actor
    # NOTE: override this!
    def run(self, actor):
        raise NotImplementedError

class Print(Node):
    """ Prints a message to the console """
    def run(self, actor):
        return actor.print(*self.sub)

class Error(Node):
    """ Prints an error message to the console, stops the program """
    def run(self, actor):
        return actor.error(*self.sub)

class Choose(Node):
    """ Prompts the user to choose an option """
    def run(self, actor):
        return actor.choose(self['prompt'], self['keys'], self.sub)

class Shell(Node):
    """ Runs a shell command """
    def run(self, actor):
        res = actor.shell(self.sub)
        return res
