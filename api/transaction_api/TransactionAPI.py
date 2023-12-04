import sys
import time
import json
from jsonschema import validate
from flask import Flask, jsonify, stream_with_context

sys.path.append('/home/hdoop/fraud-detection-system/api') 

from generated_data import transactions  

# Load the schema from customer_schema.json
with open('/home/hdoop/fraud-detection-system/api/transaction_api/transaction_schema.json') as schema_file:
    transaction_schema = json.load(schema_file)

app = Flask(__name__)

def validate_transaction(transaction):
    try:
        validate(instance=transaction, schema=transaction_schema)
        return True
    except Exception as e:
        print(f"Schema Validation Error: {e}")
        return False

def generate_transactions():
    for transaction in transactions:
        if validate_transaction(transaction):
            yield json.dumps(transaction) + '\n'
            time.sleep(1)  # Wait for two seconds before sending the next transaction

@app.route('/api/transactions', methods=['GET'])
def json_entry():
    return app.response_class(stream_with_context(generate_transactions()), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5004)
