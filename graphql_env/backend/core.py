from graphql import execute, parse, validate
from graphql.execution import ExecutionResult

from .base import GraphQLBackend, GraphQLDocument


class GraphQLCoreBackend(GraphQLBackend):
    def document_from_string(self, environment, request_string):
        return GraphQLCoreDocument(environment.schema, request_string)


class GraphQLCoreDocument(GraphQLDocument):
    errors = None

    def __init__(self, schema, request_string):
        self.schema = schema
        self.request_string = request_string
        try:
            self.document_ast = parse(request_string)
            validation_errors = validate(schema, self.document_ast)
            if validation_errors:
                self.errors = validation_errors
        except Exception as e:
            self.document_ast = None
            self.errors = [e]

    def execute(self,
                root=None,
                context=None,
                operation_name=None,
                variables=None,
                allowed_operations=None,
                **extra):
        if self.errors:
            return ExecutionResult(errors=self.errors)
        try:
            return execute(
                self.schema,
                self.document_ast,
                root_value=root,
                context_value=context,
                variable_values=variables,
                operation_name=operation_name,
                **extra)
        except Exception as e:
            return ExecutionResult(errors=[e])
