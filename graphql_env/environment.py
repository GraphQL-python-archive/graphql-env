from .backend import GraphQLBackend, get_default_backend, GraphQLDocument
from ._compat import string_types
from .params import GraphQLParams


class GraphQLEnvironment(object):
    def __init__(self, schema, backend=None, store=None):
        self.schema = schema
        if backend is None:
            backend = get_default_backend()
        else:
            assert isinstance(
                backend, GraphQLBackend
            ), "backend must be instance of GraphQLBackend"
        self.backend = backend
        self.store = store

    def document_from_string(self, source):
        """Load a document from a string. This parses the source given and
        returns a :class:`GraphQLDocument` object.
        """
        return self.backend.document_from_string(self.schema, source)

    def load_document(self, document_id):
        """
            Load a document given a document_id
        """
        if not self.store:
            raise Exception("The GraphQL Environment doesn't have set any store.")

        document = self.store[document_id]

        if isinstance(document, string_types):
            return self.document_from_string(document)
        elif isinstance(document, GraphQLDocument):
            return document

        raise Exception(
            "Document returned from the store must be an string or a GraphQLDocument. Received {}.".format(
                repr(document)
            )
        )

    def get_document_from_params(self, params):
        if params.document_id:
            return self.load_document(params.document_id)
        return self.document_from_string(params.query)

    def __call__(
        self,
        graphql_params,
        root=None,
        context=None,
        middleware=None,
        allowed_operations=None,
    ):
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
            allowed_operations=allowed_operations,
        )
