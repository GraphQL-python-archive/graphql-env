from .backend import GraphQLBackend, get_default_backend, GraphQLDocument
from .utils import get_unique_query_id, get_unique_schema_id
from ._compat import string_types
from .params import GraphQLParams


class GraphQLEnvironment(object):
    def __init__(self, schema, middleware=None, backend=None, store=None):
        self.schema = schema
        self.middleware = middleware
        if backend is None:
            backend = get_default_backend()
        else:
            assert isinstance(
                backend,
                GraphQLBackend), "backend must be instance of GraphQLBackend"
        self.backend = backend
        self.store = store
        self.schema_key = get_unique_schema_id(schema)

    def document_from_string(self, source):
        """Load a query from a string. This parses the source given and
        returns a :class:`GraphQLQuery` object.
        """
        key = (self.schema_key, get_unique_query_id(source))
        query = self.backend.document_from_cache_or_string(
            self.schema, source, key=key)
        return query

    def load_document(self, query_id):
        """
            Load a document given a query_id
        """
        if not self.store:
            raise Exception(
                "The GraphQL Environment doesn't have set any store.")

        document = self.store[query_id]

        if isinstance(document, string_types):
            return self.document_from_string(document)
        elif isinstance(document, GraphQLDocument):
            return document

        raise Exception(
            "Document returned from the store must be an string or a GraphQLDocument. Received {}.".
            format(repr(document)))

    def get_document_from_params(self, params):
        if params.query_id:
            return self.load_document(params.query_id)
        return self.document_from_string(params.query)

    def __call__(self,
                 graphql_params,
                 root=None,
                 context=None,
                 middleware=None,
                 allowed_operations=None):
        assert isinstance(
            graphql_params, GraphQLParams
        ), "GraphQL params must be an instance of GraphQLParams."

        document = self.get_document_from_params(graphql_params)
        return document.execute(
            root=root,
            context=context,
            middleware=middleware,
            operation_name=graphql_params.operation_name,
            variables=graphql_params.variables,
            allowed_operations=allowed_operations)
