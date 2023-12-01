from pyhive import hive
import json
import logging
import os
from datetime import datetime


def setup_logging(log_directory, logger_name):
    os.makedirs(log_directory, exist_ok=True)

    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(log_directory, log_filename)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler = logging.FileHandler(log_filepath)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

# Function to connect To Hive 
def connect_to_hive(host, port, conn_logger):
    try:
        conn = hive.Connection(host=host, port=port)
        conn_logger.info("Connection successful to Hive")
        return conn
    except Exception as e:
        conn_logger.error(f"Connection failed to Hive\nError: {str(e)}")
        raise  # Re-raise the exception to halt the script

def execute_hive_query(query, conn, query_logger):
    try:
        with conn.cursor() as cursor:
            if cursor.execute(query):
                query_logger.info("Query successful to Hive")
            else:
                query_logger.error("Failed query to Hive")
                raise Exception(f"Hive query failed: {query}")
    except Exception as e:
        query_logger.error(f"Exception detected in Hive query: {str(e)}")
        raise  # Re-raise the exception to halt the script

# Function to create a Hive database
def create_hive_database(database_name, conn, database_conn_logger):
    try:
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        database_conn_logger.info(create_database_query)
        execute_hive_query(create_database_query, conn, database_conn_logger)
        database_conn_logger.info(f"Database {database_name} created successfully.")
    except Exception as e:
        database_conn_logger.error(f"Failed to create Hive database\nError: {str(e)}")
        raise  # Re-raise the exception to halt the script

# Function to create Hive table based on JSON schema
def create_hive_table(database_name, table_name, json_schema, conn, query_logger):
    # Generate Hive data types based on JSON schema
    hive_data_types = {
        "string": "STRING",
        "integer": "INT",
        "number": "DOUBLE",
        "object": "STRUCT",
        "array": "ARRAY",
    }

    # Function to recursively generate Hive columns from JSON schema
    def generate_columns(schema, prefix=''):
        columns = []
        for key, value in schema.items():
            if isinstance(value, dict):
                columns.extend(generate_columns(value, f'{prefix}{key}.'))
            else:
                columns.append(f'{prefix}{key} {hive_data_types.get(value, "STRING")}')
        return columns

    # Generate Hive columns
    columns = generate_columns(json_schema)

    # Create Hive table query
    create_table_query = f"CREATE TABLE IF NOT EXISTS {database_name}.{table_name} ({', '.join(columns)}) STORED AS ORC;"

    # Execute the query
    execute_hive_query(create_table_query, conn, query_logger)
    query_logger.info(f"Table {database_name}.{table_name} created successfully.")

# Read schemas from JSON files
with open('/home/hdoop/fraud-detection-system/hive/schemas/customer_schema.json', 'r') as file:
    customers_schema = json.load(file)

with open('/home/hdoop/fraud-detection-system/hive/schemas/external_schema.json', 'r') as file:
    externals_schema = json.load(file)

with open('/home/hdoop/fraud-detection-system/hive/schemas/transaction_schema.json', 'r') as file:
    transactions_schema = json.load(file)

conn_logger = setup_logging("Log/Hive/Conn_Log_Files", "Hive_Connection")
query_logger = setup_logging("Log/Hive/Query_Log_Files", "Hive_Query")
database_conn_logger = setup_logging("Log/Hive/Database_Log_Files", "Hive_Database_Creation")

hive_database_name = "transactions"
host = "localhost"
port = 10001

try:
    conn = connect_to_hive(host, port, conn_logger)

    # Create the Hive database
    create_hive_database(hive_database_name, conn, database_conn_logger)

    # Create Hive tables for Customers, Externals, and Transactions
    create_hive_table(hive_database_name, "customers", customers_schema, conn, query_logger)
    create_hive_table(hive_database_name, "externals", externals_schema, conn, query_logger)
    create_hive_table(hive_database_name, "transactions", transactions_schema, conn, query_logger)

except Exception as e:
    print(f"An error occurred: {str(e)}")
