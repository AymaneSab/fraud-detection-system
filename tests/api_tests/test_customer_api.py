import unittest
from flask import json
import sys 

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/customer_api/') 

from CustomerAPI import app, validate_customer  # Assuming validate_customer is available in your app

class TestCustomerAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_customers(self):
        response = self.app.get('/api/customers')
        self.assertEqual(response.status_code, 200)

        for line in response.data.decode('utf-8').splitlines():
            customer_data = json.loads(line)
            self.assertTrue(validate_customer(customer_data))

if __name__ == '__main__':
    unittest.main()
