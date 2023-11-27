import sys
import json
from jsonschema import validate
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api/') 

from generated_data import external_data  

# Load the schema from external_schema.json
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

def validate_external_list(external_data):
    if validate_external(external_data):
        return [external_data]
    else:
        return []

@app.route('/api/external', methods=['GET'])
def json_entry():
    validated_external = validate_external_list(external_data)
    return jsonify(validated_external)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
