import sys
import time
import json
from jsonschema import validate
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/') 

from generated_data import transactions  

# Load the schema from customer_schema.json
with open('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/transaction_api/transaction_schema.json') as schema_file:
    transaction_schema = json.load(schema_file)

app = Flask(__name__)

def validate_transaction(transaction):
    try:
        validate(instance=transaction, schema=transaction_schema)
        return True
    except Exception as e:
        print(f"Schema Validation Error: {e}")
        return False

@app.route('/api/transactionData', methods=['GET'])
def json_entry():
    valid_transaction = [transaction for transaction in transactions if validate_transaction(transaction)]
    return jsonify(validate_transaction)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
