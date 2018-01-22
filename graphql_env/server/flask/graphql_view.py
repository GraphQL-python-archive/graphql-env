from __future__ import absolute_import

import json
import six
from graphql.error import GraphQLError, format_error as default_format_error
from graphql.execution import ExecutionResult
from flask import jsonify, request

from .graphiql import render_graphiql
from .exceptions import GraphQLHTTPError, InvalidJSONError, HTTPMethodNotAllowed
from .utils import params_from_http_request


def can_display_graphiql(request):
    if request.method != 'GET':
        return False
    if 'raw' in request.args:
        return False

    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])

    return best == 'text/html' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['application/json']


def get_graphql_params(request):
    data = {}
    content_type = request.mimetype
    if content_type == 'application/graphql':
        data = {'query': request.data.decode('utf8')}
    elif content_type == 'application/json':
        try:
            data = request.get_json()
        except:
            raise InvalidJSONError()
    elif content_type in ('application/x-www-form-urlencoded',
                          'multipart/form-data', ):
        data = request.form.to_dict()

    query_params = request.args.to_dict()
    return params_from_http_request(query_params, data)


ALL_OPERATIONS = set(("query", "mutation", "subscription"))


def get_allowed_operations(request):
    if request.method == "GET":
        return set(("query", ))
    return ALL_OPERATIONS


Request = object()


def execution_result_to_dict(execution_result, format_error):
    data = {}
    if execution_result.errors:
        data['errors'] = [
            format_error(error) for error in execution_result.errors
        ]
    if execution_result.data and not execution_result.invalid:
        data['data'] = execution_result.data
    return data


def default_serialize(execution_result, format_error=default_format_error):
    data = execution_result_to_dict(execution_result, format_error)
    return jsonify(data)  #, 200 if execution_result.errors else 400


def graphql_view(execute,
                 root=None,
                 graphiql=False,
                 context=Request,
                 middleware=None,
                 serialize=default_serialize,
                 allowed_operations=None):
    graphql_params = None
    allowed_operations = get_allowed_operations(request)
    status = 200
    try:
        if request.method not in ['GET', 'POST']:
            raise HTTPMethodNotAllowed()
        graphql_params = get_graphql_params(request)
        if context is Request:
            context = request
        execution_result = execute(
            graphql_params,
            root=root,
            context=context,
            middleware=middleware,
            allowed_operations=allowed_operations)
    except Exception as error:
        if isinstance(error, GraphQLHTTPError):
            status = error.status_code
        execution_result = ExecutionResult(errors=[error])

    if graphiql and can_display_graphiql(request):
        return render_graphiql(graphql_params, execution_result)

    if execution_result.data is None and execution_result.errors:
        status = 400

    return serialize(execution_result), status
