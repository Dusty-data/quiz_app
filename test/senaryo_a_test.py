import unittest
from main import load_json_file, save_json_file

class TestQuizApp(unittest.TestCase):
    def test_load_json(self):
        data = load_json_file("questions/questions_section1.json")
        self.assertTrue(len(data) > 0)

    def test_save_json(self):
        test_data = {"test": "data"}
        save_json_file("test.json", test_data)
        data = load_json_file("test.json")
        self.assertEqual(data, test_data)

if __name__ == "__main__":
    unittest.main()
