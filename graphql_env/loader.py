from .backend import GraphQLBackend, get_default_backend, GraphQLDocument
from ._compat import string_types
from .params import GraphQLParams


class GraphQLLoader(object):
    """GraphQLLoader is a GraphQL document loader.
    It returns a GraphQL document given params (query or document id)
    """

    def __init__(self, backend=None, store=None):
        if backend is None:
            backend = get_default_backend()
        else:
            assert isinstance(
                backend, GraphQLBackend
            ), "backend must be instance of GraphQLBackend"
        self.backend = backend
        self.store = store

    def document_from_string(self, schema, source):
        """Load a document from a string. This parses the source given and
        returns a :class:`GraphQLDocument` object.
        """
        return self.backend.document_from_string(schema, source)

    def load_document(self, schema, document_id):
        """
            Load a document given a document_id
        """
        if not self.store:
            raise Exception("GraphQLLoader doesn't have set any store.")

        document = self.store.load(schema, document_id)

        if isinstance(document, string_types):
            return self.document_from_string(schema, document)
        elif isinstance(document, GraphQLDocument):
            return document

        raise Exception(
            "Document returned from the store must be an string or a GraphQLDocument. Received {}.".format(
                repr(document)
            )
        )

    def get_document_from_params(self, schema, params):
        if params.document_id:
            return self.load_document(schema, params.document_id)
        return self.document_from_string(schema, params.query)
