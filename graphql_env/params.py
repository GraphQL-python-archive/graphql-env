from collections import Mapping

from graphql.error import GraphQLError


class GraphQLParams(object):
    """The parameters that usually came from the side of the client"""

    __slots__ = ("query", "document_id", "operation_name", "variables")

    def __init__(
        self, query=None, document_id=None, operation_name=None, variables=None
    ):
        if not query and not document_id:
            raise GraphQLError("Must provide query string.")

        if variables and not isinstance(variables, Mapping):
            raise GraphQLError(
                "variables, if provided need to be a mapping. Received {}.".format(
                    repr(variables)
                )
            )

        self.query = query
        self.document_id = document_id
        self.operation_name = operation_name
        self.variables = variables or {}
