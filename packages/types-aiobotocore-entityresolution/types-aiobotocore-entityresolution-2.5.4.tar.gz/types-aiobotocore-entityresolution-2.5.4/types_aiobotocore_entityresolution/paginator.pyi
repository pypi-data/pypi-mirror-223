"""
Type annotations for entityresolution service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_entityresolution.client import EntityResolutionClient
    from types_aiobotocore_entityresolution.paginator import (
        ListMatchingJobsPaginator,
        ListMatchingWorkflowsPaginator,
        ListSchemaMappingsPaginator,
    )

    session = get_session()
    with session.create_client("entityresolution") as client:
        client: EntityResolutionClient

        list_matching_jobs_paginator: ListMatchingJobsPaginator = client.get_paginator("list_matching_jobs")
        list_matching_workflows_paginator: ListMatchingWorkflowsPaginator = client.get_paginator("list_matching_workflows")
        list_schema_mappings_paginator: ListSchemaMappingsPaginator = client.get_paginator("list_schema_mappings")
    ```
"""
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListSchemaMappingsOutputTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListMatchingJobsPaginator",
    "ListMatchingWorkflowsPaginator",
    "ListSchemaMappingsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListMatchingJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListMatchingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
    """

    def paginate(
        self, *, workflowName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListMatchingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListMatchingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
        """

class ListMatchingWorkflowsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListMatchingWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListMatchingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListMatchingWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
        """

class ListSchemaMappingsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListSchemaMappings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListSchemaMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution.html#EntityResolution.Paginator.ListSchemaMappings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
        """
