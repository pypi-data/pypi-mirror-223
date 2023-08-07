import pandas as pd
import os
from typing import Optional
from .retrieve import get_dataframe, get_schema
from .lib import get_default_logger
from .dataset import create_file_storage_from_data, commit_dataset
from .converter import query_to_params
from .schema import Query, FieldsSchema


class APIClient(object):
    """API client with stateful authentication for lib functions and extra convenience methods."""

    def __init__(self, api_host: str, access_token: Optional[str] = None):
        """
        .. py:method:: Initialize the APIClient.

        :param api_host: str: The API host.
        :param access_token: str: The access token. If not provided, it will attempt to retrieve it from the "APICLIENT_TOKEN" environment variable.
            If the environment variable is not set, a RuntimeError will be raised.
        :raises RuntimeError:If `access_token` is not provided and the "APICLIENT_TOKEN" environment variable is not set.
        """
        # Initialize early since they're referenced in the destructor and
        # access_token checking may cause constructor to exit early.

        if access_token is None:
            access_token = os.environ.get("APICLIENT_TOKEN")
            if access_token is None:
                raise RuntimeError(
                    "$APICLIENT_TOKEN environment variable must be set when "
                    "APIClient is constructed without the access_token argument"
                )
        self.api_host = api_host
        self.access_token = access_token
        self._logger = get_default_logger()

    def get_logger(self):
        return self._logger

    def get_dataframe(
        self,
        query: Query,
        entity: Optional[str] = None,
        dataset_id: Optional[str] = None,
        clear_cache: bool = False,
    ):
        """
        .. py:method:: Retrieve a Pandas DataFrame for a given entity and query.

        :param entity: str, optional: The entity for which the data is requested.
        :param dataset_id: str, optional: The dataset ID for which the data is requested. Only one of 'entity' and 'dataset_id' should be provided.
        :param query: Query: The query object specifying the data retrieval parameters.
        :param clear_cache: bool, optional: Flag indicating whether to clear the cache before retrieving the data. Default is False.
        :return: pd.DataFrame: The retrieved data as a Pandas DataFrame.
        :raises ValueError: If both 'entity' and 'dataset_id' are provided or if neither 'entity' nor 'dataset_id' are provided.
        :raises ValueError: If the dataset or entity does not exist.
        :raises ValueError: If no data is found and the DataFrame is empty.
        """

        if entity and dataset_id:
            raise ValueError(
                "Only one of 'entity' and 'dataset_id' should be provided."
            )

        if not entity and not dataset_id:
            raise ValueError("One of 'entity' and 'dataset_id' should be provided.")

        if clear_cache:
            print(get_dataframe.cache_info())
            get_dataframe.cache_clear()

        schema: Optional[FieldsSchema] = get_schema(
            access_token=self.access_token,
            api_host=self.api_host,
            entity=entity,
            dataset_id=dataset_id,
        )

        if not schema:
            raise ValueError("dataset or entity does not exist")

        params = query_to_params(query, schema)
        dataframe: Optional[pd.DataFrame] = get_dataframe(
            access_token=self.access_token,
            api_host=self.api_host,
            entity=entity,
            dataset_id=dataset_id,
            params=params,
        )
        if dataframe.empty or dataframe is None:
            raise ValueError("no data found the dataFrame is empty")
        return dataframe

    def commit_dataset(
        self,
        df: pd.DataFrame,
        dataset_id: Optional[str] = None,
        dataset_name: Optional[str] = None,
        dataset_category: Optional[str] = "tabular",
    ) -> str:
        """
        .. py:method:: Commit a Pandas DataFrame as a dataset.

        :param df: pd.DataFrame: The DataFrame to be committed as a dataset.
        :param dataset_id: str: optional The ID of the dataset to be updated. If not provided, a new dataset will be created.
        :param dataset_name: str: optional The name of the dataset. If not provided and the `dataset_id` is provided, it will keep the old name.
        :param dataset_category: str: optional The category of the dataset. Available categories: 'tabular', 'time-series', 'depth-series'. Default is 'tabular'.
        :return: str: The ID of the committed dataset.
        :raises ValueError: If the DataFrame `df` is empty or None.
        :raises ValueError: If both `dataset_id` and `dataset_name` are missing.
        :raises ValueError: If `dataset_category` is not one of the available categories.
        :raises ValueError: If `dataset_category` is 'time-series' and the DataFrame `df` doesn't have a 'time' column.
        :raises ValueError: If `dataset_category` is 'depth-series' and the DataFrame `df` doesn't have a 'depth_time' column.
        """
        if df.empty or df is None:
            raise ValueError(
                "Invalid DataFrame. The DataFrame 'df' cannot be empty or None."
            )

        if dataset_id is None and dataset_name is None:
            raise ValueError("Either 'dataset_id' or 'dataset_name' must be provided.")

        if dataset_category not in ["tabular", "time-series", "depth-series"]:
            raise ValueError(
                "Invalid 'dataset_category' provided. Must be one of: 'tabular', 'time-series', 'depth-series'."
            )

        if dataset_category == "time-series" and "time" not in df.columns:
            raise ValueError(
                "The DataFrame 'df' must have a column called 'time' for the 'time-series' category."
            )

        if dataset_category == "depth-series" and "depth_time" not in df.columns:
            raise ValueError(
                "The DataFrame 'df' must have a column called 'depth_time' for the 'depth-series' category."
            )

        # create the file storage from dataframe
        data_file_storage = create_file_storage_from_data(df=df)

        # commit the data
        dataset_id_ = commit_dataset(
            dataset_name=dataset_name,
            dataset_category=dataset_category,
            dataset_id=dataset_id,
            data_file_storage=data_file_storage,
            access_token=self.access_token,
            api_host=self.api_host,
        )

        return dataset_id_
