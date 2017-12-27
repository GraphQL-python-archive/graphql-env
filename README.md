# GraphQL-Env [![Build Status](https://travis-ci.org/graphql-python/graphql-env.svg?branch=master)](https://travis-ci.org/graphql-python/graphql-env) [![PyPI version](https://badge.fury.io/py/graphql-env.svg)](https://badge.fury.io/py/graphql-env) [![Coverage Status](https://coveralls.io/repos/graphql-python/graphql-env/badge.svg?branch=master&service=github)](https://coveralls.io/github/graphql-python/graphql-env?branch=master)

GraphQL-Env provides a GraphQL environment with pluggable query optimizers (backends) for Python GraphQL servers.

## Installation

For instaling GraphQL-Env, just run this command in your shell

```bash
pip install graphql-env
```

## Examples

Here is one example for you to get started:

```python
from graphql_env import GraphQLEnvironment

# schema = graphene.Schema(...)

graphql_env = GraphQLEnv(
    schema=schema,
)

my_query = graphql_env.document_from_string('{ hello }')
result = my_query.execute()
```

### Usage with Quiver Cloud

Quiver is a JIT compiler for GraphQL queries. It reduces the CPU effort
to make the query to the maximum, similar performance as if you write the
data retrieval by hand (0 overhead from GraphQL).

Here is an example usage for Quiver:

```python
from graphql_env import GraphQLEnvironment
from graphql_env.backend.quiver_cloud import GraphQLQuiverCloudBackend

# schema = graphene.Schema(...)

graphql_env = GraphQLEnv(
    schema=schema,
    backend=GraphQLQuiverCloudBackend(
        'http://******@api.graphql-quiver.com'
    )
)

my_query = graphql_env.document_from_string('{ hello }')
result = my_query.execute()
```

**Note: Quiver Cloud is using `requests` under the hood. Systems like Google App Engine
need a [monkeypatch to have it working properly](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/urlfetch/requests/main.py#L20-L26)**

## Contributing

After cloning this repo, ensure dependencies are installed by running:

```sh
pip install -e ".[test]"
```

After developing, the full test suite can be evaluated by running:

```sh
py.test graphql_env --cov=graphql_env --benchmark-skip # Use -v -s for verbose mode
```

You can also run the benchmarks with:

```sh
py.test graphql_env --benchmark-only
```

### Documentation

The documentation is generated using the excellent [Sphinx](http://www.sphinx-doc.org/) and a custom theme.

The documentation dependencies are installed by running:

```sh
cd docs
pip install -r requirements.txt
```

Then to produce a HTML version of the documentation:

```sh
make html
```
