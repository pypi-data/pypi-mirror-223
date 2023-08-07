from io import BytesIO
from pickle import dump
from werkzeug.datastructures import FileStorage
import pandas as pd
import os
from .lib import post_data
from typing import Optional


def create_file_storage_from_data(df: pd.DataFrame) -> FileStorage:
    """
    .. py:method:: Create a FileStorage object from a DataFrame.

    :param df: pd.DataFrame: The DataFrame object to be stored.
    :return: FileStorage: The FileStorage object containing the DataFrame.
    """
    # Create a stream object from the DataFrame
    stream = BytesIO()
    dump(df, stream)
    stream.seek(0)  # Reset the stream pointer to the beginning
    # Create a FileStorage object from the stream
    file_storage = FileStorage(
        stream, filename="dataframe.pkl", content_type="application/octet-stream"
    )
    return file_storage


def commit_dataset(
    dataset_name: Optional[str],
    dataset_category: Optional[str],
    dataset_id: Optional[str],
    data_file_storage: FileStorage,
    access_token: str,
    api_host: str,
) -> Optional[str]:
    """
    .. py:method:: Commit a dataset file.

    :param dataset_name: str: The name of the dataset.
    :param dataset_category: str: The category of the dataset.
    :param dataset_id: str: The ID of the dataset.
    :param data_file_storage: FileStorage: The FileStorage object containing the dataset file.
    :param access_token: str: The access token for the API.
    :param api_host: str: The host URL for the API.
    :return: str: The ID of the committed dataset if successful
    """
    url = os.path.join(api_host, "dataset", "app", "commit_file")
    url = url.replace("\\", "/")

    headers = {"authorization": "Bearer " + access_token}
    data = {
        "dataset_name": dataset_name,
        "dataset_category": dataset_category,
        "dataset_id": dataset_id,
    }

    response = post_data(
        url=url, headers=headers, data=data, files={"file": data_file_storage}
    )
    if response.status_code == 200:
        return response.json()["dataset_id"]

    return None
