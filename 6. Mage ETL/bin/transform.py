import pandas as pd
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    
    # Cleaning the Data

    # ---------------------------------------------------------------------------------------

    # Removing Columns not useful for analysis

    # The 'TIME_STAMP' column is not included in the analysis.
    # It only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.

    df = df.drop(columns=['TIME_STAMP'])


    # ---------------------------------------------------------------------------------------

    # Out of Range Datetime Values

    # Capture and export invalid out of range dates in Datetime Columns

    def get_out_of_range_datetimes(time_description):
        invalid_dates = pd.DataFrame()

        for element in time_description:
            # where to_datetime fails. 
            # dt means datetime
            not_dt = pd.to_datetime(df[element], errors='coerce')

            # where column is not null and to_datetime method fails. 
            # ofr means out of range
            ofr_dt = not_dt.isna() & df[element].notnull()
            
            # Important to do the previous step as there are several blank rows for the Datetime,
            # which makes sense because the Work order may not have been started and/or
            # completed at the time of processing the data. 
            # So we are looking for 'not null' rows that are also incorrect datetimes.
            
            ofr_dt_ = df[[element, "WORKORDER_NUMBER"]].loc[ofr_dt == True]
            ofr_dt_ = pd.DataFrame(ofr_dt_)
            ofr_dt_ = ofr_dt_.assign(Time_type = element)
            ofr_dt_ = ofr_dt_.rename(columns={element: "Wrong_Datetimes"})
            
            invalid_dates = pd.concat([invalid_dates, ofr_dt_])
            
        return invalid_dates

    date_columns = ['WORKORDER_STARTED', 'WORKORDER_COMPLETED', 'WORKORDER_ADDED']

    cleaning_export_wrong_dates = get_out_of_range_datetimes(date_columns)

    if not cleaning_export_wrong_dates.empty:
        cleaning_export_wrong_dates.to_csv('cleaning_export_wrong_dates.csv')

        
        
    # Converting the out of range values and blank rows to NA values

    # Attempt to infer format of each date, and return NA for rows where conversion failed
    for element in date_columns:
        df[element] = pd.to_datetime(df[element], infer_datetime_format=True, errors = 'coerce') 

        
    # ---------------------------------------------------------------------------------------

    # Data Type Constraints

    # Enforce WORKORDER_ACTIVITY_CODE and WORKORDER_ACTIVITY_DESCRIPTION to 'String' type

    df['WORKORDER_ACTIVITY_CODE'] = df['WORKORDER_ACTIVITY_CODE'].astype('str')
    df['WORKORDER_ACTIVITY_DESCRIPTION'] = df['WORKORDER_ACTIVITY_DESCRIPTION'].astype('str')

    # String length constraints on WORKORDER_ACTIVITY_CODE and WORKORDER_ACTIVITY_DESCRIPTION
    # Truncate the specified column to specific length of characters
    df['WORKORDER_ACTIVITY_CODE'] = df['WORKORDER_ACTIVITY_CODE'].str.slice(stop=12)
    df['WORKORDER_ACTIVITY_DESCRIPTION'] = df['WORKORDER_ACTIVITY_DESCRIPTION'].str.slice(stop=300)

    # Assert the data type of WORKORDER_NUMBER is int64
    assert df['WORKORDER_NUMBER'].dtype == 'int64', "WORKORDER_NUMBER should be int64"

    # Assert the data type of SVC_REQUEST_NUMBER is int64
    assert df['SVC_REQUEST_NUMBER'].dtype == 'int64', "SVC_REQUEST_NUMBER should be int64"

    # Assert the data type of WORKORDER_STARTED is datetime64
    assert pd.api.types.is_datetime64_any_dtype(df['WORKORDER_STARTED']), "WORKORDER_STARTED should be datetime64"

    # Assert the data type of WORKORDER_COMPLETED is datetime64
    assert pd.api.types.is_datetime64_any_dtype(df['WORKORDER_COMPLETED']), "WORKORDER_COMPLETED should be datetime64"

    # Assert the data type of WORKORDER_ADDED is datetime64
    assert pd.api.types.is_datetime64_any_dtype(df['WORKORDER_ADDED']), "WORKORDER_ADDED should be datetime64"

    # Assert the data type of WORKORDER_ACTIVITY_CODE is object (string)
    assert df['WORKORDER_ACTIVITY_CODE'].dtype == 'object', "WORKORDER_ACTIVITY_CODE should be object (string)"

    # Assert the data type of WORKORDER_ACTIVITY_DESCRIPTION is object (string)
    assert df['WORKORDER_ACTIVITY_DESCRIPTION'].dtype == 'object', "WORKORDER_ACTIVITY_DESCRIPTION should be object (string)"


    # ---------------------------------------------------------------------------------------

    # Removing Duplicate Data

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

    # Extract 'wo_activity_' table
    wo_activity_dim = df[['WORKORDER_ACTIVITY_CODE', 'WORKORDER_ACTIVITY_DESCRIPTION']].drop_duplicates().rename(
        columns={'WORKORDER_ACTIVITY_CODE': 'ActivityCode', 'WORKORDER_ACTIVITY_DESCRIPTION': 'ActivityDescription'}
    ).reset_index(drop=True)
    wo_activity_dim['ActivityID'] = range(1, len(wo_activity_dim) + 1)  # Assign unique IDs

    # Extract 'service_request_' table
    service_request_dim = df[['SVC_REQUEST_NUMBER']].drop_duplicates().rename(
        columns={'SVC_REQUEST_NUMBER': 'ServiceRequestNumber'}
    ).reset_index(drop=True)
    service_request_dim['ServiceRequest_ID'] = range(1, len(service_request_dim) + 1)  # Assign unique IDs

    # Static Data for 'wo_time_type_' and 'day_of_week_' tables
    wo_time_type_dim = pd.DataFrame({
        'TimeType_ID': [1, 2, 3],
        'Time_Type': ['Started', 'Completed', 'Added']
    })

    day_of_week_dim = pd.DataFrame({
        'Day_of_week_ID': range(1, 8),
        'DayInWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    })


    # Create 'work_order_time_' table
    # Flatten out the dates from the original DataFrame
    work_order_time_started = df[['WorkOrderID', 'WORKORDER_STARTED']].dropna().rename(columns={'WORKORDER_STARTED': 'Time'})
    work_order_time_completed = df[['WorkOrderID', 'WORKORDER_COMPLETED']].dropna().rename(columns={'WORKORDER_COMPLETED': 'Time'})
    work_order_time_added = df[['WorkOrderID', 'WORKORDER_ADDED']].rename(columns={'WORKORDER_ADDED': 'Time'})

    # Add a TimeType_ID (1 for Started, 2 for Completed, 3 for Added)
    work_order_time_started['TimeType_ID'] = 1
    work_order_time_completed['TimeType_ID'] = 2
    work_order_time_added['TimeType_ID'] = 3

    # Concatenate these records and extract the date parts
    work_order_time = pd.concat([work_order_time_started, work_order_time_completed, work_order_time_added], ignore_index=True)
    work_order_time['Year'] = work_order_time['Time'].dt.year
    work_order_time['Month'] = work_order_time['Time'].dt.month
    work_order_time['Day'] = work_order_time['Time'].dt.day
    work_order_time['Hour'] = work_order_time['Time'].dt.hour
    work_order_time['Minute'] = work_order_time['Time'].dt.minute
    work_order_time['Second'] = work_order_time['Time'].dt.second
    work_order_time['Day_of_week_ID'] = work_order_time['Time'].dt.dayofweek + 1  # Assuming 1=Monday, ..., 7=Sunday

    # Add a unique Time_ID for each record
    work_order_time['Time_ID'] = range(1, len(work_order_time) + 1)

    # Select final columns for 'work_order_time_'
    work_order_time = work_order_time.rename(columns={'WorkOrderID': 'WorkOrder_ID'})[['WorkOrder_ID', 'Time_ID', 'TimeType_ID', 'Day_of_week_ID', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']]

    # Create 'work_order_fact' table
    # Merge with 'wo_activity_' to get ActivityID
    work_order_fact = df.merge(wo_activity_dim, left_on='WORKORDER_ACTIVITY_CODE', right_on='ActivityCode', how='left')
    work_order_fact = work_order_fact.merge(service_request_dim, left_on='SVC_REQUEST_NUMBER', right_on='ServiceRequestNumber', how='left')

    work_order_fact = work_order_fact.rename(columns={
        'WorkOrderID': 'WorkOrder_ID', 
        'WORKORDER_NUMBER': 'WorkOrderNumber', 
        'ActivityID': 'Activity_ID', 
        'ServiceRequest_ID': 'ServiceRequest_ID'
    })[['WorkOrder_ID', 'Activity_ID', 'ServiceRequest_ID', 'WorkOrderNumber']]

    # Add columns for Time_IDs in the fact table
    work_order_fact = work_order_fact.merge(
        work_order_time[work_order_time['TimeType_ID'] == 1][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'TimeID_Started'}),
        on='WorkOrder_ID', how='left'
    )

    work_order_fact = work_order_fact.merge(
        work_order_time[work_order_time['TimeType_ID'] == 2][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'TimeID_Completed'}),
        on='WorkOrder_ID', how='left'
    )

    work_order_fact = work_order_fact.merge(
        work_order_time[work_order_time['TimeType_ID'] == 3][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'TimeID_Added'}),
        on='WorkOrder_ID', how='left'
    )

    # Final columns for the work_order_fact table, including Time_IDs
    work_order_fact = work_order_fact[['WorkOrder_ID', 'Activity_ID', 'ServiceRequest_ID', 'WorkOrderNumber', 'TimeID_Started', 'TimeID_Completed', 'TimeID_Added']]

    # Flatten the data by merging work_order_fact with each time type
    work_order_fact_flat = pd.concat([
        work_order_fact.merge(
            work_order_time[work_order_time['TimeType_ID'] == 1][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'Time_ID'}),
            on='WorkOrder_ID', how='inner'
        ).assign(TimeType_ID=1),
        
        work_order_fact.merge(
            work_order_time[work_order_time['TimeType_ID'] == 2][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'Time_ID'}),
            on='WorkOrder_ID', how='inner'
        ).assign(TimeType_ID=2),
        
        work_order_fact.merge(
            work_order_time[work_order_time['TimeType_ID'] == 3][['WorkOrder_ID', 'Time_ID']].rename(columns={'Time_ID': 'Time_ID'}),
            on='WorkOrder_ID', how='inner'
        ).assign(TimeType_ID=3)
    ])

    # Select final columns for the flattened work_order_fact
    work_order_fact_flat = work_order_fact_flat[['WorkOrder_ID', 'Activity_ID', 'ServiceRequest_ID', 'WorkOrderNumber', 'Time_ID']]


    return {"day_of_week_":day_of_week_dim.to_dict(orient="dict"),
    "wo_time_type_":wo_time_type_dim.to_dict(orient="dict"),
    "wo_activity_":wo_activity_dim.to_dict(orient="dict"),
    "service_request_":service_request_dim.to_dict(orient="dict"),
    "work_order_time_":work_order_time.to_dict(orient="dict"),
    "work_order_fact":work_order_fact_flat.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
