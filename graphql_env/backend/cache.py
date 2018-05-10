from ..utils import get_unique_document_id, get_unique_schema_id
from .base import GraphQLBackend


class GraphQLCachedBackend(GraphQLBackend):
    def __init__(self, backend, cache_map=None):
        assert isinstance(backend, GraphQLBackend),(
            "Provided backend must be an instance of GraphQLBackend"
        )
        if cache_map is None:
            cache_map = {}
        self.backend = backend
        self.cache_map = cache_map

    def get_key_for_schema_and_document_string(self, schema, request_string):
        '''This method returns a unique key given a schema and a request_string'''
        schema_id = get_unique_schema_id(schema)
        document_id = get_unique_document_id(request_string)
        return (schema_id, document_id)

    def document_from_string(self, schema, request_string):
        '''This method returns a GraphQLQuery (from cache if present)'''
        key = self.get_key_for_schema_and_document_string(schema, request_string)
        if key not in self.cache_map:
            self.cache_map[key] = self.backend.document_from_string(
                schema, request_string)

        return self.cache_map[key]
