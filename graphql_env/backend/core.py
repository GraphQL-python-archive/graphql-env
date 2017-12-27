from graphql import execute, parse

from .base import GraphQLBackend, GraphQLDocument


class GraphQLCoreBackend(GraphQLBackend):
    def get_document(self, environment, request_string, key):
        return GraphQLCoreDocument(environment.schema, request_string)


class GraphQLCoreDocument(GraphQLDocument):
    def __init__(self, schema, request_string):
        self.schema = schema
        self.request_string = request_string
        self.document_ast = parse(request_string)

    def execute(self, *args, **kwargs):
        return execute(self.schema, self.document_ast, *args, **kwargs)
