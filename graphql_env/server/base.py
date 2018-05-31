from graphql import GraphQLSchema
from graphql_env.loader import GraphQLLoader

from .utils import format_error as default_format_error


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
        self.graphiql = graphiql
        self.graphiql_version = graphiql_version
        self.graphiql_template = graphiql_template
        self.graphiql_html_title = graphiql_html_title
        self.format_error = format_error or default_format_error
        self.context = context
        self.middleware = middleware
        self.loader = loader or GraphQLLoader()

        super(GraphQLBase, self).__init__(**kwargs)
