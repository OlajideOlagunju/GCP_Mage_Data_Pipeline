# Resolution Rate for Work Orders | Google Cloud & Mage Pipeline
An end-to-end solution to process and analyze Maintenance Work Orders using Mage, Google BigQuery, Cloud SQL, and Looker Studio. Seamless integration of cloud tools for scalable data storage, transformation, and visualization.


# Business Case
The client needs a solution to automatically ingest their maintenance work orders data from their existing spreadsheets and effectively visualize them for reporting. The key metric they are looking to visualize is the resolution rate of work orders based on the activity carried out over time.


# Functional Requirements
🟢 FR1: The system shall automatically ingest maintenance work orders from Excel spreadsheets stored in Cloud Storage daily.

🟢 FR2: The system shall provide a mechanism to validate the correctness and completeness of the ingested data (e.g., correct formatting, missing fields).

🟢 FR3: The system shall clean, transform the ingested work orders data, and store in Database, maintaining historical records of all work orders.

🟢 FR4: The system shall calculate and visualize metrics such as the "Resolution Rate" of work orders using exportable and dynamic dashboards.

🟢 FR5: The system shall notify users of ingestion failures or transformation errors via email or system alerts.

🟢 FR6: The system shall trigger alerts for work orders that are overdue based on predefined thresholds.

# Non-Functional Requirements
🟡 NFR1: The system shall be scalable to handle an increasing number of work orders (up to 1 million records) without significant degradation in performance.

🟡 NFR2: The system shall support future integration with other cloud services (e.g., additional data sources or external APIs) without requiring major re-architecture.

🟡 NFR3: Access to sensitive data (e.g., work order details, analytics dashboards) shall be role-based, with authentication and authorization mechanisms in place.

🟡 NFR4: The system shall have an availability of 99.9% to ensure data processing and reporting is available at all times for the client's maintenance team.

🟡 NFR5: Backup and recovery processes shall be in place to restore data in case of accidental deletion or system failure.

🟡 NFR6: The system’s codebase and infrastructure shall be documented to allow easy handover to new developers or administrators.

# Tools Used
Programming Language - [Python](https://www.python.org/) ![Python](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Python.png) 

Cloud Infrastructure - [Google Cloud Platform (GCP)](https://cloud.google.com/) ![Google Cloud Platform (GCP)](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20Platform.png)   

Workflow Orchestration: [Mage](https://www.mage.ai/) ![Mage](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Mage%20ai.png)

(Contibute to this open source project - https://github.com/mage-ai/mage-ai)

Storage: [Google Cloud Storage](https://cloud.google.com/storage) ![Google Cloud Storage](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20Storage.png)

Database: [Google Cloud SQL](https://cloud.google.com/sql) ![Google Cloud SQL](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20SQL.png) 

Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery/) ![Google BigQuery](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/BigQuery.png)

Computation: [Google Compute Engine Instance](https://cloud.google.com/products/compute) ![Google Compute Engine Instance](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Compute%20Engine%20Instance.png) 

Data Visualization: [Google Looker Studio](https://lookerstudio.google.com/) ![Google Looker Studio](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Looker%20Studio.png)


# High Level Architecture
![GCP Mage ETL Architecture](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/2.%20Solution%20Architecture/GCP%20Mage%20ETL%20Architecture.png)

[//]: # (Explain Architecture Choices for Tools here)



# The Source Dataset
The source data is a spreadsheet containing maintenance work orders associated with Customer Service Requests. [View the data dictionary](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.pdf) below see a more detailed description of the dataset.
![Data Dictionary - Work Order Management Module Dataset](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.jpg)

[//]: # (Explain Dataset Nuances)



# Database Schema
![Schema - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/4.%20Database%20Schema/Schema%20-%20WorkOrderModule%20DB.png)

[View the data dictionary](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20WorkOrderModule%20DB.pdf) below see a more detailed description of the Database tables.

![Data Dictionary - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20WorkOrderModule%20DB.jpg)

[//]: # (Explain Database design reasons, schema type, selections and omissions of 'TIME_STAMP' column)

