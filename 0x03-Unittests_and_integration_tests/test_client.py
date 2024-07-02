#!/usr/bin/env python3
"""Client Module"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    In a new test_client.py file, declare the
    TestGithubOrgClient(unittest.TestCase) class and
    implement the test_org method. This method should
    test that GithubOrgClient.org returns the correct
    value. Use @patch as a decorator to make sure get_json is
    called once with the expected argument but make sure
    it is not executed. Use @parameterized.expand as a
    decorator to parametrize the test with a couple of org
    examples to pass to GithubOrgClient, in this order:
        google
        abc
    Of course, no external HTTP calls should be made.
    """

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json', return_value={'login': 'mocked_org'})
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {'login': 'mocked_org'})
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}'
        )
