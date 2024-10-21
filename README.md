# Resolution Rate for Work Orders | Google Cloud & Mage Pipeline
An end-to-end data pipleline solution to process and analyze Maintenance Work Orders using Mage, Google BigQuery, Cloud SQL, and Looker Studio. This prject features integration of cloud tools for scalable data storage, transformation, and visualization based on Client requirements.


# Business Case
The client needs a solution to automatically ingest their maintenance work orders data from their existing spreadsheets and effectively visualize them for reporting. The key metric they are looking to visualize is the resolution rate of work orders based on the activity carried out over time.


# Technical Requirements
| Functional 🟢 | Non-Functional 🔵|
| ------------- | ------------- |
| The system shall automatically ingest maintenance work orders from Excel spreadsheets stored in Cloud Storage daily.  | The system shall be scalable to handle an increasing number of work orders (up to 1 million records) without significant degradation in performance.  |
| The system shall provide a mechanism to validate the correctness and completeness of the ingested data (e.g., correct formatting, missing fields).  | The system shall support future integration with other cloud services (e.g., additional data sources or external APIs) without requiring major re-architecture.  |
| The system shall clean, transform the ingested work orders data, and store in Database, maintaining historical records of all work orders.  | Access to sensitive data (e.g., work order details, analytics dashboards) shall be role-based, with authentication and authorization mechanisms in place.  |
| The system shall calculate and visualize metrics such as the "Resolution Rate" of work orders using exportable and dynamic dashboards.  | The system shall have an availability of 99.9% to ensure data processing and reporting is available at all times for the client's maintenance team.  |
| The system shall notify users of ingestion failures or transformation errors via email or system alerts.  | Backup and recovery processes shall be in place to restore data in case of accidental deletion or system failure.  |
| The system shall trigger alerts for work orders that are overdue based on predefined thresholds.  | The system’s codebase and infrastructure shall be documented to allow easy handover to new developers or administrators.  |


# Tools Used
Programming Language - [Python](https://www.python.org/) ![Python](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Python.png) 

Cloud Infrastructure - [Google Cloud Platform (GCP)](https://cloud.google.com/) ![Google Cloud Platform (GCP)](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20Platform.png)   

Workflow Orchestration: [Mage](https://www.mage.ai/) ![Mage](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Mage%20ai.png)

(Contibute to this open source project - https://github.com/mage-ai/mage-ai)

Containerization: [Docker](https://www.docker.com/) ![Docker](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Docker.png)

Storage: [Google Cloud Storage](https://cloud.google.com/storage) ![Google Cloud Storage](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20Storage.png)

Database: [Google Cloud SQL](https://cloud.google.com/sql) ![Google Cloud SQL](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20SQL.png) 

Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery/) ![Google BigQuery](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/BigQuery.png)

Computation: [Google Compute Engine Instance](https://cloud.google.com/products/compute) ![Google Compute Engine Instance](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Compute%20Engine%20Instance.png) 

Data Visualization: [Google Looker Studio](https://lookerstudio.google.com/) ![Google Looker Studio](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Looker%20Studio.png)


# High Level Architecture
![GCP Mage ETL Architecture](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/2.%20Solution%20Architecture/GCP%20Mage%20ETL%20High%20Level%20Architecture.png)

[//]: # (Explain Architecture Choices for Tools here)

Google Cloud Platform (GCP) was chosen as the Cloud platform beacuse the client already utilizes GCP for other daily processes, making it more cost-effective, and easier to manage.

Python was chosen as the coding language as it is rich with libraries for data processing, manipulation, and analysis like Pandas, NumPy etc. It also has extensive support for data pipelines and orchestration (e.g., Airflow, Mage) and integrates seamlessly with Google Cloud.

The source data is first automatically retrieved from the client's ERP (Enterprise Resource Planning) tool and stored in Google Cloud storage. Google Cloud Storage supports both batch and real-time data ingestion and provides highly scalable and secure object storage which is optimized for large volumes of unstructured data like spreadsheets. 

Mage will run via docker inside the Google Compute Engine Instance and will do the work of extracting the data from the Google Cloud Storage, Cleaning and Transforming it based on predefined rules and loading it into the Database. Mage was chosen for workflow orchestration because it provides a more user-friendly interface, easier configuration, and quicker setup for orchestrating ETL workflows compared to alternatives like Airflow. 

Google Compute Engine was selected as the compute tool as it provides scalable, high-performance VMs (virtual machines), integrates with other Google Cloud services (such as Cloud Storage and BigQuery) and enables efficient data processing. 

Google Cloud SQL is used as the database (db) of choice with a MySQL configuration. The data is loaded to the Google Cloud SQL database then connected downstream to BigQuery. Although the current source data is ingested and processed in a batch mode, the near future client consideration for this solution is to directly write the transactional data from the ERP to the Cloud SQL db in real time. Hence, the incorporation of Cloud SQL in this pipeline.

BigQuery is used as the data warehousing tool as it is ideal for handling large-scale analytics queries and is already being used by the client’s firm as their primary data warehouse. It can also handle enormous amounts of data with near-instant query response time, using its distributed architecture.

Finally, the dashboard visualization including client requested metrics will be done through Looker Studio. Since Looker Studio is part of the GCP ecosystem, it integrates well with BigQuery to provide seamless visualization of the data processed in the pipeline.



# The Source Dataset
The source data is a spreadsheet containing maintenance work orders associated with Customer Service Requests. The dataset will be updated daily from the Client's ERP tool and loaded unto the Google Cloud storage platform before the data transformation step. The primary field in the dataset is the 'WORKORDER_NUMBER' which gives the unique ERP system-generated Work order number. Most queries from the DB will be based on aggregating this field over time periods. [View the data dictionary](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.pdf) below to see a more detailed description of the dataset.

![Data Dictionary - Work Order Management Module Dataset](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.jpg)



# Database Schema
Considering this will be a 'heavy write' data pipeline, with frequent updates to the database, and a low number of users (analysts, management users) querying results, I'll use a normalized snowflake schema design for this project. This is in contrast to a denormalized schema model, ensuring data integrity during frequent transactional operations. It will help maintain accuracy and consistency in the work order records. From the dataset, the 'TIME_STAMP' column is not included in the analysis as it only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.

![Schema - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/4.%20Database%20Schema/Schema%20-%20WorkOrderModule%20DB.png)

View a snippet of the data dictionary below to see a more detailed description of the Database tables. [> View the full data dictionary here <](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20WorkOrderModule%20DB.pdf)

![Data Dictionary - WorkOrderModule DB1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20WorkOrderModule%20DB_1.jpg)


# GCP Configuration
## Setting up Google Cloud Storage
On Cloud Storage, I'll configure a 'region' bucket for the storage as seen below. 

![cloud_storage_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cloud_storage_1.png)

It has the lowest data storage cost and it includes optimized latency / bandwidth, suitable for an analytics pipeline. Some other advantages of the 'region' bucket includes:

Availability
- Activates data redundancy across availability zones (synchronous).
- RTO (recovery time objective) of zero (0). In addition, automated failover and failback on zonal failure (no need to change storage paths).

Performance
- 200 Gbps (per region, per project).
- Scalable to many Tbps by requesting higher bandwidth quota.

On this bucket, I'll store the Work Order spreadsheet for later retrieval and analysis. 

### Configure Access and Permissions
In the process of creating the bucket, I'll select 'Enforce public access prevention on this bucket' to prevent exposure of the data in the bucket to the internet, and also select 'Uniform' access control.

![cloud_storage_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cloud_storage_2.png)

![cloud_storage_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cloud_storage_3.png)


Next, I'll need to create a private key to give access to the Mage AI Instance later. Under 'IAM & Admin' on the left bar, I will select 'Service Accounts'. A default service account is usually provided for bucket instances, but if not for you, just create a new service account. Ensure to configure the required permissions for the specific principals (users, groups, domains, or service accounts - if many) including roles and IAM conditions where applicable.

I'll then create a new private key for the service account. Click on 'Add Key' then 'Create new key' and afterwards select the 'JSON' key type. The private key details will be automatically downloaded to the computer.

![cloud_storage_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cloud_storage_4.png)

### Uploading the Source Data to the Bucket
I can upload the source data to the bucket by opening the bucket and clicking on 'Upload' as seen below:

![cloud_storage_5](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cloud_storage_5.png)


## Setting up Google Compute Engine
Next up, I'll go to Compute Engine and create a new VM instance. I have selected an 'E2' series with 4 cores and 8GB of memory; the operating system (OS) is Debian GNU/Linux 12 (bookworm). I am also using a 'Spot' VM provisioning model instead of the 'Standard' model. Based on my workload and requirements, this configuration is suitable, however, create your own server based on your own design, planning, and technical requirements.

![compute_engine_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_1.png)

![compute_engine_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_2.png)

Spot VMs have significant discounts, but by design, Compute Engine might preemptively stop or delete (preempt) Spot VMs to reclaim the capacity at any time. Since the workload is currently fault-tolerant and can withstand possible instance preemptions, the Spot VM is a reasonable choice which will help reduce the Compute Engine costs significantly. 

When the workload is significantly increased in the future, and the workloads/pipeline are reconfigured to be in a Streaming mode, then I can re-provision a 'Standard' VM. Finally, because all incoming traffic from outside networks are blocked by default for VM instances, I will select the relevant boxes to allow HTTP/HTTPS traffic.

![compute_engine_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_3.png)


## Setting up Mage via Docker
I'll now open the VM via the 'SSH' button and install Git, Docker Engine / Docker Compose and Mage on the VM. 

![compute_engine_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_4.png)


- Install Git following the instructions from this link: [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 
- Install the Docker Engine using the instructions from this link: [Docker Engine](https://docs.docker.com/engine/install/debian/#install-using-the-repository) (for my VM, I used the apt repository to install the Docker Engine).
- Install the Docker Compose plugin following the instructions from this link: [Docker Compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository).

Next, I'll spin up the mage server using 'docker compose up' as seen below. Use the instructions from this link to assist you: [Mage Quickstart](https://docs.mage.ai/getting-started/setup#docker-compose-template).

    git clone https://github.com/mage-ai/compose-quickstart.git mage-quickstart \
    && cd mage-quickstart \
    && cp dev.env .env && rm dev.env \
    && docker compose up

If you get a permission denied error when spinning up the container instance, then try running the below code:

    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker

Now check to see if the access is still denied by verifying that the code below works:

    docker run hello-world

If there's still an error, try reading this thread for tips: [Stack Overflow Thread](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue).







## Setting up Google Cloud SQL



# Extracting the Data
- Connecting to Google Cloud Storage API and converting data to Dataframe


# Transforming the Data
Viewing the [Source data](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/1.%20Source%20Data/work-order-management-module.csv) seen below, it contains 206,058 Rows and 7 Columns. We will use the Mage transformer to first clean the data, then to also create our fact and dimension tables (based on the schema shown earlier). The Transformer block in Mage is vital in data transformation tasks such as filtering, aggregating, and cleansing. It ensures that data is standardized and prepared for downstream analysis.

![source_dataset_info](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/source_dataset_info.png)

![source_dataset_info_head](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/source_dataset_info_head.png)

## Cleaning the data
In this step, we will deal with out-of-range data (specifically for time values), impose Data type constraints, find and remove duplicate values.

Here are a few things we need to do in the data cleaning step:
- Remove the last column called 'TIME_STAMP' as it only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.
- Capture 'out of range' dates in Datetime Columns and export to repository for record keeping.
- Converting the out of range values to 'NA' values.
- Enforce data type constraints for each column.
- Enforce data type 'length' constraints for each column.
- Remove duplicate data.

### Removing column(s) excluded from analysis


### Dealing with 'Out of Range' Datetime values


![Out_of_range_datetimes](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/Out_of_range_datetimes.png)


### Enforcing Datatypes

Convieniently enough, the first two columns have already been formatted as integer type columns in the Pandas Dataframe. T

### Enforcing Datatype length constraints


### Removing Duplicate Records
We have removed 10,030 Duplicate Records

![cleaned_source_dataset_info](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cleaned_source_dataset_info.png)


## Creating Fact and Dimension Tables


# Loading the Data



# More GCP Configuration

## Setting up Google BigQuery



## Setting up Google Looker Studio
