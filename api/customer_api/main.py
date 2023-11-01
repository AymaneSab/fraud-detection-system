import sys
import time
import json
from jsonschema import validate
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/') 

from generated_data import customers  

# Load the schema from customer_schema.json
with open('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/customer_api/customer_schema.json') as schema_file:
    customer_schema = json.load(schema_file)

app = Flask(__name__)

def validate_customer(customer):
    try:
        validate(instance=customer, schema=customer_schema)
        return True
    except Exception as e:
        print(f"Schema Validation Error: {e}")
        return False

@app.route('/api/customerData', methods=['GET'])
def json_entry():
    valid_customers = [customer for customer in customers if validate_customer(customer)]
    return jsonify(valid_customers)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
