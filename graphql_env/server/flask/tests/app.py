from flask import Flask
from .. import graphql_view

from .schema import Schema
from graphql_env import GraphQLEnvironment, GraphQLCoreBackend
from graphql_env.backend.quiver_cloud import GraphQLQuiverCloudBackend


def create_app(path='/graphql', environment=None, **kwargs):
    app = Flask(__name__)
    app.debug = True

    graphql_env = GraphQLEnvironment(
        schema=Schema,
        backend=GraphQLCoreBackend(),
        # backend=GraphQLQuiverCloudBackend(
        #     'http://6ea643a71f96482bae042729c0eedad4:ed675996b9914c549189e2adbc8c0412@api.graphql-quiver.com',
        #     {''}
        # )
    )

    def graphql():
        return graphql_view(graphql_env, **kwargs)

    app.add_url_rule(
        path,
        view_func=graphql,
        methods=['GET', 'POST', 'PUT', 'DELETE'],
        endpoint='graphql')
    return app


if __name__ == '__main__':
    app = create_app(graphiql=True)
    app.run()
