#!/usr/bin/env python3
"""Module 7"""

from typing import List, Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Converts a key-value pair to a tuple"""
    return (k, float(v**2))
