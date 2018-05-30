#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLBackend, GraphQLCoreBackend, GraphQLDocument, GraphQLDeciderBackend, GraphQLCachedBackend
from graphql.execution.executors.sync import SyncExecutor
from .schema import schema


def test_core_backend():
    """Sample pytest test function with the pytest fixture as an argument."""
    backend = GraphQLCoreBackend()
    document = backend.document_from_string(schema, '{ hello }')
    assert isinstance(document, GraphQLDocument)
    result = document.execute()
    assert not result == {'data': {'hello': 'World'}}


def test_backend_is_not_cached_by_default():
    """Sample pytest test function with the pytest fixture as an argument."""
    backend = GraphQLCoreBackend()
    document1 = backend.document_from_string(schema, '{ hello }')
    document2 = backend.document_from_string(schema, '{ hello }')
    assert document1 != document2


def test_backend_is_cached_when_needed():
    """Sample pytest test function with the pytest fixture as an argument."""
    cached_backend = GraphQLCachedBackend(GraphQLCoreBackend())
    document1 = cached_backend.document_from_string(schema, '{ hello }')
    document2 = cached_backend.document_from_string(schema, '{ hello }')
    assert document1 == document2


def test_backend_can_execute():
    backend = GraphQLCoreBackend()
    document1 = backend.document_from_string(schema, '{ hello }')
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
    backend = GraphQLCoreBackend(executor=executor)
    document1 = backend.document_from_string(schema, '{ hello }')
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
    decider_backend = GraphQLDeciderBackend([
        backend1,
        backend2,
    ])

    decider_backend.document_from_string(schema, '{ hello }')
    assert backend1.reached
    assert not backend2.reached


def test_decider_backend_unhealthy_backend():
    backend1 = FakeBackend(raises=True)
    backend2 = FakeBackend()
    decider_backend = GraphQLDeciderBackend([
        backend1,
        backend2,
    ])

    decider_backend.document_from_string(schema, '{ hello }')
    assert backend1.reached
    assert backend2.reached


def test_decider_backend_dont_use_cache():
    backend1 = FakeBackend()
    backend2 = FakeBackend()
    decider_backend = GraphQLDeciderBackend([
        backend1,
        backend2,
    ])

    decider_backend.document_from_string(schema, '{ hello }')
    assert backend1.reached
    assert not backend2.reached

    backend1.reset()
    decider_backend.document_from_string(schema, '{ hello }')
    assert backend1.reached


def test_decider_backend_use_cache_if_provided():
    backend1 = FakeBackend()
    backend2 = FakeBackend()
    decider_backend = GraphQLDeciderBackend([
        GraphQLCachedBackend(backend1),
        GraphQLCachedBackend(backend2),
    ])

    decider_backend.document_from_string(schema, '{ hello }')
    assert backend1.reached
    assert not backend2.reached

    backend1.reset()
    decider_backend.document_from_string(schema, '{ hello }')
    assert not backend1.reached
