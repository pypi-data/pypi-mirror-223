"""
Type annotations for oam service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_oam/type_defs/)

Usage::

    ```python
    from types_aiobotocore_oam.type_defs import CreateLinkInputRequestTypeDef

    data: CreateLinkInputRequestTypeDef = ...
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import ResourceTypeType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "CreateLinkInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateSinkInputRequestTypeDef",
    "DeleteLinkInputRequestTypeDef",
    "DeleteSinkInputRequestTypeDef",
    "GetLinkInputRequestTypeDef",
    "GetSinkInputRequestTypeDef",
    "GetSinkPolicyInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListAttachedLinksInputRequestTypeDef",
    "ListAttachedLinksItemTypeDef",
    "ListLinksInputRequestTypeDef",
    "ListLinksItemTypeDef",
    "ListSinksInputRequestTypeDef",
    "ListSinksItemTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "PutSinkPolicyInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateLinkInputRequestTypeDef",
    "CreateLinkOutputTypeDef",
    "CreateSinkOutputTypeDef",
    "GetLinkOutputTypeDef",
    "GetSinkOutputTypeDef",
    "GetSinkPolicyOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "PutSinkPolicyOutputTypeDef",
    "UpdateLinkOutputTypeDef",
    "ListAttachedLinksInputListAttachedLinksPaginateTypeDef",
    "ListLinksInputListLinksPaginateTypeDef",
    "ListSinksInputListSinksPaginateTypeDef",
    "ListAttachedLinksOutputTypeDef",
    "ListLinksOutputTypeDef",
    "ListSinksOutputTypeDef",
)

_RequiredCreateLinkInputRequestTypeDef = TypedDict(
    "_RequiredCreateLinkInputRequestTypeDef",
    {
        "LabelTemplate": str,
        "ResourceTypes": Sequence[ResourceTypeType],
        "SinkIdentifier": str,
    },
)
_OptionalCreateLinkInputRequestTypeDef = TypedDict(
    "_OptionalCreateLinkInputRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateLinkInputRequestTypeDef(
    _RequiredCreateLinkInputRequestTypeDef, _OptionalCreateLinkInputRequestTypeDef
):
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

_RequiredCreateSinkInputRequestTypeDef = TypedDict(
    "_RequiredCreateSinkInputRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalCreateSinkInputRequestTypeDef = TypedDict(
    "_OptionalCreateSinkInputRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)

class CreateSinkInputRequestTypeDef(
    _RequiredCreateSinkInputRequestTypeDef, _OptionalCreateSinkInputRequestTypeDef
):
    pass

DeleteLinkInputRequestTypeDef = TypedDict(
    "DeleteLinkInputRequestTypeDef",
    {
        "Identifier": str,
    },
)

DeleteSinkInputRequestTypeDef = TypedDict(
    "DeleteSinkInputRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetLinkInputRequestTypeDef = TypedDict(
    "GetLinkInputRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetSinkInputRequestTypeDef = TypedDict(
    "GetSinkInputRequestTypeDef",
    {
        "Identifier": str,
    },
)

GetSinkPolicyInputRequestTypeDef = TypedDict(
    "GetSinkPolicyInputRequestTypeDef",
    {
        "SinkIdentifier": str,
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

_RequiredListAttachedLinksInputRequestTypeDef = TypedDict(
    "_RequiredListAttachedLinksInputRequestTypeDef",
    {
        "SinkIdentifier": str,
    },
)
_OptionalListAttachedLinksInputRequestTypeDef = TypedDict(
    "_OptionalListAttachedLinksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

class ListAttachedLinksInputRequestTypeDef(
    _RequiredListAttachedLinksInputRequestTypeDef, _OptionalListAttachedLinksInputRequestTypeDef
):
    pass

ListAttachedLinksItemTypeDef = TypedDict(
    "ListAttachedLinksItemTypeDef",
    {
        "Label": str,
        "LinkArn": str,
        "ResourceTypes": List[str],
    },
    total=False,
)

ListLinksInputRequestTypeDef = TypedDict(
    "ListLinksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListLinksItemTypeDef = TypedDict(
    "ListLinksItemTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Label": str,
        "ResourceTypes": List[str],
        "SinkArn": str,
    },
    total=False,
)

ListSinksInputRequestTypeDef = TypedDict(
    "ListSinksInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListSinksItemTypeDef = TypedDict(
    "ListSinksItemTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PutSinkPolicyInputRequestTypeDef = TypedDict(
    "PutSinkPolicyInputRequestTypeDef",
    {
        "SinkIdentifier": str,
        "Policy": str,
    },
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

UpdateLinkInputRequestTypeDef = TypedDict(
    "UpdateLinkInputRequestTypeDef",
    {
        "Identifier": str,
        "ResourceTypes": Sequence[ResourceTypeType],
    },
)

CreateLinkOutputTypeDef = TypedDict(
    "CreateLinkOutputTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Label": str,
        "LabelTemplate": str,
        "ResourceTypes": List[str],
        "SinkArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSinkOutputTypeDef = TypedDict(
    "CreateSinkOutputTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLinkOutputTypeDef = TypedDict(
    "GetLinkOutputTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Label": str,
        "LabelTemplate": str,
        "ResourceTypes": List[str],
        "SinkArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSinkOutputTypeDef = TypedDict(
    "GetSinkOutputTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Name": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSinkPolicyOutputTypeDef = TypedDict(
    "GetSinkPolicyOutputTypeDef",
    {
        "SinkArn": str,
        "SinkId": str,
        "Policy": str,
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

PutSinkPolicyOutputTypeDef = TypedDict(
    "PutSinkPolicyOutputTypeDef",
    {
        "SinkArn": str,
        "SinkId": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateLinkOutputTypeDef = TypedDict(
    "UpdateLinkOutputTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Label": str,
        "LabelTemplate": str,
        "ResourceTypes": List[str],
        "SinkArn": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListAttachedLinksInputListAttachedLinksPaginateTypeDef = TypedDict(
    "_RequiredListAttachedLinksInputListAttachedLinksPaginateTypeDef",
    {
        "SinkIdentifier": str,
    },
)
_OptionalListAttachedLinksInputListAttachedLinksPaginateTypeDef = TypedDict(
    "_OptionalListAttachedLinksInputListAttachedLinksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

class ListAttachedLinksInputListAttachedLinksPaginateTypeDef(
    _RequiredListAttachedLinksInputListAttachedLinksPaginateTypeDef,
    _OptionalListAttachedLinksInputListAttachedLinksPaginateTypeDef,
):
    pass

ListLinksInputListLinksPaginateTypeDef = TypedDict(
    "ListLinksInputListLinksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSinksInputListSinksPaginateTypeDef = TypedDict(
    "ListSinksInputListSinksPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListAttachedLinksOutputTypeDef = TypedDict(
    "ListAttachedLinksOutputTypeDef",
    {
        "Items": List[ListAttachedLinksItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLinksOutputTypeDef = TypedDict(
    "ListLinksOutputTypeDef",
    {
        "Items": List[ListLinksItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSinksOutputTypeDef = TypedDict(
    "ListSinksOutputTypeDef",
    {
        "Items": List[ListSinksItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
