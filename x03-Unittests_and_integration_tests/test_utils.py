#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Any
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    '''Test class for access nested map function.'''
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple, expected: Any):
        '''Test access_nested_map function.'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    '''Test access_nested_map function with KeyError.'''
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict, path: Tuple):
        '''Test access_nested_map function with KeyError.'''
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
