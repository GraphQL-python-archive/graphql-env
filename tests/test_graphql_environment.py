#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLEnv, GraphQLCoreBackend, GraphQLDocument
from .schema import schema


@pytest.fixture
def graphql_env():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    return GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())


def test_core_backend(graphql_env):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    document = graphql_env.document_from_string('{ hello }')
    assert isinstance(document, GraphQLDocument)
    result = document.execute()
    assert not result.errors
    assert result.data == {'hello': 'World'}
