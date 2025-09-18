#!/usr/bin/env python3
'''Generic utilities for github org client.'''

import unittest
from unittest.mock import Mock, patch, PropertyMock, call
from parameterized import parameterized, parameterized_class
from typing import Dict
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD

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

    @patch("client.get_json")
    def test_public_repos(self, get_json_mock: Mock):
        """Unit-test GithubOrgClient.public_repos."""

        # Fake payload returned by repos_payload
        fake_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]

        # Configure the mock to return a dummy value
        get_json_mock.return_value = fake_repos_payload

        # Patch GithubOrgClient._public_repos_url to return a fake URL
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/google/repos"
            )

            client = GithubOrgClient("google")

            # Call public_repos without license filter
            result = client.public_repos()
            expected_result = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_result)

            # Call public_repos with license filter
            result_with_license = client.public_repos(license="mit")
            expected_result_with_license = ["repo1"]
            self.assertEqual(result_with_license, expected_result_with_license)

            mock_public_repos_url.assert_called()
            get_json_mock.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )
            @parameterized.expand([
                ({"license": {"key": "my_license"}}, "my_license", True),
                ({"license": {"key": "other_license"}}, "my_license")
            ])
            def test_has_license(self, repo: Dict, license_key: str, expected: bool = False):
                '''Test for has_license static method.'''
                self.assertEqual(
                    GithubOrgClient.has_license(repo, license_key),
                    expected
                )
@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""
    login = "x"

    @classmethod
    def setUpClass(cls):
        """Set up class method to patch requests.get."""
        org_mock = Mock()
        org_mock.json.return_value = cls.org_payload  # type: ignore

        repos_mock = Mock()
        repos_mock.json.return_value = cls.repos_payload  # type: ignore

        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()

        # Configure the mock to return correct payloads based on URL
        def side_effect(url, *args, **kwargs):
            if url == f"https://api.github.com/orgs/{cls.login}":
                return org_mock
            if url == cls.org_payload["repos_url"]:
                return repos_mock
            raise ValueError(f"Unmocked URL: {url}")

        cls.get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns all expected repos."""
        client = GithubOrgClient(self.login)

        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.repos_payload, self.repos_payload)
        self.assertEqual(client.public_repos(), self.expected_repos)

        self.get.assert_has_calls([
            call(f"https://api.github.com/orgs/{self.login}"),
            call(self.org_payload["repos_url"])
        ])

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter 'apache-2.0'."""
        client = GithubOrgClient(self.login)

        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

        self.get.assert_has_calls([
            call(f"https://api.github.com/orgs/{self.login}"),
            call(self.org_payload["repos_url"])
        ])


    