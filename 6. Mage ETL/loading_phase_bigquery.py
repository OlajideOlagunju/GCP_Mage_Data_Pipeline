from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Exporting data to the BigQuery Data Warehouse.
    Configuration settings are in 'io_config.yaml' which is in mage server.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """

    for key, value in data.items():
        table_id = 'data-pipelines-437522.WorkOrderModule.{}'.format(key)  # Specify the name of the table to export data to
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            DataFrame(value),
            auto_clean_name=False,
            table_id,
            if_exists='append',  # Specify resolution policy if table name already exists
        )
