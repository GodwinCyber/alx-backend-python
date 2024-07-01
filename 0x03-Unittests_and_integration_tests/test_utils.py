#!/usr/bin/env python3
"""Unitest Module One"""


import unittest
from parameterized import parameterized
from utils import (access_nested_map, get_json, memoize)
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
        Create a TestAccessNestedMap class that inherits from unittest.
        TestCase. Implement the TestAccessNestedMap.test_access_nested_map
        method to test that the method returns what it is supposed to.
        Decorate the method with @parameterized.expand to test the
        function for following inputs:
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map exception aised KeyError"""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
            self.assertEqual(str(context.exception), str(path[-1]))


class TestGetJson(unittest.TestCase):
    """
        Define the TestGetJson(unittest.TestCase) class and implement the
        TestGetJson.test_get_json method to test that utils.get_json returns
        the expected result. We don’t want to make any actual external
        HTTP calls. Use unittest.mock.patch to patch requests.get. Make sure
        it returns a Mock object with a json method that returns test_payload
        which you parametrize alongside the test_url that you will pass to
        get_json with the following inputs:
        test_url="http://example.com", test_payload={"payload": True}
        test_url="http://holberton.io", test_payload={"payload": False}
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json"""
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """
        mplement the TestMemoize(unittest.TestCase) class with a
        test_memoize method. Inside test_memoize, define following class
        class TestClass:
            def a_method(self):
        return 42
        @memoize
            def a_property(self):
        return self.a_method()
    """
    class TestCase:

        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    def test_memoize(self):
        """Test memoize"""
        test_case = self.TestCase()
        with patch.object(
            test_case, 'a_method', return_value=42
        ) as mock_method:
            result1 = test_case.a_property
            result2 = test_case.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
