from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_big_query(*args, **kwargs):
    """
    Extracting data from the BigQuery Data Warehouse.
    Configuration settings are in 'io_config.yaml' which is in mage server.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    query = 'SELECT * FROM `data-pipelines-437522.WorkOrderModule.Backlog`'
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    backlog = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
    if not backlog.empty:
        backlog.to_csv('/home/src/backlog.csv')
    
    return backlog


@test
def test_output(output, *args) -> None:
    """
    Test the output to ensure it is a valid DataFrame.
    """
    # Check that the Table is not empty
    assert not output.empty, 'The output is empty'