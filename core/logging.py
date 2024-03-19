#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import logging
import itertools
from typing import TypeAlias, TypeVar, Iterable
from logging import Logger
from collections import defaultdict

logger: Logger = logging.getLogger("pywelkin.core")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.CRITICAL)
