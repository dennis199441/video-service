import unittest
from app.services.demo_service import foo, bar

class TestServiceTestCase(unittest.TestCase):

    def test_foo(self):
        self.assertEqual(foo(), "foo")

    def test_bar(self):
        self.assertEqual(bar(), "bar")
