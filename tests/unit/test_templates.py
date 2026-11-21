"""Unit tests for the generated-script templates."""

from __future__ import annotations

import pytest

from causaliq.devtools import templates
from causaliq.devtools.config import CausaliqConfig

pytestmark = pytest.mark.unit


def make_config(**overrides: object) -> CausaliqConfig:
    """Return a representative configuration for template rendering."""
    values = {
        "distribution": "causaliq-demo",
        "package": "causaliq_demo",
        "python_versions": ("3.9", "3.11"),
        "default_python": "3.11",
        "dev_extras": ("dev", "test"),
        "testpaths": ("tests/unit",),
        "fast_testpaths": ("tests/unit",),
    }
    values.update(overrides)
    return CausaliqConfig(**values)  # type: ignore[arg-type]


def test_activate_lists_every_version() -> None:
    """The activation script exposes each supported interpreter."""
    script = templates.activate_ps1(make_config())

    assert '"39" = "3.9"' in script
    assert '"311" = "3.11"' in script
    assert '$Version = "311"' in script
    assert "@@" not in script


def test_setup_env_installs_the_declared_extras() -> None:
    """The setup script installs the configured extras."""
    script = templates.setup_env_ps1(make_config())

    assert ".[dev,test]" in script
    assert '"310"' not in script
    assert "@@" not in script


def test_publish_uses_distribution_and_package() -> None:
    """The publish script targets the declared distribution and package."""
    script = templates.build_and_publish_ps1(make_config())

    assert "causaliq-demo version" in script
    assert "src\\causaliq_demo\\__init__.py" in script
    assert "@@" not in script


def test_wrapper_forwards_arguments() -> None:
    """The PowerShell wrapper passes remaining arguments to check_ci.py."""
    script = templates.check_ci_wrapper()

    assert "check_ci.py" in script
    assert "ValueFromRemainingArguments" in script


def test_entry_point_imports_the_vendored_module() -> None:
    """The Python entry point inserts the vendor path and calls main."""
    script = templates.entry_point("gate", "main", "Run the gates.")

    assert '"""Run the gates."""' in script
    assert '"gate"' not in script
    assert "from causaliq_devtools.gate import main" in script
    assert "sys.exit(main())" in script


def test_unknown_placeholders_are_left_alone() -> None:
    """Only known placeholders are replaced."""
    rendered = templates._fill("@@KNOWN@@ @@OTHER@@", {"KNOWN": "x"})

    assert rendered == "x @@OTHER@@"
