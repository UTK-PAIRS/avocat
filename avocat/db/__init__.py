""" avocat/db/__init__.py - database for finding solutions



"""

import avocat.tree as tree
import avocat.db.stackexchange as se
import shlex


# known solutions, hardcoded
db_ = {
    "Assertion Error! Cats are bad programmers.\n":
        tree.Shell(
            "echo",
            "cats are indeed bad programmers",
        ),
    "ls: cannot access 'thisdoesnotexist': No such file or directory\n":
        tree.Shell(
            "echo",
            "cats are indeed bad programmers",
        )
}

def find_sol(out, err, argv=[]):
    """ Attempt to find a solution for the given stdout/stderr """
    # hard coded solutions
    if err in db_:
        return db_[err]

    # otherwise, search stack exchange
    Qs = se.find_Qs(err)[:4]

    def from_A(a):
        """ Generate from answer """

        cmds = []
        for c in a.codes:
            if len(c) > 3:
                # TODO: make smarter filter to remove inline code/etc
                cmds.append(tree.Shell(*shlex.split(c)))

        # prepend 'all'
        cmds = [cmds[:]] + cmds

        keys = ["run all"] + [shlex.join(c.sub) for c in cmds[1:]]
        return tree.Choose(*cmds, prompt="Which commands to run?", keys=keys)

    def from_Q(q):
        return from_A(next(iter(q.As)))
        keys = []
        vals = []

        for a in q.As:
            keys.append(a.title)
            vals.append(from_A(a))

        return tree.Choose(prompt="Which answer seems right?", keys=keys)

    keys = []
    vals = []

    for q in Qs:
        keys.append(q.title)
        vals.append(from_Q(q))
    return tree.Choose(*vals, prompt="Which question seems right?", keys=keys)


def extract_codes(questions):
    """
    Get code snippets from a list of questions's answers.
    """
    code = []
    for q in questions.values():
        for a in q.answers:
            code += a.code
    
    return code

def codes_to_tree(codes):
    """
    Convert a list of codes to a tree of choices.
    """
    res = act.Choice(Q="which command looks best?", choices=[act.Shell(*c.split()) for c in codes])
    print (res)
    return res
