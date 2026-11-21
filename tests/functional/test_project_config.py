"""Functional tests for repository-level tool configuration."""

from __future__ import annotations

from pathlib import Path

import pytest

pytestmark = pytest.mark.functional
ROOT = Path(__file__).resolve().parents[2]


def test_flake8_configuration_is_committed() -> None:
    """The flake8 settings must live in a tracked file, not a local one.

    Shared CI runs ``flake8 src tests`` without passing any options. If the
    ``.flake8`` file is missing from the checkout, flake8 falls back to its
    defaults and reports E203 for black's PEP 8 slice spacing. This test
    fails as soon as the file stops being part of the repository.
    """
    config = ROOT / ".flake8"

    assert config.is_file()
    text = config.read_text(encoding="utf-8")
    assert "max-line-length = 79" in text
    assert "E203" in text
