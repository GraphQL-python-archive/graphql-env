# -*- coding: utf-8 -*-
"""Top-level package for GraphQL Environment."""

__author__ = """Syrus Akbary"""
__email__ = "me@syrusakbary.com"
__version__ = "0.1.0"

from .backend import (
    GraphQLBackend,
    GraphQLDocument,
    GraphQLCoreBackend,
    GraphQLDeciderBackend,
    GraphQLCachedBackend,
    get_default_backend,
    set_default_backend,
)
from .loader import GraphQLLoader

__all__ = [
    "GraphQLBackend",
    "GraphQLDocument",
    "GraphQLCachedBackend",
    "GraphQLCoreBackend",
    "GraphQLDeciderBackend",
    "get_default_backend",
    "set_default_backend",
    "GraphQLLoader",
]
