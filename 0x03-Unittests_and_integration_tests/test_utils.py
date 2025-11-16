#!/usr/bin/env python3
"""Unit tests for utils functions."""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(str(err.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected payload."""
        mock_response = mock_get.return_value
        mock_response.json.return_value = test_payload

        from utils import get_json
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)

class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""
        from utils import memoize

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            first = obj.a_property()
            second = obj.a_property()

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()

if __name__ == "__main__":
    unittest.main()
