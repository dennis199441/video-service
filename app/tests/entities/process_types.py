import unittest
from app.entities.process_types import ProcessType


class ProcessTypeTestCase(unittest.TestCase):

    def test_process_type(self):
        name = "testing"
        obj = ProcessType(name)
        self.assertEqual(obj.name, name)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    def test_missing_args(self):
        self.assertRaises(TypeError, ProcessType)
