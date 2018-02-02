#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLEnv, GraphQLBackend, GraphQLCoreBackend, GraphQLDocument, GraphQLDeciderBackend
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


class FakeBackend(GraphQLBackend):
    reached = False

    def __init__(self, raises=False):
        self.raises = raises

    def document_from_cache_or_string(self, *args, **kwargs):
        self.reached = True
        if self.raises:
            raise Exception("Backend failed")

    def reset(self):
        self.reached = False


def test_decider_backend_healthy_backend():
    backend1 = FakeBackend()
    backend2 = FakeBackend()
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLDeciderBackend([
            backend1,
            backend2,
        ]))

    graphql_env.document_from_string('{ hello }')
    assert backend1.reached
    assert not backend2.reached


def test_decider_backend_unhealthy_backend():
    backend1 = FakeBackend(raises=True)
    backend2 = FakeBackend()
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLDeciderBackend([
            backend1,
            backend2,
        ]))

    graphql_env.document_from_string('{ hello }')
    assert backend1.reached
    assert backend2.reached


def test_decider_backend_dont_use_cache():
    backend1 = FakeBackend()
    backend2 = FakeBackend()
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLDeciderBackend([
            backend1,
            backend2,
        ]))

    graphql_env.document_from_string('{ hello }')
    assert backend1.reached
    assert not backend2.reached

    backend1.reset()
    graphql_env.document_from_string('{ hello }')
    assert backend1.reached


def test_decider_backend_use_cache_if_provided():
    backend1 = FakeBackend()
    backend2 = FakeBackend()
    graphql_env = GraphQLEnv(
        schema=schema,
        backend=GraphQLDeciderBackend([
            backend1,
            backend2,
        ], cache={}))

    graphql_env.document_from_string('{ hello }')
    assert backend1.reached
    assert not backend2.reached

    backend1.reset()
    graphql_env.document_from_string('{ hello }')
    assert not backend1.reached
