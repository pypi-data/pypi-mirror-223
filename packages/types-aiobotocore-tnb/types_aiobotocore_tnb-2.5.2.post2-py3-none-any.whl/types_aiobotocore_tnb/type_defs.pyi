"""
Type annotations for tnb service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/type_defs/)

Usage::

    ```python
    from types_aiobotocore_tnb.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    LcmOperationTypeType,
    NsdOnboardingStateType,
    NsdOperationalStateType,
    NsdUsageStateType,
    NsLcmOperationStateType,
    NsStateType,
    OnboardingStateType,
    OperationalStateType,
    TaskStatusType,
    UsageStateType,
    VnfInstantiationStateType,
    VnfOperationalStateType,
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
    "BlobTypeDef",
    "CancelSolNetworkOperationInputRequestTypeDef",
    "CreateSolFunctionPackageInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateSolNetworkInstanceInputRequestTypeDef",
    "CreateSolNetworkPackageInputRequestTypeDef",
    "DeleteSolFunctionPackageInputRequestTypeDef",
    "DeleteSolNetworkInstanceInputRequestTypeDef",
    "DeleteSolNetworkPackageInputRequestTypeDef",
    "ErrorInfoTypeDef",
    "ToscaOverrideTypeDef",
    "GetSolFunctionInstanceInputRequestTypeDef",
    "GetSolFunctionInstanceMetadataTypeDef",
    "GetSolFunctionPackageContentInputRequestTypeDef",
    "GetSolFunctionPackageDescriptorInputRequestTypeDef",
    "GetSolFunctionPackageInputRequestTypeDef",
    "GetSolInstantiatedVnfInfoTypeDef",
    "GetSolNetworkInstanceInputRequestTypeDef",
    "GetSolNetworkInstanceMetadataTypeDef",
    "LcmOperationInfoTypeDef",
    "GetSolNetworkOperationInputRequestTypeDef",
    "GetSolNetworkOperationMetadataTypeDef",
    "ProblemDetailsTypeDef",
    "GetSolNetworkPackageContentInputRequestTypeDef",
    "GetSolNetworkPackageDescriptorInputRequestTypeDef",
    "GetSolNetworkPackageInputRequestTypeDef",
    "GetSolVnfcResourceInfoMetadataTypeDef",
    "InstantiateSolNetworkInstanceInputRequestTypeDef",
    "ListSolFunctionInstanceMetadataTypeDef",
    "PaginatorConfigTypeDef",
    "ListSolFunctionInstancesInputRequestTypeDef",
    "ListSolFunctionPackageMetadataTypeDef",
    "ListSolFunctionPackagesInputRequestTypeDef",
    "ListSolNetworkInstanceMetadataTypeDef",
    "ListSolNetworkInstancesInputRequestTypeDef",
    "ListSolNetworkOperationsMetadataTypeDef",
    "ListSolNetworkOperationsInputRequestTypeDef",
    "ListSolNetworkPackageMetadataTypeDef",
    "ListSolNetworkPackagesInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "TerminateSolNetworkInstanceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateSolFunctionPackageInputRequestTypeDef",
    "UpdateSolNetworkModifyTypeDef",
    "UpdateSolNetworkPackageInputRequestTypeDef",
    "PutSolFunctionPackageContentInputRequestTypeDef",
    "PutSolNetworkPackageContentInputRequestTypeDef",
    "ValidateSolFunctionPackageContentInputRequestTypeDef",
    "ValidateSolNetworkPackageContentInputRequestTypeDef",
    "CreateSolFunctionPackageOutputTypeDef",
    "CreateSolNetworkInstanceOutputTypeDef",
    "CreateSolNetworkPackageOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetSolFunctionPackageContentOutputTypeDef",
    "GetSolFunctionPackageDescriptorOutputTypeDef",
    "GetSolNetworkPackageContentOutputTypeDef",
    "GetSolNetworkPackageDescriptorOutputTypeDef",
    "InstantiateSolNetworkInstanceOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TerminateSolNetworkInstanceOutputTypeDef",
    "UpdateSolFunctionPackageOutputTypeDef",
    "UpdateSolNetworkInstanceOutputTypeDef",
    "UpdateSolNetworkPackageOutputTypeDef",
    "GetSolNetworkOperationTaskDetailsTypeDef",
    "FunctionArtifactMetaTypeDef",
    "NetworkArtifactMetaTypeDef",
    "GetSolNetworkInstanceOutputTypeDef",
    "GetSolVnfcResourceInfoTypeDef",
    "ListSolFunctionInstanceInfoTypeDef",
    "ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef",
    "ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef",
    "ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef",
    "ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef",
    "ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef",
    "ListSolFunctionPackageInfoTypeDef",
    "ListSolNetworkInstanceInfoTypeDef",
    "ListSolNetworkOperationsInfoTypeDef",
    "ListSolNetworkPackageInfoTypeDef",
    "UpdateSolNetworkInstanceInputRequestTypeDef",
    "GetSolNetworkOperationOutputTypeDef",
    "GetSolFunctionPackageMetadataTypeDef",
    "PutSolFunctionPackageContentMetadataTypeDef",
    "ValidateSolFunctionPackageContentMetadataTypeDef",
    "GetSolNetworkPackageMetadataTypeDef",
    "PutSolNetworkPackageContentMetadataTypeDef",
    "ValidateSolNetworkPackageContentMetadataTypeDef",
    "GetSolVnfInfoTypeDef",
    "ListSolFunctionInstancesOutputTypeDef",
    "ListSolFunctionPackagesOutputTypeDef",
    "ListSolNetworkInstancesOutputTypeDef",
    "ListSolNetworkOperationsOutputTypeDef",
    "ListSolNetworkPackagesOutputTypeDef",
    "GetSolFunctionPackageOutputTypeDef",
    "PutSolFunctionPackageContentOutputTypeDef",
    "ValidateSolFunctionPackageContentOutputTypeDef",
    "GetSolNetworkPackageOutputTypeDef",
    "PutSolNetworkPackageContentOutputTypeDef",
    "ValidateSolNetworkPackageContentOutputTypeDef",
    "GetSolFunctionInstanceOutputTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
CancelSolNetworkOperationInputRequestTypeDef = TypedDict(
    "CancelSolNetworkOperationInputRequestTypeDef",
    {
        "nsLcmOpOccId": str,
    },
)

CreateSolFunctionPackageInputRequestTypeDef = TypedDict(
    "CreateSolFunctionPackageInputRequestTypeDef",
    {
        "tags": Mapping[str, str],
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

_RequiredCreateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_RequiredCreateSolNetworkInstanceInputRequestTypeDef",
    {
        "nsName": str,
        "nsdInfoId": str,
    },
)
_OptionalCreateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_OptionalCreateSolNetworkInstanceInputRequestTypeDef",
    {
        "nsDescription": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateSolNetworkInstanceInputRequestTypeDef(
    _RequiredCreateSolNetworkInstanceInputRequestTypeDef,
    _OptionalCreateSolNetworkInstanceInputRequestTypeDef,
):
    pass

CreateSolNetworkPackageInputRequestTypeDef = TypedDict(
    "CreateSolNetworkPackageInputRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

DeleteSolFunctionPackageInputRequestTypeDef = TypedDict(
    "DeleteSolFunctionPackageInputRequestTypeDef",
    {
        "vnfPkgId": str,
    },
)

DeleteSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "DeleteSolNetworkInstanceInputRequestTypeDef",
    {
        "nsInstanceId": str,
    },
)

DeleteSolNetworkPackageInputRequestTypeDef = TypedDict(
    "DeleteSolNetworkPackageInputRequestTypeDef",
    {
        "nsdInfoId": str,
    },
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "cause": str,
        "details": str,
    },
    total=False,
)

ToscaOverrideTypeDef = TypedDict(
    "ToscaOverrideTypeDef",
    {
        "defaultValue": str,
        "name": str,
    },
    total=False,
)

GetSolFunctionInstanceInputRequestTypeDef = TypedDict(
    "GetSolFunctionInstanceInputRequestTypeDef",
    {
        "vnfInstanceId": str,
    },
)

GetSolFunctionInstanceMetadataTypeDef = TypedDict(
    "GetSolFunctionInstanceMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

GetSolFunctionPackageContentInputRequestTypeDef = TypedDict(
    "GetSolFunctionPackageContentInputRequestTypeDef",
    {
        "accept": Literal["application/zip"],
        "vnfPkgId": str,
    },
)

GetSolFunctionPackageDescriptorInputRequestTypeDef = TypedDict(
    "GetSolFunctionPackageDescriptorInputRequestTypeDef",
    {
        "accept": Literal["text/plain"],
        "vnfPkgId": str,
    },
)

GetSolFunctionPackageInputRequestTypeDef = TypedDict(
    "GetSolFunctionPackageInputRequestTypeDef",
    {
        "vnfPkgId": str,
    },
)

GetSolInstantiatedVnfInfoTypeDef = TypedDict(
    "GetSolInstantiatedVnfInfoTypeDef",
    {
        "vnfState": VnfOperationalStateType,
    },
    total=False,
)

GetSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "GetSolNetworkInstanceInputRequestTypeDef",
    {
        "nsInstanceId": str,
    },
)

GetSolNetworkInstanceMetadataTypeDef = TypedDict(
    "GetSolNetworkInstanceMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

LcmOperationInfoTypeDef = TypedDict(
    "LcmOperationInfoTypeDef",
    {
        "nsLcmOpOccId": str,
    },
)

GetSolNetworkOperationInputRequestTypeDef = TypedDict(
    "GetSolNetworkOperationInputRequestTypeDef",
    {
        "nsLcmOpOccId": str,
    },
)

GetSolNetworkOperationMetadataTypeDef = TypedDict(
    "GetSolNetworkOperationMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

_RequiredProblemDetailsTypeDef = TypedDict(
    "_RequiredProblemDetailsTypeDef",
    {
        "detail": str,
    },
)
_OptionalProblemDetailsTypeDef = TypedDict(
    "_OptionalProblemDetailsTypeDef",
    {
        "title": str,
    },
    total=False,
)

class ProblemDetailsTypeDef(_RequiredProblemDetailsTypeDef, _OptionalProblemDetailsTypeDef):
    pass

GetSolNetworkPackageContentInputRequestTypeDef = TypedDict(
    "GetSolNetworkPackageContentInputRequestTypeDef",
    {
        "accept": Literal["application/zip"],
        "nsdInfoId": str,
    },
)

GetSolNetworkPackageDescriptorInputRequestTypeDef = TypedDict(
    "GetSolNetworkPackageDescriptorInputRequestTypeDef",
    {
        "nsdInfoId": str,
    },
)

GetSolNetworkPackageInputRequestTypeDef = TypedDict(
    "GetSolNetworkPackageInputRequestTypeDef",
    {
        "nsdInfoId": str,
    },
)

GetSolVnfcResourceInfoMetadataTypeDef = TypedDict(
    "GetSolVnfcResourceInfoMetadataTypeDef",
    {
        "cluster": str,
        "helmChart": str,
        "nodeGroup": str,
    },
    total=False,
)

_RequiredInstantiateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_RequiredInstantiateSolNetworkInstanceInputRequestTypeDef",
    {
        "nsInstanceId": str,
    },
)
_OptionalInstantiateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_OptionalInstantiateSolNetworkInstanceInputRequestTypeDef",
    {
        "additionalParamsForNs": Mapping[str, Any],
        "dryRun": bool,
        "tags": Mapping[str, str],
    },
    total=False,
)

class InstantiateSolNetworkInstanceInputRequestTypeDef(
    _RequiredInstantiateSolNetworkInstanceInputRequestTypeDef,
    _OptionalInstantiateSolNetworkInstanceInputRequestTypeDef,
):
    pass

ListSolFunctionInstanceMetadataTypeDef = TypedDict(
    "ListSolFunctionInstanceMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
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

ListSolFunctionInstancesInputRequestTypeDef = TypedDict(
    "ListSolFunctionInstancesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSolFunctionPackageMetadataTypeDef = TypedDict(
    "ListSolFunctionPackageMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

ListSolFunctionPackagesInputRequestTypeDef = TypedDict(
    "ListSolFunctionPackagesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSolNetworkInstanceMetadataTypeDef = TypedDict(
    "ListSolNetworkInstanceMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

ListSolNetworkInstancesInputRequestTypeDef = TypedDict(
    "ListSolNetworkInstancesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSolNetworkOperationsMetadataTypeDef = TypedDict(
    "ListSolNetworkOperationsMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

ListSolNetworkOperationsInputRequestTypeDef = TypedDict(
    "ListSolNetworkOperationsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListSolNetworkPackageMetadataTypeDef = TypedDict(
    "ListSolNetworkPackageMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)

ListSolNetworkPackagesInputRequestTypeDef = TypedDict(
    "ListSolNetworkPackagesInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

_RequiredTerminateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_RequiredTerminateSolNetworkInstanceInputRequestTypeDef",
    {
        "nsInstanceId": str,
    },
)
_OptionalTerminateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_OptionalTerminateSolNetworkInstanceInputRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)

class TerminateSolNetworkInstanceInputRequestTypeDef(
    _RequiredTerminateSolNetworkInstanceInputRequestTypeDef,
    _OptionalTerminateSolNetworkInstanceInputRequestTypeDef,
):
    pass

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateSolFunctionPackageInputRequestTypeDef = TypedDict(
    "UpdateSolFunctionPackageInputRequestTypeDef",
    {
        "operationalState": OperationalStateType,
        "vnfPkgId": str,
    },
)

UpdateSolNetworkModifyTypeDef = TypedDict(
    "UpdateSolNetworkModifyTypeDef",
    {
        "vnfConfigurableProperties": Mapping[str, Any],
        "vnfInstanceId": str,
    },
)

UpdateSolNetworkPackageInputRequestTypeDef = TypedDict(
    "UpdateSolNetworkPackageInputRequestTypeDef",
    {
        "nsdInfoId": str,
        "nsdOperationalState": NsdOperationalStateType,
    },
)

_RequiredPutSolFunctionPackageContentInputRequestTypeDef = TypedDict(
    "_RequiredPutSolFunctionPackageContentInputRequestTypeDef",
    {
        "file": BlobTypeDef,
        "vnfPkgId": str,
    },
)
_OptionalPutSolFunctionPackageContentInputRequestTypeDef = TypedDict(
    "_OptionalPutSolFunctionPackageContentInputRequestTypeDef",
    {
        "contentType": Literal["application/zip"],
    },
    total=False,
)

class PutSolFunctionPackageContentInputRequestTypeDef(
    _RequiredPutSolFunctionPackageContentInputRequestTypeDef,
    _OptionalPutSolFunctionPackageContentInputRequestTypeDef,
):
    pass

_RequiredPutSolNetworkPackageContentInputRequestTypeDef = TypedDict(
    "_RequiredPutSolNetworkPackageContentInputRequestTypeDef",
    {
        "file": BlobTypeDef,
        "nsdInfoId": str,
    },
)
_OptionalPutSolNetworkPackageContentInputRequestTypeDef = TypedDict(
    "_OptionalPutSolNetworkPackageContentInputRequestTypeDef",
    {
        "contentType": Literal["application/zip"],
    },
    total=False,
)

class PutSolNetworkPackageContentInputRequestTypeDef(
    _RequiredPutSolNetworkPackageContentInputRequestTypeDef,
    _OptionalPutSolNetworkPackageContentInputRequestTypeDef,
):
    pass

_RequiredValidateSolFunctionPackageContentInputRequestTypeDef = TypedDict(
    "_RequiredValidateSolFunctionPackageContentInputRequestTypeDef",
    {
        "file": BlobTypeDef,
        "vnfPkgId": str,
    },
)
_OptionalValidateSolFunctionPackageContentInputRequestTypeDef = TypedDict(
    "_OptionalValidateSolFunctionPackageContentInputRequestTypeDef",
    {
        "contentType": Literal["application/zip"],
    },
    total=False,
)

class ValidateSolFunctionPackageContentInputRequestTypeDef(
    _RequiredValidateSolFunctionPackageContentInputRequestTypeDef,
    _OptionalValidateSolFunctionPackageContentInputRequestTypeDef,
):
    pass

_RequiredValidateSolNetworkPackageContentInputRequestTypeDef = TypedDict(
    "_RequiredValidateSolNetworkPackageContentInputRequestTypeDef",
    {
        "file": BlobTypeDef,
        "nsdInfoId": str,
    },
)
_OptionalValidateSolNetworkPackageContentInputRequestTypeDef = TypedDict(
    "_OptionalValidateSolNetworkPackageContentInputRequestTypeDef",
    {
        "contentType": Literal["application/zip"],
    },
    total=False,
)

class ValidateSolNetworkPackageContentInputRequestTypeDef(
    _RequiredValidateSolNetworkPackageContentInputRequestTypeDef,
    _OptionalValidateSolNetworkPackageContentInputRequestTypeDef,
):
    pass

CreateSolFunctionPackageOutputTypeDef = TypedDict(
    "CreateSolFunctionPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "tags": Dict[str, str],
        "usageState": UsageStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSolNetworkInstanceOutputTypeDef = TypedDict(
    "CreateSolNetworkInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "nsInstanceName": str,
        "nsdInfoId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSolNetworkPackageOutputTypeDef = TypedDict(
    "CreateSolNetworkPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolFunctionPackageContentOutputTypeDef = TypedDict(
    "GetSolFunctionPackageContentOutputTypeDef",
    {
        "contentType": Literal["application/zip"],
        "packageContent": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolFunctionPackageDescriptorOutputTypeDef = TypedDict(
    "GetSolFunctionPackageDescriptorOutputTypeDef",
    {
        "contentType": Literal["text/plain"],
        "vnfd": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolNetworkPackageContentOutputTypeDef = TypedDict(
    "GetSolNetworkPackageContentOutputTypeDef",
    {
        "contentType": Literal["application/zip"],
        "nsdContent": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolNetworkPackageDescriptorOutputTypeDef = TypedDict(
    "GetSolNetworkPackageDescriptorOutputTypeDef",
    {
        "contentType": Literal["text/plain"],
        "nsd": StreamingBody,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstantiateSolNetworkInstanceOutputTypeDef = TypedDict(
    "InstantiateSolNetworkInstanceOutputTypeDef",
    {
        "nsLcmOpOccId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TerminateSolNetworkInstanceOutputTypeDef = TypedDict(
    "TerminateSolNetworkInstanceOutputTypeDef",
    {
        "nsLcmOpOccId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSolFunctionPackageOutputTypeDef = TypedDict(
    "UpdateSolFunctionPackageOutputTypeDef",
    {
        "operationalState": OperationalStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSolNetworkInstanceOutputTypeDef = TypedDict(
    "UpdateSolNetworkInstanceOutputTypeDef",
    {
        "nsLcmOpOccId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSolNetworkPackageOutputTypeDef = TypedDict(
    "UpdateSolNetworkPackageOutputTypeDef",
    {
        "nsdOperationalState": NsdOperationalStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolNetworkOperationTaskDetailsTypeDef = TypedDict(
    "GetSolNetworkOperationTaskDetailsTypeDef",
    {
        "taskContext": Dict[str, str],
        "taskEndTime": datetime,
        "taskErrorDetails": ErrorInfoTypeDef,
        "taskName": str,
        "taskStartTime": datetime,
        "taskStatus": TaskStatusType,
    },
    total=False,
)

FunctionArtifactMetaTypeDef = TypedDict(
    "FunctionArtifactMetaTypeDef",
    {
        "overrides": List[ToscaOverrideTypeDef],
    },
    total=False,
)

NetworkArtifactMetaTypeDef = TypedDict(
    "NetworkArtifactMetaTypeDef",
    {
        "overrides": List[ToscaOverrideTypeDef],
    },
    total=False,
)

GetSolNetworkInstanceOutputTypeDef = TypedDict(
    "GetSolNetworkInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "lcmOpInfo": LcmOperationInfoTypeDef,
        "metadata": GetSolNetworkInstanceMetadataTypeDef,
        "nsInstanceDescription": str,
        "nsInstanceName": str,
        "nsState": NsStateType,
        "nsdId": str,
        "nsdInfoId": str,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolVnfcResourceInfoTypeDef = TypedDict(
    "GetSolVnfcResourceInfoTypeDef",
    {
        "metadata": GetSolVnfcResourceInfoMetadataTypeDef,
    },
    total=False,
)

_RequiredListSolFunctionInstanceInfoTypeDef = TypedDict(
    "_RequiredListSolFunctionInstanceInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "instantiationState": VnfInstantiationStateType,
        "metadata": ListSolFunctionInstanceMetadataTypeDef,
        "nsInstanceId": str,
        "vnfPkgId": str,
    },
)
_OptionalListSolFunctionInstanceInfoTypeDef = TypedDict(
    "_OptionalListSolFunctionInstanceInfoTypeDef",
    {
        "instantiatedVnfInfo": GetSolInstantiatedVnfInfoTypeDef,
        "vnfPkgName": str,
    },
    total=False,
)

class ListSolFunctionInstanceInfoTypeDef(
    _RequiredListSolFunctionInstanceInfoTypeDef, _OptionalListSolFunctionInstanceInfoTypeDef
):
    pass

ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef = TypedDict(
    "ListSolFunctionInstancesInputListSolFunctionInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef = TypedDict(
    "ListSolFunctionPackagesInputListSolFunctionPackagesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef = TypedDict(
    "ListSolNetworkInstancesInputListSolNetworkInstancesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef = TypedDict(
    "ListSolNetworkOperationsInputListSolNetworkOperationsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef = TypedDict(
    "ListSolNetworkPackagesInputListSolNetworkPackagesPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

_RequiredListSolFunctionPackageInfoTypeDef = TypedDict(
    "_RequiredListSolFunctionPackageInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "usageState": UsageStateType,
    },
)
_OptionalListSolFunctionPackageInfoTypeDef = TypedDict(
    "_OptionalListSolFunctionPackageInfoTypeDef",
    {
        "metadata": ListSolFunctionPackageMetadataTypeDef,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
    },
    total=False,
)

class ListSolFunctionPackageInfoTypeDef(
    _RequiredListSolFunctionPackageInfoTypeDef, _OptionalListSolFunctionPackageInfoTypeDef
):
    pass

ListSolNetworkInstanceInfoTypeDef = TypedDict(
    "ListSolNetworkInstanceInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ListSolNetworkInstanceMetadataTypeDef,
        "nsInstanceDescription": str,
        "nsInstanceName": str,
        "nsState": NsStateType,
        "nsdId": str,
        "nsdInfoId": str,
    },
)

_RequiredListSolNetworkOperationsInfoTypeDef = TypedDict(
    "_RequiredListSolNetworkOperationsInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "lcmOperationType": LcmOperationTypeType,
        "nsInstanceId": str,
        "operationState": NsLcmOperationStateType,
    },
)
_OptionalListSolNetworkOperationsInfoTypeDef = TypedDict(
    "_OptionalListSolNetworkOperationsInfoTypeDef",
    {
        "error": ProblemDetailsTypeDef,
        "metadata": ListSolNetworkOperationsMetadataTypeDef,
    },
    total=False,
)

class ListSolNetworkOperationsInfoTypeDef(
    _RequiredListSolNetworkOperationsInfoTypeDef, _OptionalListSolNetworkOperationsInfoTypeDef
):
    pass

_RequiredListSolNetworkPackageInfoTypeDef = TypedDict(
    "_RequiredListSolNetworkPackageInfoTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ListSolNetworkPackageMetadataTypeDef,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
    },
)
_OptionalListSolNetworkPackageInfoTypeDef = TypedDict(
    "_OptionalListSolNetworkPackageInfoTypeDef",
    {
        "nsdDesigner": str,
        "nsdId": str,
        "nsdInvariantId": str,
        "nsdName": str,
        "nsdVersion": str,
        "vnfPkgIds": List[str],
    },
    total=False,
)

class ListSolNetworkPackageInfoTypeDef(
    _RequiredListSolNetworkPackageInfoTypeDef, _OptionalListSolNetworkPackageInfoTypeDef
):
    pass

_RequiredUpdateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_RequiredUpdateSolNetworkInstanceInputRequestTypeDef",
    {
        "nsInstanceId": str,
        "updateType": Literal["MODIFY_VNF_INFORMATION"],
    },
)
_OptionalUpdateSolNetworkInstanceInputRequestTypeDef = TypedDict(
    "_OptionalUpdateSolNetworkInstanceInputRequestTypeDef",
    {
        "modifyVnfInfoData": UpdateSolNetworkModifyTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class UpdateSolNetworkInstanceInputRequestTypeDef(
    _RequiredUpdateSolNetworkInstanceInputRequestTypeDef,
    _OptionalUpdateSolNetworkInstanceInputRequestTypeDef,
):
    pass

GetSolNetworkOperationOutputTypeDef = TypedDict(
    "GetSolNetworkOperationOutputTypeDef",
    {
        "arn": str,
        "error": ProblemDetailsTypeDef,
        "id": str,
        "lcmOperationType": LcmOperationTypeType,
        "metadata": GetSolNetworkOperationMetadataTypeDef,
        "nsInstanceId": str,
        "operationState": NsLcmOperationStateType,
        "tags": Dict[str, str],
        "tasks": List[GetSolNetworkOperationTaskDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetSolFunctionPackageMetadataTypeDef = TypedDict(
    "_RequiredGetSolFunctionPackageMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)
_OptionalGetSolFunctionPackageMetadataTypeDef = TypedDict(
    "_OptionalGetSolFunctionPackageMetadataTypeDef",
    {
        "vnfd": FunctionArtifactMetaTypeDef,
    },
    total=False,
)

class GetSolFunctionPackageMetadataTypeDef(
    _RequiredGetSolFunctionPackageMetadataTypeDef, _OptionalGetSolFunctionPackageMetadataTypeDef
):
    pass

PutSolFunctionPackageContentMetadataTypeDef = TypedDict(
    "PutSolFunctionPackageContentMetadataTypeDef",
    {
        "vnfd": FunctionArtifactMetaTypeDef,
    },
    total=False,
)

ValidateSolFunctionPackageContentMetadataTypeDef = TypedDict(
    "ValidateSolFunctionPackageContentMetadataTypeDef",
    {
        "vnfd": FunctionArtifactMetaTypeDef,
    },
    total=False,
)

_RequiredGetSolNetworkPackageMetadataTypeDef = TypedDict(
    "_RequiredGetSolNetworkPackageMetadataTypeDef",
    {
        "createdAt": datetime,
        "lastModified": datetime,
    },
)
_OptionalGetSolNetworkPackageMetadataTypeDef = TypedDict(
    "_OptionalGetSolNetworkPackageMetadataTypeDef",
    {
        "nsd": NetworkArtifactMetaTypeDef,
    },
    total=False,
)

class GetSolNetworkPackageMetadataTypeDef(
    _RequiredGetSolNetworkPackageMetadataTypeDef, _OptionalGetSolNetworkPackageMetadataTypeDef
):
    pass

PutSolNetworkPackageContentMetadataTypeDef = TypedDict(
    "PutSolNetworkPackageContentMetadataTypeDef",
    {
        "nsd": NetworkArtifactMetaTypeDef,
    },
    total=False,
)

ValidateSolNetworkPackageContentMetadataTypeDef = TypedDict(
    "ValidateSolNetworkPackageContentMetadataTypeDef",
    {
        "nsd": NetworkArtifactMetaTypeDef,
    },
    total=False,
)

GetSolVnfInfoTypeDef = TypedDict(
    "GetSolVnfInfoTypeDef",
    {
        "vnfState": VnfOperationalStateType,
        "vnfcResourceInfo": List[GetSolVnfcResourceInfoTypeDef],
    },
    total=False,
)

ListSolFunctionInstancesOutputTypeDef = TypedDict(
    "ListSolFunctionInstancesOutputTypeDef",
    {
        "functionInstances": List[ListSolFunctionInstanceInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSolFunctionPackagesOutputTypeDef = TypedDict(
    "ListSolFunctionPackagesOutputTypeDef",
    {
        "functionPackages": List[ListSolFunctionPackageInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSolNetworkInstancesOutputTypeDef = TypedDict(
    "ListSolNetworkInstancesOutputTypeDef",
    {
        "networkInstances": List[ListSolNetworkInstanceInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSolNetworkOperationsOutputTypeDef = TypedDict(
    "ListSolNetworkOperationsOutputTypeDef",
    {
        "networkOperations": List[ListSolNetworkOperationsInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSolNetworkPackagesOutputTypeDef = TypedDict(
    "ListSolNetworkPackagesOutputTypeDef",
    {
        "networkPackages": List[ListSolNetworkPackageInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolFunctionPackageOutputTypeDef = TypedDict(
    "GetSolFunctionPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": GetSolFunctionPackageMetadataTypeDef,
        "onboardingState": OnboardingStateType,
        "operationalState": OperationalStateType,
        "tags": Dict[str, str],
        "usageState": UsageStateType,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSolFunctionPackageContentOutputTypeDef = TypedDict(
    "PutSolFunctionPackageContentOutputTypeDef",
    {
        "id": str,
        "metadata": PutSolFunctionPackageContentMetadataTypeDef,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidateSolFunctionPackageContentOutputTypeDef = TypedDict(
    "ValidateSolFunctionPackageContentOutputTypeDef",
    {
        "id": str,
        "metadata": ValidateSolFunctionPackageContentMetadataTypeDef,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolNetworkPackageOutputTypeDef = TypedDict(
    "GetSolNetworkPackageOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": GetSolNetworkPackageMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdOnboardingState": NsdOnboardingStateType,
        "nsdOperationalState": NsdOperationalStateType,
        "nsdUsageState": NsdUsageStateType,
        "nsdVersion": str,
        "tags": Dict[str, str],
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutSolNetworkPackageContentOutputTypeDef = TypedDict(
    "PutSolNetworkPackageContentOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": PutSolNetworkPackageContentMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdVersion": str,
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ValidateSolNetworkPackageContentOutputTypeDef = TypedDict(
    "ValidateSolNetworkPackageContentOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "metadata": ValidateSolNetworkPackageContentMetadataTypeDef,
        "nsdId": str,
        "nsdName": str,
        "nsdVersion": str,
        "vnfPkgIds": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSolFunctionInstanceOutputTypeDef = TypedDict(
    "GetSolFunctionInstanceOutputTypeDef",
    {
        "arn": str,
        "id": str,
        "instantiatedVnfInfo": GetSolVnfInfoTypeDef,
        "instantiationState": VnfInstantiationStateType,
        "metadata": GetSolFunctionInstanceMetadataTypeDef,
        "nsInstanceId": str,
        "tags": Dict[str, str],
        "vnfPkgId": str,
        "vnfProductName": str,
        "vnfProvider": str,
        "vnfdId": str,
        "vnfdVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
