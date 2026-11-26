"""Functional tests for verifying and refreshing generated scripts."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from causaliq.devtools import sync

pytestmark = pytest.mark.functional

CONFIG = """
[tool.causaliq]
distribution = "causaliq-demo"
package = "causaliq_demo"
python_versions = ["3.10", "3.12"]
default_python = "3.12"
dev_extras = ["dev"]
testpaths = ["tests/unit"]
"""


def make_target(root: Path) -> Path:
    """Create a package with a gate configuration."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n' + CONFIG, encoding="utf-8"
    )
    return root


def make_source(root: Path) -> Path:
    """Create a fake umbrella checkout with a devtools package."""
    source = root / "umbrella"
    devtools = source / "src" / "causaliq" / "devtools"
    devtools.mkdir(parents=True)
    (devtools / "__init__.py").write_text('"""Fake devtools."""\n')
    (devtools / "gate.py").write_text("def main():\n    return 0\n")
    return source


def test_update_writes_files_and_manifest(tmp_path: Path) -> None:
    """Updating renders every script and records its hash."""
    target = make_target(tmp_path / "target")
    source = make_source(tmp_path)

    assert sync.update(target, source, "causaliq@abc123") == 0

    entry = target / "scripts" / "check_ci.py"
    assert entry.is_file()
    assert entry.read_text(encoding="utf-8").startswith(
        "# generated from causaliq@abc123"
    )
    assert (target / "scripts" / "activate.ps1").is_file()
    assert (target / "scripts" / "build-and-publish.ps1").is_file()
    manifest = json.loads(
        (target / "scripts" / "generated.json").read_text(encoding="utf-8")
    )
    assert manifest["source"] == "causaliq@abc123"
    assert "scripts/gate.py" not in manifest["files"]
    assert "scripts/_vendor/causaliq_devtools/gate.py" in manifest["files"]


def test_check_passes_for_a_fresh_update(tmp_path: Path) -> None:
    """A freshly generated tree matches its manifest."""
    target = make_target(tmp_path / "target")
    sync.update(target, make_source(tmp_path), "causaliq@abc123")

    assert sync.check(target) == 0


def test_check_detects_a_hand_edit(tmp_path: Path) -> None:
    """Editing a generated file is reported."""
    target = make_target(tmp_path / "target")
    sync.update(target, make_source(tmp_path), "causaliq@abc123")
    entry = target / "scripts" / "check_ci.py"
    entry.write_text(
        entry.read_text(encoding="utf-8") + "# hand edit\n",
        encoding="utf-8",
    )

    assert sync.check(target) == 1


def test_check_detects_a_missing_file(tmp_path: Path) -> None:
    """Deleting a generated file is reported."""
    target = make_target(tmp_path / "target")
    sync.update(target, make_source(tmp_path), "causaliq@abc123")
    (target / "scripts" / "sync.py").unlink()

    assert sync.check(target) == 1


def test_check_requires_a_manifest(tmp_path: Path) -> None:
    """A package without a manifest is not silently accepted."""
    target = make_target(tmp_path / "target")

    assert sync.check(target) == 1


def test_invalid_manifests_are_rejected(tmp_path: Path) -> None:
    """Malformed JSON and a non-object files value both fail."""
    target = make_target(tmp_path / "target")
    scripts = target / "scripts"
    scripts.mkdir()
    manifest = scripts / "generated.json"
    manifest.write_text("not json", encoding="utf-8")
    assert sync.check(target) == 1

    manifest.write_text('{"files": []}', encoding="utf-8")
    assert sync.check(target) == 1


def test_update_requires_a_source_package(tmp_path: Path) -> None:
    """A source without devtools is a hard error."""
    target = make_target(tmp_path / "target")
    with pytest.raises(SystemExit, match="no devtools package"):
        sync.update(target, tmp_path / "absent", "causaliq@abc")


def test_main_defaults_to_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The default action is a read-only check."""
    target = make_target(tmp_path / "target")
    sync.update(target, make_source(tmp_path), "causaliq@abc123")
    monkeypatch.chdir(target)

    assert sync.main([]) == 0


def test_main_update_requires_source(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Updating without a source is a usage error."""
    target = make_target(tmp_path / "target")

    assert sync.main(["--update", "--target", str(target)]) == 2
    assert "--source" in capsys.readouterr().out


def test_main_rejects_check_and_update(
    tmp_path: Path,
) -> None:
    """The two modes are mutually exclusive."""
    with pytest.raises(SystemExit):
        sync.main(["--check", "--update"])


def test_main_update_with_source(tmp_path: Path) -> None:
    """The CLI can refresh a package from a source checkout."""
    target = make_target(tmp_path / "target")
    source = make_source(tmp_path)

    code = sync.main(
        [
            "--update",
            "--source",
            str(source),
            "--target",
            str(target),
            "--ref",
            "causaliq@abc",
        ]
    )

    assert code == 0
    assert (target / "scripts" / "check_ci.py").is_file()


def test_bootstrap_update_writes_only_the_wrappers(tmp_path: Path) -> None:
    """Bootstrap mode skips entry points and the vendored package."""
    target = make_target(tmp_path / "target")
    source = make_source(tmp_path)

    code = sync.main(
        [
            "--update",
            "--bootstrap",
            "--source",
            str(source),
            "--target",
            str(target),
            "--ref",
            "causaliq@abc",
        ]
    )

    scripts = target / "scripts"
    assert code == 0
    assert (scripts / "activate.ps1").is_file()
    assert (scripts / "setup-env.ps1").is_file()
    assert (scripts / "check_ci.ps1").is_file()
    assert not (scripts / "check_ci.py").exists()
    assert not (scripts / "_vendor").exists()
    assert sync.check(target) == 0


def test_non_object_manifest_is_rejected(tmp_path: Path) -> None:
    """A manifest whose top level is not an object is invalid."""
    target = make_target(tmp_path / "target")
    scripts = target / "scripts"
    scripts.mkdir()
    (scripts / "generated.json").write_text("[]", encoding="utf-8")

    assert sync.check(target) == 1


def test_git_returns_stripped_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Git output is stripped before it is used as a reference."""
    monkeypatch.setattr(
        sync.subprocess,
        "check_output",
        lambda command, **kwargs: " abcdef \n",
    )

    assert sync._git(tmp_path, "rev-parse", "HEAD") == "abcdef"


def test_source_ref_reads_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A clean checkout is pinned to its commit."""

    def fake_git(path: Path, *args: str) -> str:
        return "abcdef123456" if args[0] == "rev-parse" else ""

    monkeypatch.setattr(sync, "_git", fake_git)
    assert sync.source_ref(tmp_path) == "causaliq@abcdef123456"


def test_source_ref_marks_a_dirty_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Uncommitted source changes are visible in the provenance."""
    answers = iter(["abcdef123456", " M file.py"])

    monkeypatch.setattr(sync, "_git", lambda path, *args: next(answers))

    assert sync.source_ref(tmp_path) == "causaliq@abcdef123456-dirty"
    assert "uncommitted changes" in capsys.readouterr().out


def test_source_ref_without_git(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A source that is not a git checkout is still usable."""

    def fail(path: Path, *args: str) -> str:
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr(sync, "_git", fail)

    assert sync.source_ref(tmp_path) == "causaliq@unknown"


def test_bootstrap_update_writes_the_dev_env_entry_point(
    tmp_path: Path,
) -> None:
    """Bootstrap mode adds the shared-environment entry point."""
    target = make_target(tmp_path / "target")
    source = make_source(tmp_path)

    code = sync.main(
        [
            "--update",
            "--bootstrap",
            "--source",
            str(source),
            "--target",
            str(target),
            "--ref",
            "causaliq@abc",
        ]
    )

    entry = target / "scripts" / "setup_dev_env.py"
    assert code == 0
    assert entry.is_file()
    assert "causaliq.devtools.devenv" in entry.read_text(encoding="utf-8")


def test_package_update_omits_the_dev_env_entry_point(
    tmp_path: Path,
) -> None:
    """Packages never receive a script that installs their siblings."""
    target = make_target(tmp_path / "target")
    sync.update(target, make_source(tmp_path), "causaliq@abc")

    assert not (target / "scripts" / "setup_dev_env.py").exists()


def test_dev_env_modules_are_not_vendored(tmp_path: Path) -> None:
    """Umbrella-only tooling is excluded from the vendored copy."""
    target = make_target(tmp_path / "target")
    source = make_source(tmp_path)
    devtools = source / "src" / "causaliq" / "devtools"
    (devtools / "devenv.py").write_text("def main():\n    return 0\n")
    (devtools / "devenv_env.py").write_text("VALUE = 1\n")

    sync.update(target, source, "causaliq@abc")

    vendor = target / "scripts" / "_vendor" / "causaliq_devtools"
    assert (vendor / "gate.py").is_file()
    assert not (vendor / "devenv.py").exists()
    assert not (vendor / "devenv_env.py").exists()
