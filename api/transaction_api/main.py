# api/transaction_api/main.py

from flask import Flask, jsonify
from generated_data import transactions

app = Flask(__name__)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

if __name__ == '__main__':
    app.run(debug=True)
