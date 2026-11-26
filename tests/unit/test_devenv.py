"""Unit tests for the shared-environment command and orchestration."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools import devenv
from causaliq.devtools.config import ConfigError, SharedConfig
from causaliq.devtools.devenv import Options
from causaliq.devtools.devenv_env import DevenvError, Environment
from causaliq.devtools.devenv_repos import Repo

pytestmark = pytest.mark.unit


def make_repo(tmp_path: Path, name: str = "causaliq-core") -> Repo:
    """Return a repository fixture for the temporary tree."""
    return Repo(name, name.replace("-", "_"), tmp_path / name, ("dev", "test"))


def make_env(tmp_path: Path) -> Environment:
    """Return the 3.12 environment below a temporary root."""
    return Environment("3.12", tmp_path / "venv" / "py312")


def test_parse_defaults_to_empty_selections() -> None:
    """An empty command line selects nothing explicitly."""
    assert devenv._parse([]) == Options()


def test_parse_collects_repeated_versions() -> None:
    """``--python`` may be repeated."""
    options = devenv._parse(["--python", "3.12", "--python", "3.14"])

    assert options.python == ("3.12", "3.14")


def test_parse_splits_and_cleans_the_extras_list() -> None:
    """``--extras`` is a comma-separated list with empty items dropped."""
    options = devenv._parse(["--extras", "dev, test,"])

    assert options.extras == ("dev", "test")


def test_parse_reads_every_switch() -> None:
    """The boolean switches and the interpreter override are recorded."""
    options = devenv._parse(
        [
            "--install-only",
            "--recreate",
            "--check",
            "--dry-run",
            "--strict",
            "--interpreter",
            "C:/python/python.exe",
        ]
    )

    assert options.install_only is True
    assert options.recreate is True
    assert options.check is True
    assert options.dry_run is True
    assert options.strict is True
    assert options.interpreter == "C:/python/python.exe"


def test_parse_reads_repo_overrides() -> None:
    """``--repo`` accepts NAME=PATH and keeps the name."""
    options = devenv._parse(["--repo", "causaliq-core=../core"])

    name, path = options.repos[0]
    assert name == "causaliq-core"
    assert path == Path("../core")


@pytest.mark.parametrize("value", ["causaliq-core", "=path", "name="])
def test_parse_rejects_malformed_overrides(
    value: str, capsys: pytest.CaptureFixture
) -> None:
    """A malformed override is reported instead of silently ignored."""
    assert devenv.main(["--repo", value]) == 2
    assert "NAME=PATH" in capsys.readouterr().out


def test_run_rejects_an_empty_version_list(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A configuration without versions cannot build anything."""
    monkeypatch.setattr(devenv, "umbrella_root", lambda: tmp_path)
    monkeypatch.setattr(
        devenv, "load_shared", lambda root: SharedConfig((), ("dev",))
    )
    monkeypatch.setattr(devenv, "discover", lambda *args: [])

    with pytest.raises(DevenvError, match="no Python version"):
        devenv._run(Options())


def test_run_rejects_a_missing_repository(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Discovery that finds nothing is an error, not a success."""
    monkeypatch.setattr(devenv, "umbrella_root", lambda: tmp_path)
    monkeypatch.setattr(
        devenv,
        "load_shared",
        lambda root: SharedConfig(("3.12",), ("dev",)),
    )
    monkeypatch.setattr(devenv, "discover", lambda *args: [])

    with pytest.raises(DevenvError, match="no CausalIQ repository"):
        devenv._run(Options())


def test_run_requires_a_single_version_with_interpreter(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """One interpreter cannot serve two Python versions."""
    monkeypatch.setattr(devenv, "umbrella_root", lambda: tmp_path)
    monkeypatch.setattr(
        devenv,
        "load_shared",
        lambda root: SharedConfig(("3.12", "3.14"), ("dev",)),
    )
    monkeypatch.setattr(
        devenv, "discover", lambda *args: [make_repo(tmp_path)]
    )

    with pytest.raises(DevenvError, match="single --python version"):
        devenv._run(Options(interpreter="C:/python/python.exe"))


def test_run_uses_the_shared_settings_and_checks(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """``--check`` receives the configured versions, extras and strictness."""
    seen = {}

    def fake_discover(root: Path, extras: object, overrides: object) -> list:
        seen["extras"] = extras
        return [make_repo(tmp_path)]

    def fake_check(
        root: Path, versions: object, repos: object, strict: bool
    ) -> int:
        seen["check"] = (versions, strict)
        return 0

    monkeypatch.setattr(devenv, "umbrella_root", lambda: tmp_path)
    monkeypatch.setattr(
        devenv,
        "load_shared",
        lambda root: SharedConfig(("3.14",), ("test",)),
    )
    monkeypatch.setattr(devenv, "discover", fake_discover)
    monkeypatch.setattr(devenv, "check", fake_check)

    assert devenv._run(Options(check=True, strict=True)) == 0
    assert seen["extras"] == ("test",)
    assert seen["check"] == (("3.14",), True)


def test_build_reports_every_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Without strict mode every version is attempted."""
    seen: list[str] = []

    def fake_prepare(
        env: Environment, repos: object, options: Options
    ) -> bool:
        seen.append(env.version)
        return False

    monkeypatch.setattr(devenv, "_prepare", fake_prepare)

    code = devenv.build(tmp_path, ("3.12", "3.14"), [], Options())

    assert code == 1
    assert seen == ["3.12", "3.14"]


def test_build_stops_at_the_first_failure_in_strict_mode(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Strict mode abandons the run once a version fails."""
    seen: list[str] = []

    def fake_prepare(
        env: Environment, repos: object, options: Options
    ) -> bool:
        seen.append(env.version)
        return False

    monkeypatch.setattr(devenv, "_prepare", fake_prepare)

    code = devenv.build(tmp_path, ("3.12", "3.14"), [], Options(strict=True))

    assert code == 1
    assert seen == ["3.12"]


def test_build_succeeds_when_every_version_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A clean run returns zero."""
    monkeypatch.setattr(devenv, "_prepare", lambda *args: True)

    assert devenv.build(tmp_path, ("3.12",), [], Options()) == 0


def test_prepare_refuses_a_missing_environment_in_install_only_mode(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Install-only never skips a missing environment silently."""
    env = make_env(tmp_path)

    assert devenv._prepare(env, [], Options(install_only=True)) is False

    output = capsys.readouterr().out
    assert "is missing" in output
    assert "--install-only" in output


def test_prepare_reports_a_failed_create(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A missing interpreter names the launcher that lists versions."""
    monkeypatch.setattr(devenv, "run", lambda command, dry_run: 1)

    assert devenv._prepare(make_env(tmp_path), [], Options()) is False
    assert "py -0p" in capsys.readouterr().out


def test_prepare_reports_a_failed_install(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """A pip failure names the environment and stops the version."""
    env = make_env(tmp_path)
    env.target.mkdir(parents=True)
    monkeypatch.setattr(devenv, "run", lambda command, dry_run: 1)

    assert devenv._prepare(env, [], Options()) is False
    assert "pip install failed" in capsys.readouterr().out


def test_prepare_installs_and_smoke_tests(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A prepared environment runs one resolve then one import per package."""
    env = make_env(tmp_path)
    env.target.mkdir(parents=True)
    commands: list[tuple] = []

    def fake_run(command: tuple, dry_run: bool) -> int:
        commands.append(command)
        return 0

    monkeypatch.setattr(devenv, "run", fake_run)

    repos = [make_repo(tmp_path)]

    assert devenv._prepare(env, repos, Options()) is True
    assert "pip" in commands[0]
    assert "import causaliq_core" in commands[1][-1]


def test_smoke_reports_a_failing_package(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
) -> None:
    """An import failure names the package."""
    monkeypatch.setattr(devenv, "run", lambda command, dry_run: 1)

    assert devenv._smoke(make_env(tmp_path), [], Options()) is True
    assert (
        devenv._smoke(make_env(tmp_path), [make_repo(tmp_path)], Options())
        is False
    )
    assert "does not import" in capsys.readouterr().out


def test_should_create_only_when_missing_or_recreating(
    tmp_path: Path,
) -> None:
    """An existing environment is kept unless ``--recreate`` is given."""
    env = make_env(tmp_path)
    env.target.mkdir(parents=True)

    assert devenv._should_create(env, Options()) is False
    assert devenv._should_create(env, Options(recreate=True)) is True


def test_main_reports_a_configuration_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """A broken pyproject is reported with exit code two."""

    def fail(root: Path) -> SharedConfig:
        raise ConfigError("broken configuration")

    monkeypatch.setattr(devenv, "load_shared", fail)

    assert devenv.main([]) == 2
    assert "broken configuration" in capsys.readouterr().out
