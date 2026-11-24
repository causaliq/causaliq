"""Functional tests for the shared-environment command.

The trees are temporary directories: discovery, command planning and the
``--check`` reporting are exercised without creating an environment or
contacting an index. Only the probe helper runs a real process.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional, Sequence

import pytest

from causaliq.devtools import devenv, devenv_check
from causaliq.devtools.devenv_env import environment

pytestmark = pytest.mark.functional

UMBRELLA = """
[project]
name = "causaliq"

[tool.causaliq]
distribution = "causaliq"
package = "causaliq"
dev_extras = ["dev"]
shared_python_versions = ["3.12", "3.14"]
shared_extras = ["dev", "test"]
"""

SIBLING = """
[project]
name = "{name}"

[tool.causaliq]
distribution = "{name}"
package = "{package}"
dev_extras = ["dev", "test"]
"""


def make_tree(root: Path) -> Path:
    """Create an umbrella with two sibling packages beside it."""
    umbrella = root / "causaliq"
    umbrella.mkdir(parents=True)
    (umbrella / "pyproject.toml").write_text(UMBRELLA, encoding="utf-8")
    for name in ("causaliq-core", "causaliq-data"):
        path = root / name
        path.mkdir()
        text = SIBLING.format(name=name, package=name.replace("-", "_"))
        (path / "pyproject.toml").write_text(text, encoding="utf-8")
    return umbrella


def use_tree(monkeypatch: pytest.MonkeyPatch, umbrella: Path) -> None:
    """Point the command at a temporary umbrella checkout."""
    monkeypatch.setattr(devenv, "umbrella_root", lambda: umbrella)


def make_environment(root: Path, version: str) -> Path:
    """Create the directory and interpreter of an environment."""
    env = environment(root, version)
    env.python.parent.mkdir(parents=True)
    env.python.write_text("", encoding="utf-8")
    return env.target


def stub_probe(version: str, root: Path, failure: Optional[str] = None):
    """Return a probe stub that answers the version and package probes."""

    def probe(command: Sequence[str]) -> "subprocess.CompletedProcess[str]":
        script = command[-1]
        if "sys.version_info" in script:
            return subprocess.CompletedProcess(list(command), 0, version, "")
        if failure is not None:
            done = subprocess.CompletedProcess(list(command), 1, "", failure)
            return done
        folder = script.split()[1].replace("_", "-")
        located = str(root / folder / "__init__.py")
        return subprocess.CompletedProcess(list(command), 0, located, "")

    return probe


def test_dry_run_plans_both_environments(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Both environments are planned and nothing is created."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--dry-run"]) == 0

    output = capsys.readouterr().out
    assert "py312" in output
    assert "py314" in output
    assert "pip" in output
    assert "import causaliq_data" in output
    assert not (umbrella / "venv").exists()


def test_dry_run_honours_the_version_selection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """``--python`` narrows the run to one environment."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--dry-run", "--python", "3.14"]) == 0

    output = capsys.readouterr().out
    assert "py314" in output
    assert "py312" not in output


def test_dry_run_honours_the_extras_selection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """``--extras`` is intersected with the declared extras."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--dry-run", "--extras", "dev"]) == 0

    output = capsys.readouterr().out
    assert "[dev]" in output
    assert "[dev,test]" not in output


def test_recreate_asks_venv_to_clear(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """``--recreate`` clears the managed environment only."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--dry-run", "--recreate", "--python", "3.12"]) == 0

    assert "--clear" in capsys.readouterr().out


def test_install_only_reports_missing_environments(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Install-only names what is missing instead of skipping quietly."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--install-only"]) == 1

    output = capsys.readouterr().out
    assert "is missing" in output
    assert "--install-only" in output
    assert not (umbrella / "venv").exists()


def test_repo_override_installs_another_checkout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """``--repo`` replaces the discovered path for a distribution."""
    umbrella = make_tree(tmp_path)
    other = tmp_path / "elsewhere"
    other.mkdir()
    (other / "pyproject.toml").write_text(
        SIBLING.format(name="causaliq-core", package="causaliq_core"),
        encoding="utf-8",
    )
    use_tree(monkeypatch, umbrella)

    code = devenv.main(
        [
            "--dry-run",
            "--python",
            "3.12",
            "--repo",
            f"causaliq-core={other}",
        ]
    )

    assert code == 0
    assert other.as_posix() in capsys.readouterr().out


def test_check_reports_a_missing_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A missing environment is reported and fails the check."""
    umbrella = make_tree(tmp_path)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--check", "--python", "3.14"]) == 1

    assert "is missing" in capsys.readouterr().out


def test_check_reports_complete_environments(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """Every package importing is a complete environment."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)
    monkeypatch.setattr(devenv_check, "_probe", stub_probe("3.12", tmp_path))

    assert devenv.main(["--check", "--python", "3.12"]) == 0

    output = capsys.readouterr().out
    assert "interpreter Python 3.12" in output
    assert "causaliq-core: ok" in output
    assert "causaliq-data: ok" in output


def test_check_reports_a_version_mismatch(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """An environment built by the wrong interpreter is a problem."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)
    monkeypatch.setattr(devenv_check, "_probe", stub_probe("3.11", tmp_path))

    assert devenv.main(["--check", "--python", "3.12"]) == 1
    assert "wants 3.12" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("stderr", "expected"),
    [("", "import failed"), ("ModuleNotFoundError: nope", "nope")],
)
def test_check_reports_a_failed_import(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    stderr: str,
    expected: str,
) -> None:
    """A package that does not import is named with its error."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)
    monkeypatch.setattr(
        devenv_check, "_probe", stub_probe("3.12", tmp_path, stderr)
    )

    assert devenv.main(["--check", "--python", "3.12"]) == 1
    assert expected in capsys.readouterr().out


def test_check_strict_requires_the_sibling_checkout(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A package resolved outside its own checkout fails strict mode."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)
    monkeypatch.setattr(
        devenv_check, "_probe", stub_probe("3.12", tmp_path / "site")
    )

    assert devenv.main(["--check", "--strict", "--python", "3.12"]) == 1
    assert "resolved outside" in capsys.readouterr().out


def test_check_probe_reads_a_real_process() -> None:
    """The probe helper captures the output of a real command."""
    completed = devenv_check._probe((sys.executable, "-c", "print('ok')"))

    assert completed.stdout.strip() == "ok"


def test_check_strict_reports_an_empty_location(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """An import that prints no location cannot be proven local."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)

    def probe(command: Sequence[str]) -> "subprocess.CompletedProcess[str]":
        if "sys.version_info" in command[-1]:
            return subprocess.CompletedProcess(list(command), 0, "3.12", "")
        return subprocess.CompletedProcess(list(command), 0, "  ", "")

    monkeypatch.setattr(devenv_check, "_probe", probe)

    assert devenv.main(["--check", "--strict", "--python", "3.12"]) == 1
    assert "resolved outside" in capsys.readouterr().out


def test_empty_environment_path_is_reported(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """An environment without an interpreter is reported as missing."""
    umbrella = make_tree(tmp_path)
    environment(umbrella, "3.12").target.mkdir(parents=True)
    use_tree(monkeypatch, umbrella)

    assert devenv.main(["--check", "--python", "3.12"]) == 1
    assert "is missing" in capsys.readouterr().out


def test_missing_interpreter_output_is_reported(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """An interpreter that cannot report a version is a problem."""
    umbrella = make_tree(tmp_path)
    make_environment(umbrella, "3.12")
    use_tree(monkeypatch, umbrella)
    monkeypatch.setattr(
        devenv_check,
        "_probe",
        lambda command: subprocess.CompletedProcess(list(command), 1, "", ""),
    )

    assert devenv.main(["--check", "--python", "3.12"]) == 1
    assert "unknown, wants 3.12" in capsys.readouterr().out
