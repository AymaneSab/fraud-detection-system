# api/customer_api/main.py

from flask import Flask, jsonify
from generated_data import customers

app = Flask(__name__)

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
