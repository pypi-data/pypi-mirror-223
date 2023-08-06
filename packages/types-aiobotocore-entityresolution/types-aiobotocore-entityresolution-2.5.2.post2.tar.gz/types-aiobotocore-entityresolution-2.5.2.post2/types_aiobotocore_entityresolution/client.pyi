"""
Type annotations for entityresolution service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_entityresolution.client import EntityResolutionClient

    session = get_session()
    async with session.create_client("entityresolution") as client:
        client: EntityResolutionClient
    ```
"""
import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListMatchingJobsPaginator,
    ListMatchingWorkflowsPaginator,
    ListSchemaMappingsPaginator,
)
from .type_defs import (
    CreateMatchingWorkflowOutputTypeDef,
    CreateSchemaMappingOutputTypeDef,
    DeleteMatchingWorkflowOutputTypeDef,
    DeleteSchemaMappingOutputTypeDef,
    GetMatchIdOutputTypeDef,
    GetMatchingJobOutputTypeDef,
    GetMatchingWorkflowOutputTypeDef,
    GetSchemaMappingOutputTypeDef,
    IncrementalRunConfigTypeDef,
    InputSourceTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListSchemaMappingsOutputTypeDef,
    ListTagsForResourceOutputTypeDef,
    OutputSourceTypeDef,
    ResolutionTechniquesTypeDef,
    SchemaInputAttributeTypeDef,
    StartMatchingJobOutputTypeDef,
    UpdateMatchingWorkflowOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("EntityResolutionClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ExceedsLimitException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EntityResolutionClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EntityResolutionClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#exceptions)
        """
    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#can_paginate)
        """
    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#close)
        """
    async def create_matching_workflow(
        self,
        *,
        inputSourceConfig: Sequence[InputSourceTypeDef],
        outputSourceConfig: Sequence[OutputSourceTypeDef],
        resolutionTechniques: ResolutionTechniquesTypeDef,
        roleArn: str,
        workflowName: str,
        description: str = ...,
        incrementalRunConfig: IncrementalRunConfigTypeDef = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateMatchingWorkflowOutputTypeDef:
        """
        Creates a `MatchingWorkflow` object which stores the configuration of the data
        processing job to be run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_matching_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#create_matching_workflow)
        """
    async def create_schema_mapping(
        self,
        *,
        schemaName: str,
        description: str = ...,
        mappedInputFields: Sequence[SchemaInputAttributeTypeDef] = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateSchemaMappingOutputTypeDef:
        """
        Creates a schema mapping, which defines the schema of the input customer records
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.create_schema_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#create_schema_mapping)
        """
    async def delete_matching_workflow(
        self, *, workflowName: str
    ) -> DeleteMatchingWorkflowOutputTypeDef:
        """
        Deletes the `MatchingWorkflow` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_matching_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#delete_matching_workflow)
        """
    async def delete_schema_mapping(self, *, schemaName: str) -> DeleteSchemaMappingOutputTypeDef:
        """
        Deletes the `SchemaMapping` with a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.delete_schema_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#delete_schema_mapping)
        """
    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#generate_presigned_url)
        """
    async def get_match_id(
        self, *, record: Mapping[str, str], workflowName: str
    ) -> GetMatchIdOutputTypeDef:
        """
        Returns the corresponding Match ID of a customer record if the record has been
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_match_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_match_id)
        """
    async def get_matching_job(
        self, *, jobId: str, workflowName: str
    ) -> GetMatchingJobOutputTypeDef:
        """
        Gets the status, metrics, and errors (if there are any) that are associated with
        a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_matching_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_matching_job)
        """
    async def get_matching_workflow(self, *, workflowName: str) -> GetMatchingWorkflowOutputTypeDef:
        """
        Returns the `MatchingWorkflow` with a given name, if it exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_matching_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_matching_workflow)
        """
    async def get_schema_mapping(self, *, schemaName: str) -> GetSchemaMappingOutputTypeDef:
        """
        Returns the SchemaMapping of a given name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_schema_mapping)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_schema_mapping)
        """
    async def list_matching_jobs(
        self, *, workflowName: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListMatchingJobsOutputTypeDef:
        """
        Lists all jobs for a given workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_matching_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#list_matching_jobs)
        """
    async def list_matching_workflows(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListMatchingWorkflowsOutputTypeDef:
        """
        Returns a list of all the `MatchingWorkflows` that have been created for an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_matching_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#list_matching_workflows)
        """
    async def list_schema_mappings(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSchemaMappingsOutputTypeDef:
        """
        Returns a list of all the `SchemaMappings` that have been created for an AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_schema_mappings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#list_schema_mappings)
        """
    async def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceOutputTypeDef:
        """
        Displays the tags associated with an AWS Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#list_tags_for_resource)
        """
    async def start_matching_job(self, *, workflowName: str) -> StartMatchingJobOutputTypeDef:
        """
        Starts the `MatchingJob` of a workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.start_matching_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#start_matching_job)
        """
    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified AWS Entity
        Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#tag_resource)
        """
    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified AWS Entity Resolution resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#untag_resource)
        """
    async def update_matching_workflow(
        self,
        *,
        inputSourceConfig: Sequence[InputSourceTypeDef],
        outputSourceConfig: Sequence[OutputSourceTypeDef],
        resolutionTechniques: ResolutionTechniquesTypeDef,
        roleArn: str,
        workflowName: str,
        description: str = ...,
        incrementalRunConfig: IncrementalRunConfigTypeDef = ...
    ) -> UpdateMatchingWorkflowOutputTypeDef:
        """
        Updates an existing `MatchingWorkflow`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.update_matching_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#update_matching_workflow)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_matching_jobs"]
    ) -> ListMatchingJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_matching_workflows"]
    ) -> ListMatchingWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_paginator)
        """
    @overload
    def get_paginator(
        self, operation_name: Literal["list_schema_mappings"]
    ) -> ListSchemaMappingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/#get_paginator)
        """
    async def __aenter__(self) -> "EntityResolutionClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/)
        """
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/client/)
        """
