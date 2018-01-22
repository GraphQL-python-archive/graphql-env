class GraphQLHTTPError(Exception):
    status_code = 400
    default_detail = None

    def __init__(self, detail=None):
        if detail is None:
            detail = self.default_detail
        super(GraphQLHTTPError, self).__init__(detail)


class InvalidJSONError(GraphQLHTTPError):
    status_code = 400
    default_detail = 'POST body sent invalid JSON.'


class InvalidVariablesJSONError(GraphQLHTTPError):
    status_code = 400
    default_detail = 'Variables are invalid JSON.'


class HTTPMethodNotAllowed(GraphQLHTTPError):
    default_detail = 'GraphQL only supports GET and POST requests.'


class MissingQueryError(GraphQLHTTPError):
    default_detail = 'Must provide query string.'
