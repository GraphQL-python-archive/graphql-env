#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLEnv, GraphQLCoreBackend, GraphQLDocument
from .schema import schema


def test_core_backend():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())
    document = graphql_env.document_from_string('{ hello }')
    assert isinstance(document, GraphQLDocument)
    result = document.execute()
    assert not result == {'data': {'hello': 'World'}}


def test_backend_is_cached_by_default():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())
    document1 = graphql_env.document_from_string('{ hello }')
    document2 = graphql_env.document_from_string('{ hello }')
    assert document1 == document2


def test_backend_will_compute_if_cache_non_existing():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLCoreBackend(use_cache=False))
    document1 = graphql_env.document_from_string('{ hello }')
    document2 = graphql_env.document_from_string('{ hello }')
    assert document1 != document2
