import unittest
from app.entities.process import Process


class ProcessLogTestCase(unittest.TestCase):

    def test_process_log(self):
        user_id, type_id = 1, 1
        obj = Process(user_id, type_id)
        self.assertEqual(obj.user_id, user_id)
        self.assertEqual(obj.type_id, type_id)
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    def test_missing_args(self):
        self.assertRaises(TypeError, Process)
