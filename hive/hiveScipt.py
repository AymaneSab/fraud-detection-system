from pyhive import hive
import json

# Connect to Hive
conn = hive.Connection(host='your_hive_host', port=10000, username='your_username')

# Function to execute Hive queries
def execute_hive_query(query):
    with conn.cursor() as cursor:
        cursor.execute(query)

# Function to create Hive table based on JSON schema
def create_hive_table(table_name, json_schema):
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
    create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}) STORED AS ORC;"

    # Execute the query
    execute_hive_query(create_table_query)
    print(f"Table {table_name} created successfully.")

# Read schemas from JSON files
with open('customers_schema.json', 'r') as file:
    customers_schema = json.load(file)

with open('externals_schema.json', 'r') as file:
    externals_schema = json.load(file)

with open('transactions_schema.json', 'r') as file:
    transactions_schema = json.load(file)

# Create Hive tables for Customers, Externals, and Transactions
create_hive_table("customers", customers_schema)
create_hive_table("externals", externals_schema)
create_hive_table("transactions", transactions_schema)

# Close the Hive connection
conn.close()
