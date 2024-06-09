#!/usr/bin/env python3
"""Module 8"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Make a function that multiplies by multiplier"""
    def multiplier_function(value: float) -> float:
        """Multiply by multiplier"""
        return value * multiplier
    return multiplier_function
