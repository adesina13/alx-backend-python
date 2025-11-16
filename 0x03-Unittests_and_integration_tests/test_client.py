#!/usr/bin/env python3
"""Unit and integration tests for client.GithubOrgClient."""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


# -----------------------------------------------------------
# TASK 4 — Test org()
# -----------------------------------------------------------
class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value."""
        mock_payload = {"payload": True}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, mock_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


    # -----------------------------------------------------------
    # TASK 5 — Test _public_repos_url (mock a property)
    # -----------------------------------------------------------
    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL."""
        mock_org_payload = {"repos_url": "http://example.com/repos"}

        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload

            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://example.com/repos")


    # -----------------------------------------------------------
    # TASK 6 — Test public_repos()
    # -----------------------------------------------------------
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns list of repo names."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]

        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock) as mock_url:

            mock_url.return_value = "http://example.com/repos"
            client = GithubOrgClient("test")

            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://example.com/repos")


    # -----------------------------------------------------------
    # TASK 7 — Test has_license()
    # -----------------------------------------------------------
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)



# -----------------------------------------------------------
# TASK 8 — Integration Tests
# -----------------------------------------------------------
@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Mock requests.get to return fixture payloads."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Mock JSON responses depending on the URL
        def side_effect(url):
            mock_response = MagicMock()
            if url.endswith("orgs/google"):
                mock_response.json.return_value = cls.org_payload
            elif url.endswith("repos"):
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for license filtering."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
