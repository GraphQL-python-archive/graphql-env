from __future__ import absolute_import

import json
import six
from graphql import GraphQLSchema
from graphql.execution import ExecutionResult
from flask import jsonify, request
from flask.views import View

from .graphiql import render_graphiql
from .exceptions import GraphQLHTTPError, InvalidJSONError, HTTPMethodNotAllowed
from .utils import (
    params_from_http_request,
    execution_result_to_dict,
    ALL_OPERATIONS,
    QUERY_OPERATION,
    format_error as default_format_error,
)
from graphql_env.loader import GraphQLLoader


class GraphQLBase(object):
    schema = None
    executor = None
    root = None
    graphiql = False
    graphiql_version = None
    graphiql_template = None
    graphiql_html_title = None
    format_error = None
    context = None
    middleware = None
    loader = None

    def __init__(
        self,
        schema=None,
        executor=None,
        root=None,
        root_value=None,
        env=None,
        graphiql=False,
        graphiql_version=None,
        graphiql_template=None,
        graphiql_html_title=None,
        format_error=None,
        context=None,
        middleware=None,
        loader=None,
        batch=False,
        **kwargs
    ):
        if schema:
            assert isinstance(
                schema, GraphQLSchema
            ), "A Schema is required to be provided to GraphQLView."
        if batch:
            raise Exception("GraphQLView batch is no longer supported.")

        self.schema = schema
        self.executor = executor
        self.root = root or root_value
        self.env = env
        self.graphiql = graphiql
        self.graphiql_version = graphiql_version
        self.graphiql_template = graphiql_template
        self.graphiql_html_title = graphiql_html_title
        self.format_error = format_error or default_format_error
        self.context = context
        self.middleware = middleware
        self.loader = loader or GraphQLLoader()

        super(GraphQLBase, self).__init__(**kwargs)


class GraphQLView(GraphQLBase, View):

    methods = ["GET", "POST", "PUT", "DELETE"]

    def get_schema(self):
        return self.schema

    def get_root(self):
        return self.root

    def get_context(self):
        return self.context or request

    def get_middleware(self):
        return self.middleware

    def execute(
        self,
        schema,
        graphql_params,
        root=None,
        context=None,
        middleware=None,
        allowed_operations=None,
    ):
        extra = {}
        # We only do this to provide a compatibility layer with previous vesions
        if self.executor:
            extra["executor"] = self.executor

        document = self.loader.get_document_from_params(schema, graphql_params)
        return document.execute(
            root=root,
            context=context,
            middleware=middleware,
            operation_name=graphql_params.operation_name,
            variables=graphql_params.variables,
            allowed_operations=allowed_operations,
            **extra
        )

    def get_allowed_operations(self):
        if request.method == "GET":
            return QUERY_OPERATION
        return ALL_OPERATIONS

    def serialize(self, execution_result):
        data = execution_result_to_dict(execution_result, self.format_error)
        return jsonify(data)

    def can_display_graphiql(self):
        if request.method != "GET":
            return False
        if "raw" in request.args:
            return False

        best = request.accept_mimetypes.best_match(["application/json", "text/html"])

        return (
            best == "text/html"
            and request.accept_mimetypes[best]
            > request.accept_mimetypes["application/json"]
        )

    def get_graphql_params(self):
        data = {}
        content_type = request.mimetype
        if content_type == "application/graphql":
            data = {"query": request.data.decode("utf8")}
        elif content_type == "application/json":
            try:
                data = request.get_json()
            except:
                raise InvalidJSONError()
        elif content_type in (
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ):
            data = request.form.to_dict()

        query_params = request.args.to_dict()
        return params_from_http_request(query_params, data)

    def dispatch_request(self):
        graphql_params = None
        status = 200
        try:
            if request.method not in ["GET", "POST"]:
                raise HTTPMethodNotAllowed()
            schema = self.get_schema()
            execution_result = self.execute(
                schema,
                self.get_graphql_params(),
                root=self.get_root(),
                context=self.get_context(),
                middleware=self.get_middleware(),
                allowed_operations=self.get_allowed_operations(),
            )
        except Exception as error:
            if isinstance(error, GraphQLHTTPError):
                status = error.status_code
            execution_result = ExecutionResult(errors=[error])

        if self.graphiql and self.can_display_graphiql():
            return self.render_graphiql(graphql_params, execution_result)

        # If no data was included in the result, that indicates a runtime query
        # error, indicate as such with a generic status code.
        # Note: Information about the error itself will still be contained in
        # the resulting JSON payload.
        # http://facebook.github.io/graphql/#sec-Data

        if status == 200 and execution_result and execution_result.data is None:
            status = 500

        return self.serialize(execution_result), status
