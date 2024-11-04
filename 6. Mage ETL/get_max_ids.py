from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mysql import MySQL
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

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

@test
def test_output(output, *args) -> None:
    # Test to ensure all tables have max ID values
    assert isinstance(output, dict), 'Output should be a dictionary'
    for table in ['service_request_', 'wo_activity_', 'started_', 'completed_', 'added_', 'work_order_fact']:
        assert table in output, f'Missing max ID for table {table}'
