"""Functional tests for reading ``[tool.causaliq]`` from pyproject.toml."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools.config import (
    ConfigError,
    build_config,
    build_shared,
    find_pyproject,
    load_config,
    load_shared,
    read_section,
)

pytestmark = pytest.mark.functional

BLOCK = """
[tool.causaliq]
distribution = "causaliq-demo"
package = "causaliq_demo"
python_versions = ["3.9", "3.11"]
default_python = "3.11"
dev_extras = ["dev", "test"]
testpaths = ["tests/unit"]
fast_testpaths = ["tests/unit"]
slow_marker = "slow"
extra_steps = []
"""


def write_project(root: Path, block: str = BLOCK) -> Path:
    """Write a minimal pyproject.toml and return its path."""
    path = root / "pyproject.toml"
    path.write_text('[project]\nname = "demo"\n' + block, encoding="utf-8")
    return path


def test_loads_every_setting(tmp_path: Path) -> None:
    """Every declared key is returned as a typed value."""
    write_project(tmp_path)

    config = load_config(tmp_path)

    assert config.distribution == "causaliq-demo"
    assert config.package == "causaliq_demo"
    assert config.python_versions == ("3.9", "3.11")
    assert config.default_python == "3.11"
    assert config.dev_extras == ("dev", "test")
    assert config.testpaths == ("tests/unit",)
    assert config.slow_marker == "slow"


def test_defaults_are_applied(tmp_path: Path) -> None:
    """A block with only a package name falls back to defaults."""
    write_project(tmp_path, '\n[tool.causaliq]\npackage = "demo_pkg"\n')

    config = load_config(tmp_path)

    assert config.distribution == "demo_pkg"
    assert config.python_versions == ("3.10",)
    assert config.dev_extras == ("dev",)
    assert config.testpaths == ("tests",)
    assert config.fast_testpaths == ("tests/unit", "tests/functional")


def test_slow_filter_and_extras_spec(tmp_path: Path) -> None:
    """Derived helpers expose the marker and the pip extras."""
    write_project(tmp_path)

    config = load_config(tmp_path)

    assert config.slow_filter == ("-m", "not slow")
    assert config.extras_spec == "dev,test"


def test_finds_pyproject_above_the_start(tmp_path: Path) -> None:
    """A nested directory resolves to the project root."""
    write_project(tmp_path)
    nested = tmp_path / "src" / "pkg"
    nested.mkdir(parents=True)

    assert find_pyproject(nested) == tmp_path / "pyproject.toml"


def test_finds_pyproject_from_a_file(tmp_path: Path) -> None:
    """A file start resolves from its parent directory."""
    path = write_project(tmp_path)

    assert find_pyproject(path) == path


def test_missing_pyproject_raises(tmp_path: Path) -> None:
    """A tree without pyproject.toml is reported clearly."""
    with pytest.raises(ConfigError, match="no pyproject.toml"):
        find_pyproject(tmp_path)


def test_multiline_arrays_and_comments(tmp_path: Path) -> None:
    """Arrays may span lines and contain comments between entries."""
    write_project(
        tmp_path,
        """
[tool.causaliq]
package = "demo_pkg"
python_versions = [
    "3.10",  # oldest supported
    "3.11",
]
""",
    )

    config = load_config(tmp_path)

    assert config.python_versions == ("3.10", "3.11")


def test_booleans_and_integers_are_parsed(tmp_path: Path) -> None:
    """Scalars other than strings are parsed and ignored when unknown."""
    write_project(
        tmp_path,
        """
[tool.causaliq]
package = "demo_pkg"
enabled = true
retries = 3
""",
    )

    values = read_section(tmp_path / "pyproject.toml")

    assert values["enabled"] is True
    assert values["retries"] == 3


def test_missing_section_raises(tmp_path: Path) -> None:
    """A pyproject without the section is rejected."""
    write_project(tmp_path, "\n[project.optional-dependencies]\n")

    with pytest.raises(ConfigError, match="has no "):
        read_section(tmp_path / "pyproject.toml")


def test_empty_section_raises(tmp_path: Path) -> None:
    """A section with no keys is rejected."""
    write_project(tmp_path, "\n[tool.causaliq]\n")

    with pytest.raises(ConfigError, match="empty"):
        read_section(tmp_path / "pyproject.toml")


def test_unsupported_scalar_raises(tmp_path: Path) -> None:
    """An unquoted value that is not a boolean or integer is rejected."""
    write_project(tmp_path, "\n[tool.causaliq]\npackage = demo_pkg\n")

    with pytest.raises(ConfigError, match="unsupported value"):
        load_config(tmp_path)


def test_missing_equals_raises(tmp_path: Path) -> None:
    """A line without ``=`` is rejected."""
    write_project(tmp_path, "\n[tool.causaliq]\npackage\n")

    with pytest.raises(ConfigError, match="key = value"):
        load_config(tmp_path)


def test_unterminated_array_raises(tmp_path: Path) -> None:
    """An array left open at the end of the section is rejected."""
    write_project(
        tmp_path,
        '\n[tool.causaliq]\npackage = "demo"\ntestpaths = ["tests"\n',
    )

    with pytest.raises(ConfigError, match="unterminated value"):
        load_config(tmp_path)


def test_package_must_be_a_string(tmp_path: Path) -> None:
    """A numeric package name is rejected."""
    write_project(tmp_path, "\n[tool.causaliq]\npackage = 3\n")

    with pytest.raises(ConfigError, match="non-empty string"):
        load_config(tmp_path)


def test_testpaths_must_be_an_array(tmp_path: Path) -> None:
    """A string testpaths value is rejected."""
    write_project(
        tmp_path,
        '\n[tool.causaliq]\npackage = "demo"\ntestpaths = "tests"\n',
    )

    with pytest.raises(ConfigError, match="array of strings"):
        load_config(tmp_path)


def test_arrays_must_hold_strings(tmp_path: Path) -> None:
    """A non-string entry is rejected."""
    write_project(
        tmp_path,
        '\n[tool.causaliq]\npackage = "demo"\ntestpaths = ["tests", 3]\n',
    )

    with pytest.raises(ConfigError, match="non-empty strings"):
        load_config(tmp_path)


def test_python_versions_must_not_be_empty() -> None:
    """An empty version list is rejected by the builder."""
    with pytest.raises(ConfigError, match="must not be empty"):
        build_config({"package": "demo", "python_versions": []})


def test_optional_string_must_be_a_string(tmp_path: Path) -> None:
    """A non-string optional setting is rejected."""
    write_project(
        tmp_path,
        '\n[tool.causaliq]\npackage = "demo"\nslow_marker = 3\n',
    )

    with pytest.raises(ConfigError, match="must be a non-empty string"):
        load_config(tmp_path)


def test_shared_settings_use_the_code_defaults(tmp_path: Path) -> None:
    """The shared-environment keys fall back to the documented defaults."""
    write_project(tmp_path, '\n[tool.causaliq]\npackage = "demo_pkg"\n')

    shared = load_shared(tmp_path)

    assert shared.python_versions == ("3.12", "3.14")
    assert shared.extras == ("dev", "test")


def test_shared_settings_are_read_from_the_section(tmp_path: Path) -> None:
    """Declared shared settings override the defaults."""
    write_project(
        tmp_path,
        """
[tool.causaliq]
package = "demo_pkg"
shared_python_versions = ["3.12"]
shared_extras = ["dev"]
""",
    )

    shared = build_shared(read_section(tmp_path / "pyproject.toml"))

    assert shared.python_versions == ("3.12",)
    assert shared.extras == ("dev",)
