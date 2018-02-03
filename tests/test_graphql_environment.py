#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import (GraphQLEnv, GraphQLBackend, GraphQLCoreBackend,
                         GraphQLDocument, GraphQLDeciderBackend,
                         GraphQLThreadedLazyBackend)
from graphql.execution.executors.sync import SyncExecutor
from threading import Event
from time import sleep
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
        super(FakeBackend, self).__init__()
        self.raises = raises

    def document_from_cache_or_string(self, schema, request_string, key):
        self.reached = True
        if self.raises:
            raise Exception("Backend failed")
        document = GraphQLDocument()
        self._cache[key] = document
        return document

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


def test_graphql_threaded_backend():
    e = Event()
    e2 = Event()

    class LockBackend(FakeBackend):
        def document_from_cache_or_string(self, schema, request_string, key):
            sleep(.1)
            document = super(LockBackend, self).document_from_cache_or_string(
                schema, request_string, key)
            e.set()
            # e2.wait()
            return document

    backend = LockBackend()
    graphql_env = GraphQLEnv(
        schema=schema, backend=GraphQLThreadedLazyBackend(backend))

    with pytest.raises(Exception) as exc_info:
        graphql_env.document_from_string('{ hello }')

    assert str(exc_info.value) == "Document not ready yet."

    assert not backend.reached
    e.wait()
    assert backend.reached
    doc = graphql_env.document_from_string('{ hello }')
    assert isinstance(doc, GraphQLDocument)
