""" avocat/__main__.py - commandline interface to avocat


@author: Cade Brown <cade@cade.utk>
@author: Gregory Croisdale <>
"""

import avocat
from avocat import act

# create actor to execute actions through
actor = act.Actor(auto=True)

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

tree = act.Print(
    act.Const(data="hey, you said: "),
    act.Choice(Q="what do you want to enter?", data={ 'abc': 'abc', 'foo': 'foo', 'v123': '1.2.3', 'v456': '4.5.6' }),
)


# print out the tree
print(tree)

# now, run the action item
res = actor.run(tree)




####


"""


actor, proc_shell = avocat.shell(auto=True)

for match in avocat.search(proc_shell.stderr):
    tree = avocat.find_tree_solution(match)
    if tree is None:
        # ... tell themwe dont know how, OR look on stackoverflow
        # OR just display stackoverflow answers
        pass

    actor.run(tree)

"""
