from datetime import datetime
from .schema import (
    NUMBER_ACCEPTED_OPS,
    STRING_ACCEPTED_OPS,
    GEO_POINT_ACCEPTED_OPS,
    LIST_NUMBER_ACCEPTED_OPS,
    LIST_STRING_ACCEPTED_OPS,
    DICT_NUMBER_ACCEPTED_OPS,
    DOWNSAMPLING_ALLOWED_TIME_INTERVALS,
)
from typing import Any, Dict
from .schema import QueryFilter, FilterValue, QueryMeta
from typeguard import typechecked


class CheckFilterValueByType:
    @staticmethod
    def boolean(col: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if not isinstance(value, bool):
            raise ValueError(f"VALUE FOR {col} SHOULD BE boolean")

    @staticmethod
    def time(col: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        check_date_format: bool = True
        if isinstance(value, str):
            try:
                datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                check_date_format = False
        elif isinstance(value, datetime):
            try:
                value.strftime("%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                check_date_format = False
        else:
            check_date_format = False

        if not check_date_format:
            raise ValueError(
                f"value for {col} does not have the right format %Y-%m-%dT%H:%M:%S.%f"
            )

    @staticmethod
    def number(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"value for {col} , must be number",
            )

        if op not in NUMBER_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: string, op MUST BE IN: {','.join(NUMBER_ACCEPTED_OPS)}"
            )

    @staticmethod
    def string(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if not isinstance(value, str):
            raise ValueError(
                f"value for {col} must be string",
            )

        if op not in STRING_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: string, op MUST BE IN: {','.join(STRING_ACCEPTED_OPS)}",
            )

    @staticmethod
    def geo_point(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if op not in GEO_POINT_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: geo_point, op MUST BE IN: {','.join(GEO_POINT_ACCEPTED_OPS)}",
            )

        for v in value:
            if not isinstance(v, float):
                raise ValueError(
                    f"value for {col} , must be float ",
                )

    @staticmethod
    def list_number(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if op not in LIST_NUMBER_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: list_number, op MUST BE IN: {','.join(LIST_NUMBER_ACCEPTED_OPS)}",
            )

    @staticmethod
    @typechecked
    def list_string(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if op not in LIST_STRING_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: list_string, op MUST BE IN: {','.join(LIST_STRING_ACCEPTED_OPS)}",
            )

    @staticmethod
    @typechecked
    def dict_(col: str, op: str, value: Any) -> None:
        """
        check the filter to value
        :param col: str: filter field
        :param value: Any: filter value
        """
        if op not in DICT_NUMBER_ACCEPTED_OPS:
            raise ValueError(
                f"col: {col}, type: dict, op MUST BE IN: {','.join(DICT_NUMBER_ACCEPTED_OPS)}",
            )

        if "=" not in value:
            raise ValueError(
                f"col: {col}, type: dict, op: dcontains, '=' MUST BE IN VALUE: {value}",
            )


@typechecked
def check_filter_validity(filter_: QueryFilter, field_to_type: Dict[str, str]) -> None:
    """
    check the filter conformity
    it will abort the operation if the filter is not conform
    :param filter_: QueryFilter: filter (list[dict{col,op,value}])
    :param field_to_type: dict: dictionary field -> type
    """
    for i in range(len(filter_)):
        f = filter_[i]
        col = f["col"]
        op = f["op"]
        value: FilterValue = f["value"]

        # if the field specified does not exist
        if col not in field_to_type:
            raise ValueError(
                f"col: {col}, does not exist in the entity ",
            )

        # get the field type
        type_ = field_to_type[col]

        if type_ == "boolean":
            CheckFilterValueByType.boolean(col, value)

        if type_ == "time":
            CheckFilterValueByType.time(col, value)

        if type_ in ["number"]:
            CheckFilterValueByType.number(col, op, value)

        if type_ in ["string"]:
            CheckFilterValueByType.string(col, op, value)

        if type_ == "geo_point":
            CheckFilterValueByType.geo_point(col, op, value)

        if type_ == "list_number":
            CheckFilterValueByType.list_number(col, op, value)

        if type_ == "list_string":
            CheckFilterValueByType.list_string(col, op, value)

        if type_ in ["dict", "object"]:
            CheckFilterValueByType.dict_(col, op, value)


@typechecked
def check_meta_validity(meta: QueryMeta):
    """
    Check the validity of meta dictionary
    :param meta: QueryMeta: meta dictionary
    """

    # check logical_op
    if "logical_op" in meta:
        if meta["logical_op"] not in ["and", "or"]:
            raise ValueError(
                '"logical_op" must be "or" or "and"',
            )

    # check sort
    sort = meta.get("sort", None)
    if sort:
        if "order_by" in sort and "order" in sort:
            if isinstance(sort["order"], list):
                if len(sort["order_by"]) != len(sort["order"]):
                    raise ValueError(
                        '"sort_col" and "sort_order" lists must be of the same length',
                    )
                for element in sort["order"]:
                    if element not in [1, -1]:
                        raise ValueError(
                            "Order should either be 1 or -1",
                        )

    # check downsampling
    downsampling = meta.get("downsampling", None)
    if downsampling:
        if "interval" not in downsampling and "nb_pts" not in downsampling:
            raise ValueError("Time interval OR Nb of pts not specified")

        if "interval" in downsampling and downsampling["interval"] is not None:
            if downsampling["interval"][-1] not in DOWNSAMPLING_ALLOWED_TIME_INTERVALS:
                raise ValueError("Time interval invalid")
