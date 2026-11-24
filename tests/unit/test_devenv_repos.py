"""Unit tests for discovering sibling CausalIQ repositories."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools.config import CausaliqConfig
from causaliq.devtools.devenv_repos import (
    discover,
    select_extras,
    umbrella_root,
)

pytestmark = pytest.mark.unit


def write_repo(root: Path, name: str, extras: str = '["dev", "test"]') -> Path:
    """Create a sibling repository that declares the configuration block."""
    path = root / name
    path.mkdir(parents=True)
    block = (
        '[project]\nname = "demo"\n\n[tool.causaliq]\n'
        f'distribution = "{name}"\n'
        f'package = "{name.replace("-", "_")}"\n'
        f"dev_extras = {extras}\n"
    )
    (path / "pyproject.toml").write_text(block, encoding="utf-8")
    return path


def test_discover_returns_sorted_repositories(tmp_path: Path) -> None:
    """Siblings are discovered in a stable order."""
    write_repo(tmp_path, "causaliq-data")
    write_repo(tmp_path, "causaliq-core")

    repos = discover(tmp_path, ("dev", "test"))

    assert [repo.distribution for repo in repos] == [
        "causaliq-core",
        "causaliq-data",
    ]


def test_package_name_uses_the_import_name(tmp_path: Path) -> None:
    """The result carries the import name and the absolute path."""
    path = write_repo(tmp_path, "causaliq-core")

    repo = discover(tmp_path, ("dev",))[0]

    assert repo.package == "causaliq_core"
    assert repo.path == path.resolve()


def test_directories_without_the_section_are_skipped(
    tmp_path: Path,
) -> None:
    """A pyproject without the configuration block is not a repository."""
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    (legacy / "pyproject.toml").write_text(
        '[project]\nname = "legacy"\n', encoding="utf-8"
    )

    assert discover(tmp_path, ("dev",)) == []


def test_directories_without_a_manifest_are_skipped(
    tmp_path: Path,
) -> None:
    """A directory without pyproject.toml is ignored."""
    (tmp_path / "notes").mkdir()

    assert discover(tmp_path, ("dev",)) == []


def test_template_directories_are_skipped(tmp_path: Path) -> None:
    """The repository template is a scaffold, not a package."""
    write_repo(tmp_path, "causaliq-repo-template")

    assert discover(tmp_path, ("dev",)) == []


def test_extras_are_intersected(tmp_path: Path) -> None:
    """Only extras the package declares are requested from pip."""
    write_repo(tmp_path, "causaliq", extras='["dev"]')

    repo = discover(tmp_path, ("dev", "test", "docs"))[0]

    assert repo.extras == ("dev",)


def test_requirement_lists_the_extras(tmp_path: Path) -> None:
    """The editable requirement names the path and the extras."""
    write_repo(tmp_path, "causaliq-core")

    repo = discover(tmp_path, ("dev", "test"))[0]

    assert repo.requirement.endswith("[dev,test]")
    assert repo.requirement.startswith(repo.path.as_posix())


def test_requirement_without_extras(tmp_path: Path) -> None:
    """A package without extras is installed without brackets."""
    write_repo(tmp_path, "causaliq-core", extras="[]")

    repo = discover(tmp_path, ("dev",))[0]

    assert repo.requirement == repo.path.as_posix()


def test_select_extras_keeps_the_requested_order() -> None:
    """Requested extras are filtered by the declared list."""
    config = CausaliqConfig(
        distribution="demo",
        package="demo",
        python_versions=("3.12",),
        default_python="3.12",
        dev_extras=("dev", "docs"),
        testpaths=("tests",),
        fast_testpaths=("tests",),
    )

    assert select_extras(config, ("test", "docs", "dev")) == (
        "docs",
        "dev",
    )


def test_overrides_replace_a_discovered_entry(tmp_path: Path) -> None:
    """``--repo`` points a distribution at another checkout."""
    write_repo(tmp_path, "causaliq-core")
    other = write_repo(tmp_path, "causaliq-core-work", extras='["dev"]')

    repos = discover(tmp_path, ("dev",), {"causaliq-core": other})

    paths = {repo.distribution: repo.path for repo in repos}
    assert paths["causaliq-core"] == other.resolve()


def test_overrides_add_an_unknown_entry(tmp_path: Path) -> None:
    """An override may name a distribution discovery did not find."""
    write_repo(tmp_path, "causaliq-core")
    extra = write_repo(tmp_path, "elsewhere", extras='["dev"]')

    repos = discover(tmp_path, ("dev",), {"other": extra})

    paths = {repo.distribution: repo.path for repo in repos}
    assert paths["other"] == extra.resolve()
    assert "causaliq-core" in paths


def test_umbrella_root_is_this_checkout() -> None:
    """The umbrella root contains the canonical devtools package."""
    root = umbrella_root()

    assert (root / "pyproject.toml").is_file()
    assert (root / "src" / "causaliq" / "devtools").is_dir()
