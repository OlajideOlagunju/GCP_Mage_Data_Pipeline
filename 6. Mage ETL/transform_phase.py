if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@transformer
def transform(data, data_2, *args, **kwargs): # data_2 is output from the get_max_IDs block. data is output from extraction_phase block.

    # Specify your transformation logic here
    
    # Cleaning the Data

    # ---------------------------------------------------------------------------------------

    # Removing Columns not useful for analysis

    # The 'TIME_STAMP' column is not included in the analysis.
    # It only shows the date that the data was exported from the Client's ERP to excel which is not relevant for our project.
    df = data
    df = df.drop(columns=['TIME_STAMP'])

    # ---------------------------------------------------------------------------------------

    # Out of Range Datetime Values

    # Capture and export invalid out of range dates in Datetime Columns
        
    date_columns = ['WORKORDER_STARTED', 'WORKORDER_COMPLETED', 'WORKORDER_ADDED']
    
    invalid_dates = pd.DataFrame()

    for element in date_columns:
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

    if not invalid_dates.empty:
        invalid_dates.to_csv('/home/src/cleaning_export_wrong_dates.csv')

        
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

    
    # 'max_ids' dictionary containing max IDs for each table
    max_ids = data_2

    for key, value in max_ids.items():
        if value is None:
            max_ids[key] = 0

    # Prepare the data transformations

    # Extract unique Activity data
    activity_df = df[['WORKORDER_ACTIVITY_CODE', 'WORKORDER_ACTIVITY_DESCRIPTION']].drop_duplicates().rename(
        columns={'WORKORDER_ACTIVITY_CODE': 'ActivityCode', 'WORKORDER_ACTIVITY_DESCRIPTION': 'ActivityDescription'}
    )
    activity_df['Activity_ID'] = range(max_ids['wo_activity_'] + 1, max_ids['wo_activity_'] + 1 + len(activity_df))

    # Extract unique Service Request data
    service_request_df = df[['SVC_REQUEST_NUMBER']].drop_duplicates().rename(
        columns={'SVC_REQUEST_NUMBER': 'ServiceRequestNumber'}
    )
    service_request_df['ServiceRequest_ID'] = range(max_ids['service_request_'] + 1, max_ids['service_request_'] + 1 + len(service_request_df))

    # Map Activity and Service Request IDs back to the main DataFrame
    df = df.merge(activity_df, left_on='WORKORDER_ACTIVITY_CODE', right_on='ActivityCode', how='left')
    df = df.merge(service_request_df, left_on='SVC_REQUEST_NUMBER', right_on='ServiceRequestNumber', how='left')

    # Function to extract time components
    def extract_time_components(datetime_series):
        return pd.DataFrame({
            'Year': datetime_series.dt.year,
            'Quarter': datetime_series.dt.quarter,
            'Month': datetime_series.dt.month,
            'Day_of_Week': datetime_series.dt.dayofweek,
            'Day': datetime_series.dt.day,
            'Hour': datetime_series.dt.hour,
            'Minute': datetime_series.dt.minute
        })

    # Create time component DataFrames for started, completed, and added times
    df_started_components = extract_time_components(df['WORKORDER_STARTED'])
    df_completed_components = extract_time_components(df['WORKORDER_COMPLETED'])
    df_added_components = extract_time_components(df['WORKORDER_ADDED'])

    # Unique Started, Completed, and Added tables with IDs starting from max IDs in `max_ids`
    started_df = df_started_components.drop_duplicates().reset_index(drop=True)
    started_df['Started_ID'] = range(max_ids['started_'] + 1, max_ids['started_'] + 1 + len(started_df))

    completed_df = df_completed_components.drop_duplicates().reset_index(drop=True)
    completed_df['Completed_ID'] = range(max_ids['completed_'] + 1, max_ids['completed_'] + 1 + len(completed_df))

    added_df = df_added_components.drop_duplicates().reset_index(drop=True)
    added_df['Added_ID'] = range(max_ids['added_'] + 1, max_ids['added_'] + 1 + len(added_df))

    # Merge Started, Completed, and Added IDs back to the main DataFrame using time components
    df = df.merge(
        df_started_components.merge(started_df, on=['Year', 'Quarter', 'Month', 'Day_of_Week', 'Day', 'Hour', 'Minute'], how='left'),
        left_index=True, right_index=True, suffixes=('', '_y')
    ).drop(columns=[col for col in df.columns if '_y' in col])

    df = df.merge(
        df_completed_components.merge(completed_df, on=['Year', 'Quarter', 'Month', 'Day_of_Week', 'Day', 'Hour', 'Minute'], how='left'),
        left_index=True, right_index=True, suffixes=('', '_y')
    ).drop(columns=[col for col in df.columns if '_y' in col])

    df = df.merge(
        df_added_components.merge(added_df, on=['Year', 'Quarter', 'Month', 'Day_of_Week', 'Day', 'Hour', 'Minute'], how='left'),
        left_index=True, right_index=True, suffixes=('', '_y')
    ).drop(columns=[col for col in df.columns if '_y' in col])

    # Create the work_order_fact table with unique WorkOrder_IDs
    work_order_fact_df = df[['WorkOrderID', 'Activity_ID', 'ServiceRequest_ID', 'Started_ID', 'Completed_ID', 'Added_ID', 'WORKORDER_NUMBER']].rename(
        columns={
            'WorkOrderID': 'WorkOrder_ID',
            'WORKORDER_NUMBER': 'WorkOrderNumber'
        }
    )

    work_order_fact_df['WorkOrder_ID'] = range(max_ids['work_order_fact'] + 1, max_ids['work_order_fact'] + 1 + len(work_order_fact_df))

    work_order_dict = {"wo_activity_" : activity_df.to_dict(),
        "service_request_" : service_request_df.to_dict(),
        "started_" : started_df.to_dict(),
        "completed_" : completed_df.to_dict(),
        "added_" : added_df.to_dict(),
        "work_order_fact" : work_order_fact_df.to_dict()
        }
    
    return work_order_dict


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
