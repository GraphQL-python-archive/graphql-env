#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `graphql_env` package."""

import pytest

from graphql_env import GraphQLCoreBackend, GraphQLCachedBackend
from graphql.execution.executors.sync import SyncExecutor
from .schema import schema


def test_backend_is_cached_when_needed():
    cached_backend = GraphQLCachedBackend(GraphQLCoreBackend())
    document1 = cached_backend.document_from_string(schema, "{ hello }")
    document2 = cached_backend.document_from_string(schema, "{ hello }")
    assert document1 == document2
