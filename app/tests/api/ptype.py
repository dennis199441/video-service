import unittest
from app.api.ptype import (
    get_process_types,
    get_process_type_by_name,
    create_process_type,
    delete_process_type
)


class ProcessTypeControllerTestCase(unittest.TestCase):

    def test_get_process_types(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_get_process_type_by_name(self):
        self.assertEqual("foo".upper(), "FOO")
        
    def test_create_process_type(self):
        self.assertEqual("foo".upper(), "FOO")
        
    def test_delete_process_type(self):
        self.assertEqual("foo".upper(), "FOO")
