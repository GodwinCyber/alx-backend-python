#!/usr/bin/env python3
"""moude 100"""

from typing import Sequence, Any, Union, Optional


# The types of the elements of the input are not know
def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Duck type annotation"""
    if lst:
        return lst[0]
    else:
        return None
