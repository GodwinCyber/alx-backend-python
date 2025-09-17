#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from parameterized import parameterized
from typing import Dict, Tuple, Any
from uitls import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    '''Test class for access nested map function.'''
    @parameterized.expand([
        ({"a": 1}, ("a,"), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Dict, path: Tuple, expected: Any):
        '''Test access_nested_map function.'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == "__main__":
    unittest.main()
