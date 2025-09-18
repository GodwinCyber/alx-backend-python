#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from unittest.mock import Mock, patch, PropertyMock
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

    def test_public_repos(self):
        '''Implement the test_public_repos_url method to unit-test GithubOrgClient._public_repos_url.'''
  
        # Fake payload returned by org
        fake_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch GithubOrgClient.org so it behave like a property returning fake_payload
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = fake_payload
            
            client = GithubOrgClient('google')
            
            result = client._public_repos_url

            self.assertEqual(result, "https://api.github.com/orgs/google/repos")
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json:Mock):
        '''Test for public_repos method'''
        # Fake payload returned by repos_payload
        fake_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        
        # Configure the mock to return a dummy value
        mock_get_json.return_value = fake_repos_payload

        # Patch GithubOrgClient._public_repos_url to return a fake URL
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient('google')

            # Call public_repos without license filter
            result = client.public_repos()
            expected_result = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_result)

            # Call public_repos with license filter
            result_with_license = client.public_repos(license="mit")
            expected_result_with_license = ["repo1"]
            self.assertEqual(result_with_license, expected_result_with_license)

            mock_public_repos_url.assert_called()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")


