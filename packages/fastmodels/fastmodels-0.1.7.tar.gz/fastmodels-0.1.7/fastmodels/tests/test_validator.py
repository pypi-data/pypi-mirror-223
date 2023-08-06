import unittest
from fastmodels.utils.validator import validate_jsonl

class TestValidator(unittest.TestCase):
    def test_validate_json_valid(self):
        file = 'valid.jsonl'
        self.assertTrue(validate_jsonl(file))

    def test_validate_json_invalid(self):
        file = 'invalid.jsonl'
        self.assertFalse(validate_jsonl(file))

    def test_validate_json_not_exists(self):
        try:
            validate_jsonl("not_json")
        except FileNotFoundError:
            return
        # fail the test
        self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
