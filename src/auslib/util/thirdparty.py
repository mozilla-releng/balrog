import site
import sys
from os import path


def extendsyspath():
    # we want to add the current directory and the vendor/lib/python directory
    # at the beginning of sys.path

    root_dir = path.abspath(path.join(path.dirname(path.abspath(__file__)), "..", ".."))
    prev_sys_path = list(sys.path)  # make a copy of the list

    site.addsitedir(path.join(root_dir, "vendor/lib/python"))

    # Now, move the new items to the front of sys.path. (via virtualenv)
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path
