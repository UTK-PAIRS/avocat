""" avocat/__main__.py - commandline interface to avocat


@author: Cade Brown <cade@cade.utk>
@author: Gregory Croisdale <>
"""

import avocat
from avocat import act

# create actor to execute actions through
actor = act.Actor()

# create action item
tree = act.Print(
    act.Const(data="hey, you said: "),
    act.Choice(Q="what do you want to enter?", choices=["abc", "xyz", "foo", "bar", 123, 456]),
)


# print out the tree
print(tree)

# now, run the action item
res = actor.run(tree)


