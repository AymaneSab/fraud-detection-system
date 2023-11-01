# api/external_api/main.py

from flask import Flask, jsonify
from generated_data import external_data

app = Flask(__name__)

@app.route('/api/externalData', methods=['GET'])
def get_external_data():
    return jsonify(external_data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
