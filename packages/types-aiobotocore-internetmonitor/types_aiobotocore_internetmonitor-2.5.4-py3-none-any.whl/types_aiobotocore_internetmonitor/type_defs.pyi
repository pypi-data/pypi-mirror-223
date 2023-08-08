"""
Type annotations for internetmonitor service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_internetmonitor/type_defs/)

Usage::

    ```python
    from types_aiobotocore_internetmonitor.type_defs import AvailabilityMeasurementTypeDef

    data: AvailabilityMeasurementTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    HealthEventImpactTypeType,
    HealthEventStatusType,
    LocalHealthEventsConfigStatusType,
    LogDeliveryStatusType,
    MonitorConfigStateType,
    MonitorProcessingStatusCodeType,
    TriangulationEventTypeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AvailabilityMeasurementTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteMonitorInputRequestTypeDef",
    "GetHealthEventInputRequestTypeDef",
    "GetMonitorInputRequestTypeDef",
    "LocalHealthEventsConfigTypeDef",
    "S3ConfigTypeDef",
    "PaginatorConfigTypeDef",
    "TimestampTypeDef",
    "ListMonitorsInputRequestTypeDef",
    "MonitorTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "NetworkTypeDef",
    "RoundTripTimeTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "CreateMonitorOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "UpdateMonitorOutputTypeDef",
    "HealthEventsConfigTypeDef",
    "InternetMeasurementsLogDeliveryTypeDef",
    "ListMonitorsInputListMonitorsPaginateTypeDef",
    "ListHealthEventsInputListHealthEventsPaginateTypeDef",
    "ListHealthEventsInputRequestTypeDef",
    "ListMonitorsOutputTypeDef",
    "NetworkImpairmentTypeDef",
    "PerformanceMeasurementTypeDef",
    "CreateMonitorInputRequestTypeDef",
    "GetMonitorOutputTypeDef",
    "UpdateMonitorInputRequestTypeDef",
    "InternetHealthTypeDef",
    "ImpactedLocationTypeDef",
    "GetHealthEventOutputTypeDef",
    "HealthEventTypeDef",
    "ListHealthEventsOutputTypeDef",
)

AvailabilityMeasurementTypeDef = TypedDict(
    "AvailabilityMeasurementTypeDef",
    {
        "ExperienceScore": float,
        "PercentOfTotalTrafficImpacted": float,
        "PercentOfClientLocationImpacted": float,
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

DeleteMonitorInputRequestTypeDef = TypedDict(
    "DeleteMonitorInputRequestTypeDef",
    {
        "MonitorName": str,
    },
)

GetHealthEventInputRequestTypeDef = TypedDict(
    "GetHealthEventInputRequestTypeDef",
    {
        "MonitorName": str,
        "EventId": str,
    },
)

GetMonitorInputRequestTypeDef = TypedDict(
    "GetMonitorInputRequestTypeDef",
    {
        "MonitorName": str,
    },
)

LocalHealthEventsConfigTypeDef = TypedDict(
    "LocalHealthEventsConfigTypeDef",
    {
        "Status": LocalHealthEventsConfigStatusType,
        "HealthScoreThreshold": float,
        "MinTrafficImpact": float,
    },
    total=False,
)

S3ConfigTypeDef = TypedDict(
    "S3ConfigTypeDef",
    {
        "BucketName": str,
        "BucketPrefix": str,
        "LogDeliveryStatus": LogDeliveryStatusType,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

TimestampTypeDef = Union[datetime, str]
ListMonitorsInputRequestTypeDef = TypedDict(
    "ListMonitorsInputRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "MonitorStatus": str,
    },
    total=False,
)

_RequiredMonitorTypeDef = TypedDict(
    "_RequiredMonitorTypeDef",
    {
        "MonitorName": str,
        "MonitorArn": str,
        "Status": MonitorConfigStateType,
    },
)
_OptionalMonitorTypeDef = TypedDict(
    "_OptionalMonitorTypeDef",
    {
        "ProcessingStatus": MonitorProcessingStatusCodeType,
    },
    total=False,
)

class MonitorTypeDef(_RequiredMonitorTypeDef, _OptionalMonitorTypeDef):
    pass

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

NetworkTypeDef = TypedDict(
    "NetworkTypeDef",
    {
        "ASName": str,
        "ASNumber": int,
    },
)

RoundTripTimeTypeDef = TypedDict(
    "RoundTripTimeTypeDef",
    {
        "P50": float,
        "P90": float,
        "P95": float,
    },
    total=False,
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

CreateMonitorOutputTypeDef = TypedDict(
    "CreateMonitorOutputTypeDef",
    {
        "Arn": str,
        "Status": MonitorConfigStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMonitorOutputTypeDef = TypedDict(
    "UpdateMonitorOutputTypeDef",
    {
        "MonitorArn": str,
        "Status": MonitorConfigStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HealthEventsConfigTypeDef = TypedDict(
    "HealthEventsConfigTypeDef",
    {
        "AvailabilityScoreThreshold": float,
        "PerformanceScoreThreshold": float,
        "AvailabilityLocalHealthEventsConfig": LocalHealthEventsConfigTypeDef,
        "PerformanceLocalHealthEventsConfig": LocalHealthEventsConfigTypeDef,
    },
    total=False,
)

InternetMeasurementsLogDeliveryTypeDef = TypedDict(
    "InternetMeasurementsLogDeliveryTypeDef",
    {
        "S3Config": S3ConfigTypeDef,
    },
    total=False,
)

ListMonitorsInputListMonitorsPaginateTypeDef = TypedDict(
    "ListMonitorsInputListMonitorsPaginateTypeDef",
    {
        "MonitorStatus": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListHealthEventsInputListHealthEventsPaginateTypeDef = TypedDict(
    "_RequiredListHealthEventsInputListHealthEventsPaginateTypeDef",
    {
        "MonitorName": str,
    },
)
_OptionalListHealthEventsInputListHealthEventsPaginateTypeDef = TypedDict(
    "_OptionalListHealthEventsInputListHealthEventsPaginateTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "EventStatus": HealthEventStatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListHealthEventsInputListHealthEventsPaginateTypeDef(
    _RequiredListHealthEventsInputListHealthEventsPaginateTypeDef,
    _OptionalListHealthEventsInputListHealthEventsPaginateTypeDef,
):
    pass

_RequiredListHealthEventsInputRequestTypeDef = TypedDict(
    "_RequiredListHealthEventsInputRequestTypeDef",
    {
        "MonitorName": str,
    },
)
_OptionalListHealthEventsInputRequestTypeDef = TypedDict(
    "_OptionalListHealthEventsInputRequestTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "NextToken": str,
        "MaxResults": int,
        "EventStatus": HealthEventStatusType,
    },
    total=False,
)

class ListHealthEventsInputRequestTypeDef(
    _RequiredListHealthEventsInputRequestTypeDef, _OptionalListHealthEventsInputRequestTypeDef
):
    pass

ListMonitorsOutputTypeDef = TypedDict(
    "ListMonitorsOutputTypeDef",
    {
        "Monitors": List[MonitorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetworkImpairmentTypeDef = TypedDict(
    "NetworkImpairmentTypeDef",
    {
        "Networks": List[NetworkTypeDef],
        "AsPath": List[NetworkTypeDef],
        "NetworkEventType": TriangulationEventTypeType,
    },
)

PerformanceMeasurementTypeDef = TypedDict(
    "PerformanceMeasurementTypeDef",
    {
        "ExperienceScore": float,
        "PercentOfTotalTrafficImpacted": float,
        "PercentOfClientLocationImpacted": float,
        "RoundTripTime": RoundTripTimeTypeDef,
    },
    total=False,
)

_RequiredCreateMonitorInputRequestTypeDef = TypedDict(
    "_RequiredCreateMonitorInputRequestTypeDef",
    {
        "MonitorName": str,
    },
)
_OptionalCreateMonitorInputRequestTypeDef = TypedDict(
    "_OptionalCreateMonitorInputRequestTypeDef",
    {
        "Resources": Sequence[str],
        "ClientToken": str,
        "Tags": Mapping[str, str],
        "MaxCityNetworksToMonitor": int,
        "InternetMeasurementsLogDelivery": InternetMeasurementsLogDeliveryTypeDef,
        "TrafficPercentageToMonitor": int,
        "HealthEventsConfig": HealthEventsConfigTypeDef,
    },
    total=False,
)

class CreateMonitorInputRequestTypeDef(
    _RequiredCreateMonitorInputRequestTypeDef, _OptionalCreateMonitorInputRequestTypeDef
):
    pass

GetMonitorOutputTypeDef = TypedDict(
    "GetMonitorOutputTypeDef",
    {
        "MonitorName": str,
        "MonitorArn": str,
        "Resources": List[str],
        "Status": MonitorConfigStateType,
        "CreatedAt": datetime,
        "ModifiedAt": datetime,
        "ProcessingStatus": MonitorProcessingStatusCodeType,
        "ProcessingStatusInfo": str,
        "Tags": Dict[str, str],
        "MaxCityNetworksToMonitor": int,
        "InternetMeasurementsLogDelivery": InternetMeasurementsLogDeliveryTypeDef,
        "TrafficPercentageToMonitor": int,
        "HealthEventsConfig": HealthEventsConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateMonitorInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMonitorInputRequestTypeDef",
    {
        "MonitorName": str,
    },
)
_OptionalUpdateMonitorInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMonitorInputRequestTypeDef",
    {
        "ResourcesToAdd": Sequence[str],
        "ResourcesToRemove": Sequence[str],
        "Status": MonitorConfigStateType,
        "ClientToken": str,
        "MaxCityNetworksToMonitor": int,
        "InternetMeasurementsLogDelivery": InternetMeasurementsLogDeliveryTypeDef,
        "TrafficPercentageToMonitor": int,
        "HealthEventsConfig": HealthEventsConfigTypeDef,
    },
    total=False,
)

class UpdateMonitorInputRequestTypeDef(
    _RequiredUpdateMonitorInputRequestTypeDef, _OptionalUpdateMonitorInputRequestTypeDef
):
    pass

InternetHealthTypeDef = TypedDict(
    "InternetHealthTypeDef",
    {
        "Availability": AvailabilityMeasurementTypeDef,
        "Performance": PerformanceMeasurementTypeDef,
    },
    total=False,
)

_RequiredImpactedLocationTypeDef = TypedDict(
    "_RequiredImpactedLocationTypeDef",
    {
        "ASName": str,
        "ASNumber": int,
        "Country": str,
        "Status": HealthEventStatusType,
    },
)
_OptionalImpactedLocationTypeDef = TypedDict(
    "_OptionalImpactedLocationTypeDef",
    {
        "Subdivision": str,
        "Metro": str,
        "City": str,
        "Latitude": float,
        "Longitude": float,
        "CountryCode": str,
        "SubdivisionCode": str,
        "ServiceLocation": str,
        "CausedBy": NetworkImpairmentTypeDef,
        "InternetHealth": InternetHealthTypeDef,
    },
    total=False,
)

class ImpactedLocationTypeDef(_RequiredImpactedLocationTypeDef, _OptionalImpactedLocationTypeDef):
    pass

GetHealthEventOutputTypeDef = TypedDict(
    "GetHealthEventOutputTypeDef",
    {
        "EventArn": str,
        "EventId": str,
        "StartedAt": datetime,
        "EndedAt": datetime,
        "CreatedAt": datetime,
        "LastUpdatedAt": datetime,
        "ImpactedLocations": List[ImpactedLocationTypeDef],
        "Status": HealthEventStatusType,
        "PercentOfTotalTrafficImpacted": float,
        "ImpactType": HealthEventImpactTypeType,
        "HealthScoreThreshold": float,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredHealthEventTypeDef = TypedDict(
    "_RequiredHealthEventTypeDef",
    {
        "EventArn": str,
        "EventId": str,
        "StartedAt": datetime,
        "LastUpdatedAt": datetime,
        "ImpactedLocations": List[ImpactedLocationTypeDef],
        "Status": HealthEventStatusType,
        "ImpactType": HealthEventImpactTypeType,
    },
)
_OptionalHealthEventTypeDef = TypedDict(
    "_OptionalHealthEventTypeDef",
    {
        "EndedAt": datetime,
        "CreatedAt": datetime,
        "PercentOfTotalTrafficImpacted": float,
        "HealthScoreThreshold": float,
    },
    total=False,
)

class HealthEventTypeDef(_RequiredHealthEventTypeDef, _OptionalHealthEventTypeDef):
    pass

ListHealthEventsOutputTypeDef = TypedDict(
    "ListHealthEventsOutputTypeDef",
    {
        "HealthEvents": List[HealthEventTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
