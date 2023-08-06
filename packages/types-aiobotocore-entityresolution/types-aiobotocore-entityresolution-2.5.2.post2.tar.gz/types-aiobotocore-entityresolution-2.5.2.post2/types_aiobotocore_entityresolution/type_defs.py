"""
Type annotations for entityresolution service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/type_defs/)

Usage::

    ```python
    from types_aiobotocore_entityresolution.type_defs import IncrementalRunConfigTypeDef

    data: IncrementalRunConfigTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AttributeMatchingModelType,
    JobStatusType,
    ResolutionTypeType,
    SchemaAttributeTypeType,
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
    "IncrementalRunConfigTypeDef",
    "InputSourceTypeDef",
    "ResponseMetadataTypeDef",
    "SchemaInputAttributeTypeDef",
    "DeleteMatchingWorkflowInputRequestTypeDef",
    "DeleteSchemaMappingInputRequestTypeDef",
    "ErrorDetailsTypeDef",
    "GetMatchIdInputRequestTypeDef",
    "GetMatchingJobInputRequestTypeDef",
    "JobMetricsTypeDef",
    "GetMatchingWorkflowInputRequestTypeDef",
    "GetSchemaMappingInputRequestTypeDef",
    "JobSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ListMatchingJobsInputRequestTypeDef",
    "ListMatchingWorkflowsInputRequestTypeDef",
    "MatchingWorkflowSummaryTypeDef",
    "ListSchemaMappingsInputRequestTypeDef",
    "SchemaMappingSummaryTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "OutputAttributeTypeDef",
    "RuleTypeDef",
    "StartMatchingJobInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "DeleteMatchingWorkflowOutputTypeDef",
    "DeleteSchemaMappingOutputTypeDef",
    "GetMatchIdOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "StartMatchingJobOutputTypeDef",
    "CreateSchemaMappingInputRequestTypeDef",
    "CreateSchemaMappingOutputTypeDef",
    "GetSchemaMappingOutputTypeDef",
    "GetMatchingJobOutputTypeDef",
    "ListMatchingJobsOutputTypeDef",
    "ListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    "ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef",
    "ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef",
    "ListMatchingWorkflowsOutputTypeDef",
    "ListSchemaMappingsOutputTypeDef",
    "OutputSourceTypeDef",
    "RuleBasedPropertiesTypeDef",
    "ResolutionTechniquesTypeDef",
    "CreateMatchingWorkflowInputRequestTypeDef",
    "CreateMatchingWorkflowOutputTypeDef",
    "GetMatchingWorkflowOutputTypeDef",
    "UpdateMatchingWorkflowInputRequestTypeDef",
    "UpdateMatchingWorkflowOutputTypeDef",
)

IncrementalRunConfigTypeDef = TypedDict(
    "IncrementalRunConfigTypeDef",
    {
        "incrementalRunType": Literal["IMMEDIATE"],
    },
    total=False,
)

_RequiredInputSourceTypeDef = TypedDict(
    "_RequiredInputSourceTypeDef",
    {
        "inputSourceARN": str,
        "schemaName": str,
    },
)
_OptionalInputSourceTypeDef = TypedDict(
    "_OptionalInputSourceTypeDef",
    {
        "applyNormalization": bool,
    },
    total=False,
)


class InputSourceTypeDef(_RequiredInputSourceTypeDef, _OptionalInputSourceTypeDef):
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

_RequiredSchemaInputAttributeTypeDef = TypedDict(
    "_RequiredSchemaInputAttributeTypeDef",
    {
        "fieldName": str,
        "type": SchemaAttributeTypeType,
    },
)
_OptionalSchemaInputAttributeTypeDef = TypedDict(
    "_OptionalSchemaInputAttributeTypeDef",
    {
        "groupName": str,
        "matchKey": str,
    },
    total=False,
)


class SchemaInputAttributeTypeDef(
    _RequiredSchemaInputAttributeTypeDef, _OptionalSchemaInputAttributeTypeDef
):
    pass


DeleteMatchingWorkflowInputRequestTypeDef = TypedDict(
    "DeleteMatchingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)

DeleteSchemaMappingInputRequestTypeDef = TypedDict(
    "DeleteSchemaMappingInputRequestTypeDef",
    {
        "schemaName": str,
    },
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "errorMessage": str,
    },
    total=False,
)

GetMatchIdInputRequestTypeDef = TypedDict(
    "GetMatchIdInputRequestTypeDef",
    {
        "record": Mapping[str, str],
        "workflowName": str,
    },
)

GetMatchingJobInputRequestTypeDef = TypedDict(
    "GetMatchingJobInputRequestTypeDef",
    {
        "jobId": str,
        "workflowName": str,
    },
)

JobMetricsTypeDef = TypedDict(
    "JobMetricsTypeDef",
    {
        "inputRecords": int,
        "matchIDs": int,
        "recordsNotProcessed": int,
        "totalRecordsProcessed": int,
    },
    total=False,
)

GetMatchingWorkflowInputRequestTypeDef = TypedDict(
    "GetMatchingWorkflowInputRequestTypeDef",
    {
        "workflowName": str,
    },
)

GetSchemaMappingInputRequestTypeDef = TypedDict(
    "GetSchemaMappingInputRequestTypeDef",
    {
        "schemaName": str,
    },
)

_RequiredJobSummaryTypeDef = TypedDict(
    "_RequiredJobSummaryTypeDef",
    {
        "jobId": str,
        "startTime": datetime,
        "status": JobStatusType,
    },
)
_OptionalJobSummaryTypeDef = TypedDict(
    "_OptionalJobSummaryTypeDef",
    {
        "endTime": datetime,
    },
    total=False,
)


class JobSummaryTypeDef(_RequiredJobSummaryTypeDef, _OptionalJobSummaryTypeDef):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredListMatchingJobsInputRequestTypeDef = TypedDict(
    "_RequiredListMatchingJobsInputRequestTypeDef",
    {
        "workflowName": str,
    },
)
_OptionalListMatchingJobsInputRequestTypeDef = TypedDict(
    "_OptionalListMatchingJobsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListMatchingJobsInputRequestTypeDef(
    _RequiredListMatchingJobsInputRequestTypeDef, _OptionalListMatchingJobsInputRequestTypeDef
):
    pass


ListMatchingWorkflowsInputRequestTypeDef = TypedDict(
    "ListMatchingWorkflowsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

MatchingWorkflowSummaryTypeDef = TypedDict(
    "MatchingWorkflowSummaryTypeDef",
    {
        "createdAt": datetime,
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
    },
)

ListSchemaMappingsInputRequestTypeDef = TypedDict(
    "ListSchemaMappingsInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

SchemaMappingSummaryTypeDef = TypedDict(
    "SchemaMappingSummaryTypeDef",
    {
        "createdAt": datetime,
        "schemaArn": str,
        "schemaName": str,
        "updatedAt": datetime,
    },
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "resourceArn": str,
    },
)

_RequiredOutputAttributeTypeDef = TypedDict(
    "_RequiredOutputAttributeTypeDef",
    {
        "name": str,
    },
)
_OptionalOutputAttributeTypeDef = TypedDict(
    "_OptionalOutputAttributeTypeDef",
    {
        "hashed": bool,
    },
    total=False,
)


class OutputAttributeTypeDef(_RequiredOutputAttributeTypeDef, _OptionalOutputAttributeTypeDef):
    pass


RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "matchingKeys": Sequence[str],
        "ruleName": str,
    },
)

StartMatchingJobInputRequestTypeDef = TypedDict(
    "StartMatchingJobInputRequestTypeDef",
    {
        "workflowName": str,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

DeleteMatchingWorkflowOutputTypeDef = TypedDict(
    "DeleteMatchingWorkflowOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSchemaMappingOutputTypeDef = TypedDict(
    "DeleteSchemaMappingOutputTypeDef",
    {
        "message": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMatchIdOutputTypeDef = TypedDict(
    "GetMatchIdOutputTypeDef",
    {
        "matchId": str,
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

StartMatchingJobOutputTypeDef = TypedDict(
    "StartMatchingJobOutputTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateSchemaMappingInputRequestTypeDef = TypedDict(
    "_RequiredCreateSchemaMappingInputRequestTypeDef",
    {
        "schemaName": str,
    },
)
_OptionalCreateSchemaMappingInputRequestTypeDef = TypedDict(
    "_OptionalCreateSchemaMappingInputRequestTypeDef",
    {
        "description": str,
        "mappedInputFields": Sequence[SchemaInputAttributeTypeDef],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateSchemaMappingInputRequestTypeDef(
    _RequiredCreateSchemaMappingInputRequestTypeDef, _OptionalCreateSchemaMappingInputRequestTypeDef
):
    pass


CreateSchemaMappingOutputTypeDef = TypedDict(
    "CreateSchemaMappingOutputTypeDef",
    {
        "description": str,
        "mappedInputFields": List[SchemaInputAttributeTypeDef],
        "schemaArn": str,
        "schemaName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSchemaMappingOutputTypeDef = TypedDict(
    "GetSchemaMappingOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "mappedInputFields": List[SchemaInputAttributeTypeDef],
        "schemaArn": str,
        "schemaName": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMatchingJobOutputTypeDef = TypedDict(
    "GetMatchingJobOutputTypeDef",
    {
        "endTime": datetime,
        "errorDetails": ErrorDetailsTypeDef,
        "jobId": str,
        "metrics": JobMetricsTypeDef,
        "startTime": datetime,
        "status": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMatchingJobsOutputTypeDef = TypedDict(
    "ListMatchingJobsOutputTypeDef",
    {
        "jobs": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredListMatchingJobsInputListMatchingJobsPaginateTypeDef = TypedDict(
    "_RequiredListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    {
        "workflowName": str,
    },
)
_OptionalListMatchingJobsInputListMatchingJobsPaginateTypeDef = TypedDict(
    "_OptionalListMatchingJobsInputListMatchingJobsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListMatchingJobsInputListMatchingJobsPaginateTypeDef(
    _RequiredListMatchingJobsInputListMatchingJobsPaginateTypeDef,
    _OptionalListMatchingJobsInputListMatchingJobsPaginateTypeDef,
):
    pass


ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef = TypedDict(
    "ListMatchingWorkflowsInputListMatchingWorkflowsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef = TypedDict(
    "ListSchemaMappingsInputListSchemaMappingsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListMatchingWorkflowsOutputTypeDef = TypedDict(
    "ListMatchingWorkflowsOutputTypeDef",
    {
        "nextToken": str,
        "workflowSummaries": List[MatchingWorkflowSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSchemaMappingsOutputTypeDef = TypedDict(
    "ListSchemaMappingsOutputTypeDef",
    {
        "nextToken": str,
        "schemaList": List[SchemaMappingSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredOutputSourceTypeDef = TypedDict(
    "_RequiredOutputSourceTypeDef",
    {
        "output": Sequence[OutputAttributeTypeDef],
        "outputS3Path": str,
    },
)
_OptionalOutputSourceTypeDef = TypedDict(
    "_OptionalOutputSourceTypeDef",
    {
        "KMSArn": str,
        "applyNormalization": bool,
    },
    total=False,
)


class OutputSourceTypeDef(_RequiredOutputSourceTypeDef, _OptionalOutputSourceTypeDef):
    pass


RuleBasedPropertiesTypeDef = TypedDict(
    "RuleBasedPropertiesTypeDef",
    {
        "attributeMatchingModel": AttributeMatchingModelType,
        "rules": Sequence[RuleTypeDef],
    },
)

ResolutionTechniquesTypeDef = TypedDict(
    "ResolutionTechniquesTypeDef",
    {
        "resolutionType": ResolutionTypeType,
        "ruleBasedProperties": RuleBasedPropertiesTypeDef,
    },
    total=False,
)

_RequiredCreateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "_RequiredCreateMatchingWorkflowInputRequestTypeDef",
    {
        "inputSourceConfig": Sequence[InputSourceTypeDef],
        "outputSourceConfig": Sequence[OutputSourceTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowName": str,
    },
)
_OptionalCreateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "_OptionalCreateMatchingWorkflowInputRequestTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateMatchingWorkflowInputRequestTypeDef(
    _RequiredCreateMatchingWorkflowInputRequestTypeDef,
    _OptionalCreateMatchingWorkflowInputRequestTypeDef,
):
    pass


CreateMatchingWorkflowOutputTypeDef = TypedDict(
    "CreateMatchingWorkflowOutputTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMatchingWorkflowOutputTypeDef = TypedDict(
    "GetMatchingWorkflowOutputTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "tags": Dict[str, str],
        "updatedAt": datetime,
        "workflowArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredUpdateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "_RequiredUpdateMatchingWorkflowInputRequestTypeDef",
    {
        "inputSourceConfig": Sequence[InputSourceTypeDef],
        "outputSourceConfig": Sequence[OutputSourceTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowName": str,
    },
)
_OptionalUpdateMatchingWorkflowInputRequestTypeDef = TypedDict(
    "_OptionalUpdateMatchingWorkflowInputRequestTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
    },
    total=False,
)


class UpdateMatchingWorkflowInputRequestTypeDef(
    _RequiredUpdateMatchingWorkflowInputRequestTypeDef,
    _OptionalUpdateMatchingWorkflowInputRequestTypeDef,
):
    pass


UpdateMatchingWorkflowOutputTypeDef = TypedDict(
    "UpdateMatchingWorkflowOutputTypeDef",
    {
        "description": str,
        "incrementalRunConfig": IncrementalRunConfigTypeDef,
        "inputSourceConfig": List[InputSourceTypeDef],
        "outputSourceConfig": List[OutputSourceTypeDef],
        "resolutionTechniques": ResolutionTechniquesTypeDef,
        "roleArn": str,
        "workflowName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
