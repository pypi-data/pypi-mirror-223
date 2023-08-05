from enum import Enum, auto

from mstrio.utils.enum_helper import AutoName


class Function(AutoName):
    """Enumeration constant used to specify the function used for calculation
    in expression nodes"""

    THIRD_PARTY = auto()
    CUSTOM = auto()
    PLUS = auto()
    MINUS = auto()
    TIMES = auto()
    DIVIDE = auto()
    UNARY_MINUS = auto()
    EQUALS = auto()
    NOT_EQUAL = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()
    SUM = auto()
    COUNT = auto()
    AVG = auto()
    MIN = auto()
    MAX = auto()
    BETWEEN = auto()
    LIKE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    RANK = auto()
    ABS = auto()
    RUNNING_SUM = auto()
    RUNNING_AVG = auto()
    MOVING_SUM = auto()
    MOVING_AVG = auto()
    PRODUCT = auto()
    MEDIAN = auto()
    MODE = auto()
    STDEV = auto()
    VAR = auto()
    GEOMEAN = auto()
    EQUAL_ENHANCED = auto()
    NOT_EQUAL_ENHANCED = auto()
    GREATER_EQUAL_ENHANCED = auto()
    LESS_EQUAL_ENHANCED = auto()
    BETWEEN_ENHANCED = auto()
    BANDING = auto()
    BANDING_C = auto()
    BANDING_P = auto()
    NOT_LIKE = auto()
    NOT_BETWEEN = auto()
    INTERSECT = auto()
    INTERSECT_IN = auto()
    NULL_TO_ZERO = auto()
    ZERO_TO_NULL = auto()
    APPLY_SIMPLE = auto()
    APPLY_AGGREGATION = auto()
    APPLY_LOGIC = auto()
    APPLY_COMPARISON = auto()
    APPLY_RELATIVE = auto()
    IS_NULL = auto()
    IS_NOT_NULL = auto()
    UCASE = auto()
    NOT_IN = auto()
    N_TILE = auto()
    PERCENTILE = auto()
    MOVING_MAX = auto()
    MOVING_MIN = auto()
    MOVING_DIFFERENCE = auto()
    MOVING_STDEV = auto()
    EXP_WGH_MOVING_AVG = auto()
    MOVING_COUNT = auto()
    RUNNING_MAX = auto()
    RUNNING_MIN = auto()
    RUNNING_STDEV = auto()
    RUNNING_COUNT = auto()
    EXP_WGH_RUNNING_AVG = auto()
    NOT_BETWEEN_ENHANCED = auto()
    CONCAT = auto()
    FIRST_IN_RANGE = auto()
    LAST_IN_RANGE = auto()
    VALUE_SEGMENT = auto()
    CONTAINS = auto()
    BEGINS_WITH = auto()
    ENDS_WITH = auto()
    NOT_CONTAINS = auto()
    NOT_BEGINS_WITH = auto()
    NOT_ENDS_WITH = auto()
    CASE = auto()
    CASE_V = auto()
    STDEV_P = auto()
    RUNNING_STDEV_P = auto()
    MOVING_STDEV_P = auto()
    N_TILE_S = auto()
    N_TILE_VS = auto()
    VAR_P = auto()
    CURRENT_DATE = auto()
    DAY_OF_MONTH = auto()
    DAY_OF_WEEK = auto()
    DAY_OF_YEAR = auto()
    WEEK = auto()
    MONTH = auto()
    QUARTER = auto()
    YEAR = auto()
    CURRENT_DATE_TIME = auto()
    CURRENT_TIME = auto()
    HOUR = auto()
    MINUTE = auto()
    SECOND = auto()
    MILLI_SECOND = auto()
    CONCAT_NO_BLANK = auto()
    LENGTH = auto()
    LOWER = auto()
    L_TRIM = auto()
    POSITION = auto()
    R_TRIM = auto()
    SUB_STR = auto()
    INIT_CAP = auto()
    TRIM = auto()
    RIGHT_STR = auto()
    LEFT_STR = auto()
    GREATEST = auto()
    LEAST = auto()
    FIRST = auto()
    LAST = auto()
    DATE = auto()
    DAYS_BETWEEN = auto()
    MONTHS_BETWEEN = auto()
    ADD_DAYS = auto()
    ADD_MONTHS = auto()
    MONTH_START_DATE = auto()
    MONTH_END_DATE = auto()
    YEAR_START_DATE = auto()
    YEAR_END_DATE = auto()
    IF = auto()
    APPLY_OPTIONAL = auto()
    APPLY_CS_SECURITY_FILTER = auto()
    UNION = auto()
    EXCEPT = auto()
    COALESCE = auto()
    ADD = auto()
    AVERAGE = auto()
    MULTIPLY = auto()
    BANDING_M = auto()
    OLAP_SUM = auto()
    OLAP_AVG = auto()
    OLAP_COUNT = auto()
    OLAP_MAX = auto()
    OLAP_MIN = auto()
    LAG = auto()
    LEAD = auto()
    OLAP_RANK = auto()
    REPEAT = auto()
    BIT_AND = auto()
    BIT_OR = auto()
    BIT_XOR = auto()
    BIT_NOT = auto()
    BIT_LEFT_SHIFT = auto()
    BIT_RIGHT_SHIFT = auto()
    AMPERSAND = auto()
    ORDINAL_RANK = auto()
    HISTOGRAM_MEDIAN = auto()
    BAND_NAMES = auto()
    PERCENT_RANK_RELATIVE = auto()
    SEARCH = auto()
    IF_BY_DIMTY = auto()
    GET_EXTRA_OUTPUT = auto()
    TO_DATE_TIME = auto()
    QUARTER_START_DATE = auto()
    WEEK_START_DATE = auto()
    TO_STRING = auto()
    TO_NUMBER = auto()
    PERCENT_RANK = auto()
    STR_REPLACE = auto()
    STR_MATCH = auto()
    STR_SPLIT = auto()
    STR_CHAR = auto()
    STR_REPEAT = auto()
    DATE_DIFF = auto()
    STR_BEGINS_WITH = auto()
    STR_ENDS_WITH = auto()
    WEIGHT_STD_P = auto()
    WEIGHT_MEAN_AVE = auto()
    CONCAT_AGG = auto()
    WEIGHT_COV = auto()
    WEIGHT_CORR = auto()
    STR_LAST_POSITION = auto()
    STR_TITLE_CAP = auto()
    FISCAL_WEEK = auto()
    FISCAL_MONTH = auto()
    FISCAL_QUARTER = auto()
    FISCAL_YEAR = auto()
    NULL_TO_EMPTY = auto()
    DESCENDANTS = auto()
    ANCESTORS = auto()
    PARENTS = auto()
    CHILDREN = auto()
    TUPLE = auto()


class ExpressionType(AutoName):
    """Enumeration constant indicating the expression type of expression node"""

    DYNAMIC = auto()
    STATIC = auto()
    GENERIC = auto()
    FILTER_SINGLE_BASE_FORM_QUAL = auto()
    FILTER_MULTI_BASE_FORM_QUAL = auto()
    FILTER_JOINT_FORM_QUAL = auto()
    FILTER_LIST_QUAL = auto()
    FILTER_LIST_FORM_QUAL = auto()
    FILTER_JOINT_LIST_QUAL = auto()
    FILTER_JOINT_LIST_FORM_QUAL = auto()
    FILTER_SINGLE_BASE_FORM_EXPRESSION = auto()
    FILTER_SINGLE_METRIC_QUAL = auto()
    FILTER_MULTI_METRIC_QUAL = auto()
    FILTER_METRIC_EXPRESSION = auto()
    FILTER_EMBED_QUAL = auto()
    FILTER_BRANCH_QUAL = auto()
    FILTER_RELATIONSHIP_QUAL = auto()
    FILTER_ALL_ATTRIBUTE_QUAL = auto()
    FILTER_ATTRIBUTE_ID_QUAL = auto()
    FILTER_ATTRIBUTE_DESC_QUAL = auto()
    AGG_METRIC = auto()
    BANDING = auto()
    FILTER_REPORT_QUAL = auto()
    MDX_SAP_VARIABLE = auto()
    SQL_QUERY_QUAL = auto()
    CANCELED_PROMPT = auto()
    ELEMENT_LIST = auto()
    ELEMENT_SINGLE = auto()
    FORM_OF_THIS_ATTRIBUTE = auto()
    CSI_UPDATE = auto()
    CSI_INSERT = auto()
    CSI_DELETE = auto()
    CSI_GROUP = auto()


class DimtyType(AutoName):
    """Enumeration constant  indicating the dimty type of expression node"""

    NONE = auto()
    CONTINUATION = auto()
    EXCLUSIVE_CONTINUATION = auto()
    OUTPUT_LEVEL = auto()
    BREAK_BY = auto()
    EMBEDDED = auto()
    UNSPECIFIED = auto()
    PARAMETER = auto()


class DependenceType(AutoName):
    """Enumeration constant indicating the dependence type of expression node"""

    DEFAULT = auto()
    INDEPENDENT = auto()
    DEPENDENT = auto()


class NodeType(AutoName):
    """Enumeration constant indicating the type of node within
    the expression tree
    """

    OPERATOR = auto()
    OBJECT_REFERENCE = auto()
    COLUMN_REFERENCE = auto()
    CONSTANT = auto()
    RELATIONSHIP = auto()
    FORM_SHORTCUT = auto()
    DYNAMIC_DATE_TIME = auto()
    PREDICATE_CUSTOM = auto()
    PREDICATE_PROMPT_QUALIFICATION = auto()
    PREDICATE_METRIC_QUALIFICATION = auto()
    PREDICATE_RELATIONSHIP = auto()
    PREDICATE_JOINT_ELEMENT_LIST = auto()
    PREDICATE_ELEMENT_LIST = auto()
    PREDICATE_FORM_QUALIFICATION = auto()
    PREDICATE_FILTER_QUALIFICATION = auto()
    PREDICATE_REPORT_QUALIFICATION = auto()
    PREDICATE_BANDING_SIZE = auto()
    PREDICATE_BANDING_COUNT = auto()
    PREDICATE_BANDING_POINTS = auto()
    PREDICATE_BANDING_DISTINCT = auto()


class IsIndependent(Enum):
    """Flag that indicates whether a node will be evaluated independently
    of other parts of the larger expression"""

    YES = 1
    NO = 0


class ExpressionFormat(AutoName):
    """ "Expression format to be fetched from server, it might be tree or token:
    - tree: tree data structure fully defining the expression. This format can
    be used if you want to examine and modify the expression programmatically.
    - tokens: list of parsed tokens. This format can be used if you want
    to examine and modify the expression using the parser component. Note that
    generating tokens requires additional time.
    """

    TREE = auto()
    TOKENS = auto()
