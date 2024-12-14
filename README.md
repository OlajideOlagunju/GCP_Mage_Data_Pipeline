# Resolution Rate for Work Orders | Google Cloud & Mage Pipeline
An end-to-end data pipeline solution to process and analyze Maintenance Work Orders using Mage, Google BigQuery, MariaDB, and Looker Studio. This project features integration of cloud tools for scalable data storage, transformation, and visualization based on Client requirements.

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

(Contribute to this open source project - https://github.com/mage-ai/mage-ai)

Containerization: [Docker](https://www.docker.com/) ![Docker](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Docker.png)

Storage: [Google Cloud Storage](https://cloud.google.com/storage) ![Google Cloud Storage](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Cloud%20Storage.png)

Database: [MariaDB](https://mariadb.org/) ![MariaDB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/MariaDB.png) 

Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery/) ![Google BigQuery](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/BigQuery.png)

Computation: [Google Compute Engine Instance](https://cloud.google.com/products/compute) ![Google Compute Engine Instance](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Google%20Compute%20Engine%20Instance.png) 

Data Visualization: [Google Looker Studio](https://lookerstudio.google.com/) ![Google Looker Studio](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/7.%20Icons/Looker%20Studio.png)


# High Level Architecture
![GCP Mage ETL Architecture](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/2.%20Solution%20Architecture/GCP%20Mage%20ETL%20High%20Level%20Architecture.gif)

[//]: # (Explain Architecture Choices for Tools here)

Google Cloud Platform (GCP) was chosen as the Cloud platform because the client already utilizes GCP for other daily processes, making it more cost-effective, and easier to manage.

Python was chosen as the coding language as it is rich with libraries for data processing, manipulation, and analysis like Pandas, NumPy etc. It also has extensive support for data pipelines and orchestration (e.g., Airflow, Mage) and integrates seamlessly with Google Cloud.

The source data is first automatically retrieved from the client's ERP (Enterprise Resource Planning) tool and stored in Google Cloud storage. Google Cloud Storage supports both batch and real-time data ingestion and provides highly scalable and secure object storage which is optimized for large volumes of unstructured data like spreadsheets. 

Mage will run via docker inside the Google Compute Engine Instance and will do the work of extracting the data from the Google Cloud Storage, Cleaning and Transforming it based on predefined rules and loading it into the Database. Mage was chosen for workflow orchestration because it provides a more user-friendly interface, easier configuration, and quicker setup for orchestrating ETL workflows compared to alternatives like Airflow. 

Google Compute Engine was selected as the compute tool as it provides scalable, high-performance VMs (virtual machines), integrates with other Google Cloud services (such as Cloud Storage and BigQuery) and enables efficient data processing. 

MariaDB is used as the database (db) of choice running inside of Docker. It is an open-source, improved version of MySQL which offers faster performance, broader feature set, and active community development. The data is loaded to the MariaDB database then connected downstream to BigQuery. Although the current source data is ingested and processed in a batch mode, the near future client consideration for this solution is to directly write the transactional data from the ERP to the database in real time. Hence, the incorporation of MariaDB in this pipeline.

BigQuery is used as the data warehousing tool as it is ideal for handling large-scale analytics queries and is already being used by the client’s firm as their primary data warehouse. It can also handle enormous amounts of data with near-instant query response time, using its distributed architecture.

Finally, the dashboard visualization including client requested metrics will be done through Looker Studio. Since Looker Studio is part of the GCP ecosystem, it integrates well with BigQuery to provide seamless visualization of the data processed in the pipeline.


# The Source Dataset
The source data is a spreadsheet containing maintenance work orders associated with Customer Service Requests. The dataset will be updated daily from the Client's ERP tool and loaded unto the Google Cloud storage platform before the data transformation step. The primary field in the dataset is the 'WORKORDER_NUMBER' which gives the unique ERP system-generated Work order number. Most queries from the DB will be based on aggregating this field over time periods. [View the data dictionary](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.pdf) below to see a more detailed description of the dataset.

![Data Dictionary - Work Order Management Module Dataset](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20Work%20Order%20Management%20Module%20Dataset.jpg)


# Database Schema
Considering this will be a 'heavy write' data pipeline, with frequent updates to the database, and a low number of users (analysts, management users) querying results, I'll use a normalized snowflake schema design for this project. This is in contrast to a denormalized schema model, ensuring data integrity during frequent transactional operations. It will help maintain accuracy and consistency in the work order records. From the dataset, the 'TIME_STAMP' column is not included in the analysis as it only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.

![Schema - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/4.%20Database%20Schema/Schema%20-%20WorkOrderModule%20DB.png)

View the [data dictionary](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/Data%20Dictionary%20-%20WorkOrderModule%20DB.pdf) below to see a more detailed description of the Database tables.

![Data Dictionary - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/3.%20Data%20Dictionary/bin/Data%20Dictionary%20-%20WorkOrderModule%20DB.jpg)


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
Next up, I'll go to Compute Engine and create a new VM instance. I have selected an 'E2' series with the appropriate amount of cores and memory space; the operating system (OS) is Debian GNU/Linux 12 (bookworm). I am also using a 'Spot' VM provisioning model instead of the 'Standard' model. Based on my workload and requirements, I picked a configuration that is suitable, however, create your own server based on your own design, planning, and technical requirements.

![compute_engine_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_1.png)

![compute_engine_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_2.png)

Spot VMs have significant discounts, but by design, Compute Engine might preemptively stop or delete (preempt) Spot VMs to reclaim the capacity at any time. Since the workload is currently fault-tolerant and can withstand possible instance preemptions, the Spot VM is a reasonable choice which will help reduce the Compute Engine costs significantly. 

When the workload is significantly increased in the future, and the workloads/pipeline are reconfigured to be in a Streaming mode, then I can re-provision a 'Standard' VM. Finally, because all incoming traffic from outside networks are blocked by default for VM instances, I will select the relevant boxes to allow HTTP/HTTPS traffic.

![compute_engine_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_3.png)


## Setting up Mage via Docker
I'll now open the VM via the 'SSH' button and install Git and Docker Engine / Docker Compose. 

![compute_engine_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_4.png)

When you get in the bash terminal:
- Install Git following the instructions from this link: [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 
- Install the Docker Engine using the instructions from this link: [Docker Engine](https://docs.docker.com/engine/install/debian/#install-using-the-repository) (for my VM, I used the apt repository to install the Docker Engine).
- Install the Docker Compose plugin following the instructions from this link: [Docker Compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository).

Next, I'll spin up a container (I'll be running Mage and MariaDB from this container) using 'docker compose up' from a custom github private repository I made in my account. You can fork a sample repository link [here](https://github.com/mage-ai/compose-quickstart). Next edit the Dockerfile as you wish (if necessary for your case). I also edited the 'dev.env' file to reflect the project name as 'GCP_Pipeline'. 'GCP_Pipeline' would later on reflect as the name of my project in Mage.

Let's see a snippet of the docker-compose.yml file that spins up the Mage instance and MariaDB database:

    services:
        mage:
            image: mageai/mageai:latest
            command: mage start ${PROJECT_NAME}
            env_file:
                - .env
            build:
                context: .
                dockerfile: Dockerfile
            environment:
                USER_CODE_PATH: /home/src/${PROJECT_NAME}
                ENV: ${ENV}
            ports:
                - 6789:6789
            volumes:
                - .:/home/src/
            restart: on-failure:5

    mariadb:
        image: mariadb
        environment:
            MYSQL_ROOT_PASSWORD: <insert your root password>
            MYSQL_USER: <insert your preferred username>
            MYSQL_PASSWORD: <insert your preferred user password>
            MYSQL_DATABASE: WorkOrderModule
        ports:
            - 3306:3306
        volumes:
            # create a persistent docker volume
            - ./data:/var/lib/mysql
            # mount configuration
            - ./config/:/etc/mysql/conf.d
            # initialize tables using script
            - ./WO_DB_Tables_Initialization.sql:/docker-entrypoint-initdb.d/1.sql
        restart: on-failure:5

Under "environment" you can type in what you prefer your access details to be. In addition, the "/WO_DB_Tables_Initialization.sql:/docker-entrypoint-initdb.d/1.sql" under "volumes" enables me to initialize my MariaDB instance with a SQL script I have already put in the directory where the MariaDB instance is installed (The script can be found [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/5.%20SQL%20Queries/BigQuery/WO_DB_Tables_Initialization.sql)).

Next, edit the code below with details pertinent to your github account and repository. Remember the Cloud storage private key that was downloaded to your computer during the cloud storage setup? Please also add that Private Key file (should be a '.json' file) to the custom github repository, then proceed to the next step.

    git clone https://<your github access token goes here>@github.com/<github account name>/<repository name>.git gcp_mage_pipeline \
    && cd gcp_mage_pipeline \
    && cp dev.env .env && rm dev.env \
    && docker compose up

Run the above code in the bash terminal.

If you get a permission denied error when spinning up the container instance, then try running the below code:

    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker

Now check to see if the access is still denied by verifying that the code below works:

    docker run hello-world

If there's still an error, try reading this thread for tips: [Stack Overflow Thread](https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue).

Mage and MariaDB should run on the External IP address of your VM plus the respective ports specified.

For example, mage should run on "XX.XX.XX.XXX:6789" and Maria DB can be logged into via the server host IP of XX.XX.XX.XXX and port of 3306. Mage by default runs on  port 6789, while Maria DB runs on port 3306.


## Accessing MariaDB
Once the 'docker compose up' command has been run as shown earlier, you can use any SQL administration tool to access the DB. In my case, I'll use HeidiSQL to access the DB. After opening HeidiSQL, create a new session, select the "Network type" as MariaDB, for "Hostname / IP" use the IP address for your server instance in compute engine (Which is where your Docker container that contains Maria DB is running). Finally enter the username, password, and port specified in the docker compose script previously.

![mariadb_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mariadb_1.png)

If everything has been setup properly, when you login to access the database, you should see the following empty tables below:

![mariadb_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mariadb_2.png)


## Configuring Mage Instance
Log onto the Mage instance on your web browser using the socket address: "XX.XX.XX.XXX:6789". Replace XX.XX.XX.XXX with the IP address for your server instance in compute engine. Once you login, select Pipelines on the left bar, and then create a new pipeline. I'll select 'Standard (batch)' for the type of pipeline and then name the pipeline.

![mage_pipeline_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_1.png)

![mage_pipeline_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_2.png)

Once created, select 'Edit pipeline' to begin configuring your pipeline and also create the elements inside it.

![mage_pipeline_2a](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_2a.png)

To configure the pipeline, we need to set our Google Cloud and MariaDB variables in the 'io_config.yaml' file. Click on it and edit based on the details for your GCP and MariaDB services. Note that the 'GOOGLE_SERVICE_ACC_KEY_FILEPATH' should be the relative path to the GCP private key downloaded earlier and added to your custom github repository. That json private key file would be in home folder of your Mage instance. In addition, the 'GOOGLE_LOCATION' should be the server location where the GCP Bucket was created - in my case it is 'africa-south1'. The rest of the 'GOOGLE_SERVICE_ACC_KEY' parameters can be commented out and ignored.

![mage_pipeline_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_4.png)

![mage_pipeline_5](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_5.png)


# Extracting the Data using Mage
Create a new 'data loader' block in your pipeline to get started. Since we want to connect to our Cloud Storage bucket in GCP and extract the work order data, we can select the 'Google Cloud Storage' block.

![mage_pipeline_14](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_14.png)

Here the code snippet that helps connect to the Google Cloud Storage API and convert the resulting object into a Dataframe in Mage.

    @data_loader
    def load_from_google_cloud_storage(*args, **kwargs):
        """
        Loading data from a Google Cloud Storage bucket.
        Specify your configuration settings in 'io_config.yaml'.

        Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
        """
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        bucket_name = 'work_order_gcp_mage_pipeline-cloudgeek' # Specify the Bucket name
        object_key = 'work-order-management-module.csv' # Specify the file name in the Bucket

        response = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
            bucket_name,
            object_key,
        )
        return response

View the full source code for this step [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/6.%20Mage%20ETL/extract_phase.py).

In addition, we also need to get the last ID for each of the tables in MariaDB/BigQuery so that when our batch pipeline runs, it appends new surrogate IDs for each element in the tables, making sure there is no clash of IDs. Hence, I'll create another 'data loader' block as part of our Extraction phase which will later on feed the Transformation phase.

Here is a snippet of the code that'll help us do that:

    @data_loader
    def load_data_from_mysql(*args, **kwargs) -> dict:
        # Database configuration settings are specified in 'io_config.yaml'
        db_tables_and_IDs = {
            'service_request_': 'ServiceRequest_ID',
            'wo_activity_': 'Activity_ID',
            'started_': 'Started_ID',
            'completed_': 'Completed_ID',
            'added_': 'Added_ID',
            'work_order_fact': 'WorkOrder_ID'
        }
        
        max_ids = {}
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'
        
        with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            for table, primary_key in db_tables_and_IDs.items():
                query = f'SELECT MAX({primary_key}) AS max_id FROM {table}'
                result = loader.load(query)
                max_ids[table] = result['max_id'][0] if not result.empty else None  # Store the max ID in the dictionary
        return max_ids

View the full source code for this step [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/6.%20Mage%20ETL/get_max_ids.py).


# Transforming the Data in Mage
I'll use the Mage transformer block to carry out data cleaning and transformation steps, then I'll also create our fact and dimension tables (based on the schema shown earlier). The Transformer block in Mage is very useful as it ensures that data is standardized and prepared for downstream analysis, i.e. when we want to export/load data to the database/data warehouse. In the mage transformer ensure to import the pandas library in python i.e. "import pandas as pd".

View the full source code for the Mage transformation step [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/6.%20Mage%20ETL/transform_phase.py).

The Mage script should work fine, however, for the sake of understanding each of the steps in the data transformation (which is the 'T' in ETL), I have replicated the transformation process in Jupyter notebooks (See full Jupyter Notebook [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/6.%20Mage%20ETL/bin/WorkOrder%20Module%20Data%20Transformation%20in%20Jupyter%20Notebook.ipynb)) and I'll use the notebook outputs to show the transformation results for the steps.

The [Source data](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/1.%20Source%20Data/work-order-management-module.csv) loaded as a dataframe shows that it contains 206,058 Rows and 7 Columns as seen below:

![source_dataset_info](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/source_dataset_info.png)

![source_dataset_info_head](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/source_dataset_info_head.png)


## Cleaning the data
In this step, I'll deal with out-of-range data (specifically for time values), impose Data type constraints, find and remove duplicate values.

Here are a few things we need to do in the data cleaning step:
- Remove the last column called 'TIME_STAMP' as it only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.
- Capture 'out of range' dates in Datetime Columns and export to VM for record keeping.
- Converting the out of range values to 'NA' values.
- Enforce data type constraints for each column.
- Enforce data type 'length' constraints for each column.
- Remove duplicate data.


### Removing column(s) excluded from analysis
The 'TIME_STAMP' column is not included in the analysis. It only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project. I'll remove it using the '.drop' method in pandas.
    
    df = data
    df = df.drop(columns=['TIME_STAMP'])


### Dealing with 'Out of Range' Datetime values
In this step, we'd extract all the out of range date values for the 'WORKORDER_STARTED', 'WORKORDER_COMPLETED', 'WORKORDER_ADDED' columns. To do this, I'll use the 'to_datetime' method to convert all the non-null data in each column to a datetime object. If the conversion fails, it means that the data is not in the datetime range or is not a valid input. Here is a snippet of the code:

    invalid_dates = pd.DataFrame()

    for element in date_columns:
        # where to_datetime fails. 
        # dt means datetime
        not_dt = pd.to_datetime(df[element], errors='coerce')

        # where column is not null and to_datetime method fails. 
        # ofr means out of range
        ofr_dt = not_dt.isna() & df[element].notnull()
        
        # Important to do the previous step as there are several blank rows for the Datetime, which makes sense because the Work order may not have been started and/or completed at the time of processing the data. So we are looking for 'not null' rows that are also incorrect datetimes.
        
        ofr_dt_ = df[[element, "WORKORDER_NUMBER"]].loc[ofr_dt == True]
        ofr_dt_ = pd.DataFrame(ofr_dt_)
        ofr_dt_ = ofr_dt_.assign(Time_type = element)
        ofr_dt_ = ofr_dt_.rename(columns={element: "Wrong_Datetimes"})
        
        invalid_dates = pd.concat([invalid_dates, ofr_dt_])

After the conversion, if there are indeed invalid dates, we would then save it in a spreadsheet on the VM as shown below:

    if not invalid_dates.empty:
        invalid_dates.to_csv('/home/src/cleaning_export_wrong_dates.csv')

![compute_engine_7](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_7.png)

![Out_of_range_datetimes](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/Out_of_range_datetimes.png)

Finally for this step, I'll convert the out of range values and blank rows to 'NULL'.

    # Converting the out of range values and blank rows to NA values
    # Attempt to infer format of each date, and return NA for rows where conversion failed
    for element in date_columns:
        df[element] = pd.to_datetime(df[element], infer_datetime_format=True, errors = 'coerce') 


### Enforcing datatypes and datatype length constraints
I'll make sure all the columns are of the right data type and length so that processing downstream (e.g. to the Database) is easy. Here is a snippet of the code:

    # Enforce WORKORDER_ACTIVITY_CODE and WORKORDER_ACTIVITY_DESCRIPTION to 'String' type

    df['WORKORDER_ACTIVITY_CODE'] = df['WORKORDER_ACTIVITY_CODE'].astype('str')
    df['WORKORDER_ACTIVITY_DESCRIPTION'] = df['WORKORDER_ACTIVITY_DESCRIPTION'].astype('str')

    # String length constraints on WORKORDER_ACTIVITY_CODE and WORKORDER_ACTIVITY_DESCRIPTION
    # Truncate the specified column to specific length of characters
    df['WORKORDER_ACTIVITY_CODE'] = df['WORKORDER_ACTIVITY_CODE'].str.slice(stop=12)
    df['WORKORDER_ACTIVITY_DESCRIPTION'] = df['WORKORDER_ACTIVITY_DESCRIPTION'].str.slice(stop=300)

    # Assert the data type of WORKORDER_NUMBER is int64
    assert df['WORKORDER_NUMBER'].dtype == 'int64', "WORKORDER_NUMBER should be int64"

    # Assert the data type of WORKORDER_STARTED is datetime64
    assert pd.api.types.is_datetime64_any_dtype(df['WORKORDER_STARTED']), "WORKORDER_STARTED should be datetime64"

    # Assert the data type of WORKORDER_ACTIVITY_CODE is object (string)
    assert df['WORKORDER_ACTIVITY_CODE'].dtype == 'object', "WORKORDER_ACTIVITY_CODE should be object (string)"


### Removing Duplicate Records
Next, we need to remove duplicate values on the dataset. Here is a snippet of the code:

    # Drop duplicates based on 'WORKORDER_NUMBER' column and reset the index
    df = df.drop_duplicates(subset=['WORKORDER_NUMBER']).reset_index(drop=True)
    
    # Create a new column called 'WorkOrderID' for the index
    df['WorkOrderID'] = df.index
    
    # Rearrange the column order
    df = df[['WorkOrderID', 
            'WORKORDER_NUMBER', 
            'WORKORDER_ACTIVITY_CODE', 
            'WORKORDER_ACTIVITY_DESCRIPTION', 
            'SVC_REQUEST_NUMBER', 
            'WORKORDER_STARTED', 
            'WORKORDER_COMPLETED', 
            'WORKORDER_ADDED']]

We have removed 10,030 Duplicate Records and the datatypes are appropriate for downstream analysis as shown below:

![cleaned_source_dataset_info](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/cleaned_source_dataset_info.png)


## Creating Fact and Dimension Tables
In this step, I'll create 6 tables according to the database schema and map the cleaned data to these tables. 

![Schema - WorkOrderModule DB](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/4.%20Database%20Schema/Schema%20-%20WorkOrderModule%20DB.png)

But before we start with that, we need to ensure the Max IDs for each table from the earlier data loading step is incorporated here in the transformation step. If there is no Max ID from the data loading step earlier, then it most likely means that the individual table is empty and we need to initialize the Max ID variable as zero (0). Here is a snippet of the code:

    # 'max_ids' dictionary containing max IDs for each table
    max_ids = data_2

    for key, value in max_ids.items():
        if value is None:
            max_ids[key] = 0

Next we create dimension tables for the Work Order Activity ("activity_df"), Service Request ("service_request_df"), and Time Dimensions (Time added, started, completed). Here is a snippet of the code:

    # Extract unique Activity data
    activity_df = df[['WORKORDER_ACTIVITY_CODE', 'WORKORDER_ACTIVITY_DESCRIPTION']].drop_duplicates().dropna().rename(
        columns={'WORKORDER_ACTIVITY_CODE': 'ActivityCode', 'WORKORDER_ACTIVITY_DESCRIPTION': 'ActivityDescription'}
    )
    activity_df['Activity_ID'] = range(max_ids['wo_activity_'] + 1, max_ids['wo_activity_'] + 1 + len(activity_df))

    # Map Activity IDs back to the main DataFrame
    df = df.merge(activity_df, left_on='WORKORDER_ACTIVITY_CODE', right_on='ActivityCode', how='left')


    # Extract unique Started datetime data, and generate IDs starting from max IDs in `max_ids`
    started_df = df[['WORKORDER_STARTED']].dropna().reset_index(drop=True).rename(
        columns={'WORKORDER_STARTED': 'Date_time'}
    )
    started_df['Started_ID'] = range(max_ids['started_'] + 1, max_ids['started_'] + 1 + len(started_df))

    df = df.merge(started_df, left_on='WORKORDER_STARTED', right_on='Date_time', how='left')

You'd notice that while creating the activity_df table, the .drop_duplicates() is used but not while creating the started_df table. This is because we don't want to remove duplicates for the Time dimensions, since there will be many instances (confirmed from parsing through the data) where the different Work orders instances can have identical datetime values.

Finally we create the main fact table (work_order_fact_df) as shown in the schema.

    # Create the work_order_fact table with unique WorkOrder_IDs
    work_order_fact_df = df[['WorkOrderID', 'Activity_ID', 'ServiceRequest_ID', 'Started_ID', 'Completed_ID', 'Added_ID', 'WORKORDER_NUMBER']].rename(
        columns={
            'WorkOrderID': 'WorkOrder_ID',
            'WORKORDER_NUMBER': 'WorkOrderNumber'
        }
    )

    work_order_fact_df['WorkOrder_ID'] = range(max_ids['work_order_fact'] + 1, max_ids['work_order_fact'] + 1 + len(work_order_fact_df))

We can now put all the transformed tables in a dictionary/hashmap 'work_order_dict' for further processing downstream of the data pipeline.

    work_order_dict = {"wo_activity_" : activity_df.to_dict(),
        "service_request_" : service_request_df.to_dict(),
        "started_" : started_df.to_dict(),
        "completed_" : completed_df.to_dict(),
        "added_" : added_df.to_dict(),
        "work_order_fact" : work_order_fact_df.to_dict()
        }

We can verify the resulting tables as seen below:

![fact_and_dimension_tables](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/fact_and_dimension_tables.png)

Also key to note that the Mage pipeline blocks natively give room for testing code. For the transformation step, here is a snippet of the testing function that is run for the block:

    @test
    def test_output(output, *args) -> None:
        """
        Test the output to ensure it is a valid dictionary with expected keys and structure.
        """
        # Check that the output is a dictionary
        assert isinstance(output, dict), 'The output is not a dictionary'
        
        # Define expected keys in the output dictionary
        expected_keys = ["wo_activity_", "service_request_", "started_", "completed_", "added_", "work_order_fact"]
        
        # Check that all expected keys are present in the output dictionary
        missing_keys = [key for key in expected_keys if key not in output]
        assert not missing_keys, f'Missing keys in output: {missing_keys}'
        
        # Check each key's value type to ensure they are DataFrame-like dictionaries
        for key in expected_keys:
            assert isinstance(output[key], dict), f'The value for key {key} is not a dictionary'
        
        # Check that the main DataFrame dictionary (work_order_fact) is not empty
        assert output["work_order_fact"], "The work_order_fact dictionary is empty"


# Loading the Data to MariaDB and BigQuery Data Warehouse
in this step, I'll setup Google BigQuery, then I will configure the Mage Exporter to load data into MariaDB and BigQuery. Finally, I will create views in BigQuery to later aid my Data Visualization step in Looker Studio.


## Setting up Google BigQuery
Open the BigQuery studio from the google cloud console, click on the 3 dots next to the project name and click on 'Create dataset'. Pick a name for your dataset, specify the location type, region and create the dataset. Note the Dataset ID to use in the Mage Exporter.

![bigquery_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_1.png)

![bigquery_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_2.png)

![bigquery_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_3.png)


## Mage Data Exporter
I'll create two exporter blocks - one for MariaDB and one for BigQuery. For the exporter blocks, every time we run the batch pipeline, it'll append the new data to the Database and BigQuery Data Warehouse. You don't need to manually create the tables in BigQuery dataset, as it would create it automatically on the first run. Here is a snippet of the code:

Export to MariaDB

    @data_exporter
    def export_data_to_mysql(data, **kwargs) -> None:
        """
        Exporting data to the MariaDB database.
        Configuration settings are in 'io_config.yaml' which is in mage server.

        Docs: https://docs.mage.ai/design/data-loading#mysql
        """
        for key, value in data.items():
            table_name = '{}'.format(key)  # Specify the name of the table to export data to
            config_path = path.join(get_repo_path(), 'io_config.yaml')
            config_profile = 'default'

            with MySQL.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
                loader.export(
                    DataFrame(value),
                    schema_name=None,
                    auto_clean_name=False,
                    table_name=table_name,
                    index=False,  # Specifies whether to include index in exported table
                    if_exists='append',  # Specify resolution policy if table name already exists
                )

Export to BigQuery
    
    @data_exporter
    def export_data_to_big_query(data, **kwargs) -> None:
        """
        Exporting data to the BigQuery Data Warehouse.
        Configuration settings are in 'io_config.yaml' which is in mage server.

        Docs: https://docs.mage.ai/design/data-loading#bigquery
        """   
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'
        
        for key, value in data.items():
            table_id = 'data-pipelines-437522.WorkOrderModule.{}'.format(key)  # Specify the name of the dataset and table to export data to
            BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
                DataFrame(value),
                table_id,
                if_exists='append',  # Specify resolution policy if table name already exists
            )

Once the export is done we can verify the results in HeidiSQL for the database and in BigQuery as well.

![mariadb_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mariadb_3.png)

![mariadb_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mariadb_4.png)

![bigquery_4](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_4.png)

![bigquery_5](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_5.png)


# Mage Data Orchestration Summary
A wholistic view of the ETL pipeline is shown below. In the Extract (E) step, the source data is extracted from Cloud storage on GCP, then the Highest IDs for the tables are gotten from the MariaDB database. In the Transform (T) step, the data is cleaned, and processed to give dimension and fact tables. This data is then taken to the final stage which is the Load (L) step, where the data is loaded to MariaDB and the BigQuery data warehouse.

![mage_pipeline_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_3.png)


## Creating Views on BigQuery
In Bigquery, I'll run a few queries to get the:
- Resolution rate of Work Orders
- Oldest Work Orders (Backlog)
- Cumulative Backlog Count
- Completed versus Not Completed Work Order Ratio

Here's a snippet of the SQL query to get the resolution rate of the Work Orders:

    SELECT CAST(FLOOR((COUNT(fact_.Completed_ID) / COUNT(fact_.WorkOrderNumber))*100) AS INT64) AS Resolution_Rate, 
        EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) AS Year_Added

    FROM `WorkOrderModule.work_order_fact` AS fact_
    LEFT JOIN `WorkOrderModule.added_` AS add_ on fact_.Added_ID = add_.Added_ID

    WHERE EXTRACT(YEAR FROM PARSE_DATETIME('%Y-%m-%dT%H:%M:%S', add_.Date_time)) IS NOT NULL
    GROUP BY Year_Added
    ORDER BY Year_Added DESC;

View all the queries [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/tree/main/5.%20SQL%20Queries/BigQuery).

Next, I'll save each query as a view in BigQuery. 

![bigquery_6](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_6.png)

![bigquery_7](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/bigquery_7.png)


## Extracting Backlog Data from BigQuery using Mage
In this step, I'll create another Mage pipeline to extract all the backlog work orders. I define backlog as work orders that have not been completed in over 3 years. Inside this new pipeline, I'll create a single data loader block to extract the Backlog data from BigQuery. Once I extract them, I'll save them to the VM.

![mage_pipeline_11](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_11.png)

![mage_pipeline_12](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_12.png)

Here's a snippet of the data loader block in Mage. The block will extract the data from the 'Oldest_WorkOrders' View in BigQuery and then save to the VM.

    @data_loader
    def load_data_from_big_query(*args, **kwargs):
        """
        Extracting data from the BigQuery Data Warehouse.
        Configuration settings are in 'io_config.yaml' which is in mage server.

        Docs: https://docs.mage.ai/design/data-loading#bigquery
        """
        query = 'SELECT * FROM `data-pipelines-437522.WorkOrderModule.Oldest_WorkOrders`'
        
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'
        backlog = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
        if not backlog.empty:
            backlog.to_csv('/home/src/backlog.csv')
        
        return backlog

View the full source code for this step [here](https://github.com/OlajideOlagunju/GCP_Mage_Data_Pipeline/blob/main/6.%20Mage%20ETL/extract_backlog.py).

I can verify the Work Order Backlog list is saved on the VM as seen below:

![compute_engine_8](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/compute_engine_8.png)

![backlog_list](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/backlog_list.png)


## Scheduling Pipeline Runs via Mage Triggers
Next, I'll schedule the pipeline to run daily. On the left pane, select 'Triggers', then click to create a new trigger. For this pipeline, I'll select the trigger type as 'Schedule' and frequency to 'Daily'. I'll also replicate the same for the Backlog list pipeline and schedule it to 'Monthly'.

![mage_pipeline_6](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_6.png)

![mage_pipeline_7](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_7.png)

![mage_pipeline_8](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_8.png)

![mage_pipeline_13](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_13.png)

Next, we'll enable the trigger. You can run the trigger once to test the pipeline if you'd like. In addition, if you click the icon under 'Logs' you can see the status of the pipeline running. If there are errors on the pipeline, you can pinpoint them and troubleshoot.

![mage_pipeline_9](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_9.png)

![mage_pipeline_10](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/mage_pipeline_10.png)


# Data Viz - Setting up Google Looker Studio
The final step here is to setup our data visualization in Google Looker Studio. Open [Looker Studio](https://lookerstudio.google.com/), then click on create, select 'Report', then add your BigQuery Data source to the Report. You will need to add the four Views (Tables) that we created in BigQuery to this Report.

![looker_1](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/looker_1.png)

![looker_2](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/looker_2.png)

![looker_3](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/looker_3.png)

Once done, configure your report / visualizations based on your preference. For a good tutorial on using Looker Studio, visit this [link](https://measureschool.com/looker-studio-charts/).

My visualization can be viewed via this [link](https://lookerstudio.google.com/reporting/cf1ba5c7-4392-40b6-af22-c29703d6357c/page/pfFWE) and below:

![looker_5](https://github.com/OlaOlagunju/GCP_Mage_Data_Pipeline/blob/main/8.%20Images/looker_5.jpg)


# Conclusion
Through the solution created, the main business needs for my client has been met. I am able to automatically ingest the maintenance work orders from spreadsheets on a daily schedule, transform them, load them to database / data warehouse and finally visualize the data. The key metric 'Resolution Rate' can be monitored by the client through this Dashboard.

The functional and non-functional requirements for this solution have been carefully considered in the design and implementation, and this pipeline can be scaled up / improved when there is a technical and practical reason to do so.