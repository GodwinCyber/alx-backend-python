#!/usr/bin/env python3
"""Module 8"""


def make_multiplier(multiplier: float) -> float:
    """Make a function that multiplies by multiplier"""
    def multiplier_function(x: float) -> float:
        """Multiply by multiplier"""
        return x * multiplier
    return multiplier_function
