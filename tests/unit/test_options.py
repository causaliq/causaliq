"""Unit tests for gate option parsing."""

from __future__ import annotations

import pytest

from causaliq.devtools.options import GateOptions, OptionError, parse_args

pytestmark = pytest.mark.unit


def test_defaults_are_all_off() -> None:
    """No arguments selects the default full gate."""
    assert parse_args([]) == GateOptions()


def test_flags_are_recognised() -> None:
    """Every documented flag maps to its attribute."""
    options = parse_args(["--fix", "--fast", "--include-slow", "--ci"])

    assert options.fix is True
    assert options.fast is True
    assert options.include_slow is True
    assert options.ci is True


def test_value_flags_accept_both_forms() -> None:
    """Value flags work with a separate argument and with ``=``."""
    separate = parse_args(["--junit", "out.xml"])
    joined = parse_args(["--coverage-xml=coverage.xml"])

    assert separate.junit == "out.xml"
    assert joined.coverage_xml == "coverage.xml"


def test_unknown_option_is_rejected() -> None:
    """An unrecognised switch is an error rather than being ignored."""
    with pytest.raises(OptionError, match="--nope"):
        parse_args(["--nope"])


def test_missing_value_is_treated_as_absent() -> None:
    """A value flag at the end of the line yields None."""
    assert parse_args(["--junit"]).junit is None


def test_rules_and_no_tests_flags() -> None:
    """The rules-only and no-tests switches are exposed."""
    options = parse_args(["--rules", "--no-tests"])

    assert options.rules_only is True
    assert options.no_tests is True


def test_legacy_powershell_switches_are_accepted() -> None:
    """The wrapper forwards ``-Fast``, ``-Fix`` and ``-IncludeSlow``."""
    options = parse_args(["-Fast", "-Fix", "-IncludeSlow", "-INCLUDESLOW"])

    assert options.fast is True
    assert options.fix is True
    assert options.include_slow is True
