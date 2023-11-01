# api/customer_api/main.py

import os 
import sys 
from flask import Flask, jsonify

sys.path.append('/Users/sabri/Desktop/Study /Youcode/Github/Sprint_4/fraud-detection-system/api') 

from generated_data import customers




app = Flask(__name__)

@app.route('/api/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
