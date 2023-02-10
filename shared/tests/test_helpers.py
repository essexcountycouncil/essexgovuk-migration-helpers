import unittest
from shared.helpers import FixedKeyDict


class TestFixedKeyDict(unittest.TestCase):
    def test_valid_blank(self):
        r = FixedKeyDict("foo", "bar")
        self.assertEqual(r["foo"], "")
        self.assertEqual(r["bar"], "")

    def test_valid_full(self):
        r = FixedKeyDict("foo", "bar")
        r["foo"] = 5
        self.assertEqual(r["foo"], 5)

    def test_invalid_set(self):
        r = FixedKeyDict("foo", "bar")
        with self.assertRaises(KeyError):
            r["baz"] = 2

    def test_invalid_get(self):
        r = FixedKeyDict("foo", "bar")
        with self.assertRaises(KeyError):
            r["baz"]


if __name__ == "__main__":
    unittest.main()
