# Fraud Detection System

![Alt text](https://miro.medium.com/v2/resize:fit:1400/0*aH57NAkEfKj0zLoj.jpg)

## Project Architectur 
```
fraud-detection-system/
│
├── .github/                    # GitHub Actions workflows
│   ├── workflows/
│   │   └── ci-cd.yml
│
├── airflow/                    # Apache Airflow DAGs and configurations
│   ├── dags/
│   │   └── data_processing_dag.py
│   ├── config/
│   │   └── airflow.cfg
│
├── api/                        # API development
│   ├── transaction_api/
│   │   └── main.py
│   ├── customer_api/
│   │   └── main.py
│   ├── external_api/
│   │   └── main.py
│
├── data/                       # Sample or test data
│   ├── transaction_data/
│   ├── customer_data/
│   └── external_data/
│
├── hive/                       # HiveQL scripts and schemas
│   ├── schemas/
│   │   ├── transaction_schema.hql
│   │   ├── customer_schema.hql
│   │   └── external_schema.hql
│   ├── queries/
│   │   ├── fraud_detection_rules.hql
│   │   └── data_management_strategies.hql
│
├── tests/                      # Unit tests
│   ├── api_tests/
│   │   ├── test_transaction_api.py
│   │   ├── test_customer_api.py
│   │   └── test_external_api.py
│   ├── data_tests/
│   │   ├── test_data_cleaning.py
│   │   └── test_data_integrity.py
│   ├── hive_tests/
│   │   ├── test_fraud_detection_queries.py
│   │   └── test_data_management_queries.py
│
├── .gitignore                  # Git ignore file
├── README.md                   # Project README
├── requirements.txt            # Python dependencies
├── LICENSE                      # Project license
└── .vscode/                    # VSCode-specific configurations
    └── settings.json
```

## Project Overview

As a Data Developer, the goal of this project is to detect suspicious activities in near real-time and minimize false alerts. The project involves developing APIs, collecting and integrating transaction and client data, storing and managing the data using Hive, and implementing a rule-based fraud detection system. The entire process is orchestrated using Apache Airflow, with continuous integration and deployment (CI/CD) integrated through GitHub Actions.

## Table of Contents

- [API Development](#api-development)
  - [Transaction Data API](#transaction-data-api)
  - [Customer Data API](#customer-data-api)
  - [External Data API](#external-data-api)
- [Data Collection and Integration](#data-collection-and-integration)
- [Storage and Data Management with Hive](#storage-and-data-management-with-hive)
- [Rule-Based Fraud Detection](#rule-based-fraud-detection)
- [Deployment](#deployment)

## API Development

### Transaction Data API

- Endpoint: `/api/transactions`
- Provides access to transaction data, including transaction ID, date and time, amount, currency, merchant details, customer ID, and transaction type.

### Customer Data API

- Endpoint: `/api/customers`
- Provides access to customer data, including customer ID, account history, demographic information, and behavioral patterns.

### External Data API

- Endpoint: `/api/externalData`
- Retrieves external data, such as blacklist information, credit scores, and fraud reports.

## Data Collection and Integration

- Utilizes the developed APIs to collect transaction, customer, and external data.
- Ensures collected data is clean, relevant, and in a format suitable for analysis.

## Storage and Data Management with Hive

- Designs and implements Hive tables to store transaction, customer, and external data.
- Applies partitioning and indexing strategies for efficient data management.

## Rule-Based Fraud Detection

- Uses HiveQL to write queries for detecting fraudulent transactions based on identified indicators.
- Examples of rules include detecting unusually high transaction amounts, high transaction frequency in a short time, transactions from unusual locations, and transactions with customers on the blacklist.

## Deployment

- Sets up an Apache Airflow DAG (Directed Acyclic Graph) to orchestrate the data collection, processing, and alerting process.
- Integrates CI/CD with GitHub Actions for automatic and secure updating of scripts and DAGs.

## How to Run

Include instructions on how to run the project, dependencies, and any configuration steps.

## Contributors

List the contributors and their roles in the project.

## License

https://github.com/AymaneSab/fraud-detection-system/blob/main/LICENSE

