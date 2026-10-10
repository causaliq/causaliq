---
paths:
  - "tests/**"
---
# Rules for Writing Tests

## The "Two Hats" Rule

- **Hat 1 - Test Rules for Features & Fixes:**
  - Write unit tests targeting only the new functionality or regression bug.
  - Do not modify existing, unrelated test files or refactor test fixtures.


- **Hat 2 - Test Rules for Structural Refactoring:**
  - **Mirror Code Structure:** When a module is split or reorganised (e.g., decomposing a monolithic file into a sub-package), refactor the test suite concurrently to mirror the new code layout (e.g., splitting a single test file into corresponding test sub-modules).
  - **Import & Setup Rewiring:** Update import statements, path references, and test setup/fixtures to match new class or sub-module locations.
  - **Patch Targets:** When a function moves, update `mock.patch` and `monkeypatch.setattr` target strings to the new module path. Path-only edits are permitted; assertions stay frozen.
  - **Strict Assertion Freeze:** Never alter test logic, expected outputs, or `assert` statements during structural test refactoring.
  - **No Coverage Shrinkage:** Do not delete existing test cases during Hat 2 execution — the test suite must strictly prove behavioural equivalence before and after the code moves.

## Standards
- **Framework**: `pytest` ONLY. Do not use the `unittest` library, including
  `unittest.mock`. Use the `pytest-mock` `mocker` fixture or
  `pytest.MonkeyPatch` for external boundaries. Existing `unittest.mock`
  imports are quarantined under the legacy rule and are converted to
  `pytest-mock` when their test module is touched.
- **Style**: Standalone `test_*` functions with single-line comments above each for VS Code outlines.
- **Line Limit**: 79-character limit applied to test code and fixture data structures.
- **File Length:** Keep new and re-structured test modules under ~800 total
  lines. Split suites by responsibility rather than accumulating a monolithic
  `test_all.py`. Legacy oversize suites are quarantined until touched.

## Test Function Granularity
- **Function Size:** Individual `@pytest` test functions SHOULD be short (under 15 statements).
- **Single Focus:** Each test function should test only one assertion or scenario/edge-case.
- **Parametrization:** Use `@pytest.mark.parametrize` to test multiple input/output variations rather than duplicating test functions.

## Directory Layout
Organize under `tests/`:
- `unit/`: Pure logic, no I/O, uses mocks.
- `functional/`: File system and local resource I/O.
- `integration/`: Non-Python dependencies or external services.
- `data/`: Tracked input assets (git) and temporary output cleanup.
- `fixtures/`: Common setup/teardown capabilities.