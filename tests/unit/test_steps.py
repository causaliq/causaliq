"""Unit tests for building and running gate steps."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from causaliq.devtools import steps
from causaliq.devtools.config import CausaliqConfig
from causaliq.devtools.options import GateOptions

pytestmark = pytest.mark.unit

CONFIG = CausaliqConfig(
    distribution="causaliq-demo",
    package="causaliq_demo",
    python_versions=("3.9", "3.11"),
    default_python="3.11",
    dev_extras=("dev",),
    testpaths=("tests/unit", "tests/functional", "tests/integration"),
    fast_testpaths=("tests/unit", "tests/functional"),
)


def names(options: GateOptions) -> list:
    """Return the step names selected by ``options``."""
    return [step.name for step in steps.build_steps(CONFIG, options)]


def tests_command(options: GateOptions) -> tuple:
    """Return the pytest command selected by ``options``."""
    built = steps.build_steps(CONFIG, options)
    return built[-1].command or ()


def test_default_step_order() -> None:
    """The full gate runs formatting, linting, rules, typing and tests."""
    assert names(GateOptions()) == [
        "black",
        "isort",
        "flake8",
        "code rules",
        "mypy",
        "tests",
    ]


def test_fast_skips_typing_and_narrower_tests() -> None:
    """Fast mode drops mypy, integration tests and coverage."""
    command = tests_command(GateOptions(fast=True))

    assert "mypy" not in names(GateOptions(fast=True))
    assert "tests/integration" not in command
    assert "--cov=causaliq_demo" not in command


def test_rules_only_runs_one_step() -> None:
    """Rules-only mode is used by the coding policy."""
    assert names(GateOptions(rules_only=True)) == ["code rules"]


def test_no_tests_keeps_quality_steps() -> None:
    """The no-tests switch only removes the pytest step."""
    assert "tests" not in names(GateOptions(no_tests=True))


def test_fix_removes_check_flags() -> None:
    """Fix mode lets black and isort write changes."""
    built = {
        step.name: step.command
        for step in steps.build_steps(CONFIG, GateOptions(fix=True))
    }

    assert "--check" not in built["black"]
    assert "--check-only" not in built["isort"]


def test_default_excludes_the_slow_marker() -> None:
    """The default run passes the exclusion expression explicitly."""
    command = tests_command(GateOptions())

    assert "not slow" in command


def test_include_slow_overrides_the_marker_filter() -> None:
    """Including slow tests passes an expression that matches everything."""
    command = tests_command(GateOptions(include_slow=True))

    assert command[command.index("-m") + 1] == "pytest"
    assert "slow or not slow" in command
    assert "not slow" not in command


def test_slow_marker_is_configurable() -> None:
    """A package may rename the slow marker."""
    config = replace(CONFIG, slow_marker="selenium")
    built = steps.build_steps(config, GateOptions())

    assert "not selenium" in (built[-1].command or ())


def test_ci_reports_are_added() -> None:
    """JUnit and coverage XML paths appear in the pytest command."""
    options = GateOptions(junit="build/junit.xml", coverage_xml="out.xml")
    command = tests_command(options)

    assert "--junitxml=build/junit.xml" in command
    assert "--cov-report=xml:out.xml" in command


def test_extra_steps_are_appended() -> None:
    """Configured extra steps become ordinary steps."""
    config = replace(CONFIG, extra_steps=("python -m pip check",))
    built = steps.build_steps(config, GateOptions())

    assert [step.name for step in built][-2:] == ["python", "tests"]
    assert built[-2].command == ("python", "-m", "pip", "check")


def test_blank_extra_step_is_ignored() -> None:
    """An empty extra step does not produce a step."""
    config = replace(CONFIG, extra_steps=("",))
    assert "tests" in [
        step.name for step in steps.build_steps(config, GateOptions())
    ]


def test_run_step_without_command_uses_code_rules(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The rules step runs in-process against the source directory."""
    seen = {}

    def fake_main(argv: list) -> int:
        seen["argv"] = argv
        return 0

    monkeypatch.setattr(steps.code_rules, "main", fake_main)
    result = steps.run_step(steps.Step("code rules"), tmp_path)

    assert result.passed is True
    assert seen["argv"][-1] == str(tmp_path / "src")


def test_run_step_records_a_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A non-zero rules exit code marks the step as failed."""
    monkeypatch.setattr(steps.code_rules, "main", lambda argv: 1)
    result = steps.run_step(steps.Step("code rules"), tmp_path)

    assert result.passed is False


def test_run_step_runs_external_commands(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """External steps delegate to subprocess and keep the exit code."""
    seen = {}

    def fake_call(command: list) -> int:
        seen["command"] = command
        return 3

    monkeypatch.setattr(steps.subprocess, "call", fake_call)
    step = steps.Step("black", ("black", "--check", "src/"))
    result = steps.run_step(step, tmp_path)

    assert seen["command"] == ["black", "--check", "src/"]
    assert result == steps.StepResult("black", False, "exit 3")


def test_run_all_prints_each_outcome(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Every step is announced and summarised as it runs."""
    monkeypatch.setattr(
        steps,
        "run_step",
        lambda step, root: steps.StepResult(step.name, step.name != "mypy"),
    )
    built = [steps.Step("black"), steps.Step("mypy")]

    results = steps.run_all(built, tmp_path)

    output = capsys.readouterr().out
    assert "== black ==" in output
    assert "-- mypy: FAILED" in output
    assert [result.passed for result in results] == [True, False]
