from .base import GraphQLBackend


class GraphQLDeciderBackend(GraphQLBackend):
    def __init__(self, backends=None, cache=None, use_cache=None):
        if not backends:
            raise Exception("Need to provide backends to decide into.")
        if not isinstance(backends, (list, tuple)):
            raise Exception("Provided backends need to be a list or tuple.")
        if cache is None and use_cache is None:
            use_cache = False
        self.backends = backends
        super(GraphQLDeciderBackend, self).__init__(
            cache=cache, use_cache=use_cache)

    def document_from_cache_or_string(self, schema, request_string, key):
        cached_document = self.document_from_cache(key)
        if cached_document:
            return cached_document

        for backend in self.backends:
            try:
                document = backend.document_from_cache_or_string(
                    schema, request_string, key)
                # If no error has been raised, we are ok :)
                self.document_to_cache(key, document)
                return document
            except Exception:
                continue

        raise Exception(
            "GraphQLDeciderBackend was not able to retrieve a document. Backends tried: {}".
            format(repr(self.backends)))

    # def document_from_string(self, schema, request_string):
    #     for backend in self.backends:
    #         try:
    #             return backend.document_from_string(schema, request_string)
    #         except
    #             continue
    #     raise Exception("GraphQLDeciderBackend was not able to retrieve a document. Backends tried: {}".format(repr(self.backends)))
