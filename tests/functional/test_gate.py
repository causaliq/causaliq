"""Functional tests for the gate orchestration."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools import gate
from causaliq.devtools.steps import StepResult

pytestmark = pytest.mark.functional

CONFIG = """
[tool.causaliq]
distribution = "causaliq-demo"
package = "causaliq_demo"
testpaths = ["tests/unit"]
fast_testpaths = ["tests/unit"]
"""


def make_project(root: Path) -> None:
    """Write a minimal project with a gate configuration."""
    (root / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n' + CONFIG, encoding="utf-8"
    )
    (root / "src").mkdir()
    (root / "tests" / "unit").mkdir(parents=True)


def activate(monkeypatch: pytest.MonkeyPatch, root: Path) -> None:
    """Point the gate at the project and a repository-local venv."""
    monkeypatch.chdir(root)
    monkeypatch.setenv("VIRTUAL_ENV", str(root / "venv"))
    monkeypatch.setattr(gate.sys, "prefix", str(root / "venv"))


def patch_results(monkeypatch: pytest.MonkeyPatch, passed: bool) -> None:
    """Replace the real step execution with a fixed outcome."""

    def fake_run(steps: list, root: Path) -> list:
        return [StepResult(step.name, passed) for step in steps]

    monkeypatch.setattr(gate, "run_all", fake_run)


def test_unknown_option_returns_two(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """An unsupported switch is a usage error."""
    monkeypatch.chdir(tmp_path)

    assert gate.main(["--nope"]) == 2


def test_missing_configuration_returns_two(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A tree without the configuration block cannot run the gate."""
    monkeypatch.chdir(tmp_path)

    assert gate.main([]) == 2


def test_foreign_environment_is_refused(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A different project's venv is not silently reused."""
    make_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)

    assert gate.main([]) == 2
    assert "not this repository" in capsys.readouterr().out


def test_foreign_environment_reports_the_variable(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A stale VIRTUAL_ENV is named in the refusal message."""
    make_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("VIRTUAL_ENV", "C:/somewhere/else")

    assert gate.main([]) == 2
    assert "VIRTUAL_ENV=" in capsys.readouterr().out


def test_foreign_environment_is_accepted_in_ci(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """CI runners install into a shared environment, so continue."""
    make_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    patch_results(monkeypatch, True)

    assert gate.main(["--ci"]) == 0
    assert "continuing in CI mode" in capsys.readouterr().out


def test_rules_only_runs_the_real_checker(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Rules-only mode exercises the in-process checker end to end."""
    make_project(tmp_path)
    activate(monkeypatch, tmp_path)

    assert gate.main(["--rules"]) == 0


def test_passing_gate_reports_success(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """All steps passing yields a zero exit code and a summary."""
    make_project(tmp_path)
    activate(monkeypatch, tmp_path)
    patch_results(monkeypatch, True)

    assert gate.main([]) == 0
    output = capsys.readouterr().out
    assert "black: PASSED" in output
    assert "All checks passed." in output


def test_failing_gate_reports_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A failing step yields exit code one."""
    make_project(tmp_path)
    activate(monkeypatch, tmp_path)
    patch_results(monkeypatch, False)

    assert gate.main([]) == 1
    assert "Some checks FAILED." in capsys.readouterr().out


def test_fix_and_slow_flags_are_announced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """The plan states when formatting writes and slow tests run."""
    make_project(tmp_path)
    activate(monkeypatch, tmp_path)
    patch_results(monkeypatch, True)

    assert gate.main(["--fix", "--include-slow"]) == 0
    output = capsys.readouterr().out
    assert "fix mode" in output
    assert "slow tests (slow) are included" in output


def test_fast_selection_is_announced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Fast mode is visible in the plan."""
    make_project(tmp_path)
    activate(monkeypatch, tmp_path)
    patch_results(monkeypatch, True)

    assert gate.main(["--fast"]) == 0
    assert "fast test selection" in capsys.readouterr().out


def test_ci_creates_report_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """CI mode fills in and creates the report locations."""
    make_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    seen = {}

    def fake_run(built: list, root: Path) -> list:
        seen["command"] = built[-1].command
        return [StepResult(step.name, True) for step in built]

    monkeypatch.setattr(gate, "run_all", fake_run)

    assert gate.main(["--ci"]) == 0
    assert (tmp_path / "build" / "ci").is_dir()
    assert any("junit.xml" in item for item in seen["command"])
    assert any("coverage.xml" in item for item in seen["command"])


def test_ci_keeps_explicit_report_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Explicit report paths are not replaced by the defaults."""
    make_project(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    seen = {}

    def fake_run(built: list, root: Path) -> list:
        seen["command"] = built[-1].command
        return [StepResult(step.name, True) for step in built]

    monkeypatch.setattr(gate, "run_all", fake_run)

    assert gate.main(["--ci", "--junit", "custom.xml"]) == 0
    assert "--junitxml=custom.xml" in seen["command"]
