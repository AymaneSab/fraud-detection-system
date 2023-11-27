import requests

# Example API endpoints
transaction_api_url = 'http://localhost:5004/api/transactions'
customer_api_url    = 'http://localhost:5002/api/customers'
external_api_url    = 'http://localhost:5003/api/external'

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


# Print or further process the collected data
print("Transaction Data:", transactions)
print("Customer Data:", customers)
print("External Data:", external_data)

