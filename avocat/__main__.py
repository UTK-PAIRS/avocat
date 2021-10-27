""" avocat/__main__.py - avocat CLI implementation


@author: Cade Brown <cade@cade.utk>
@author: Gregory Croisdale <>
"""

import avocat

import subprocess

import argparse

parser = argparse.ArgumentParser(description='avocat: your terminal advocate')

parser.add_argument('-e','--stderr', help='path to the stderr file')
parser.add_argument('-o','--stdout', help='path to the stdout file')

parser.add_argument('-f','--file', help='path to the command file to run')


args = parser.parse_args()

if args.file:
    proc = subprocess.run(["sh", args.file], capture_output=True, text=True)
    out, err = proc.stdout, proc.stderr
else:
    if not args.stdout or not args.stderr:
        raise Exception("'-e' and '-o' are required! (or, use '-f'). run with '--help' to see all options")
    # read contents of stdout and stderr
    out, err = open(args.stdout, 'r').read(), open(args.stderr, 'r').read()


# find solution tree
sol = avocat.find_sol(out, err)

print (sol)

# create actor
act = avocat.Actor()


print (act)

print(act.run(sol))



# create action item
#tree = act.Print(
#    act.Find(name='act/__init__.py', req=True),
#    act.FindClose(name='act/__initff__.py', req=True),
#    sep='\n',
#)



"""
NPM: no such module react-native-elements
"""

"""
tree = act.PackageInstall(
    pkgman=act.Data('PACKAGE_MANAGER'),
    name=act.Data('PACKAGE_NAME'),
)
"""

"""

tree = act.Print(
    act.Const(data="hey, you said: "),
    act.Choice(Q="what do you want to enter?", data={ 'abc': 'abc', 'foo': 'foo', 'v123': '1.2.3', 'v456': '4.5.6' }),
)


# print out the tree
print(tree)

# now, run the action item
res = actor.run(tree)


actor, proc_shell = avocat.shell(auto=True)

for match in avocat.search(proc_shell.stderr):
    tree = avocat.find_tree_solution(match)
    if tree is None:
        # ... tell themwe dont know how, OR look on stackoverflow
        # OR just display stackoverflow answers
        pass

    actor.run(tree)

"""
