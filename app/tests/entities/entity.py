import unittest
from app.entities.entity import Entity


class EntityTestCase(unittest.TestCase):

    def test_entity(self):
        obj = Entity()
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)
