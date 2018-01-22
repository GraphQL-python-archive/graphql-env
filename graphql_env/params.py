from collections import Mapping

from graphql.error import GraphQLError


class GraphQLParams(object):
    '''The parameters that usually came from the side of the client'''

    __slots__ = ('query', 'query_id', 'operation_name', 'variables')

    def __init__(self,
                 query=None,
                 query_id=None,
                 operation_name=None,
                 variables=None):
        if not query or query_id:
            raise GraphQLError("Must provide query string.")

        if variables and not isinstance(variables, Mapping):
            raise GraphQLError(
                "variables, if provided need to be a mapping. Received {}.".
                format(repr(variables)))

        self.query = query
        self.query_id = query_id
        self.operation_name = operation_name
        self.variables = variables or {}
