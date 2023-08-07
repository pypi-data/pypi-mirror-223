from __future__ import print_function
from typing import List, Union, TypedDict, Optional, Tuple, Any
from datetime import datetime


# meta sort, example:
# {"order_by": ["col1", "col2], "order": [1, -1]}
class FilterMetaSort(TypedDict):
    order_by: List[str]
    order: List[int]


# filter meta for time down-sampling
# to be used in QueryMeta
# between interval and nb_pts only one should be specified
class FilterMetaDownsampling(TypedDict, total=False):
    interval: Optional[str]  # time interval for down-sampling
    nb_pts: Optional[int]  # number of point to returned (if specified no)
    agg_op: Optional[str]  # down-sampling aggregation operator (avg, min, etc.)
    grp_by: Optional[str]
    grp_by_pn: Optional[int]
    grp_by_ps: Optional[int]


# query meta for geo-spatial down-sampling
# to be used in QueryMeta
# bounds is the bounds of area to consider
# (lon_min;lon_max;lat_min;lat_max)
class FilterMetaGDownsampling(TypedDict, total=False):
    ncells: Optional[int]  # number of cells to consider
    bounds: Optional[Union[List[float], Tuple[float, float, float, float]]]


# query metadata
class QueryMeta(TypedDict, total=False):
    logical_op: str  # and/or
    page_num: Optional[int]  # page number
    page_size: Optional[int]  # page size
    sample_size: Optional[int]  # number of samples
    sort: Optional[FilterMetaSort]
    downsampling: Optional[FilterMetaDownsampling]
    gdownsampling: Optional[FilterMetaGDownsampling]
    time_min: Optional[Union[datetime, str]]  # time min
    time_max: Optional[Union[datetime, str]]  # time max
    depth_min: Optional[float]  # depth min
    depth_max: Optional[float]  # depth max
    cols: Optional[List[str]]
    cumulative: Optional[bool]
    formulas: Optional[List[str]]
    entities: Optional[List[str]]


# geo polygon schema
GeoPolygon = List[List[List[float]]]

# value of a filter
FilterValue = Union[
    bool, str, int, float, datetime, List[str], List[int], List[float], GeoPolygon, None
]


# filter, example: {"col": "c", "op": "=", "value": 1}
class Filter(TypedDict, total=False):
    col: str  # column/field
    op: str  # operator (=, >, contains, etc.)
    value: FilterValue  # value
    type: str  # type of the field (string, number, etc.)


# query filter, it's a list of Filter
QueryFilter = List[Filter]


# Query contains QueryFilter and QueryMeta and neighbors
# neighbors is a list of neighbor entities (parent, children, etc.)
# to the target entity
class Query(TypedDict, total=False):
    filter: QueryFilter  # query filter
    meta: QueryMeta  # meta filter
    neighbors: List[str]  # neighbors of the target entity


# ordinary field of an entity
class FieldSchema(TypedDict, total=False):
    name: str  # id of the field
    label: Optional[str]  # label
    desc: Optional[str]  # description
    unit: Optional[str]  # unit if the field
    type: str  # type (number, string, etc.)
    family: Optional[str]  # unit family
    values: Optional[List[Any]]  # accepted values
    indexed: Optional[Union[int, str]]  # indexing (1, -1, none)
    is_meta_field: Optional[bool]  # is meta field (only for series)
    is_foreign_key: Optional[bool]  # is a foreign_key
    is_related_ids: Optional[bool]  # is a property that contains related ids
    secret: Optional[bool]  # is it secret
    default: Optional[Any]  # default value
    required: Optional[bool]  # is it required
    not_nullable: Optional[bool]  # is it not nullable
    entity_text_indexed: Optional[bool]  # only for str
    scope: Optional[str]  # scope to group fields
    validation_regex: Optional[str]  # regex to validation


# schema of an entity: List of FieldSchema
FieldsSchema = List[FieldSchema]


# ACCEPTED OPS FOR NUMBERS
NUMBER_ACCEPTED_OPS = [
    "=",
    "!=",
    ">=",
    "<=",
    ">",
    "<",
    "IN",
    "NOT IN",
    "null",
    "not_null",
]

# ACCEPTED OPERATORS FOR STRINGS
STRING_ACCEPTED_OPS = [
    "=",
    "!=",
    ">=",
    "<=",
    ">",
    "<",
    "contains",
    "lcontains",
    "stext",
    "IN",
    "NOT IN",
    "null",
    "not_null",
]


# ACCEPTED OPERATORS FOR STRINGS
GEO_POINT_ACCEPTED_OPS = ["gwithin", "gnear"]

# ACCEPTED OPERATORS FOR list_number
LIST_NUMBER_ACCEPTED_OPS = ["lcontains", "!=", "="]

# ACCEPTED OPERATORS FOR list_string
LIST_STRING_ACCEPTED_OPS = ["lcontains", "!=", "=", "contains"]

# ACCEPTED OPERATORS FOR DICT_NUMBER
DICT_NUMBER_ACCEPTED_OPS = ["dcontains"]

# DOWNSAMPLING TIME INTERVALS
DOWNSAMPLING_ALLOWED_TIME_INTERVALS = [
    "s",
    "m",
    "h",
    "d",
    "w",
    "M",
    "q",
    "y",
]
