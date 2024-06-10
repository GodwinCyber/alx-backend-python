#!/usr/bin/env python3
"""module 101"""

from typing import TypeVar, Union, Any, Mapping

T = TypeVar('T')


def safely_get_value(
    dct: Mapping,
    key: Any,
    default: Union[T, None] = None
) -> Union[T, Any]:
    """Retrieve value from a dictionary with default fallback
    Args:
        dct (Mapping): The dictionary to retrieve value from:
        key (Any): The key to look up in the dictionary.
        default (Union[T, None]): The default value to return
        if key is not found. Defaults to None
    Return:
        Union[T, None]: The value from dictionary if key exist,
        otherwise default value
    """
    if key in dct:
        return dct[key]
    else:
        return default
