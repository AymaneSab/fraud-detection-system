import os
from datetime import datetime
import logging
import requests
import json
import threading
from pyhive import hive
from flask import Flask

app = Flask(__name__)

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

def select_Database(database , logger):
    cursor = conn.cursor()
    try:
        # Customize the query based on your Hive table structure
        query = f"USE {database}"
        cursor.execute(query)

        logger.info("Database Connected Successfully")

    except Exception as e:
        logger.error(f"Error Connecting To Database: {e}")

    finally:
        cursor.close()

def setup_Customers_logging():
    return setup_logging("Log/API_Customers_LogFiles", "customers_logger")

def setup_Transactions_logging():
    return setup_logging("Log/API_Transactions_LogFiles", "transactions_logger")

def setup_Externals_logging():
    return setup_logging("Log/API_Externals_LogFiles", "externals_logger")

def setup_Hive_logging():
    return setup_logging("Log/API_Hive_LogFiles", "Dataase_connection")

def is_merchant_blacklisted(merchant_details, logger):
    try:
        # HiveQL Query to check if merchant_details is in the blacklist_info of externals table
        query = f"""
            SELECT COUNT(*)
            FROM externals
            WHERE array_contains(blacklist_info, '{merchant_details}')
        """
        
        # Execute the HiveQL query using your preferred method (e.g., pyhive, pandasql)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()

        # If result is greater than 0, merchant is blacklisted
        return result > 0

    except Exception as e:
        logger.error(f"Error checking merchant blacklist: {e}")
        return False

def is_transaction_amount_below_credit_score(customer_id, transaction_amount, logger):
    try:
        # HiveQL Query to get the credit score of the client
        credit_score_query = f"""
            SELECT credit_scores['{customer_id}']
            FROM externals
        """
        
        # Execute the HiveQL query using your preferred method (e.g., pyhive, pandasql)
        cursor = conn.cursor()
        cursor.execute(credit_score_query)
        credit_score = cursor.fetchone()[0]
        cursor.close()

        # Check if the transaction amount is below the client's credit score
        return transaction_amount < credit_score

    except Exception as e:
        logger.error(f"Error checking transaction amount against credit score: {e}")
        return False

def insert_customer_data(customer, logger):
    cursor = conn.cursor()

    try:
        # Customize the query
        query = f"INSERT INTO TABLE customers SELECT '{customer['customer_id']}', array('{','.join(customer['account_history'])}'), {customer['demographics']['age']}, '{customer['demographics']['location']}', {customer['behavioral_patterns']['avg_transaction_value']}"
        
        cursor.execute(query)
        logger.info("Query Executed")

        conn.commit()
        logger.info("Event Committed")

        logger.info("Customer Emitted To Hive SUCCFFULLY")
        
    except Exception as e:
        logger.error(f"Error Inserting To Customer Table: {e}")

    finally:
        cursor.close()

def insert_external_data(external, logger):
    cursor = conn.cursor()

    try:
        # Check if 'external' is a list with at least one dictionary
        if isinstance(external, list) and external and isinstance(external[0], dict):
            external_data = external[0]  # Extract the dictionary from the list
            # Check if required keys are present in the extracted dictionary
            if 'credit_scores' in external_data and 'fraud_reports' in external_data and 'blacklist_info' in external_data:

                blacklist_info_json = json.dumps(external_data['blacklist_info'])
                logger.info(f"blacklist_info_json: {blacklist_info_json}")

                # Convert the lists and maps to JSON strings
                credit_scores_json = json.dumps(external_data['credit_scores'])
                logger.info(f"credit_scores_json: {credit_scores_json}")

                fraud_reports_json = json.dumps(external_data['fraud_reports'])
                logger.info(f"fraud_reports_json: {fraud_reports_json}")

                # Customize the query based on your Hive table structure
                query = f"""
                    INSERT INTO TABLE externals 
                    SELECT 
                        array('{",".join(external_data['blacklist_info'])}'),
                        map({','.join(f'"{k}", {v}' for k, v in external_data['credit_scores'].items())}),
                        map({','.join(f'"{k}", {v}' for k, v in external_data['fraud_reports'].items())})
                """
                cursor.execute(query)
                logger.info("External data inserted successfully")

            else:
                logger.error("Required keys are missing in the 'external' dictionary.")

        else:
            logger.error("'external' is not in the expected format (list with at least one dictionary).")
        pass

    except Exception as e:
        logger.error(f"Error inserting external data: {e}")

    finally:
        cursor.close()

def insert_transactions_data(transaction, logger):
    cursor = conn.cursor()
    logger.info("Connected Successfully To Hive __________ Transaction ")

    try:
        # Check if merchant_details is in the blacklist_info of externals table
        if is_merchant_blacklisted(transaction['merchant_details'], logger):
            logger.info(f"Merchant {transaction['merchant_details']} is blacklisted. Skipping transaction insertion.")
            return

        # Check if the transaction amount is less than the client's credit score
        if is_transaction_amount_below_credit_score(transaction['customer_id'], transaction['amount'], logger):
            logger.info("Transaction amount is below the client's credit score. Skipping transaction insertion.")
            return

        # Customize the query based on your Hive table structure
        query = f"INSERT INTO TABLE transactions VALUES ('{transaction['transaction_id']}', '{transaction['date_time']}', {transaction['amount']}, '{transaction['currency']}', '{transaction['merchant_details']}', '{transaction['customer_id']}', '{transaction['transaction_type']}', '{transaction['location']}')"

        cursor.execute(query)
        logger.info("Query Executed")

        conn.commit()
        logger.info("Event Committed")

        logger.info("Transaction Emitted To Hive SUCC")

    except Exception as e:
        logger.error(f"Error inserting transaction data: {e}")

    finally:
        cursor.close()

def getCustomers(logger):
    try:
        while True:
            try:
                # Use the streaming endpoint to get customer data
                customer_data_endpoint = 'http://localhost:5002/api/customers'
                response = requests.get(customer_data_endpoint, stream=True)

                for line in response.iter_lines():
                    try:
                        if line:
                            customer_json = json.loads(line)

                            insert_customer_data(customer_json , logger)
                            
                    except ValueError as ve:
                        # Log the error if the JSON parsing fails
                        logger.info(f"Error parsing JSON: {ve}")

                    except Exception as ex:
                        # Log other validation errors
                        logger.info(f"Error In GetCustomers  : {ex}")

                # Close the response after processing all lines
                response.close()
                pass
            except Exception as e:
                logger.error("Error getting customer data: " + str(e))
        pass
    except Exception as e:
        logger.error("Error In GetCustomers() : " + str(e))

def getTransactions(logger):
    try:
        while True:
            try:
                transactions_data_endpoint = 'http://localhost:5004/api/transactions'
                response = requests.get(transactions_data_endpoint, stream=True)

                for line in response.iter_lines():
                    try:
                        if line:
                            transaction_json = json.loads(line)
                            insert_transactions_data(transaction_json , logger)

                            logger.info(transaction_json)

                    except ValueError as ve:
                        # Log the error if the JSON parsing fails
                        logger.info(f"Error parsing JSON: {ve}")

                    except Exception as ex:
                        # Log other validation errors
                        logger.info(f"Error validating transactions : {ex}")

                # Close the response after processing all lines
                response.close()
                pass
            except Exception as e:
                logger.error("Error getting transaction data: " + str(e))
        pass
    except Exception as e:
        logger.error("Error In GetCustomers: " + str(e))

def getExternals(logger):

    try:
        external_api_url = 'http://localhost:5003/api/external'

        # Function to collect data from API
        response = requests.get(external_api_url)

        if response.status_code == 200:

            external_data = response.json()

            # Insert external data into Hive
            insert_external_data(external_data , logger)

            logger.info(f"External data: {external_data}")

        else:
            logger.error(f"Error collecting data from {external_api_url}")

        pass
    except Exception as e:
        logger.error("Error: " + str(e))

def runCustomersInsertion(logger):
    getCustomers(logger)

def runExternalsInsertion(logger):
    getExternals(logger)

def runTransactionsInsertion(logger):
    getTransactions(logger)

try:
    
    # Connection parameters for Hive : 

    hive_host = 'localhost'
    hive_port = 10001
    db = "fraudedetection1"

    # Create a Hive connection : 

    conn = hive.connect(host=hive_host, port = hive_port , database = db)

    customers_logger = setup_Customers_logging()
    transactions_logger = setup_Transactions_logging()
    externals_logger = setup_Externals_logging()
    hive_logger = setup_Hive_logging()

    select_Database(db, hive_logger)

    runTransactionsInsertion(transactions_logger)

except Exception as setup_error:

    print(f"An unexpected error occurred during setup: {setup_error}")