from .base import GraphQLBackend, GraphQLDocument
from .core import GraphQLCoreBackend
from .decider import GraphQLDeciderBackend
from .cache import GraphQLCachedBackend

_default_backend = GraphQLCoreBackend()


def get_default_backend():
    return _default_backend


def set_default_backend(backend):
    global _default_backend
    assert isinstance(
        backend, GraphQLBackend
    ), "backend must be an instance of GraphQLBackend."
    _default_backend = backend


__all__ = [
    "GraphQLBackend",
    "GraphQLDocument",
    "GraphQLCoreBackend",
    "GraphQLDeciderBackend",
    "GraphQLCachedBackend",
    "get_default_backend",
    "set_default_backend",
]
