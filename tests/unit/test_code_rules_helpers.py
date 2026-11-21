"""Unit tests for the small code-rules helpers."""

from __future__ import annotations

import ast

import pytest

from causaliq.devtools import code_rules

pytestmark = pytest.mark.unit


def test_multi_statement_if_is_not_a_guard() -> None:
    """Only a single exiting statement counts as a guard clause."""
    node = ast.parse("if x:\n    a = 1\n    b = 2\n").body[0]

    assert isinstance(node, ast.If)
    assert code_rules._is_guard(node) is False


def test_node_without_a_line_number_is_not_excluded() -> None:
    """Nodes without source positions carry no pragma."""
    node = ast.Module(body=[], type_ignores=[])

    assert code_rules._is_excluded(node, []) is False


def test_pragma_beyond_the_file_is_not_excluded() -> None:
    """A line number past the end of the source is not excluded."""
    node = ast.parse("x = 1\n").body[0]

    assert code_rules._is_excluded(node, []) is False
