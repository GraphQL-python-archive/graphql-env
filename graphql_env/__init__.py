# -*- coding: utf-8 -*-
"""Top-level package for GraphQL Environment."""

__author__ = """Syrus Akbary"""
__email__ = 'me@syrusakbary.com'
__version__ = '0.1.0'

from .environment import GraphQLEnvironment
from .backend import (GraphQLBackend, GraphQLDocument, GraphQLCoreBackend,
                      get_default_backend, set_default_backend)

GraphQLEnv = GraphQLEnvironment

__all__ = [
    'GraphQLEnv',
    'GraphQLEnvironment',
    'GraphQLBackend',
    'GraphQLDocument',
    'GraphQLCoreBackend',
    'get_default_backend',
    'set_default_backend',
]
