"""Unit tests for environment paths, interpreters and command builders."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools import devenv_env
from causaliq.devtools.devenv_env import (
    DevenvError,
    create_command,
    environment,
    install_command,
    launcher,
    run,
    smoke_command,
)
from causaliq.devtools.devenv_repos import Repo

pytestmark = pytest.mark.unit


def make_repo(tmp_path: Path, name: str = "causaliq-core") -> Repo:
    """Return a repository fixture with two requested extras."""
    return Repo(name, name.replace("-", "_"), tmp_path / name, ("dev", "test"))


def test_environment_uses_the_venv_key(tmp_path: Path) -> None:
    """Environments live under venv/ with a compact version key."""
    env = environment(tmp_path, "3.14")

    assert env.target == tmp_path / "venv" / "py314"
    assert env.version == "3.14"


def test_environment_python_on_windows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Windows keeps the interpreter in Scripts."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", True)

    env = environment(tmp_path, "3.12")

    assert env.python == env.target / "Scripts" / "python.exe"


def test_environment_python_on_posix(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """POSIX keeps the interpreter in bin."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", False)

    env = environment(tmp_path, "3.12")

    assert env.python == env.target / "bin" / "python"


def test_launcher_uses_py_on_windows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Windows uses the launcher so several versions can coexist."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", True)

    assert launcher("3.12") == ("py", "-3.12")


def test_launcher_prefers_the_versioned_posix_python(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A versioned POSIX interpreter is preferred when it exists."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", False)
    monkeypatch.setattr(
        devenv_env.shutil, "which", lambda name: "/usr/bin/python"
    )

    assert launcher("3.12") == ("python3.12",)


def test_launcher_falls_back_to_python3(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without a versioned name the generic interpreter is used."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", False)
    monkeypatch.setattr(
        devenv_env.shutil, "which", lambda name: name == "python3"
    )

    assert launcher("3.12") == ("python3",)


def test_launcher_reports_a_missing_interpreter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A POSIX host without any interpreter fails loudly."""
    monkeypatch.setattr(devenv_env, "IS_WINDOWS", False)
    monkeypatch.setattr(devenv_env.shutil, "which", lambda name: None)

    with pytest.raises(DevenvError, match="not available"):
        launcher("3.12")


def test_launcher_honours_the_interpreter_override() -> None:
    """``--interpreter`` replaces the platform lookup."""
    assert launcher("3.12", "C:/python/python.exe") == (
        "C:/python/python.exe",
    )


def test_create_command_builds_a_venv(tmp_path: Path) -> None:
    """The create command passes the target directory last."""
    env = environment(tmp_path, "3.12")

    command = create_command(env, "C:/python/python.exe", False)

    assert command == (
        "C:/python/python.exe",
        "-m",
        "venv",
        str(env.target),
    )


def test_create_command_can_clear(tmp_path: Path) -> None:
    """Recreating asks venv to empty the directory first."""
    env = environment(tmp_path, "3.14")

    command = create_command(env, "py", True)

    assert "--clear" in command
    assert command[-1] == str(env.target)


def test_install_command_repeats_editable(tmp_path: Path) -> None:
    """One pip resolve installs every package editable."""
    env = environment(tmp_path, "3.12")
    repos = [
        make_repo(tmp_path, "causaliq-core"),
        make_repo(tmp_path, "causaliq-data"),
    ]

    command = install_command(env, repos)

    assert command[:5] == (str(env.python), "-m", "pip", "install", "-e")
    assert command[5].endswith("[dev,test]")
    assert command[6] == "-e"


def test_smoke_command_imports_the_package(tmp_path: Path) -> None:
    """The smoke test imports the package and prints its location."""
    env = environment(tmp_path, "3.12")

    command = smoke_command(env, make_repo(tmp_path))

    assert "import causaliq_core" in command[-1]
    assert "__file__" in command[-1]


def test_run_prints_and_skips_in_dry_run(
    capsys: pytest.CaptureFixture,
) -> None:
    """Dry-run shows the command without running it."""
    assert run(("python", "-c", "pass"), True) == 0
    assert "python -c pass" in capsys.readouterr().out


def test_run_returns_the_child_exit_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The child exit code is passed through."""
    seen: list[tuple[str, ...]] = []

    def fake_call(command: list[str]) -> int:
        seen.append(tuple(command))
        return 3

    monkeypatch.setattr(devenv_env.subprocess, "call", fake_call)

    assert run(("tool", "--flag"), False) == 3
    assert seen == [("tool", "--flag")]


def test_run_reports_a_missing_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """A launcher that is not installed is reported, not raised."""

    def fail(command: list[str]) -> int:
        raise FileNotFoundError("no such command")

    monkeypatch.setattr(devenv_env.subprocess, "call", fail)

    assert run(("missing",), False) == 1
    assert "no such command" in capsys.readouterr().out
