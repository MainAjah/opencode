import os
import tempfile
import unittest

from app import create_app
from app.database import init_db


class ApiTestCase(unittest.TestCase):
    """Base test case with an isolated database per test."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE": os.path.join(self._tmp.name, "test.db"),
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            init_db()

    def tearDown(self):
        self._tmp.cleanup()

    def create_item(self, name="Multimeter", total_stock=10):
        response = self.client.post(
            "/items",
            json={"name": name, "total_stock": total_stock},
        )
        self.assertEqual(response.status_code, 201, response.get_json())
        return response.get_json()

    def get_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        return response.get_json()
