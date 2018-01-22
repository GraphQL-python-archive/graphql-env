class GraphQLBackend(object):
    def __init__(self, cache=None, use_cache=True):
        if cache is None and use_cache:
            cache = {}
        self._cache = cache

    def document_from_cache_or_string(self, schema, request_string, key):
        '''This method should return a GraphQLQuery'''
        if not key or self._cache is None:
            # We return without caching
            return self.document_from_string(schema, request_string)

        if key not in self._cache:
            self._cache[key] = self.document_from_string(
                schema, request_string)

        return self._cache[key]

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
