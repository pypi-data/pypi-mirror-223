from typing import Iterable
from nxtomo.nxobject.nxobject import NXobject


def concatenate(nx_objects: Iterable, **kwargs):
    if len(nx_objects) == 0:
        return None
    else:
        if not isinstance(nx_objects[0], NXobject):
            raise TypeError("nx_objects are expected to be instances of NXobject")
        return type(nx_objects[0]).concatenate(nx_objects=nx_objects, **kwargs)
