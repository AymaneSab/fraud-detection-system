import sys
import time
import json
from jsonschema import validate
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/') 

from generated_data import external_data  

# Load the schema from customer_schema.json
with open('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/external_api/external_schema.json') as schema_file:
    external_schema = json.load(schema_file)

app = Flask(__name__)

def validate_external(external):
    try:
        validate(instance=external, schema=external_schema)
        return True
    except Exception as e:
        print(f"Schema Validation Error: {e}")
        return False

@app.route('/api/externalData', methods=['GET'])
def json_entry():
    valid_external = [external for external in external_data if validate_external(external)]
    return jsonify(valid_external)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
