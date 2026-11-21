"""Functional tests for the code-rules checker."""

from __future__ import annotations

from pathlib import Path

import pytest

from causaliq.devtools import code_rules

pytestmark = pytest.mark.functional


def write_module(root: Path, source: str, name: str = "mod.py") -> Path:
    """Write a module under ``root/src`` and return its path."""
    path = root / "src" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def run(root: Path, *extra: str) -> int:
    """Run the checker over ``root/src``."""
    return code_rules.main(["check", str(root / "src"), *extra])


def test_compliant_module_passes(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A short function with a guard clause is within the limits."""
    write_module(
        tmp_path,
        "def f(items):\n"
        "    for item in items:\n"
        "        if item:\n"
        "            return item\n"
        "    return None\n",
    )

    assert run(tmp_path, "--strict") == 0
    assert "0 breaches" in capsys.readouterr().out


def test_long_function_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A function over the statement target is listed."""
    body = "".join(f"    x{i} = {i}\n" for i in range(16))
    write_module(tmp_path, "def f():\n" + body)

    assert run(tmp_path, "--strict") == 1
    output = capsys.readouterr().out
    assert "f depth=0 stmts=16" in output
    assert "rules (strict): 1 breaches" in output


def test_advisory_mode_does_not_fail(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Legacy breaches are reported but do not change the exit code."""
    body = "".join(f"    x{i} = {i}\n" for i in range(16))
    write_module(tmp_path, "def f():\n" + body)

    assert run(tmp_path) == 0
    assert "Advisory mode" in capsys.readouterr().out


def test_deep_nesting_is_reported(tmp_path: Path) -> None:
    """Three nested blocks breach the depth limit."""
    write_module(
        tmp_path,
        "def f(items):\n"
        "    for item in items:\n"
        "        if item:\n"
        "            try:\n"
        "                return item\n"
        "            except ValueError:\n"
        "                return None\n",
    )

    assert run(tmp_path, "--strict") == 1


def test_docstrings_and_pragmas_do_not_count(tmp_path: Path) -> None:
    """Docstrings and pragma lines are excluded from the statement count."""
    body = "".join(f"    x{i} = {i}\n" for i in range(14))
    source = (
        "def f():\n"
        '    """Docstring."""\n' + body + "    y = 1  # pragma: no cover\n"
    )
    write_module(tmp_path, source)

    assert run(tmp_path, "--strict") == 0


def test_oversize_module_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A module above the statement target is listed."""
    write_module(tmp_path, "".join(f"x{i} = {i}\n" for i in range(201)))

    assert run(tmp_path, "--strict") == 1
    assert "module has 201 statements" in capsys.readouterr().out


def test_syntax_error_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """An unparsable module is a breach rather than a crash."""
    write_module(tmp_path, "def broken(:\n")

    assert run(tmp_path, "--strict") == 1
    assert "could not parse" in capsys.readouterr().out


def test_single_file_target_is_accepted(
    tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """A file argument is checked directly."""
    path = write_module(tmp_path, "x = 1\n")

    assert code_rules.main(["check", str(path)]) == 0
    assert "across all 1 modules" in capsys.readouterr().out


def test_environment_directories_are_skipped(tmp_path: Path) -> None:
    """Modules under venv or cache directories are not scanned."""
    write_module(tmp_path, "".join(f"x{i} = {i}\n" for i in range(201)))
    write_module(
        tmp_path,
        "".join(f"x{i} = {i}\n" for i in range(201)),
        name="venv/lib/mod.py",
    )

    assert run(tmp_path, "--strict") == 1


def test_missing_directory_is_empty(tmp_path: Path) -> None:
    """A non-existent target yields no modules and no breaches."""
    assert code_rules.main(["check", str(tmp_path / "absent")]) == 0
