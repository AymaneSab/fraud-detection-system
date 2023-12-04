import unittest
from unittest.mock import patch
from your_script_name import app, validate_external_list

class TestExternalAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_json_entry_valid(self):
        # Mocking external_data to be a valid entry
        with patch('your_script_name.external_data', {"valid_key": "valid_value"}):
            response = self.app.get('/api/external')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [{"valid_key": "valid_value"}])

    def test_json_entry_invalid(self):
        # Mocking external_data to be an invalid entry
        with patch('your_script_name.external_data', {"invalid_key": "invalid_value"}):
            response = self.app.get('/api/external')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [])

    def test_schema_validation_error(self):
        # Mocking external_data to raise a schema validation error
        with patch('your_script_name.external_data', {"invalid_key": "invalid_value"}), \
             patch('your_script_name.validate_external_list', side_effect=Exception("Schema Validation Error")):
            response = self.app.get('/api/external')
            data = response.get_json()

            self.assertEqual(response.status_code, 500)
            self.assertIn("Schema Validation Error", data['message'])

if __name__ == '__main__':
    unittest.main()
