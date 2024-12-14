from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'work_order_gcp_mage_pipeline-cloudgeek'
    object_key = 'work-order-management-module.csv'

    response = GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )
    return response


@test
def test_output(output, *args) -> None:
    """
    Test the output to ensure it is a valid DataFrame.
    """
    # Check that the DataFrame is not empty
    assert not output.empty, 'The output DataFrame is empty'