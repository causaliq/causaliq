"""Unit tests for the run/wait helpers, including both platforms."""

from __future__ import annotations

import argparse
import ctypes
import subprocess
import sys
from pathlib import Path

import pytest

from causaliq.devtools import processes, run_checked

pytestmark = pytest.mark.unit


class FakeKernel:
    """Stand-in for kernel32 used by the Windows liveness probe."""

    def __init__(self, handle: int, wait_result: int) -> None:
        self.handle = handle
        self.wait_result = wait_result
        self.closed = None

    def OpenProcess(self, access: int, inherit: bool, pid: int) -> int:
        """Return the configured handle."""
        return self.handle

    def WaitForSingleObject(self, handle: int, timeout: int) -> int:
        """Return the configured wait result."""
        return self.wait_result

    def CloseHandle(self, handle: int) -> None:
        """Record that the handle was closed."""
        self.closed = handle


def test_clean_removes_the_separator() -> None:
    """Argparse keeps ``--`` in the remainder; the tool removes it."""
    assert run_checked._clean(["--", "python", "-c", "x"]) == [
        "python",
        "-c",
        "x",
    ]


def test_artefact_paths(tmp_path: Path) -> None:
    """Exit and pid artefacts hang off the log path."""
    log = tmp_path / "run.log"

    assert run_checked._exit_path(log) == Path(f"{log}.exit")
    assert run_checked._pid_path(log) == Path(f"{log}.pid")


def test_read_pid_handles_missing_and_invalid(tmp_path: Path) -> None:
    """A missing or malformed pid file reads as zero."""
    log = tmp_path / "run.log"

    assert run_checked._read_pid(log) == 0
    Path(f"{log}.pid").write_text("nope", encoding="utf-8")
    assert run_checked._read_pid(log) == 0


def test_read_pid_reads_a_number(tmp_path: Path) -> None:
    """A recorded pid is returned as an integer."""
    log = tmp_path / "run.log"
    Path(f"{log}.pid").write_text("4321", encoding="utf-8")

    assert run_checked._read_pid(log) == 4321


def test_read_exit_handles_bad_files(tmp_path: Path) -> None:
    """Missing or malformed exit files read as failure."""
    path = tmp_path / "run.log.exit"

    assert run_checked._read_exit(path) == 1
    path.write_text("garbage", encoding="utf-8")
    assert run_checked._read_exit(path) == 1
    path.write_text("EXIT_CODE=7", encoding="utf-8")
    assert run_checked._read_exit(path) == 7


def test_print_tail_is_bounded(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Only the requested number of trailing lines is printed."""
    log = tmp_path / "run.log"
    log.write_text("one\ntwo\nthree\n", encoding="utf-8")

    run_checked._print_tail(log, 2)
    assert capsys.readouterr().out == "two\nthree\n"


def test_print_tail_ignores_absent_and_empty_logs(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Missing and empty logs produce no output."""
    run_checked._print_tail(tmp_path / "absent.log", 5)
    empty = tmp_path / "empty.log"
    empty.write_text("", encoding="utf-8")
    run_checked._print_tail(empty, 5)

    assert capsys.readouterr().out == ""


def test_process_alive_rejects_non_positive_pids() -> None:
    """Zero and negative pids are never alive."""
    assert processes.is_alive(0) is False
    assert processes.is_alive(-1) is False


def test_process_alive_posix(monkeypatch: pytest.MonkeyPatch) -> None:
    """The POSIX probe treats a successful signal as alive."""
    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    monkeypatch.setattr(processes.os, "kill", lambda pid, sig: None)

    assert processes.is_alive(10) is True


def test_process_alive_posix_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    """A vanished process is not alive."""

    def missing(pid: int, sig: int) -> None:
        raise ProcessLookupError

    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    monkeypatch.setattr(processes.os, "kill", missing)

    assert processes.is_alive(10) is False


def test_process_alive_posix_denied(monkeypatch: pytest.MonkeyPatch) -> None:
    """A process we may not signal is assumed alive."""

    def denied(pid: int, sig: int) -> None:
        raise PermissionError

    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    monkeypatch.setattr(processes.os, "kill", denied)

    assert processes.is_alive(10) is True


def test_process_alive_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """The Windows probe delegates to the kernel32 helper."""
    monkeypatch.setattr(processes, "IS_WINDOWS", True)
    monkeypatch.setattr(processes, "_is_alive_windows", lambda pid: True)

    assert processes.is_alive(10) is True


def test_is_alive_windows_waits(monkeypatch: pytest.MonkeyPatch) -> None:
    """A handle that times out means the process is still running."""
    kernel = FakeKernel(handle=99, wait_result=0x00000102)
    monkeypatch.setattr(
        ctypes, "WinDLL", lambda *args, **kwargs: kernel, raising=False
    )

    assert processes._is_alive_windows(10) is True
    assert kernel.closed == 99


def test_is_alive_windows_exited(monkeypatch: pytest.MonkeyPatch) -> None:
    """A signalled handle means the process has exited."""
    kernel = FakeKernel(handle=99, wait_result=0)
    monkeypatch.setattr(
        ctypes, "WinDLL", lambda *args, **kwargs: kernel, raising=False
    )

    assert processes._is_alive_windows(10) is False


def test_is_alive_windows_missing_handle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed OpenProcess means the process is gone."""
    kernel = FakeKernel(handle=0, wait_result=0)
    monkeypatch.setattr(
        ctypes, "WinDLL", lambda *args, **kwargs: kernel, raising=False
    )

    assert processes._is_alive_windows(10) is False


def test_kill_tree_ignores_non_positive_pids() -> None:
    """Nothing is killed for an absent pid."""
    processes.kill_tree(0)


def test_kill_tree_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """Windows uses taskkill for the whole tree."""
    seen = {}
    monkeypatch.setattr(processes, "IS_WINDOWS", True)
    monkeypatch.setattr(
        subprocess,
        "call",
        lambda command, **kwargs: seen.setdefault("command", command),
    )

    processes.kill_tree(55)

    assert seen["command"][:3] == ["taskkill", "/PID", "55"]


def test_kill_tree_posix(monkeypatch: pytest.MonkeyPatch) -> None:
    """POSIX signals the whole process group."""
    seen = {}
    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    monkeypatch.setattr(processes.os, "getpgid", lambda pid: 7, raising=False)
    monkeypatch.setattr(
        processes.os,
        "killpg",
        lambda group, sig: seen.setdefault("group", group),
        raising=False,
    )

    processes.kill_tree(55)

    assert seen["group"] == 7


def test_kill_tree_posix_missing_group(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A vanished group is ignored."""

    def missing(pid: int) -> int:
        raise ProcessLookupError

    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    monkeypatch.setattr(processes.os, "getpgid", missing, raising=False)

    processes.kill_tree(55)


def test_windows_flags_detach_from_the_console() -> None:
    """The Windows flags include console and job detachment."""
    flags = processes.windows_flags()

    assert isinstance(flags, int)
    assert flags >= 0
    assert processes.windows_flags(False) <= flags


def test_spawn_uses_a_posix_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """POSIX starts the child in a new session."""
    seen = {}

    def fake_popen(command, **kwargs):
        seen.update(kwargs)
        return object()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    monkeypatch.setattr(processes, "IS_WINDOWS", False)
    with (tmp_path / "out").open("wb") as handle:
        processes.spawn(["python"], handle)

    assert seen["start_new_session"] is True
    assert "creationflags" not in seen


def test_popen_passes_creation_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The Windows helper forwards its creation flags."""
    seen = {}

    def fake_popen(command, **kwargs):
        seen.update(kwargs)
        return object()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    with (tmp_path / "out").open("wb") as handle:
        processes._popen(["python"], handle, 8)

    assert seen["creationflags"] == 8


def test_spawn_uses_the_windows_helper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On Windows, spawning delegates with the requested breakaway flag."""
    seen = {}

    def fake_process(command, handle, breakaway):
        seen["breakaway"] = breakaway
        return object()

    monkeypatch.setattr(processes, "IS_WINDOWS", True)
    monkeypatch.setattr(processes, "_windows_process", fake_process)
    with (tmp_path / "out").open("wb") as handle:
        processes.spawn(["python"], handle, True)

    assert seen["breakaway"] is True


def test_windows_spawn_falls_back_without_breakaway(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A job that forbids breakaway still starts the supervisor."""
    calls = []
    sentinel = object()

    def fake_popen(command, handle, flags):
        calls.append(flags)
        if len(calls) == 1:
            raise PermissionError("breakaway denied")
        return sentinel

    monkeypatch.setattr(processes, "_popen", fake_popen)
    with (tmp_path / "out").open("wb") as handle:
        result = processes._windows_process(["python"], handle, True)

    assert result is sentinel
    assert calls == [
        processes.windows_flags(True),
        processes.windows_flags(False),
    ]


def test_windows_spawn_without_breakaway_propagates_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Children never request breakaway, so they never retry."""

    def fake_popen(command, handle, flags):
        raise PermissionError("denied")

    monkeypatch.setattr(processes, "_popen", fake_popen)
    with (tmp_path / "out").open("wb") as handle:
        with pytest.raises(PermissionError):
            processes._windows_process(["python"], handle, False)


def test_spawn_detached_redirects_diagnostics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The supervisor's sidecar file is created and closed."""

    def fake_spawn(command, handle, breakaway=False):
        return "spawned"

    monkeypatch.setattr(processes, "spawn", fake_spawn)
    result = run_checked._spawn_detached(["python"], tmp_path / "log")

    assert result == "spawned"
    assert (tmp_path / "log.supervisor").is_file()


def test_supervisor_command_bootstraps_the_module(tmp_path: Path) -> None:
    """The supervisor is started with an importable bootstrap program."""
    command = run_checked._supervisor_command(
        tmp_path / "log", 5.0, ["python"]
    )

    assert command[:2] == [sys.executable, "-c"]
    assert "run_checked" in command[2]
    assert command[-2:] == ["--", "python"]
    assert "--timeout" in command


def test_bootstrap_code_names_the_package() -> None:
    """The bootstrap imports the module that is actually running."""
    code = run_checked._bootstrap_code()

    assert "from causaliq.devtools.run_checked import main" in code
    assert "sys.exit(main())" in code


def test_await_pid_returns_a_recorded_pid(tmp_path: Path) -> None:
    """A pid file that appears during the grace period is returned."""
    log = tmp_path / "log"
    Path(f"{log}.pid").write_text("123", encoding="utf-8")

    assert run_checked._await_pid(log) == 123


def test_await_pid_returns_zero_when_the_run_finished(tmp_path: Path) -> None:
    """An exit artefact means there is no supervisor left to wait for."""
    log = tmp_path / "log"
    Path(f"{log}.exit").write_text("EXIT_CODE=0", encoding="utf-8")

    assert run_checked._await_pid(log) == 0


def test_await_pid_gives_up_after_the_grace_period(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A supervisor that never writes a pid is not waited for forever."""
    monkeypatch.setattr(run_checked, "STARTUP_SECONDS", 0.3)

    assert run_checked._await_pid(tmp_path / "log") == 0


def test_has_timed_out_handles_absent_and_past_deadlines() -> None:
    """No deadline never times out; a past deadline always does."""
    assert run_checked._has_timed_out(None) is False
    assert run_checked._has_timed_out(0.0) is True


def test_wait_reports_missing_exit_when_child_is_gone(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """A vanished child without an exit artefact reads as failure."""
    log = tmp_path / "log"
    Path(f"{log}.pid").write_text("999999", encoding="utf-8")
    options = argparse.Namespace(log=str(log), timeout=1.0, tail=5, wait=True)
    monkeypatch.setattr(processes, "is_alive", lambda pid: False)

    assert run_checked._wait(options) == 1
    assert "EXIT_CODE=1" in capsys.readouterr().out
