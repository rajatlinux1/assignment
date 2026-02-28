import logging

from django.conf import settings
from django.db import connection
from elasticsearch import Elasticsearch

logger = logging.getLogger("Project")

# Natively boots up standard or mocked ES clients based on connection URL
es_client = Elasticsearch([settings.ELASTICSEARCH_URL])


def get_tenant_index_name(model_name):
    """
    Returns the absolute localized index name tightly coupling the request's
    schema name and the model being indexed.
    Example: 'test_item', 'public_globalcategory'
    """
    return f"{connection.schema_name}_{model_name.lower()}"


def index_document(model_name, document_id, data):
    """
    Pushes or updates a document into the tenant's isolated index.
    """
    index_name = get_tenant_index_name(model_name)
    try:
        es_client.index(index=index_name, id=document_id, document=data)
        logger.info(
            f"Indexed document {document_id} into ES index '{index_name}' successfully."
        )
    except Exception as e:
        # In a robust production environment we would log this and use Celery to retry
        logger.error(f"Failed to index document {document_id} into {index_name}: {e}")


def remove_document(model_name, document_id):
    """
    Removes a document from the tenant's isolated index.
    """
    index_name = get_tenant_index_name(model_name)
    try:
        es_client.delete(index=index_name, id=document_id)
        logger.info(f"Deleted document {document_id} from ES index '{index_name}'.")
    except Exception as e:
        logger.warning(
            f"Failed to delete document {document_id} from {index_name}: {e}"
        )


def search_tenant_documents(model_name, query_string):
    """
    Executes a search query Strictly against the tenant's isolated index.
    """
    index_name = get_tenant_index_name(model_name)
    body = {"query": {"multi_match": {"query": query_string, "fields": ["*"]}}}

    try:
        # We set ignore_unavailable=True so if the tenant has no index yet, it responds empty
        # instead of throwing an index_not_found_exception
        response = es_client.search(
            index=index_name, body=body, ignore_unavailable=True
        )
        hits = response.get("hits", {}).get("hits", [])
        logger.info(
            f"Search executed against '{index_name}' returned {len(hits)} hits."
        )
        return [hit["_source"] for hit in hits]
    except Exception as e:
        logger.error(f"Failed to search index {index_name}: {e}")
        return []
