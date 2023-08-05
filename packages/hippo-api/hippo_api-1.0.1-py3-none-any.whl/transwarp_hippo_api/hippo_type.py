import json
import types
from enum import Enum


class HippoType(Enum):
    INT8 = "int8"
    INT16 = "int16"
    INT32 = "int32"
    INT64 = "int64"
    FLOAT = "float"
    DOUBLE = "double"
    BOOL = "bool"
    STRING = "string"
    CHAR = "char"
    VARCHAR = "varchar"
    VARCHAR2 = "varchar2"
    DATE = "date"
    TIMESTAMP = "timestamp"
    DATETIME = "datetime"
    TIME = "time"
    FLOAT_VECTOR = "float_vector"
    BINARY_VECTOR = "binary_vector"


HippoTypeAliases = types.MappingProxyType({
    HippoType.INT64: ["bigint"]
})

HippoVector = list[float]
DataVector = list
HippoResult = dict[str, DataVector]


class HippoTypesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HippoType):
            return obj.value
        return super().default(obj)


class HippoJobStatus(Enum):
    HIPPO_JOB_PENDING = "SHIVA_JOB_PENDING"
    HIPPO_JOB_RUNNING = "SHIVA_JOB_RUNNING"
    HIPPO_JOB_CANCELED = "SHIVA_JOB_CANCELED"
    HIPPO_JOB_FAILED = "SHIVA_JOB_FAILED"
    HIPPO_JOB_SUCCESS = "SHIVA_JOB_SUCCESS"
    HIPPO_JOB_INVALID = "SHIVA_JOB_INVALID"


class IndexType(Enum):
    FLAT = "FLAT"
    IVF_FLAT = "IVF_FLAT"
    IVF_SQ = "IVF_SQ"
    IVF_PQ = "IVF_PQ"
    HNSW = "HNSW"
    ANNOY = "ANNOY"


class MetricType(Enum):
    L2 = "l2"
    IP = "ip"
