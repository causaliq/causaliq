# Rules for Running Tests & Terminal Operations

## Terminal & Session Setup
- Ensure terminal working directory matches the relevant package root.
- Use PowerShell terminals.
- **Session Chaining**: Always chain virtual environment activation with commands:
  ```powershell
  .\scripts\activate.ps1; python -m pytest
  ```
- **Confirm the Environment**: `scripts/check_ci.ps1` reuses an already-active
  environment, so an active venv from another project silently runs every gate
  against the wrong interpreter (missing stubs, wrong dependencies). Check the
  active environment before running tools.

## Test Workflow
- Fix issues systematically in sequence: `black` $\rightarrow$ `isort` $\rightarrow$ `flake8` $\rightarrow$ `pytest`
- Prefer targeted test modules; do not run the whole suite as a routine step.
- NEVER run `scripts/check_ci.ps1` — that is the user's gate and final sanity
  check.
- Running the full suite is permitted in two cases only: final verification of
  a package-wide refactor, and triage of order-dependent failures. Report the
  result; do not iterate on it.