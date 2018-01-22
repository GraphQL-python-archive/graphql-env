import json
import six

from ...params import GraphQLParams
from .exceptions import InvalidVariablesJSONError, MissingQueryError


def params_from_http_request(query_params, data):
    variables = data.get('variables') or query_params.get('variables')
    if isinstance(variables, six.string_types):
        try:
            variables = json.loads(variables)
        except:
            raise InvalidVariablesJSONError()

    return GraphQLParams(
        query=data.get('query') or query_params.get('query'),
        query_id=data.get('queryId') or query_params.get('queryId'),
        operation_name=data.get('operationName') or
        query_params.get('operationName'),
        variables=variables)
