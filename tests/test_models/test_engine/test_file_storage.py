#!/usr/bin/python3
"""Unittest for FileStorage"""

import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):
    """Tests the FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.model = BaseModel()
        self.storage.new(self.model)

    def tearDown(self):
        """Clean up file.json after tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_object(self):
        key = "{}.{}".format(self.model.__class__.__name__, self.model.id)
        self.assertIn(key, self.storage.all())

    def test_save_creates_file(self):
        self.storage.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        self.storage.save()
        self.storage._FileStorage__objects = {}  # Clear in-memory objects
        self.storage.reload()
        key = "{}.{}".format(self.model.__class__.__name__, self.model.id)
        self.assertIn(key, self.storage.all())


if __name__ == "__main__":
    unittest.main()
