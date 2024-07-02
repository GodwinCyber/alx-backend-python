#!/usr/bin/env python3
"""Client Module"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
    @patch('client.get_json')
    def test_org(self, input, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_class = GithubOrgClient(input)
        test_class.org()
        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{input}'
        )

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
            memoize turns methods into properties. Read up on how to
            mock a property (see resource). Implement the test_public_repos_url
            method to unit-test GithubOrgClient._public_repos_url.
            Use patch as a context manager to patch GithubOrgClient.org
            and make it return a known payload. Test that the result of
            _public_repos_url is the expected one based on the mocked payload.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "World"}
            mock_org.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
            Implement TestGithubOrgClient.test_public_repos to unit-test
            GithubOrgClient.public_repos. Use @patch as a decorator to
            mock get_json and make it return a payload of your choice.
            Use patch as a context manager to mock
            GithubOrgClient._public_repos_url and return a value of
            your choice. Test that the list of repos is what you expect
            from the chosen payload. Test that the mocked property and the
            mocked get_json was called once.
        """
        json_payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "hello/world"
            test_class = GithubOrgClient('test')
            result = test_class.public_repos()

            check = [i["name"] for i in json_payload]
            self.assertEqual(result, check)

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with('hello/world')

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
@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
        Create the TestIntegrationGithubOrgClient(unittest.TestCase)
        class and implement the setUpClass and tearDownClass which are
        part of the unittest.TestCase API. Use @parameterized_class to
        decorate the class and parameterize it with fixtures found in
        fixtures.py. The file contains the following fixtures:
        org_payload, repos_payload, expected_repos, apache2_repos
        The setupClass should mock requests.get to return example
        payloads found in the fixtures. Use patch to start a
        patcher named get_patcher, and use side_effect to make sure
        the mock of requests.get(url).json() returns the correct
        fixtures for the various values of url that you anticipate
        to receive. Implement the tearDownClass class
        method to stop the patcher.
    """
    @classmethod
    def setUpClass(cls):
        """A class method called before tests in an individual class are run"""
        config = {'return_value.json.side_effect':
                  [cls.org_payload, cls.repos_payload]}
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """
            Implement the test_public_repos method to test
            GithubOrgClient.public_repos. Make sure that the method
            returns the expected results based on the fixtures.
            Implement test_public_repos_with_license to test the
            public_repos with the argument license="apache-2.0" and
            make sure the result matches the expected value from the fixtures.
        """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos("apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
