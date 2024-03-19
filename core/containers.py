#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import itertools
from typing import Generic, Iterable, TypeVar, Optional


class NestedDict(dict):
    """Nested dictionary of arbitrary depth.
    Each leaf is an empty :class NestedDict:.

    Any method with a parameter :param keys:
    takes in an iterable. Takes in
    non-iterable as a singleton.
    """

    def __init__(self, *args, **kwargs):
        super(NestedDict, self).__init__(*args, **kwargs)

    def __getitem__(self, keys: Iterable):
        # TODO: remove this check; it is a bit messy
        # We only want to do this for single item objects
        if not isinstance(keys, Iterable):
            keys = (keys,)
        result = self
        for key in keys:
            result = result.setdefault(key, {})
        return result

    def __setitem__(self, keys, value):
        if not isinstance(keys, Iterable):
            keys = (keys,)
        head = self
        iterator = itertools.chain(keys, value)
        for node in iterator:
            head = head.setdefault(node, {})


RootType = TypeVar("RootType")
MappedValueType = TypeVar("MappedValueType")


class RootedMapping:
    """Mapping with a special, external element :param root:."""

    root: RootType

    map: dict[int, MappedValueType] = {}

    def __init__(
        self, root: Optional[RootType], map: Optional[dict[int, MappedValueType]]
    ):
        self.root = root
        self.map = map

    def __getitem(self, index: int):
        if index == 0:
            return self.root
        else:
            return self.map.setdefault(index, None)


Node = TypeVar("Node")
