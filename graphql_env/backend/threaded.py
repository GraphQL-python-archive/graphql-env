from .base import GraphQLBackend
from threading import Thread


class GraphQLThreadedLazyBackend(GraphQLBackend):
    def __init__(self, backend):
        self.backend = backend
        assert backend._cache is not None, "The lazy backend requires cache enabled in the input backend."
        self._threads = {}

    def document_from_cache_or_string(self, schema, request_string, key):
        document = self.backend.document_from_cache(key)
        if document:
            return document

        # We check so we don't create more than one thread
        # for the same key
        if key not in self._threads:
            thread = Thread(
                target=
                lambda: self.backend.document_from_cache_or_string(schema, request_string, key)
            )
            self._threads[thread] = thread
            thread.start()

        # If we are already waiting for the thread to complete
        raise Exception("Document not ready yet.")

    # def document_from_string(self, schema, request_string):
    #     for backend in self.backends:
    #         try:
    #             return backend.document_from_string(schema, request_string)
    #         except
    #             continue
    #     raise Exception("GraphQLDeciderBackend was not able to retrieve a document. Backends tried: {}".format(repr(self.backends)))
