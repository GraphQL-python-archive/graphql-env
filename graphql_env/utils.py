from hashlib import sha1

from graphql import GraphQLSchema

from ._compat import string_types

_schemas = {}

_queries = {}


def get_unique_schema_id(schema):
    '''Get a unique id given a GraphQLSchema'''
    assert isinstance(schema, GraphQLSchema), (
        "Must receive a GraphQLSchema as schema. Received {}"
    ).format(repr(schema))

    if schema not in _schemas:
        _schemas[schema] = sha1(str(schema).encode('utf-8')).hexdigest()
    return _schemas[schema]


def get_unique_query_id(query_str):
    '''Get a unique id given a query_string'''
    assert isinstance(query_str, string_types), (
        "Must receive a string as query_str. Received {}"
    ).format(repr(query_str))

    if query_str not in _queries:
        _queries[query_str] = sha1(str(query_str).encode('utf-8')).hexdigest()
    return _queries[query_str]
