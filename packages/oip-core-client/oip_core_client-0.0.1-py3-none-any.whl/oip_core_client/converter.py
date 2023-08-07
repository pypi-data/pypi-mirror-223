from .schema import Query, QueryFilter, QueryMeta, FieldsSchema
from typing import FrozenSet, Set, Tuple
from .units import check_filter_validity, check_meta_validity
from typeguard import typechecked


@typechecked
def query_filter_to_params(
    query_filter: QueryFilter, schema: FieldsSchema
) -> Set[Tuple[str, str]]:
    """
    Convert the filter list into a set of tuples representing the filter parameters.

    :param query_filter: QueryFilter: The filter list containing dictionaries with 'col', 'op', and 'value' keys.
    :return params: set[Tuple[str, str]]: A set of tuples representing the filter parameters.
    """
    field_to_type = {filed["name"]: filed["type"] for filed in schema}

    check_filter_validity(filter_=query_filter, field_to_type=field_to_type)

    if not query_filter:
        return set()

    for f in query_filter:
        if not all(key in f for key in ["col", "op", "value"]):
            raise ValueError(
                "All items in 'query_filter' list must contain 'col', 'op', and 'value' keys."
            )

    params = set()

    filter_cols = []
    filter_ops = []
    filter_vals = []

    for f in query_filter:
        filter_cols.append(f["col"])
        filter_ops.append(f["op"])
        filter_vals.append(f["value"])

    params = {
        ("filter_cols", "|".join(filter_cols)),
        ("filter_ops", "|".join(filter_ops)),
        (
            "filter_vals",
            "|".join(
                [
                    (";".join(map(str, val)) if isinstance(val, list) else str(val))
                    for val in filter_vals
                ]
            ),
        ),
    }
    return params


@typechecked
def query_meta_to_params(query_meta: QueryMeta) -> Set[Tuple[str, str]]:
    """
    Convert the meta dictionary into a set of tuples representing the meta parameters.

    :param meta: QueryMeta: The meta dictionary containing key-value pairs.
    :return params: set[Tuple[str, str]]: A set of tuples representing the meta parameters.
    """
    if not query_meta:
        return set()

    check_meta_validity(meta=query_meta)

    valid_keys = {
        # int , str
        "page_num",
        "page_size",
        "sample_size",
        "logical_op",
        # booleans
        "cumulative",
        # lists
        "cols",
        "entities",
        "formulas",
        # dicts
        "sort",
        "downsampling",
        "gdownsampling",
    }

    params = set()

    for key, value in query_meta.items():
        if key not in valid_keys:
            raise ValueError(f"Invalid key found in 'query_meta': {key}")

        if isinstance(value, dict):
            if key == "sort":
                sort_col = "|".join(map(str, value["order_by"]))
                sort_order = "|".join(map(str, value["order"]))
                params.add(("sort_col", sort_col))
                params.add(("sort_order", sort_order))

            if key == "downsampling":
                downsampling_keys_map = {
                    "interval": "ds_interval",
                    "nb_pts": "ds_nb_pts",
                    "agg_op": "ds_agg_op",
                    "grp_by": "ds_grp_by",
                    "grp_by_pn": "ds_grp_by_pn",
                    "grp_by_ps": "ds_grp_by_ps",
                }

                for k in downsampling_keys_map:
                    v = value.get(k, None)
                    if v:
                        params.add((downsampling_keys_map[k], str(v)))

            if key == "gdownsampling":
                ncells = str(value["ncells"])
                bounds = ";".join(map(str, value["bounds"]))
                params.add(("gds_ncells", ncells))
                params.add(("gds_bds", bounds))

        elif isinstance(value, list):
            value = "|".join(map(str, value))
            params.add((key, value))
        else:
            value = str(value)
            params.add((key, value))

    return params


@typechecked
def query_to_params(query: Query, schema: FieldsSchema) -> FrozenSet:
    """
    Convert the query to set of tuples representing the parameters

    :param query: Query: The query dict that contains the filters and meta
    :return params: set[Tuple[str, str]]: frozenset representing the parameters

    """
    params = {
        *query_filter_to_params(query.get("filter", list()), schema),
        *query_meta_to_params(query.get("meta", dict())),
    }
    return frozenset(params)
