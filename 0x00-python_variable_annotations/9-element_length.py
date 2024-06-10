#!/usr/bin/env python3
"""Module 9"""

from typing import Iterable, List, Tuple, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """return an Iterable object"""
    return [(i, len(i)) for i in lst]
