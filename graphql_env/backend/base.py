class GraphQLBackend(object):
    def __init__(self, cache=None, use_cache=True):
        if cache is None and use_cache:
            cache = {}
        self._cache = cache

    def document_from_cache(self, key):
        if self._cache and key in self._cache:
            return self._cache[key]

    def document_to_cache(self, key, document):
        if self._cache is not None:
            self._cache[key] = document

    def document_from_cache_or_string(self, schema, request_string, key):
        '''This method should return a GraphQLQuery'''
        cached_document = self.document_from_cache(key)
        if cached_document:
            return cached_document

        # If is not in cache
        document = self.document_from_string(schema, request_string)
        self.document_to_cache(key, document)
        return document

    def document_from_string(self, schema, request_string):
        raise NotImplementedError(
            "document_from_string method not implemented in {}.".format(
                self.__class__))


class GraphQLDocument(object):
    # @property
    # def query_string(self):
    #     raise NotImplementedError(
    #         "query_string property not implemented in {}.".format(
    #             self.__class__))

    # @property
    # def ast(self):
    #     raise NotImplementedError(
    #         "query_ast property not implemented in {}.".format(self.__class__))

    # @property
    # def schema(self):
    #     raise NotImplementedError(
    #         "schema property not implemented in {}.".format(self.__class__))

    def execute(self, *args, **kwargs):
        raise NotImplementedError(
            "execute method not implemented in {}.".format(self.__class__))
