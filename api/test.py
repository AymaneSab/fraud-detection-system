import requests
import json

def get_customer_data():
    url = 'http://localhost:5002/api/externalData'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        customer_data = response.json()
        print("Customer Data:")
        print(json.dumps(customer_data, indent=1))

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == '__main__':
    get_customer_data()
