from .utils import get_unique_schema_id, get_unique_query_id

from .backend import GraphQLBackend, get_default_backend


class GraphQLEnvironment(object):
    def __init__(self, schema, middleware=None, backend=None):
        self.schema = schema
        self.schema_id = get_unique_schema_id(schema)
        self.middleware = middleware
        if backend is None:
            backend = get_default_backend()
        else:
            assert isinstance(
                backend,
                GraphQLBackend), "backend must be instance of GraphQLBackend"
        self.backend = backend

    def get_key(self, source):
        return '{}_{}'.format(self.schema_id, get_unique_query_id(source))

    def document_from_string(self, source):
        """Load a query from a string.  This parses the source given and
        returns a :class:`GraphQLQuery` object.
        """
        key = self.get_key(source)
        query = self.backend.get_document(self, source, key=key)
        return query
