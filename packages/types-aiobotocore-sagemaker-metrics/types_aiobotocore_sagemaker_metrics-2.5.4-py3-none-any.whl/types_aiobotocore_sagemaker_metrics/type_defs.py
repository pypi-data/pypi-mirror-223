"""
Type annotations for sagemaker-metrics service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_metrics/type_defs/)

Usage::

    ```python
    from types_aiobotocore_sagemaker_metrics.type_defs import BatchPutMetricsErrorTypeDef

    data: BatchPutMetricsErrorTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import PutMetricsErrorCodeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchPutMetricsErrorTypeDef",
    "ResponseMetadataTypeDef",
    "TimestampTypeDef",
    "BatchPutMetricsResponseTypeDef",
    "RawMetricDataTypeDef",
    "BatchPutMetricsRequestRequestTypeDef",
)

BatchPutMetricsErrorTypeDef = TypedDict(
    "BatchPutMetricsErrorTypeDef",
    {
        "Code": PutMetricsErrorCodeType,
        "MetricIndex": int,
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

TimestampTypeDef = Union[datetime, str]
BatchPutMetricsResponseTypeDef = TypedDict(
    "BatchPutMetricsResponseTypeDef",
    {
        "Errors": List[BatchPutMetricsErrorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredRawMetricDataTypeDef = TypedDict(
    "_RequiredRawMetricDataTypeDef",
    {
        "MetricName": str,
        "Timestamp": TimestampTypeDef,
        "Value": float,
    },
)
_OptionalRawMetricDataTypeDef = TypedDict(
    "_OptionalRawMetricDataTypeDef",
    {
        "Step": int,
    },
    total=False,
)


class RawMetricDataTypeDef(_RequiredRawMetricDataTypeDef, _OptionalRawMetricDataTypeDef):
    pass


BatchPutMetricsRequestRequestTypeDef = TypedDict(
    "BatchPutMetricsRequestRequestTypeDef",
    {
        "TrialComponentName": str,
        "MetricData": Sequence[RawMetricDataTypeDef],
    },
)
