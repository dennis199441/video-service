import unittest
import app
import os
from flask import Flask
from app.api.process import process
from app.api.ptype import ptype


class CreateAppTestCase(unittest.TestCase):

    def test_create_app(self):
        server = app.create_app()
        self.assertIsInstance(server, Flask)
        self.assertFalse(server.config["JWT_ACCESS_TOKEN_EXPIRES"])
        self.assertFalse(server.config["JWT_REFRESH_TOKEN_EXPIRES"])
        self.assertEqual(server.config["JWT_SECRET_KEY"], os.getenv("JWT_SECRET_KEY"))
        self.assertEqual(server.config["DB_HOST"], os.getenv("VIDEO_SERVICE_SQL_INSTANCE"))
        self.assertEqual(server.config["DB_NAME"], os.getenv("VIDEO_SERVICE_DB_NAME"))
        self.assertEqual(server.config["DB_USER"], os.getenv("VIDEO_SERVICE_DB_USER"))
        self.assertEqual(server.config["DB_PASSWORD"], os.getenv("VIDEO_SERVICE_DB_PASSWORD"))
        self.assertEqual(server.config["PORT"], os.getenv("PORT"))
        self.assertEqual(server.blueprints["process"], process)
        self.assertEqual(server.blueprints["ptype"], ptype)
