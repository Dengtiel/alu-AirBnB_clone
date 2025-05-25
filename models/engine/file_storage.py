import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class."""

    def setUp(self):
        """Set up test environment."""
        self.storage = FileStorage()
        # Clear __objects dict before each test
        FileStorage._FileStorage__objects = {}
        # Remove file.json if exists to ensure a clean slate
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def tearDown(self):
        """Clean up test artifacts."""
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        """all() should return the internal __objects dict."""
        self.assertIsInstance(self.storage.all(), dict)
        self.assertEqual(len(self.storage.all()), 0)

    def test_new_and_all(self):
        """new() adds an object, and all() returns it."""
        bm = BaseModel()
        self.storage.new(bm)
        all_objs = self.storage.all()
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, all_objs)
        self.assertEqual(all_objs[key], bm)

    def test_save_creates_file(self):
        """save() should serialize objects to file.json."""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))

        with open(FileStorage._FileStorage__file_path, "r") as f:
            data = json.load(f)
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, data)
        self.assertEqual(data[key]["id"], bm.id)

    def test_reload_loads_objects(self):
        """reload() should deserialize objects from file.json."""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()

        # Clear __objects to simulate fresh start
        FileStorage._FileStorage__objects = {}
        self.storage.reload()

        all_objs = self.storage.all()
        key = f"BaseModel.{bm.id}"
        self.assertIn(key, all_objs)
        self.assertIsInstance(all_objs[key], BaseModel)
        self.assertEqual(all_objs[key].id, bm.id)

    def test_delete_removes_object(self):
        """delete() should remove an object from __objects."""
        bm = BaseModel()
        self.storage.new(bm)
        self.assertIn(f"BaseModel.{bm.id}", self.storage.all())

        self.storage.delete(bm)
        self.assertNotIn(f"BaseModel.{bm.id}", self.storage.all())

    def test_all_with_class_filter(self):
        """all(cls) should return only objects of that class."""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.storage.new(bm1)
        self.storage.new(bm2)
        filtered = self.storage.all(BaseModel)
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(isinstance(obj, BaseModel) for obj in filtered.values()))

        class Dummy:
            __name__ = "Dummy"

        filtered_empty = self.storage.all(Dummy)
        self.assertEqual(filtered_empty, {})

if __name__ == "__main__":
    unittest.main()
