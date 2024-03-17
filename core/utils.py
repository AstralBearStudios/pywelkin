#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import logging
import itertools
from typing import TypeAlias, TypeVar, Iterable
from logging import Logger
from collections import defaultdict

logger: Logger = logging.getLogger("pywelkin.core")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.CRITICAL)


class NestedDict(dict):
    """Nested dictionary of arbitrary depth.
    Each leaf is an empty :class NestedDict:.
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
