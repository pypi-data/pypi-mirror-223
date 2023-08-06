"""
Main interface for entityresolution service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_entityresolution import (
        Client,
        EntityResolutionClient,
        ListMatchingJobsPaginator,
        ListMatchingWorkflowsPaginator,
        ListSchemaMappingsPaginator,
    )

    session = get_session()
    async with session.create_client("entityresolution") as client:
        client: EntityResolutionClient
        ...


    list_matching_jobs_paginator: ListMatchingJobsPaginator = client.get_paginator("list_matching_jobs")
    list_matching_workflows_paginator: ListMatchingWorkflowsPaginator = client.get_paginator("list_matching_workflows")
    list_schema_mappings_paginator: ListSchemaMappingsPaginator = client.get_paginator("list_schema_mappings")
    ```
"""
from .client import EntityResolutionClient
from .paginator import (
    ListMatchingJobsPaginator,
    ListMatchingWorkflowsPaginator,
    ListSchemaMappingsPaginator,
)

Client = EntityResolutionClient

__all__ = (
    "Client",
    "EntityResolutionClient",
    "ListMatchingJobsPaginator",
    "ListMatchingWorkflowsPaginator",
    "ListSchemaMappingsPaginator",
)
