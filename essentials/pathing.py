# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


import __main__
from distutils import dir_util

# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


def path(*objects):
    newPath = ((__main__.__file__).split("\\"))[:-1]
    for i in objects:
        newPath.append(i)
    return '\\'.join(str(y) for y in newPath)

# ///////////////////////////////////////////////////////// #
#
# ////////////////////////
#
#
# ///////////////////////////////////////////////////////// #


def mkdir(*objects):
    dir_util.mkpath(path(*objects))
