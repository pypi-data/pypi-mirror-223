"""
Type annotations for datasync service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_datasync/type_defs/)

Usage::

    ```python
    from mypy_boto3_datasync.type_defs import CredentialsTypeDef

    data: CredentialsTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AgentStatusType,
    AtimeType,
    AzureAccessTierType,
    DiscoveryJobStatusType,
    DiscoveryResourceTypeType,
    EfsInTransitEncryptionType,
    EndpointTypeType,
    GidType,
    HdfsAuthenticationTypeType,
    HdfsDataTransferProtectionType,
    HdfsRpcProtectionType,
    LocationFilterNameType,
    LogLevelType,
    MtimeType,
    NfsVersionType,
    ObjectStorageServerProtocolType,
    ObjectTagsType,
    OperatorType,
    OverwriteModeType,
    PhaseStatusType,
    PosixPermissionsType,
    PreserveDeletedFilesType,
    PreserveDevicesType,
    RecommendationStatusType,
    S3StorageClassType,
    SmbSecurityDescriptorCopyFlagsType,
    SmbVersionType,
    StorageSystemConnectivityStatusType,
    TaskExecutionStatusType,
    TaskFilterNameType,
    TaskQueueingType,
    TaskStatusType,
    TransferModeType,
    UidType,
    VerifyModeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CredentialsTypeDef",
    "DiscoveryServerConfigurationTypeDef",
    "TagListEntryTypeDef",
    "ResponseMetadataTypeDef",
    "AgentListEntryTypeDef",
    "AzureBlobSasConfigurationTypeDef",
    "BlobTypeDef",
    "CancelTaskExecutionRequestRequestTypeDef",
    "CapacityTypeDef",
    "Ec2ConfigTypeDef",
    "HdfsNameNodeTypeDef",
    "QopConfigurationTypeDef",
    "NfsMountOptionsTypeDef",
    "OnPremConfigTypeDef",
    "S3ConfigTypeDef",
    "SmbMountOptionsTypeDef",
    "FilterRuleTypeDef",
    "OptionsTypeDef",
    "TaskScheduleTypeDef",
    "DeleteAgentRequestRequestTypeDef",
    "DeleteLocationRequestRequestTypeDef",
    "DeleteTaskRequestRequestTypeDef",
    "DescribeAgentRequestRequestTypeDef",
    "PrivateLinkConfigTypeDef",
    "DescribeDiscoveryJobRequestRequestTypeDef",
    "DescribeLocationAzureBlobRequestRequestTypeDef",
    "DescribeLocationEfsRequestRequestTypeDef",
    "DescribeLocationFsxLustreRequestRequestTypeDef",
    "DescribeLocationFsxOntapRequestRequestTypeDef",
    "DescribeLocationFsxOpenZfsRequestRequestTypeDef",
    "DescribeLocationFsxWindowsRequestRequestTypeDef",
    "DescribeLocationHdfsRequestRequestTypeDef",
    "DescribeLocationNfsRequestRequestTypeDef",
    "DescribeLocationObjectStorageRequestRequestTypeDef",
    "DescribeLocationS3RequestRequestTypeDef",
    "DescribeLocationSmbRequestRequestTypeDef",
    "DescribeStorageSystemRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "TimestampTypeDef",
    "DescribeStorageSystemResourcesRequestRequestTypeDef",
    "DescribeTaskExecutionRequestRequestTypeDef",
    "TaskExecutionResultDetailTypeDef",
    "DescribeTaskRequestRequestTypeDef",
    "DiscoveryJobListEntryTypeDef",
    "GenerateRecommendationsRequestRequestTypeDef",
    "IOPSTypeDef",
    "LatencyTypeDef",
    "ListAgentsRequestRequestTypeDef",
    "ListDiscoveryJobsRequestRequestTypeDef",
    "LocationFilterTypeDef",
    "LocationListEntryTypeDef",
    "ListStorageSystemsRequestRequestTypeDef",
    "StorageSystemListEntryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTaskExecutionsRequestRequestTypeDef",
    "TaskExecutionListEntryTypeDef",
    "TaskFilterTypeDef",
    "TaskListEntryTypeDef",
    "MaxP95PerformanceTypeDef",
    "RecommendationTypeDef",
    "ThroughputTypeDef",
    "RemoveStorageSystemRequestRequestTypeDef",
    "StopDiscoveryJobRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAgentRequestRequestTypeDef",
    "UpdateDiscoveryJobRequestRequestTypeDef",
    "UpdateStorageSystemRequestRequestTypeDef",
    "AddStorageSystemRequestRequestTypeDef",
    "CreateAgentRequestRequestTypeDef",
    "CreateLocationFsxLustreRequestRequestTypeDef",
    "CreateLocationFsxWindowsRequestRequestTypeDef",
    "StartDiscoveryJobRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "AddStorageSystemResponseTypeDef",
    "CreateAgentResponseTypeDef",
    "CreateLocationAzureBlobResponseTypeDef",
    "CreateLocationEfsResponseTypeDef",
    "CreateLocationFsxLustreResponseTypeDef",
    "CreateLocationFsxOntapResponseTypeDef",
    "CreateLocationFsxOpenZfsResponseTypeDef",
    "CreateLocationFsxWindowsResponseTypeDef",
    "CreateLocationHdfsResponseTypeDef",
    "CreateLocationNfsResponseTypeDef",
    "CreateLocationObjectStorageResponseTypeDef",
    "CreateLocationS3ResponseTypeDef",
    "CreateLocationSmbResponseTypeDef",
    "CreateTaskResponseTypeDef",
    "DescribeDiscoveryJobResponseTypeDef",
    "DescribeLocationAzureBlobResponseTypeDef",
    "DescribeLocationFsxLustreResponseTypeDef",
    "DescribeLocationFsxWindowsResponseTypeDef",
    "DescribeLocationObjectStorageResponseTypeDef",
    "DescribeStorageSystemResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartDiscoveryJobResponseTypeDef",
    "StartTaskExecutionResponseTypeDef",
    "ListAgentsResponseTypeDef",
    "CreateLocationAzureBlobRequestRequestTypeDef",
    "UpdateLocationAzureBlobRequestRequestTypeDef",
    "CreateLocationObjectStorageRequestRequestTypeDef",
    "UpdateLocationObjectStorageRequestRequestTypeDef",
    "CreateLocationEfsRequestRequestTypeDef",
    "DescribeLocationEfsResponseTypeDef",
    "CreateLocationHdfsRequestRequestTypeDef",
    "DescribeLocationHdfsResponseTypeDef",
    "UpdateLocationHdfsRequestRequestTypeDef",
    "FsxProtocolNfsTypeDef",
    "CreateLocationNfsRequestRequestTypeDef",
    "DescribeLocationNfsResponseTypeDef",
    "UpdateLocationNfsRequestRequestTypeDef",
    "CreateLocationS3RequestRequestTypeDef",
    "DescribeLocationS3ResponseTypeDef",
    "CreateLocationSmbRequestRequestTypeDef",
    "DescribeLocationSmbResponseTypeDef",
    "FsxProtocolSmbTypeDef",
    "UpdateLocationSmbRequestRequestTypeDef",
    "StartTaskExecutionRequestRequestTypeDef",
    "UpdateTaskExecutionRequestRequestTypeDef",
    "CreateTaskRequestRequestTypeDef",
    "DescribeTaskResponseTypeDef",
    "UpdateTaskRequestRequestTypeDef",
    "DescribeAgentResponseTypeDef",
    "ListAgentsRequestListAgentsPaginateTypeDef",
    "ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef",
    "ListStorageSystemsRequestListStorageSystemsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef",
    "DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef",
    "DescribeStorageSystemResourceMetricsRequestRequestTypeDef",
    "DescribeTaskExecutionResponseTypeDef",
    "ListDiscoveryJobsResponseTypeDef",
    "ListLocationsRequestListLocationsPaginateTypeDef",
    "ListLocationsRequestRequestTypeDef",
    "ListLocationsResponseTypeDef",
    "ListStorageSystemsResponseTypeDef",
    "ListTaskExecutionsResponseTypeDef",
    "ListTasksRequestListTasksPaginateTypeDef",
    "ListTasksRequestRequestTypeDef",
    "ListTasksResponseTypeDef",
    "NetAppONTAPClusterTypeDef",
    "NetAppONTAPSVMTypeDef",
    "NetAppONTAPVolumeTypeDef",
    "P95MetricsTypeDef",
    "FsxProtocolTypeDef",
    "ResourceDetailsTypeDef",
    "ResourceMetricsTypeDef",
    "CreateLocationFsxOntapRequestRequestTypeDef",
    "CreateLocationFsxOpenZfsRequestRequestTypeDef",
    "DescribeLocationFsxOntapResponseTypeDef",
    "DescribeLocationFsxOpenZfsResponseTypeDef",
    "DescribeStorageSystemResourcesResponseTypeDef",
    "DescribeStorageSystemResourceMetricsResponseTypeDef",
)

CredentialsTypeDef = TypedDict(
    "CredentialsTypeDef",
    {
        "Username": str,
        "Password": str,
    },
)

_RequiredDiscoveryServerConfigurationTypeDef = TypedDict(
    "_RequiredDiscoveryServerConfigurationTypeDef",
    {
        "ServerHostname": str,
    },
)
_OptionalDiscoveryServerConfigurationTypeDef = TypedDict(
    "_OptionalDiscoveryServerConfigurationTypeDef",
    {
        "ServerPort": int,
    },
    total=False,
)


class DiscoveryServerConfigurationTypeDef(
    _RequiredDiscoveryServerConfigurationTypeDef, _OptionalDiscoveryServerConfigurationTypeDef
):
    pass


_RequiredTagListEntryTypeDef = TypedDict(
    "_RequiredTagListEntryTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagListEntryTypeDef = TypedDict(
    "_OptionalTagListEntryTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagListEntryTypeDef(_RequiredTagListEntryTypeDef, _OptionalTagListEntryTypeDef):
    pass


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

AgentListEntryTypeDef = TypedDict(
    "AgentListEntryTypeDef",
    {
        "AgentArn": str,
        "Name": str,
        "Status": AgentStatusType,
    },
    total=False,
)

AzureBlobSasConfigurationTypeDef = TypedDict(
    "AzureBlobSasConfigurationTypeDef",
    {
        "Token": str,
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
CancelTaskExecutionRequestRequestTypeDef = TypedDict(
    "CancelTaskExecutionRequestRequestTypeDef",
    {
        "TaskExecutionArn": str,
    },
)

CapacityTypeDef = TypedDict(
    "CapacityTypeDef",
    {
        "Used": int,
        "Provisioned": int,
        "LogicalUsed": int,
        "ClusterCloudStorageUsed": int,
    },
    total=False,
)

Ec2ConfigTypeDef = TypedDict(
    "Ec2ConfigTypeDef",
    {
        "SubnetArn": str,
        "SecurityGroupArns": Sequence[str],
    },
)

HdfsNameNodeTypeDef = TypedDict(
    "HdfsNameNodeTypeDef",
    {
        "Hostname": str,
        "Port": int,
    },
)

QopConfigurationTypeDef = TypedDict(
    "QopConfigurationTypeDef",
    {
        "RpcProtection": HdfsRpcProtectionType,
        "DataTransferProtection": HdfsDataTransferProtectionType,
    },
    total=False,
)

NfsMountOptionsTypeDef = TypedDict(
    "NfsMountOptionsTypeDef",
    {
        "Version": NfsVersionType,
    },
    total=False,
)

OnPremConfigTypeDef = TypedDict(
    "OnPremConfigTypeDef",
    {
        "AgentArns": Sequence[str],
    },
)

S3ConfigTypeDef = TypedDict(
    "S3ConfigTypeDef",
    {
        "BucketAccessRoleArn": str,
    },
)

SmbMountOptionsTypeDef = TypedDict(
    "SmbMountOptionsTypeDef",
    {
        "Version": SmbVersionType,
    },
    total=False,
)

FilterRuleTypeDef = TypedDict(
    "FilterRuleTypeDef",
    {
        "FilterType": Literal["SIMPLE_PATTERN"],
        "Value": str,
    },
    total=False,
)

OptionsTypeDef = TypedDict(
    "OptionsTypeDef",
    {
        "VerifyMode": VerifyModeType,
        "OverwriteMode": OverwriteModeType,
        "Atime": AtimeType,
        "Mtime": MtimeType,
        "Uid": UidType,
        "Gid": GidType,
        "PreserveDeletedFiles": PreserveDeletedFilesType,
        "PreserveDevices": PreserveDevicesType,
        "PosixPermissions": PosixPermissionsType,
        "BytesPerSecond": int,
        "TaskQueueing": TaskQueueingType,
        "LogLevel": LogLevelType,
        "TransferMode": TransferModeType,
        "SecurityDescriptorCopyFlags": SmbSecurityDescriptorCopyFlagsType,
        "ObjectTags": ObjectTagsType,
    },
    total=False,
)

TaskScheduleTypeDef = TypedDict(
    "TaskScheduleTypeDef",
    {
        "ScheduleExpression": str,
    },
)

DeleteAgentRequestRequestTypeDef = TypedDict(
    "DeleteAgentRequestRequestTypeDef",
    {
        "AgentArn": str,
    },
)

DeleteLocationRequestRequestTypeDef = TypedDict(
    "DeleteLocationRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DeleteTaskRequestRequestTypeDef = TypedDict(
    "DeleteTaskRequestRequestTypeDef",
    {
        "TaskArn": str,
    },
)

DescribeAgentRequestRequestTypeDef = TypedDict(
    "DescribeAgentRequestRequestTypeDef",
    {
        "AgentArn": str,
    },
)

PrivateLinkConfigTypeDef = TypedDict(
    "PrivateLinkConfigTypeDef",
    {
        "VpcEndpointId": str,
        "PrivateLinkEndpoint": str,
        "SubnetArns": List[str],
        "SecurityGroupArns": List[str],
    },
    total=False,
)

DescribeDiscoveryJobRequestRequestTypeDef = TypedDict(
    "DescribeDiscoveryJobRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
    },
)

DescribeLocationAzureBlobRequestRequestTypeDef = TypedDict(
    "DescribeLocationAzureBlobRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationEfsRequestRequestTypeDef = TypedDict(
    "DescribeLocationEfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationFsxLustreRequestRequestTypeDef = TypedDict(
    "DescribeLocationFsxLustreRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationFsxOntapRequestRequestTypeDef = TypedDict(
    "DescribeLocationFsxOntapRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationFsxOpenZfsRequestRequestTypeDef = TypedDict(
    "DescribeLocationFsxOpenZfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationFsxWindowsRequestRequestTypeDef = TypedDict(
    "DescribeLocationFsxWindowsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationHdfsRequestRequestTypeDef = TypedDict(
    "DescribeLocationHdfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationNfsRequestRequestTypeDef = TypedDict(
    "DescribeLocationNfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationObjectStorageRequestRequestTypeDef = TypedDict(
    "DescribeLocationObjectStorageRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationS3RequestRequestTypeDef = TypedDict(
    "DescribeLocationS3RequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeLocationSmbRequestRequestTypeDef = TypedDict(
    "DescribeLocationSmbRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)

DescribeStorageSystemRequestRequestTypeDef = TypedDict(
    "DescribeStorageSystemRequestRequestTypeDef",
    {
        "StorageSystemArn": str,
    },
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
_RequiredDescribeStorageSystemResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeStorageSystemResourcesRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
        "ResourceType": DiscoveryResourceTypeType,
    },
)
_OptionalDescribeStorageSystemResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeStorageSystemResourcesRequestRequestTypeDef",
    {
        "ResourceIds": Sequence[str],
        "Filter": Mapping[Literal["SVM"], Sequence[str]],
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeStorageSystemResourcesRequestRequestTypeDef(
    _RequiredDescribeStorageSystemResourcesRequestRequestTypeDef,
    _OptionalDescribeStorageSystemResourcesRequestRequestTypeDef,
):
    pass


DescribeTaskExecutionRequestRequestTypeDef = TypedDict(
    "DescribeTaskExecutionRequestRequestTypeDef",
    {
        "TaskExecutionArn": str,
    },
)

TaskExecutionResultDetailTypeDef = TypedDict(
    "TaskExecutionResultDetailTypeDef",
    {
        "PrepareDuration": int,
        "PrepareStatus": PhaseStatusType,
        "TotalDuration": int,
        "TransferDuration": int,
        "TransferStatus": PhaseStatusType,
        "VerifyDuration": int,
        "VerifyStatus": PhaseStatusType,
        "ErrorCode": str,
        "ErrorDetail": str,
    },
    total=False,
)

DescribeTaskRequestRequestTypeDef = TypedDict(
    "DescribeTaskRequestRequestTypeDef",
    {
        "TaskArn": str,
    },
)

DiscoveryJobListEntryTypeDef = TypedDict(
    "DiscoveryJobListEntryTypeDef",
    {
        "DiscoveryJobArn": str,
        "Status": DiscoveryJobStatusType,
    },
    total=False,
)

GenerateRecommendationsRequestRequestTypeDef = TypedDict(
    "GenerateRecommendationsRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
        "ResourceIds": Sequence[str],
        "ResourceType": DiscoveryResourceTypeType,
    },
)

IOPSTypeDef = TypedDict(
    "IOPSTypeDef",
    {
        "Read": float,
        "Write": float,
        "Other": float,
        "Total": float,
    },
    total=False,
)

LatencyTypeDef = TypedDict(
    "LatencyTypeDef",
    {
        "Read": float,
        "Write": float,
        "Other": float,
    },
    total=False,
)

ListAgentsRequestRequestTypeDef = TypedDict(
    "ListAgentsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListDiscoveryJobsRequestRequestTypeDef = TypedDict(
    "ListDiscoveryJobsRequestRequestTypeDef",
    {
        "StorageSystemArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

LocationFilterTypeDef = TypedDict(
    "LocationFilterTypeDef",
    {
        "Name": LocationFilterNameType,
        "Values": Sequence[str],
        "Operator": OperatorType,
    },
)

LocationListEntryTypeDef = TypedDict(
    "LocationListEntryTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
    },
    total=False,
)

ListStorageSystemsRequestRequestTypeDef = TypedDict(
    "ListStorageSystemsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

StorageSystemListEntryTypeDef = TypedDict(
    "StorageSystemListEntryTypeDef",
    {
        "StorageSystemArn": str,
        "Name": str,
    },
    total=False,
)

_RequiredListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceRequestRequestTypeDef(
    _RequiredListTagsForResourceRequestRequestTypeDef,
    _OptionalListTagsForResourceRequestRequestTypeDef,
):
    pass


ListTaskExecutionsRequestRequestTypeDef = TypedDict(
    "ListTaskExecutionsRequestRequestTypeDef",
    {
        "TaskArn": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

TaskExecutionListEntryTypeDef = TypedDict(
    "TaskExecutionListEntryTypeDef",
    {
        "TaskExecutionArn": str,
        "Status": TaskExecutionStatusType,
    },
    total=False,
)

TaskFilterTypeDef = TypedDict(
    "TaskFilterTypeDef",
    {
        "Name": TaskFilterNameType,
        "Values": Sequence[str],
        "Operator": OperatorType,
    },
)

TaskListEntryTypeDef = TypedDict(
    "TaskListEntryTypeDef",
    {
        "TaskArn": str,
        "Status": TaskStatusType,
        "Name": str,
    },
    total=False,
)

MaxP95PerformanceTypeDef = TypedDict(
    "MaxP95PerformanceTypeDef",
    {
        "IopsRead": float,
        "IopsWrite": float,
        "IopsOther": float,
        "IopsTotal": float,
        "ThroughputRead": float,
        "ThroughputWrite": float,
        "ThroughputOther": float,
        "ThroughputTotal": float,
        "LatencyRead": float,
        "LatencyWrite": float,
        "LatencyOther": float,
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "StorageType": str,
        "StorageConfiguration": Dict[str, str],
        "EstimatedMonthlyStorageCost": str,
    },
    total=False,
)

ThroughputTypeDef = TypedDict(
    "ThroughputTypeDef",
    {
        "Read": float,
        "Write": float,
        "Other": float,
        "Total": float,
    },
    total=False,
)

RemoveStorageSystemRequestRequestTypeDef = TypedDict(
    "RemoveStorageSystemRequestRequestTypeDef",
    {
        "StorageSystemArn": str,
    },
)

StopDiscoveryJobRequestRequestTypeDef = TypedDict(
    "StopDiscoveryJobRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Keys": Sequence[str],
    },
)

_RequiredUpdateAgentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateAgentRequestRequestTypeDef",
    {
        "AgentArn": str,
    },
)
_OptionalUpdateAgentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateAgentRequestRequestTypeDef",
    {
        "Name": str,
    },
    total=False,
)


class UpdateAgentRequestRequestTypeDef(
    _RequiredUpdateAgentRequestRequestTypeDef, _OptionalUpdateAgentRequestRequestTypeDef
):
    pass


UpdateDiscoveryJobRequestRequestTypeDef = TypedDict(
    "UpdateDiscoveryJobRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
        "CollectionDurationMinutes": int,
    },
)

_RequiredUpdateStorageSystemRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStorageSystemRequestRequestTypeDef",
    {
        "StorageSystemArn": str,
    },
)
_OptionalUpdateStorageSystemRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStorageSystemRequestRequestTypeDef",
    {
        "ServerConfiguration": DiscoveryServerConfigurationTypeDef,
        "AgentArns": Sequence[str],
        "Name": str,
        "CloudWatchLogGroupArn": str,
        "Credentials": CredentialsTypeDef,
    },
    total=False,
)


class UpdateStorageSystemRequestRequestTypeDef(
    _RequiredUpdateStorageSystemRequestRequestTypeDef,
    _OptionalUpdateStorageSystemRequestRequestTypeDef,
):
    pass


_RequiredAddStorageSystemRequestRequestTypeDef = TypedDict(
    "_RequiredAddStorageSystemRequestRequestTypeDef",
    {
        "ServerConfiguration": DiscoveryServerConfigurationTypeDef,
        "SystemType": Literal["NetAppONTAP"],
        "AgentArns": Sequence[str],
        "ClientToken": str,
        "Credentials": CredentialsTypeDef,
    },
)
_OptionalAddStorageSystemRequestRequestTypeDef = TypedDict(
    "_OptionalAddStorageSystemRequestRequestTypeDef",
    {
        "CloudWatchLogGroupArn": str,
        "Tags": Sequence[TagListEntryTypeDef],
        "Name": str,
    },
    total=False,
)


class AddStorageSystemRequestRequestTypeDef(
    _RequiredAddStorageSystemRequestRequestTypeDef, _OptionalAddStorageSystemRequestRequestTypeDef
):
    pass


_RequiredCreateAgentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateAgentRequestRequestTypeDef",
    {
        "ActivationKey": str,
    },
)
_OptionalCreateAgentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateAgentRequestRequestTypeDef",
    {
        "AgentName": str,
        "Tags": Sequence[TagListEntryTypeDef],
        "VpcEndpointId": str,
        "SubnetArns": Sequence[str],
        "SecurityGroupArns": Sequence[str],
    },
    total=False,
)


class CreateAgentRequestRequestTypeDef(
    _RequiredCreateAgentRequestRequestTypeDef, _OptionalCreateAgentRequestRequestTypeDef
):
    pass


_RequiredCreateLocationFsxLustreRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationFsxLustreRequestRequestTypeDef",
    {
        "FsxFilesystemArn": str,
        "SecurityGroupArns": Sequence[str],
    },
)
_OptionalCreateLocationFsxLustreRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationFsxLustreRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationFsxLustreRequestRequestTypeDef(
    _RequiredCreateLocationFsxLustreRequestRequestTypeDef,
    _OptionalCreateLocationFsxLustreRequestRequestTypeDef,
):
    pass


_RequiredCreateLocationFsxWindowsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationFsxWindowsRequestRequestTypeDef",
    {
        "FsxFilesystemArn": str,
        "SecurityGroupArns": Sequence[str],
        "User": str,
        "Password": str,
    },
)
_OptionalCreateLocationFsxWindowsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationFsxWindowsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
        "Domain": str,
    },
    total=False,
)


class CreateLocationFsxWindowsRequestRequestTypeDef(
    _RequiredCreateLocationFsxWindowsRequestRequestTypeDef,
    _OptionalCreateLocationFsxWindowsRequestRequestTypeDef,
):
    pass


_RequiredStartDiscoveryJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartDiscoveryJobRequestRequestTypeDef",
    {
        "StorageSystemArn": str,
        "CollectionDurationMinutes": int,
        "ClientToken": str,
    },
)
_OptionalStartDiscoveryJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartDiscoveryJobRequestRequestTypeDef",
    {
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class StartDiscoveryJobRequestRequestTypeDef(
    _RequiredStartDiscoveryJobRequestRequestTypeDef, _OptionalStartDiscoveryJobRequestRequestTypeDef
):
    pass


TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagListEntryTypeDef],
    },
)

AddStorageSystemResponseTypeDef = TypedDict(
    "AddStorageSystemResponseTypeDef",
    {
        "StorageSystemArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAgentResponseTypeDef = TypedDict(
    "CreateAgentResponseTypeDef",
    {
        "AgentArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationAzureBlobResponseTypeDef = TypedDict(
    "CreateLocationAzureBlobResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationEfsResponseTypeDef = TypedDict(
    "CreateLocationEfsResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationFsxLustreResponseTypeDef = TypedDict(
    "CreateLocationFsxLustreResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationFsxOntapResponseTypeDef = TypedDict(
    "CreateLocationFsxOntapResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationFsxOpenZfsResponseTypeDef = TypedDict(
    "CreateLocationFsxOpenZfsResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationFsxWindowsResponseTypeDef = TypedDict(
    "CreateLocationFsxWindowsResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationHdfsResponseTypeDef = TypedDict(
    "CreateLocationHdfsResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationNfsResponseTypeDef = TypedDict(
    "CreateLocationNfsResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationObjectStorageResponseTypeDef = TypedDict(
    "CreateLocationObjectStorageResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationS3ResponseTypeDef = TypedDict(
    "CreateLocationS3ResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLocationSmbResponseTypeDef = TypedDict(
    "CreateLocationSmbResponseTypeDef",
    {
        "LocationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateTaskResponseTypeDef = TypedDict(
    "CreateTaskResponseTypeDef",
    {
        "TaskArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDiscoveryJobResponseTypeDef = TypedDict(
    "DescribeDiscoveryJobResponseTypeDef",
    {
        "StorageSystemArn": str,
        "DiscoveryJobArn": str,
        "CollectionDurationMinutes": int,
        "Status": DiscoveryJobStatusType,
        "JobStartTime": datetime,
        "JobEndTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLocationAzureBlobResponseTypeDef = TypedDict(
    "DescribeLocationAzureBlobResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "AuthenticationType": Literal["SAS"],
        "BlobType": Literal["BLOCK"],
        "AccessTier": AzureAccessTierType,
        "AgentArns": List[str],
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLocationFsxLustreResponseTypeDef = TypedDict(
    "DescribeLocationFsxLustreResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "SecurityGroupArns": List[str],
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLocationFsxWindowsResponseTypeDef = TypedDict(
    "DescribeLocationFsxWindowsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "SecurityGroupArns": List[str],
        "CreationTime": datetime,
        "User": str,
        "Domain": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLocationObjectStorageResponseTypeDef = TypedDict(
    "DescribeLocationObjectStorageResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "AccessKey": str,
        "ServerPort": int,
        "ServerProtocol": ObjectStorageServerProtocolType,
        "AgentArns": List[str],
        "CreationTime": datetime,
        "ServerCertificate": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStorageSystemResponseTypeDef = TypedDict(
    "DescribeStorageSystemResponseTypeDef",
    {
        "StorageSystemArn": str,
        "ServerConfiguration": DiscoveryServerConfigurationTypeDef,
        "SystemType": Literal["NetAppONTAP"],
        "AgentArns": List[str],
        "Name": str,
        "ErrorMessage": str,
        "ConnectivityStatus": StorageSystemConnectivityStatusType,
        "CloudWatchLogGroupArn": str,
        "CreationTime": datetime,
        "SecretsManagerArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartDiscoveryJobResponseTypeDef = TypedDict(
    "StartDiscoveryJobResponseTypeDef",
    {
        "DiscoveryJobArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTaskExecutionResponseTypeDef = TypedDict(
    "StartTaskExecutionResponseTypeDef",
    {
        "TaskExecutionArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAgentsResponseTypeDef = TypedDict(
    "ListAgentsResponseTypeDef",
    {
        "Agents": List[AgentListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLocationAzureBlobRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationAzureBlobRequestRequestTypeDef",
    {
        "ContainerUrl": str,
        "AuthenticationType": Literal["SAS"],
        "AgentArns": Sequence[str],
    },
)
_OptionalCreateLocationAzureBlobRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationAzureBlobRequestRequestTypeDef",
    {
        "SasConfiguration": AzureBlobSasConfigurationTypeDef,
        "BlobType": Literal["BLOCK"],
        "AccessTier": AzureAccessTierType,
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationAzureBlobRequestRequestTypeDef(
    _RequiredCreateLocationAzureBlobRequestRequestTypeDef,
    _OptionalCreateLocationAzureBlobRequestRequestTypeDef,
):
    pass


_RequiredUpdateLocationAzureBlobRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLocationAzureBlobRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)
_OptionalUpdateLocationAzureBlobRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLocationAzureBlobRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "AuthenticationType": Literal["SAS"],
        "SasConfiguration": AzureBlobSasConfigurationTypeDef,
        "BlobType": Literal["BLOCK"],
        "AccessTier": AzureAccessTierType,
        "AgentArns": Sequence[str],
    },
    total=False,
)


class UpdateLocationAzureBlobRequestRequestTypeDef(
    _RequiredUpdateLocationAzureBlobRequestRequestTypeDef,
    _OptionalUpdateLocationAzureBlobRequestRequestTypeDef,
):
    pass


_RequiredCreateLocationObjectStorageRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationObjectStorageRequestRequestTypeDef",
    {
        "ServerHostname": str,
        "BucketName": str,
        "AgentArns": Sequence[str],
    },
)
_OptionalCreateLocationObjectStorageRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationObjectStorageRequestRequestTypeDef",
    {
        "ServerPort": int,
        "ServerProtocol": ObjectStorageServerProtocolType,
        "Subdirectory": str,
        "AccessKey": str,
        "SecretKey": str,
        "Tags": Sequence[TagListEntryTypeDef],
        "ServerCertificate": BlobTypeDef,
    },
    total=False,
)


class CreateLocationObjectStorageRequestRequestTypeDef(
    _RequiredCreateLocationObjectStorageRequestRequestTypeDef,
    _OptionalCreateLocationObjectStorageRequestRequestTypeDef,
):
    pass


_RequiredUpdateLocationObjectStorageRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLocationObjectStorageRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)
_OptionalUpdateLocationObjectStorageRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLocationObjectStorageRequestRequestTypeDef",
    {
        "ServerPort": int,
        "ServerProtocol": ObjectStorageServerProtocolType,
        "Subdirectory": str,
        "AccessKey": str,
        "SecretKey": str,
        "AgentArns": Sequence[str],
        "ServerCertificate": BlobTypeDef,
    },
    total=False,
)


class UpdateLocationObjectStorageRequestRequestTypeDef(
    _RequiredUpdateLocationObjectStorageRequestRequestTypeDef,
    _OptionalUpdateLocationObjectStorageRequestRequestTypeDef,
):
    pass


_RequiredCreateLocationEfsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationEfsRequestRequestTypeDef",
    {
        "EfsFilesystemArn": str,
        "Ec2Config": Ec2ConfigTypeDef,
    },
)
_OptionalCreateLocationEfsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationEfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
        "AccessPointArn": str,
        "FileSystemAccessRoleArn": str,
        "InTransitEncryption": EfsInTransitEncryptionType,
    },
    total=False,
)


class CreateLocationEfsRequestRequestTypeDef(
    _RequiredCreateLocationEfsRequestRequestTypeDef, _OptionalCreateLocationEfsRequestRequestTypeDef
):
    pass


DescribeLocationEfsResponseTypeDef = TypedDict(
    "DescribeLocationEfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "Ec2Config": Ec2ConfigTypeDef,
        "CreationTime": datetime,
        "AccessPointArn": str,
        "FileSystemAccessRoleArn": str,
        "InTransitEncryption": EfsInTransitEncryptionType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLocationHdfsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationHdfsRequestRequestTypeDef",
    {
        "NameNodes": Sequence[HdfsNameNodeTypeDef],
        "AuthenticationType": HdfsAuthenticationTypeType,
        "AgentArns": Sequence[str],
    },
)
_OptionalCreateLocationHdfsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationHdfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "BlockSize": int,
        "ReplicationFactor": int,
        "KmsKeyProviderUri": str,
        "QopConfiguration": QopConfigurationTypeDef,
        "SimpleUser": str,
        "KerberosPrincipal": str,
        "KerberosKeytab": BlobTypeDef,
        "KerberosKrb5Conf": BlobTypeDef,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationHdfsRequestRequestTypeDef(
    _RequiredCreateLocationHdfsRequestRequestTypeDef,
    _OptionalCreateLocationHdfsRequestRequestTypeDef,
):
    pass


DescribeLocationHdfsResponseTypeDef = TypedDict(
    "DescribeLocationHdfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "NameNodes": List[HdfsNameNodeTypeDef],
        "BlockSize": int,
        "ReplicationFactor": int,
        "KmsKeyProviderUri": str,
        "QopConfiguration": QopConfigurationTypeDef,
        "AuthenticationType": HdfsAuthenticationTypeType,
        "SimpleUser": str,
        "KerberosPrincipal": str,
        "AgentArns": List[str],
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLocationHdfsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLocationHdfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)
_OptionalUpdateLocationHdfsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLocationHdfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "NameNodes": Sequence[HdfsNameNodeTypeDef],
        "BlockSize": int,
        "ReplicationFactor": int,
        "KmsKeyProviderUri": str,
        "QopConfiguration": QopConfigurationTypeDef,
        "AuthenticationType": HdfsAuthenticationTypeType,
        "SimpleUser": str,
        "KerberosPrincipal": str,
        "KerberosKeytab": BlobTypeDef,
        "KerberosKrb5Conf": BlobTypeDef,
        "AgentArns": Sequence[str],
    },
    total=False,
)


class UpdateLocationHdfsRequestRequestTypeDef(
    _RequiredUpdateLocationHdfsRequestRequestTypeDef,
    _OptionalUpdateLocationHdfsRequestRequestTypeDef,
):
    pass


FsxProtocolNfsTypeDef = TypedDict(
    "FsxProtocolNfsTypeDef",
    {
        "MountOptions": NfsMountOptionsTypeDef,
    },
    total=False,
)

_RequiredCreateLocationNfsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationNfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "ServerHostname": str,
        "OnPremConfig": OnPremConfigTypeDef,
    },
)
_OptionalCreateLocationNfsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationNfsRequestRequestTypeDef",
    {
        "MountOptions": NfsMountOptionsTypeDef,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationNfsRequestRequestTypeDef(
    _RequiredCreateLocationNfsRequestRequestTypeDef, _OptionalCreateLocationNfsRequestRequestTypeDef
):
    pass


DescribeLocationNfsResponseTypeDef = TypedDict(
    "DescribeLocationNfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "OnPremConfig": OnPremConfigTypeDef,
        "MountOptions": NfsMountOptionsTypeDef,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateLocationNfsRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLocationNfsRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)
_OptionalUpdateLocationNfsRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLocationNfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "OnPremConfig": OnPremConfigTypeDef,
        "MountOptions": NfsMountOptionsTypeDef,
    },
    total=False,
)


class UpdateLocationNfsRequestRequestTypeDef(
    _RequiredUpdateLocationNfsRequestRequestTypeDef, _OptionalUpdateLocationNfsRequestRequestTypeDef
):
    pass


_RequiredCreateLocationS3RequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationS3RequestRequestTypeDef",
    {
        "S3BucketArn": str,
        "S3Config": S3ConfigTypeDef,
    },
)
_OptionalCreateLocationS3RequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationS3RequestRequestTypeDef",
    {
        "Subdirectory": str,
        "S3StorageClass": S3StorageClassType,
        "AgentArns": Sequence[str],
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationS3RequestRequestTypeDef(
    _RequiredCreateLocationS3RequestRequestTypeDef, _OptionalCreateLocationS3RequestRequestTypeDef
):
    pass


DescribeLocationS3ResponseTypeDef = TypedDict(
    "DescribeLocationS3ResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "S3StorageClass": S3StorageClassType,
        "S3Config": S3ConfigTypeDef,
        "AgentArns": List[str],
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateLocationSmbRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationSmbRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "ServerHostname": str,
        "User": str,
        "Password": str,
        "AgentArns": Sequence[str],
    },
)
_OptionalCreateLocationSmbRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationSmbRequestRequestTypeDef",
    {
        "Domain": str,
        "MountOptions": SmbMountOptionsTypeDef,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationSmbRequestRequestTypeDef(
    _RequiredCreateLocationSmbRequestRequestTypeDef, _OptionalCreateLocationSmbRequestRequestTypeDef
):
    pass


DescribeLocationSmbResponseTypeDef = TypedDict(
    "DescribeLocationSmbResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "AgentArns": List[str],
        "User": str,
        "Domain": str,
        "MountOptions": SmbMountOptionsTypeDef,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredFsxProtocolSmbTypeDef = TypedDict(
    "_RequiredFsxProtocolSmbTypeDef",
    {
        "Password": str,
        "User": str,
    },
)
_OptionalFsxProtocolSmbTypeDef = TypedDict(
    "_OptionalFsxProtocolSmbTypeDef",
    {
        "Domain": str,
        "MountOptions": SmbMountOptionsTypeDef,
    },
    total=False,
)


class FsxProtocolSmbTypeDef(_RequiredFsxProtocolSmbTypeDef, _OptionalFsxProtocolSmbTypeDef):
    pass


_RequiredUpdateLocationSmbRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLocationSmbRequestRequestTypeDef",
    {
        "LocationArn": str,
    },
)
_OptionalUpdateLocationSmbRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLocationSmbRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "User": str,
        "Domain": str,
        "Password": str,
        "AgentArns": Sequence[str],
        "MountOptions": SmbMountOptionsTypeDef,
    },
    total=False,
)


class UpdateLocationSmbRequestRequestTypeDef(
    _RequiredUpdateLocationSmbRequestRequestTypeDef, _OptionalUpdateLocationSmbRequestRequestTypeDef
):
    pass


_RequiredStartTaskExecutionRequestRequestTypeDef = TypedDict(
    "_RequiredStartTaskExecutionRequestRequestTypeDef",
    {
        "TaskArn": str,
    },
)
_OptionalStartTaskExecutionRequestRequestTypeDef = TypedDict(
    "_OptionalStartTaskExecutionRequestRequestTypeDef",
    {
        "OverrideOptions": OptionsTypeDef,
        "Includes": Sequence[FilterRuleTypeDef],
        "Excludes": Sequence[FilterRuleTypeDef],
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class StartTaskExecutionRequestRequestTypeDef(
    _RequiredStartTaskExecutionRequestRequestTypeDef,
    _OptionalStartTaskExecutionRequestRequestTypeDef,
):
    pass


UpdateTaskExecutionRequestRequestTypeDef = TypedDict(
    "UpdateTaskExecutionRequestRequestTypeDef",
    {
        "TaskExecutionArn": str,
        "Options": OptionsTypeDef,
    },
)

_RequiredCreateTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTaskRequestRequestTypeDef",
    {
        "SourceLocationArn": str,
        "DestinationLocationArn": str,
    },
)
_OptionalCreateTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTaskRequestRequestTypeDef",
    {
        "CloudWatchLogGroupArn": str,
        "Name": str,
        "Options": OptionsTypeDef,
        "Excludes": Sequence[FilterRuleTypeDef],
        "Schedule": TaskScheduleTypeDef,
        "Tags": Sequence[TagListEntryTypeDef],
        "Includes": Sequence[FilterRuleTypeDef],
    },
    total=False,
)


class CreateTaskRequestRequestTypeDef(
    _RequiredCreateTaskRequestRequestTypeDef, _OptionalCreateTaskRequestRequestTypeDef
):
    pass


DescribeTaskResponseTypeDef = TypedDict(
    "DescribeTaskResponseTypeDef",
    {
        "TaskArn": str,
        "Status": TaskStatusType,
        "Name": str,
        "CurrentTaskExecutionArn": str,
        "SourceLocationArn": str,
        "DestinationLocationArn": str,
        "CloudWatchLogGroupArn": str,
        "SourceNetworkInterfaceArns": List[str],
        "DestinationNetworkInterfaceArns": List[str],
        "Options": OptionsTypeDef,
        "Excludes": List[FilterRuleTypeDef],
        "Schedule": TaskScheduleTypeDef,
        "ErrorCode": str,
        "ErrorDetail": str,
        "CreationTime": datetime,
        "Includes": List[FilterRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateTaskRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTaskRequestRequestTypeDef",
    {
        "TaskArn": str,
    },
)
_OptionalUpdateTaskRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTaskRequestRequestTypeDef",
    {
        "Options": OptionsTypeDef,
        "Excludes": Sequence[FilterRuleTypeDef],
        "Schedule": TaskScheduleTypeDef,
        "Name": str,
        "CloudWatchLogGroupArn": str,
        "Includes": Sequence[FilterRuleTypeDef],
    },
    total=False,
)


class UpdateTaskRequestRequestTypeDef(
    _RequiredUpdateTaskRequestRequestTypeDef, _OptionalUpdateTaskRequestRequestTypeDef
):
    pass


DescribeAgentResponseTypeDef = TypedDict(
    "DescribeAgentResponseTypeDef",
    {
        "AgentArn": str,
        "Name": str,
        "Status": AgentStatusType,
        "LastConnectionTime": datetime,
        "CreationTime": datetime,
        "EndpointType": EndpointTypeType,
        "PrivateLinkConfig": PrivateLinkConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAgentsRequestListAgentsPaginateTypeDef = TypedDict(
    "ListAgentsRequestListAgentsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef = TypedDict(
    "ListDiscoveryJobsRequestListDiscoveryJobsPaginateTypeDef",
    {
        "StorageSystemArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListStorageSystemsRequestListStorageSystemsPaginateTypeDef = TypedDict(
    "ListStorageSystemsRequestListStorageSystemsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListTagsForResourceRequestListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceRequestListTagsForResourcePaginateTypeDef,
):
    pass


ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef = TypedDict(
    "ListTaskExecutionsRequestListTaskExecutionsPaginateTypeDef",
    {
        "TaskArn": str,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef = TypedDict(
    "_RequiredDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef",
    {
        "DiscoveryJobArn": str,
        "ResourceType": DiscoveryResourceTypeType,
        "ResourceId": str,
    },
)
_OptionalDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef = TypedDict(
    "_OptionalDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class DescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef(
    _RequiredDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef,
    _OptionalDescribeStorageSystemResourceMetricsRequestDescribeStorageSystemResourceMetricsPaginateTypeDef,
):
    pass


_RequiredDescribeStorageSystemResourceMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeStorageSystemResourceMetricsRequestRequestTypeDef",
    {
        "DiscoveryJobArn": str,
        "ResourceType": DiscoveryResourceTypeType,
        "ResourceId": str,
    },
)
_OptionalDescribeStorageSystemResourceMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeStorageSystemResourceMetricsRequestRequestTypeDef",
    {
        "StartTime": TimestampTypeDef,
        "EndTime": TimestampTypeDef,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class DescribeStorageSystemResourceMetricsRequestRequestTypeDef(
    _RequiredDescribeStorageSystemResourceMetricsRequestRequestTypeDef,
    _OptionalDescribeStorageSystemResourceMetricsRequestRequestTypeDef,
):
    pass


DescribeTaskExecutionResponseTypeDef = TypedDict(
    "DescribeTaskExecutionResponseTypeDef",
    {
        "TaskExecutionArn": str,
        "Status": TaskExecutionStatusType,
        "Options": OptionsTypeDef,
        "Excludes": List[FilterRuleTypeDef],
        "Includes": List[FilterRuleTypeDef],
        "StartTime": datetime,
        "EstimatedFilesToTransfer": int,
        "EstimatedBytesToTransfer": int,
        "FilesTransferred": int,
        "BytesWritten": int,
        "BytesTransferred": int,
        "Result": TaskExecutionResultDetailTypeDef,
        "BytesCompressed": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDiscoveryJobsResponseTypeDef = TypedDict(
    "ListDiscoveryJobsResponseTypeDef",
    {
        "DiscoveryJobs": List[DiscoveryJobListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLocationsRequestListLocationsPaginateTypeDef = TypedDict(
    "ListLocationsRequestListLocationsPaginateTypeDef",
    {
        "Filters": Sequence[LocationFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListLocationsRequestRequestTypeDef = TypedDict(
    "ListLocationsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[LocationFilterTypeDef],
    },
    total=False,
)

ListLocationsResponseTypeDef = TypedDict(
    "ListLocationsResponseTypeDef",
    {
        "Locations": List[LocationListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStorageSystemsResponseTypeDef = TypedDict(
    "ListStorageSystemsResponseTypeDef",
    {
        "StorageSystems": List[StorageSystemListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTaskExecutionsResponseTypeDef = TypedDict(
    "ListTaskExecutionsResponseTypeDef",
    {
        "TaskExecutions": List[TaskExecutionListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTasksRequestListTasksPaginateTypeDef = TypedDict(
    "ListTasksRequestListTasksPaginateTypeDef",
    {
        "Filters": Sequence[TaskFilterTypeDef],
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListTasksRequestRequestTypeDef = TypedDict(
    "ListTasksRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "Filters": Sequence[TaskFilterTypeDef],
    },
    total=False,
)

ListTasksResponseTypeDef = TypedDict(
    "ListTasksResponseTypeDef",
    {
        "Tasks": List[TaskListEntryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NetAppONTAPClusterTypeDef = TypedDict(
    "NetAppONTAPClusterTypeDef",
    {
        "CifsShareCount": int,
        "NfsExportedVolumes": int,
        "ResourceId": str,
        "ClusterName": str,
        "MaxP95Performance": MaxP95PerformanceTypeDef,
        "ClusterBlockStorageSize": int,
        "ClusterBlockStorageUsed": int,
        "ClusterBlockStorageLogicalUsed": int,
        "Recommendations": List[RecommendationTypeDef],
        "RecommendationStatus": RecommendationStatusType,
        "LunCount": int,
        "ClusterCloudStorageUsed": int,
    },
    total=False,
)

NetAppONTAPSVMTypeDef = TypedDict(
    "NetAppONTAPSVMTypeDef",
    {
        "ClusterUuid": str,
        "ResourceId": str,
        "SvmName": str,
        "CifsShareCount": int,
        "EnabledProtocols": List[str],
        "TotalCapacityUsed": int,
        "TotalCapacityProvisioned": int,
        "TotalLogicalCapacityUsed": int,
        "MaxP95Performance": MaxP95PerformanceTypeDef,
        "Recommendations": List[RecommendationTypeDef],
        "NfsExportedVolumes": int,
        "RecommendationStatus": RecommendationStatusType,
        "TotalSnapshotCapacityUsed": int,
        "LunCount": int,
    },
    total=False,
)

NetAppONTAPVolumeTypeDef = TypedDict(
    "NetAppONTAPVolumeTypeDef",
    {
        "VolumeName": str,
        "ResourceId": str,
        "CifsShareCount": int,
        "SecurityStyle": str,
        "SvmUuid": str,
        "SvmName": str,
        "CapacityUsed": int,
        "CapacityProvisioned": int,
        "LogicalCapacityUsed": int,
        "NfsExported": bool,
        "SnapshotCapacityUsed": int,
        "MaxP95Performance": MaxP95PerformanceTypeDef,
        "Recommendations": List[RecommendationTypeDef],
        "RecommendationStatus": RecommendationStatusType,
        "LunCount": int,
    },
    total=False,
)

P95MetricsTypeDef = TypedDict(
    "P95MetricsTypeDef",
    {
        "IOPS": IOPSTypeDef,
        "Throughput": ThroughputTypeDef,
        "Latency": LatencyTypeDef,
    },
    total=False,
)

FsxProtocolTypeDef = TypedDict(
    "FsxProtocolTypeDef",
    {
        "NFS": FsxProtocolNfsTypeDef,
        "SMB": FsxProtocolSmbTypeDef,
    },
    total=False,
)

ResourceDetailsTypeDef = TypedDict(
    "ResourceDetailsTypeDef",
    {
        "NetAppONTAPSVMs": List[NetAppONTAPSVMTypeDef],
        "NetAppONTAPVolumes": List[NetAppONTAPVolumeTypeDef],
        "NetAppONTAPClusters": List[NetAppONTAPClusterTypeDef],
    },
    total=False,
)

ResourceMetricsTypeDef = TypedDict(
    "ResourceMetricsTypeDef",
    {
        "Timestamp": datetime,
        "P95Metrics": P95MetricsTypeDef,
        "Capacity": CapacityTypeDef,
        "ResourceId": str,
        "ResourceType": DiscoveryResourceTypeType,
    },
    total=False,
)

_RequiredCreateLocationFsxOntapRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationFsxOntapRequestRequestTypeDef",
    {
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": Sequence[str],
        "StorageVirtualMachineArn": str,
    },
)
_OptionalCreateLocationFsxOntapRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationFsxOntapRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationFsxOntapRequestRequestTypeDef(
    _RequiredCreateLocationFsxOntapRequestRequestTypeDef,
    _OptionalCreateLocationFsxOntapRequestRequestTypeDef,
):
    pass


_RequiredCreateLocationFsxOpenZfsRequestRequestTypeDef = TypedDict(
    "_RequiredCreateLocationFsxOpenZfsRequestRequestTypeDef",
    {
        "FsxFilesystemArn": str,
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": Sequence[str],
    },
)
_OptionalCreateLocationFsxOpenZfsRequestRequestTypeDef = TypedDict(
    "_OptionalCreateLocationFsxOpenZfsRequestRequestTypeDef",
    {
        "Subdirectory": str,
        "Tags": Sequence[TagListEntryTypeDef],
    },
    total=False,
)


class CreateLocationFsxOpenZfsRequestRequestTypeDef(
    _RequiredCreateLocationFsxOpenZfsRequestRequestTypeDef,
    _OptionalCreateLocationFsxOpenZfsRequestRequestTypeDef,
):
    pass


DescribeLocationFsxOntapResponseTypeDef = TypedDict(
    "DescribeLocationFsxOntapResponseTypeDef",
    {
        "CreationTime": datetime,
        "LocationArn": str,
        "LocationUri": str,
        "Protocol": FsxProtocolTypeDef,
        "SecurityGroupArns": List[str],
        "StorageVirtualMachineArn": str,
        "FsxFilesystemArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLocationFsxOpenZfsResponseTypeDef = TypedDict(
    "DescribeLocationFsxOpenZfsResponseTypeDef",
    {
        "LocationArn": str,
        "LocationUri": str,
        "SecurityGroupArns": List[str],
        "Protocol": FsxProtocolTypeDef,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStorageSystemResourcesResponseTypeDef = TypedDict(
    "DescribeStorageSystemResourcesResponseTypeDef",
    {
        "ResourceDetails": ResourceDetailsTypeDef,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStorageSystemResourceMetricsResponseTypeDef = TypedDict(
    "DescribeStorageSystemResourceMetricsResponseTypeDef",
    {
        "Metrics": List[ResourceMetricsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
