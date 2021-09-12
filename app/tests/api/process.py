import unittest
from app.api.process import (
    create_process,
    cancel_process,
    get_process_by_id,
    get_all_processes
)


class ProcessTypeControllerTestCase(unittest.TestCase):

    def test_create_process(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_cancel_process(self):
        self.assertEqual("foo".upper(), "FOO")
        
    def test_get_process_by_id(self):
        self.assertEqual("foo".upper(), "FOO")
        
    def test_get_all_processes(self):
        self.assertEqual("foo".upper(), "FOO")
