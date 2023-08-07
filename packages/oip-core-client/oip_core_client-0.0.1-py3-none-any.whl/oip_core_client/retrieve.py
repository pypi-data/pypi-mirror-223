import os
from functools import lru_cache
from .lib import get_data
import pandas as pd
from typing import FrozenSet, Optional, Dict
from .schema import FieldsSchema


@lru_cache(maxsize=None)
def get_dataframe(
    access_token: str,
    api_host: str,
    entity: Optional[str],
    dataset_id: Optional[str],
    params: FrozenSet,
) -> Optional[pd.DataFrame]:
    """
    Retrieve a DataFrame from the API based on the provided parameters.

    :param access_token: str: The access token for authentication.
    :param api_host: str: The host URL of the API.
    :param entity: Optional[str]: The name of the entity for which to retrieve the data.
    :param dataset_id: Optional[str]: The dataset ID for which the data is requested.
    :param params: FrozenSet: Additional parameters for the API request.
    :return: pd.DataFrame: The retrieved data as a DataFrame.
    """
    if entity:
        url = os.path.join(api_host, "app", entity)
    else:
        url = os.path.join(api_host, "dataset", "app", dataset_id)
    url = url.replace("\\", "/")
    headers = {"authorization": "Bearer " + access_token}
    resp = get_data(url, headers, dict(params))
    if resp.status_code == 200:
        props = [
            e["name"]
            for e in resp.json()["meta"]["schema"]
            if not e["name"].startswith("_")
        ]
        df = pd.DataFrame(resp.json()["data"])
        props = list(set(props) & set(df.columns))
        return df[props] if len(props) > 0 else df

    return None


@lru_cache(maxsize=None)
def get_schema(
    access_token: str, api_host: str, entity: Optional[str], dataset_id: Optional[str]
) -> Optional[FieldsSchema]:
    """
    .. py:method:: Get the entity fields schema for a given entity or dataset

    :param access_token: str: The access token for authentication.
    :param api_host: str: The host URL of the API.
    :param entity: str: The name of the entity for which to retrieve the fields schema.
    :param dataset_id: str: The dataset ID for which the data is requested.
    """
    if entity:
        url = os.path.join(api_host, "meta", entity, "schema")
    else:
        url = os.path.join(api_host, "dataset", "meta", dataset_id, "schema")
    url = url.replace("\\", "/")
    headers = {"authorization": "Bearer " + access_token}
    params: Dict[str, str] = dict()
    resp = get_data(url, headers, params)
    if resp.status_code == 200:
        return resp.json()

    return None
