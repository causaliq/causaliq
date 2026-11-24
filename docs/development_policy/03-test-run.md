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

## Running the gate

The gate is generated from the umbrella repository; see
[Development Scripts](05-scripts.md) for its provenance and configuration.

```powershell
.\scripts\check_ci.ps1
```

The same gate is available on every platform, and is the only form CI uses:

```powershell
python scripts/check_ci.py
```

A package may also be checked against the umbrella's shared environments
(see [Development Scripts](05-scripts.md#shared-development-environments)).
The gate accepts such an interpreter only with `--ci`, because the
environment does not live inside the repository:

```powershell
& ..\causaliq\venv\py312\Scripts\python.exe scripts\check_ci.py --ci
```

Agents and contributors may run the gate to verify a change, but must not use
`--fix` on files they are not already editing. The final gate run before a
commit remains the author's responsibility.

## Running tests and checking results

Completion is defined by an artefact, never by console output. Use the
mandated launch-and-wait pair:

```powershell
python scripts/run_checked.py --log .pytest.log --timeout 3600 -- python -m pytest
python scripts/run_checked.py --wait --log .pytest.log --timeout 3600
```

- Do not use Start-Sleep polling loops to check whether a command has finished.
- Do not read a command's output file until it is known to have exited.
- Read the log once, through `--wait --tail`, rather than repeatedly.
- For pytest, pass `--junitxml=<path>` when a machine-readable report is
  needed; the file appearing is itself a completion signal.
- A timeout kills the process tree and reports exit code 124.
- Clean up temporary PID, exit and log files when the command has finished.


