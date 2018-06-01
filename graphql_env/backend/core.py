from graphql import execute, parse, validate, GraphQLError
from graphql.execution import ExecutionResult
from graphql.language import ast

from .base import GraphQLBackend, GraphQLDocument


class GraphQLCoreBackend(GraphQLBackend):
    def __init__(self, executor=None, **kwargs):
        super(GraphQLCoreBackend, self).__init__(**kwargs)
        self.execute_params = {"executor": executor}

    def document_from_string(self, schema, request_string):
        return GraphQLCoreDocument(schema, request_string, self.execute_params)


def get_operation_from_operation_name(document_ast, operation_name):
    for definition in document_ast.definitions:
        if isinstance(definition, ast.OperationDefinition):
            if (
                not operation_name
                or definition.name
                and definition.name.value == operation_name
            ):
                return definition.operation
    return None


class GraphQLCoreDocument(GraphQLDocument):
    errors = None

    def __init__(self, schema, request_string, execute_params=None):
        self.schema = schema
        self.request_string = request_string
        self.execute_params = execute_params or {}
        try:
            self.document_ast = parse(request_string)
            validation_errors = validate(schema, self.document_ast)
            if validation_errors:
                self.errors = validation_errors
        except Exception as e:
            self.document_ast = None
            self.errors = [e]

    def execute(
        self,
        root=None,
        context=None,
        middleware=None,
        operation_name=None,
        variables=None,
        allowed_operations=None,
    ):
        if self.errors:
            return ExecutionResult(errors=self.errors, invalid=True)
        try:
            if allowed_operations is not None:
                operation_type = get_operation_from_operation_name(
                    self.document_ast, operation_name
                )
                if operation_type and operation_type not in allowed_operations:
                    raise GraphQLError(
                        "{} operations are not allowed.".format(operation_type)
                    )
            return execute(
                self.schema,
                self.document_ast,
                root_value=root,
                middleware=middleware,
                context_value=context,
                variable_values=variables or {},
                operation_name=operation_name,
                **self.execute_params
            )
        except Exception as e:
            return ExecutionResult(errors=[e])
