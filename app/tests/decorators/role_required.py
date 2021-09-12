import unittest
from app.decorators.role_required import role_required
from flask_jwt_extended.exceptions import NoAuthorizationError
from unittest.mock import MagicMock, patch

class RoleRequiredTestCase(unittest.TestCase):
          
    def test_empty_roles(self):
        @role_required([])
        def test():
            return 1
        self.assertRaises(NoAuthorizationError, test)
