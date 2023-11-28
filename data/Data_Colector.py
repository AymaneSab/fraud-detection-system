import os 
from datetime import datetime 
import logging 
import requests
import json 
import threading

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

def setup_Customers_logging():
    return setup_logging("Log/API_Customers_LogFiles", "customers_logger")

def setup_Transactions_logging():
    return setup_logging("Log/API_Transactions_LogFiles", "transactions_logger")

def setup_Externals_logging():
    return setup_logging("Log/API_Externals_LogFiles", "externals_logger")

def getCustomers(logger):
    try:
        while True:
            try:
                # Use the streaming endpoint to get movie data
                customer_data_endpoint = 'http://localhost:5002/api/customers'
                response = requests.get(customer_data_endpoint, stream=True)

                for line in response.iter_lines():
                    try:
                        if line:
                            customer_json = json.loads(line)
                            logger.info(customer_json)

                    except ValueError as ve:
                        # Log the error if the JSON parsing fails
                        logger.info(f"Error parsing JSON: {ve}")

                    except Exception as ex:
                        # Log other validation errors
                        logger.info(f"Error validating Kafka message: {ex}")

                # Close the response after processing all lines
                response.close()

            except Exception as e:
                logger.error("Error getting movie data: " + str(e))

    except Exception as e:
        logger.error("Error producing to Kafka: " + str(e))

def getTransactions(logger):
    try:
        while True:
            try:
                # Use the streaming endpoint to get movie data
                transactions_data_endpoint = 'http://localhost:5004/api/transactions'
                response = requests.get(transactions_data_endpoint, stream=True)

                for line in response.iter_lines():
                    try:
                        if line:
                            transaction_json = json.loads(line)
                            logger.info(transaction_json)

                    except ValueError as ve:
                        # Log the error if the JSON parsing fails
                        logger.info(f"Error parsing JSON: {ve}")

                    except Exception as ex:
                        # Log other validation errors
                        logger.info(f"Error validating Kafka message: {ex}")

                # Close the response after processing all lines
                response.close()

            except Exception as e:
                logger.error("Error getting movie data: " + str(e))

    except Exception as e:
        logger.error("Error producing to Kafka: " + str(e))

def getExternals(logger):
    try:
        external_api_url    = 'http://localhost:5003/api/external'

        # Function to collect data from API
        response = requests.get(external_api_url)
        if response.status_code == 200:
            logger.info(f"External data: {response.json()}")

        else:
            print(f"Error collecting data from {external_api_url}")
            return None

    except Exception as e:
        logger.error("Error: " + str(e))

def runDataCollector(customers, transactions, externals):
    try:
        # Create threads for sparkTreatment_movies and sparkTreatment_reviews
        customers_thread = threading.Thread(target=getCustomers, args=(customers,))
        transactions_thread = threading.Thread(target=getTransactions, args=(transactions,))
        externals_thread = threading.Thread(target=getExternals, args=(externals,))

        # Start the threads
        customers_thread.start()
        transactions_thread.start()
        externals_thread.start()

        # Wait for both threads to finish
        customers_thread.join()
        transactions_thread.join()
        externals_thread.join()

    except KeyboardInterrupt:
        logging.info("API Collector Stopped")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        logging.exception("An unexpected error occurred in Data Collector Script")

customers_logger = setup_Customers_logging()
transactions_logger = setup_Transactions_logging()
externals_logger = setup_Externals_logging()

runDataCollector(customers_logger, transactions_logger, externals_logger)