#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLEnv, GraphQLBackend, GraphQLCoreBackend, GraphQLDocument, GraphQLDeciderBackend, GraphQLCachedBackend
from graphql.execution.executors.sync import SyncExecutor
from .schema import schema


def test_core_backend():
    """Sample pytest test function with the pytest fixture as an argument."""
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())
    document = graphql_env.document_from_string('{ hello }')
    assert isinstance(document, GraphQLDocument)
    result = document.execute()
    assert not result == {'data': {'hello': 'World'}}


def test_backend_is_not_cached_by_default():
    """Sample pytest test function with the pytest fixture as an argument."""
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())
    document1 = graphql_env.document_from_string('{ hello }')
    document2 = graphql_env.document_from_string('{ hello }')
    assert document1 != document2


def test_backend_is_cached_when_needed():
    """Sample pytest test function with the pytest fixture as an argument."""
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCachedBackend(GraphQLCoreBackend()))
    document1 = graphql_env.document_from_string('{ hello }')
    document2 = graphql_env.document_from_string('{ hello }')
    assert document1 == document2


def test_backend_can_execute():
    graphql_env = GraphQLEnv(schema=schema, backend=GraphQLCoreBackend())
    document1 = graphql_env.document_from_string('{ hello }')
    result = document1.execute()
    assert not result.errors
    assert result.data == {'hello': 'World'}


class BaseExecutor(SyncExecutor):
    executed = False

    def execute(self, *args, **kwargs):
        self.executed = True
        return super(BaseExecutor, self).execute(*args, **kwargs)


def test_backend_can_execute_custom_executor():
    executor = BaseExecutor()
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLCoreBackend(executor=executor))
    document1 = graphql_env.document_from_string('{ hello }')
    result = document1.execute()
    assert not result.errors
    assert result.data == {'hello': 'World'}
    assert executor.executed


class FakeBackend(GraphQLBackend):
    reached = False

    def __init__(self, raises=False):
        self.raises = raises

    def document_from_string(self, *args, **kwargs):
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
            GraphQLCachedBackend(backend1),
            GraphQLCachedBackend(backend2),
        ]))

    graphql_env.document_from_string('{ hello }')
    assert backend1.reached
    assert not backend2.reached

    backend1.reset()
    graphql_env.document_from_string('{ hello }')
    assert not backend1.reached
