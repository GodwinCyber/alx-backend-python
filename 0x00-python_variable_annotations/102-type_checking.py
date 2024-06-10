#!/usr/bin/env python3
"""Module 102"""

from typing import List


def zoom_array(lst: List[int], factor: int = 2) -> List[int]:
    """corrected"""
    zoomed_in: List[int] = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in


# return [item for item in lst for _ in range(factor)]
array: List[int] = [12, 72, 91]

zoom_2x: List[int] = zoom_array(array)

zoom_3x: List[int] = zoom_array(array, 3)
