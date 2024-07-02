#!/usr/bin/env python3
"""Client Module"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
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

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the correct value"""
        expected_repos_url = "https://api.github.com/orgs/google/repos"
        mock_org.return_value = {'repos_url': expected_repos_url}
        client = GithubOrgClient('google')
        self.assertEqual(client._public_repos_url, expected_repos_url)
        mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repositories"""
        repos_payload = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo3', 'license': None},
        ]
        mock_get_json.return_value = repos_payload
        expected_repos = ['repo1', 'repo2', 'repo3']

        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                'https://api.github.com/orgs/google/repos'
            )
            client = GithubOrgClient('google')
            self.assertEqual(client.public_repos(), expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self, repo, license_key, expected_has_license
    ):
        """Test GithubOrgClient.has_license method"""
        client = GithubOrgClient('google')
        self.assertEqual(
            client.has_license(repo, license_key), expected_has_license
        )
