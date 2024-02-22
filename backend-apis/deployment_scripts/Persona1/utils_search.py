# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Utility module for Vertex AI Search API
"""

import base64

from typing import List
from google.cloud import discoveryengine


def complete_query(
    search_query: str,
    project_id: str,
    location: str,
    search_engine_id: str,
    complete_client: discoveryengine.CompletionServiceClient
) -> List[str]:
    """Completes a search query with suggestions.

    Args:
        search_query (str): 
            The search query to complete.
        project_id (str): 
            The ID of the project that owns the search engine.
        location (str): 
            The location of the search engine.
        search_engine_id (str): 
            The ID of the search engine.
        complete_client (discoveryengine.CompletionServiceClient): 
            The completion client.

    Returns:
        A list of suggested queries.
    """
    suggestions_list = []
    
    if len(search_query) > 2:
        # The full resource name of the search engine data store
        # e.g. projects/*/locations/global/collections/default_collection/dataStores/default_data_store
        data_store_path = complete_client.data_store_path(
            project=project_id,
            location=location,
            data_store=search_engine_id
        )
        # Initialize request argument(s)
        request = discoveryengine.CompleteQueryRequest(
            data_store=data_store_path,
            query=search_query,
        )

        # Make the request
        response = complete_client.complete_query(request=request)

        for query_suggestion in response.query_suggestions:
            suggestions_list.append(query_suggestion.suggestion)

    # Handle the response
    return suggestions_list


def search_website_text(
    search_client: discoveryengine.SearchServiceClient,
    search_query: str,
    project_id: str,
    datastore_location: str,
    datastore_id: str,
    serving_config_id: str = "default_config",
    return_snippet: bool = True,
    summary_result_count: int = 2,
    include_citations: bool = True,
    max_extractive_answer_count: int = 1,
    max_extractive_segment_count: int = 1,
    return_extractive_segment_score: bool = True,
    num_previous_segments: int = 1,
    num_next_segments: int = 1
) -> List[discoveryengine.SearchResponse.SearchResult]:
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id:
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=datastore_location,
        data_store=datastore_id,
        serving_config=serving_config_id)

    snippet_spec = discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
        return_snippet=return_snippet)
    summary_spec = discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
        summary_result_count=summary_result_count, 
        include_citations=include_citations)
    extractive_content_spec = discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
        max_extractive_answer_count=max_extractive_answer_count,
        max_extractive_segment_count=max_extractive_segment_count,
        return_extractive_segment_score=return_extractive_segment_score,
        num_previous_segments=num_previous_segments,
        num_next_segments=num_next_segments
    )

    content_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=snippet_spec,
        summary_spec=summary_spec,
        extractive_content_spec=extractive_content_spec
    )

    request = discoveryengine.SearchRequest(
        content_search_spec=content_spec,
        serving_config=serving_config,
        query=search_query,

    )

    return search_client.search(request)


def search_website_image(
    search_client: discoveryengine.SearchServiceClient,
    project_id: str,
    datastore_location: str,
    datastore_id: str,
    image_bytes: str,
    serving_config_id: str = "default_config"
) -> List[discoveryengine.SearchResponse.SearchResult]:
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id:
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=datastore_location,
        data_store=datastore_id,
        serving_config=serving_config_id)

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        image_query=discoveryengine.SearchRequest.ImageQuery(
            image_bytes=base64.b64encode(image_bytes)
        )
    )

    return search_client.search(request)


def search_structure_text(
    search_client: discoveryengine.SearchServiceClient,
    search_query: str,
    project_id: str,
    datastore_location: str,
    datastore_id: str,
    serving_config_id: str = "default_config"
) -> List[discoveryengine.SearchResponse.SearchResult]:
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id:
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=datastore_location,
        data_store=datastore_id,
        serving_config=serving_config_id)

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query)

    return search_client.search(request)


def search_unstructured_text(
    search_client: discoveryengine.SearchServiceClient,
    search_query: str,
    project_id: str,
    datastore_location: str,
    datastore_id: str,
    conversation_id: str,
    serving_config_id: str = "default_config"
) -> List[discoveryengine.SearchResponse.SearchResult]:
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id:
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=datastore_location,
        data_store=datastore_id,
        serving_config=serving_config_id)

    request = discoveryengine.ConverseConversationRequest(
        name=conversation_id,
        query=discoveryengine.TextInput(input=search_query),
        serving_config=serving_config
    )

    return search_client.search(request)


def search_for_salesforce(
    search_client: discoveryengine.SearchServiceClient,
    search_query: str,
    project_id: str,
    datastore_location: str,
    datastore_id: str,
    serving_config_id: str = "default_config",
    return_snippet: bool = True,
    summary_result_count: int = 5,
    include_citations: bool = True
) -> List[discoveryengine.SearchResponse.SearchResult]:
    """Searches for documents that match the given query.

    Args:
        search_query: 
            The search query.
        project_id: 
            The ID of the project that owns the search engine.
        location: 
            The location of the search engine.
        search_engine_id:
            The ID of the search engine.
        serving_config_id: 
            The ID of the serving config.
        search_client: 
            A `discoveryengine.SearchServiceClient` instance.

    Returns:
        A list of `discoveryengine.SearchResponse.SearchResult` objects.
    """
    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = search_client.serving_config_path(
        project=project_id,
        location=datastore_location,
        data_store=datastore_id,
        serving_config=serving_config_id)

    snippet_spec = discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
        return_snippet=return_snippet)
    summary_spec = discoveryengine.SearchRequest.ContentSearchSpec.SummarySpec(
        summary_result_count=summary_result_count, 
        include_citations=include_citations)

    content_spec = discoveryengine.SearchRequest.ContentSearchSpec(
        snippet_spec=snippet_spec,
        summary_spec=summary_spec)

    request = discoveryengine.SearchRequest(
        content_search_spec=content_spec,
        serving_config=serving_config,
        query=search_query)

    return search_client.search(request)
