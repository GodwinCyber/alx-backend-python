#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Dict, Tuple, Any
from utils import access_nested_map, memoize
import utils

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

class TestGetJson(unittest.TestCase):
    '''Test class for get_json function.'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str, test_payload: Dict, mock_get: Mock):
        '''Tests that get_json returns the expected result and calls requests.get once'''
        # configure the mock to return a response with the test payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # call the function under test
        results = utils.get_json(test_url)

        # assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(results, test_payload)


class TestMemoize(unittest.TestCase):
    '''Test cclass for memoize '''
    def test_memoize(self):
        '''Test that memoize caches results and calls underlying method once.'''
        class TestClass:
            '''Class for testing memoize'''
            def a_method(self):
                '''Method'''
                return 42

            @memoize
            def a_property(self):
                '''Property'''
                return self.a_method()
        with patch.object(TestClass, 'a_method', return_value=42) as mock_a_method:
            test_class = TestClass()
            result1 = test_class.a_property
            result2 = test_class.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()


