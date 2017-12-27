class GraphQLBackend(object):
    def get_document(self, environment, request_string, key):
        '''This method should return a GraphQLQuery'''
        raise NotImplementedError("get_document method not implemented in {}.".
                                  format(self.__class__))


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
