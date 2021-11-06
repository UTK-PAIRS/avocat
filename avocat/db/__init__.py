""" avocat/db/__init__.py - database for finding solutions



"""

import avocat.act as act
import avocat.db.stackexchange as se


# known solutions, hardcoded
db_ = {
    "Assertion Error! Cats are bad programmers.\n":
        act.Shell(
            act.Const(data="echo"), 
            act.Const(data="cats are indeed bad programmers"), 
        ),
    "ls: cannot access 'thisdoesnotexist': No such file or directory\n":
        act.Shell(
            act.Const(data="echo"), 
            act.Const(data="you are an idiot"), 
        )
}

def find_sol(out, err, argv=[]):
    """ find a solution tree for the given stderr/stdout (optionally, the arguments ran with) """
    # hard coded solutions
    if err in db_:
        return db_[err]

    Qs = se.find_Qs(err)[:4]

    # just do first now
    Q = Qs[0]

    res = {}
    for q in Qs:
        rr = {}
        for a in q.As:
            cs = a.codes[0]
            rr[cs] = act.Shell(cs.split())
        res[q.title] = act.Choice(Q="what command to run?", data=rr)

    return act.Choice(Q="what question is most relevant?", data=res)
    #return act.Choice(Q="what command should i run?", data={'$ ' + text: act.Shell(text.split()) for text in Q.As[0].codes()})

    #return codes_to_tree(extract_codes(
    #    api.getAnswers(api.querySO("", tags=[argv[0]] if len(argv) > 0 else []))
    #))
    #act.Choice(Q="which looks right?", choices=["abc", "xyz"])
    #return act.Tree()

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
