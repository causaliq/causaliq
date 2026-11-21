"""Functional tests for the checked long-running command protocol."""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

from causaliq.devtools import run_checked

pytestmark = pytest.mark.functional
SLEEPER = "import time; time.sleep(30)"


def wait_for(path: Path, seconds: float = 15.0) -> None:
    """Wait for an artefact to appear, failing the test on timeout."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if path.exists():
            return
        time.sleep(0.05)
    raise AssertionError(f"timed out waiting for {path}")


def launch(log: Path, *command: str, timeout: float = 30.0) -> int:
    """Launch a command through the protocol and return the tool's code."""
    return run_checked.main(
        ["--log", str(log), "--timeout", str(timeout), "--", *command]
    )


def test_run_and_wait_report_success(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A successful child is reported with its exit code and log tail."""
    log = tmp_path / "run.log"

    assert launch(log, sys.executable, "-c", "print('hello')") == 0
    wait_for(Path(f"{log}.exit"))
    code = run_checked.main(["--wait", "--log", str(log)])

    assert code == 0
    output = capsys.readouterr().out
    assert "hello" in output
    assert "EXIT_CODE=0" in output


def test_failing_child_code_is_mirrored(tmp_path: Path) -> None:
    """A non-zero child exit is reported unchanged."""
    log = tmp_path / "fail.log"

    launch(log, sys.executable, "-c", "raise SystemExit(3)")
    wait_for(Path(f"{log}.exit"))

    assert run_checked.main(["--wait", "--log", str(log)]) == 3


def test_wait_timeout_kills_and_reports_124(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A timeout kills the process tree and reports exit 124."""
    log = tmp_path / "slow.log"

    launch(log, sys.executable, "-c", SLEEPER)
    wait_for(Path(f"{log}.pid"))
    code = run_checked.main(["--wait", "--log", str(log), "--timeout", "1"])

    assert code == 124
    assert "timed out" in capsys.readouterr().out


def test_supervisor_timeout_records_124(tmp_path: Path) -> None:
    """The supervisor also enforces its own timeout."""
    log = tmp_path / "supervised.log"

    code = run_checked.main(
        [
            "--supervise",
            "--log",
            str(log),
            "--timeout",
            "1",
            "--",
            sys.executable,
            "-c",
            SLEEPER,
        ]
    )

    assert code == 0
    assert Path(f"{log}.exit").read_text(encoding="utf-8").strip() == (
        "EXIT_CODE=124"
    )


def test_supervisor_runs_a_child_directly(tmp_path: Path) -> None:
    """The supervisor writes the exit artefact for a quick command."""
    log = tmp_path / "direct.log"

    code = run_checked.main(
        [
            "--supervise",
            "--log",
            str(log),
            "--",
            sys.executable,
            "-c",
            "print(7)",
        ]
    )

    assert code == 0
    assert "EXIT_CODE=0" in Path(f"{log}.exit").read_text(encoding="utf-8")


def test_launch_without_command_is_a_usage_error(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Launching nothing is rejected."""
    assert run_checked.main(["--log", str(tmp_path / "x.log")]) == 2
    assert "no command" in capsys.readouterr().out
