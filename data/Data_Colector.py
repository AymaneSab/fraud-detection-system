import requests

# Example API endpoints
transaction_api_url = "http://localhost:5001/transactions"
customer_api_url = "http://localhost:5002/customers"
external_api_url = "http://localhost:5003/external"

# Function to collect data from API
def collect_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error collecting data from {api_url}")
        return None

# Collect data from each API
transactions = collect_data(transaction_api_url)
customers = collect_data(customer_api_url)
external_data = collect_data(external_api_url)

# Perform any necessary data cleaning and validation here
# ...

# Print or further process the collected data
print("Transaction Data:", transactions)
print("Customer Data:", customers)
print("External Data:", external_data)

# Example data integration using Python
integrated_data = []

# for customer in customers:
#     customer_id = customer["customer_id"]

#     # Find transactions for the current customer
#     customer_transactions = [transaction for transaction in transactions if transaction["customer_id"] == customer_id]

#     # Find external data for the current customer
#     customer_external_data = external_data.get(customer_id, {})

#     # Combine data into a single dictionary
#     integrated_customer_data = {
#         "customer_id": customer_id,
#         "customer_info": customer,
#         "transactions": customer_transactions,
#         "external_data": customer_external_data
#     }

#     integrated_data.append(integrated_customer_data)

# # Perform further processing or analysis on integrated_data
# # ...
