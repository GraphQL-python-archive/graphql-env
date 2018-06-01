from __future__ import absolute_import

import json
import six
from graphql.execution import ExecutionResult
from flask import jsonify, request
from flask.views import View

from .graphiql import render_graphiql
from ..exceptions import GraphQLHTTPError, InvalidJSONError, HTTPMethodNotAllowed
from ..utils import (
    params_from_http_request,
    execution_result_to_dict,
    ALL_OPERATIONS,
    QUERY_OPERATION,
)
from ..base import GraphQLBase


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
        return execution_result_to_dict(execution_result, self.format_error)

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

    def render_graphiql(self, graphql_params, execution_result):
        return render_graphiql(
            graphql_params,
            json.dumps(execution_result, indent=2, separators=(",", ": ")),
            graphiql_version=self.graphiql_version,
            graphiql_template=self.graphiql_template,
            graphiql_html_title=self.graphiql_html_title,
        )

    def dispatch_request(self):
        graphql_params = None
        status = 200
        try:
            if request.method not in ["GET", "POST"]:
                raise HTTPMethodNotAllowed()
            schema = self.get_schema()
            graphql_params = self.get_graphql_params()
            execution_result = self.execute(
                schema,
                graphql_params,
                root=self.get_root(),
                context=self.get_context(),
                middleware=self.get_middleware(),
                allowed_operations=self.get_allowed_operations(),
            )
        except Exception as error:
            if isinstance(error, GraphQLHTTPError):
                status = error.status_code
            execution_result = ExecutionResult(errors=[error])

        # If no data was included in the result, that indicates a runtime query
        # error, indicate as such with a generic status code.
        # Note: Information about the error itself will still be contained in
        # the resulting JSON payload.
        # http://facebook.github.io/graphql/#sec-Data

        if status == 200 and execution_result and execution_result.data is None:
            status = 500

        result = self.serialize(execution_result)
        if self.graphiql and self.can_display_graphiql():
            return self.render_graphiql(graphql_params, result)

        return jsonify(result), status
