#!/usr/bin/env python3
"""module 6 sum-mixed type annotations"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """return sum of float"""
    return sum(mxd_lst)
