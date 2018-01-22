import json
import six
from collections import Mapping
from .exceptions import InvalidVariablesJSONError, MissingQueryError


class GraphQLParams(object):
    '''The parameters that usually came from the side of the client'''

    __slots__ = ('query', 'query_id', 'operation_name', 'variables')

    def __init__(self,
                 query=None,
                 query_id=None,
                 operation_name=None,
                 variables=None):
        if not query or query_id:
            raise MissingQueryError()
        assert not variables or isinstance(
            variables, Mapping
        ), "variables, if provided need to be a mapping. Received {}.".format(
            repr(variables))
        self.query = query
        self.query_id = query_id
        self.operation_name = operation_name
        self.variables = variables or {}

    @classmethod
    def from_http_request(cls, query_params, data):
        variables = data.get('variables') or query_params.get('variables')
        if isinstance(variables, six.string_types):
            try:
                variables = json.loads(variables)
            except:
                raise InvalidVariablesJSONError()

        return cls(
            query=data.get('query') or query_params.get('query'),
            query_id=data.get('queryId') or query_params.get('queryId'),
            operation_name=data.get('operationName') or
            query_params.get('operationName'),
            variables=variables)
