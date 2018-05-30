from graphql.type.definition import (
    GraphQLArgument,
    GraphQLField,
    GraphQLNonNull,
    GraphQLObjectType,
)
from graphql.type.scalars import GraphQLString
from graphql.type.schema import GraphQLSchema

from promise import Promise


def resolve_raises(*_):
    raise Exception("Throws!")


query_root_type = GraphQLObjectType(
    name="QueryRoot",
    fields={
        "thrower": GraphQLField(GraphQLNonNull(GraphQLString), resolver=resolve_raises),
        "request": GraphQLField(
            GraphQLNonNull(GraphQLString),
            resolver=lambda obj, info: info.context.args.get("q"),
        ),
        "context": GraphQLField(
            GraphQLNonNull(GraphQLString), resolver=lambda obj, info: info.context
        ),
        "test": GraphQLField(
            type=GraphQLString,
            args={"who": GraphQLArgument(GraphQLString)},
            resolver=lambda obj, info, who=None: Promise.resolve(
                "Hello %s" % (who or "World")
            ),
        ),
    },
)

mutation_root_type = GraphQLObjectType(
    name="MutationRoot",
    fields={
        "writeTest": GraphQLField(
            type=query_root_type, resolver=lambda *_: query_root_type
        )
    },
)

schema = GraphQLSchema(query_root_type, mutation_root_type)
