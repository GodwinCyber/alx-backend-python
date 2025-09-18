#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Dict, Tuple, Any
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    '''Test class for GitHubOrgClient.'''
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch('client.get_json')
    def test_org(self, org_name:str, expected_payload: Dict, mock_get_json:Mock):
        '''Test for org property.'''

        # Configure the mock to return a dummy value
        mock_get_json.return_value = expected_payload
        
        # Instantiate the client
        client = GithubOrgClient(org_name)
        
        # Call the method under test
        result = client.org
        
        # Assert the expected URL was called
        expected_url = (f"https://api.github.com/orgs/{org_name}")
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, expected_payload)
        




