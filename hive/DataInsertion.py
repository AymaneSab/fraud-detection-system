from pyhive import hive
from flask import Flask, jsonify, stream_with_context

app = Flask(__name__)

# Connection parameters for Hive
hive_host = 'your_hive_server_host'
hive_port = 10000
hive_username = 'your_hive_username'
hive_password = 'your_hive_password'

# Create a Hive connection
conn = hive.connect(host=hive_host, port=hive_port, username=hive_username, password=hive_password, auth='CUSTOM')

# Function to insert data into the customer table
def insert_customer_data():
    cursor = conn.cursor()
    
    for customer in customers:
        if validate_customer(customer):
            # Customize the query based on your Hive table structure
            query = f"INSERT INTO TABLE your_customer_table_name VALUES ('{customer['customer_id']}', '{customer['demographics']['location']}', {customer['demographics']['age']})"
            cursor.execute(query)

    cursor.close()

# Function to insert external data into the Hive table
def insert_external_data():
    cursor = conn.cursor()

    for external in external_data:
        if validate_external(external):
            # Customize the query based on your Hive table structure
            query = f"INSERT INTO TABLE your_external_table_name VALUES ('{external['blacklist_info'][0]}', {external['credit_scores']['your_credit_score_column']}, {external['fraud_reports']['your_fraud_reports_column']})"
            cursor.execute(query)

    cursor.close()

# Function to insert transactions data into the Hive table
def insert_transactions_data():
    cursor = conn.cursor()

    for transaction in transactions:
        if validate_transaction(transaction):
            # Customize the query based on your Hive table structure
            query = f"INSERT INTO TABLE your_transaction_table_name VALUES ('{transaction['transaction_id']}', '{transaction['date_time']}', {transaction['amount']}, '{transaction['currency']}', '{transaction['merchant_details']}', '{transaction['customer_id']}', '{transaction['transaction_type']}', '{transaction['location']}')"
            cursor.execute(query)

    cursor.close()

if __name__ == '__main__':
    # Uncomment and run the appropriate function based on your needs
    # insert_customer_data()
    # insert_external_data()
    # insert_transactions_data()
    app.run(debug=True, port=5005)
