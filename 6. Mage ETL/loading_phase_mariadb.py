from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mysql import MySQL
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


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