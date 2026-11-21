"""Integration test: a generated package runs its gate without the umbrella."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from causaliq.devtools import sync

pytestmark = pytest.mark.integration
UMBRELLA = Path(__file__).resolve().parents[2]
CONFIG = """
[tool.causaliq]
distribution = "causaliq-demo"
package = "demo"
python_versions = ["3.9", "3.11"]
default_python = "3.11"
dev_extras = ["dev"]
testpaths = ["tests/unit"]
fast_testpaths = ["tests/unit"]
"""


def build_target(root: Path) -> Path:
    """Create a minimal package and generate its scripts."""
    target = root / "demo"
    (target / "src" / "demo").mkdir(parents=True)
    (target / "src" / "demo" / "__init__.py").write_text(
        '"""Demo package."""\n', encoding="utf-8"
    )
    (target / "tests" / "unit").mkdir(parents=True)
    (target / "pyproject.toml").write_text(
        '[project]\nname = "demo"\n' + CONFIG, encoding="utf-8"
    )
    sync.update(target, UMBRELLA, "causaliq@test")
    return target


def run_script(target: Path, name: str, *args: str) -> int:
    """Run a generated script without the umbrella on PYTHONPATH."""
    environment = {
        key: value for key, value in os.environ.items() if key != "PYTHONPATH"
    }
    return subprocess.call(
        [sys.executable, str(target / "scripts" / name), *args],
        cwd=str(target),
        env=environment,
    )


def test_generated_gate_runs_offline(tmp_path: Path) -> None:
    """The vendored gate runs without the umbrella or network access."""
    target = build_target(tmp_path)

    assert run_script(target, "check_ci.py", "--ci", "--rules") == 0


def test_generated_sync_detects_edits(tmp_path: Path) -> None:
    """The vendored sync verifies hashes and reports a hand edit."""
    target = build_target(tmp_path)

    assert run_script(target, "sync.py", "--check") == 0
    entry = target / "scripts" / "check_ci.py"
    entry.write_text(
        entry.read_text(encoding="utf-8") + "# edit\n", encoding="utf-8"
    )
    assert run_script(target, "sync.py", "--check") == 1


def test_manifest_records_provenance(tmp_path: Path) -> None:
    """The manifest names the source and every generated file."""
    target = build_target(tmp_path)

    manifest = json.loads(
        (target / "scripts" / "generated.json").read_text(encoding="utf-8")
    )

    assert manifest["source"] == "causaliq@test"
    assert "scripts/run_checked.py" in manifest["files"]
    assert len(manifest["files"]) >= 10
