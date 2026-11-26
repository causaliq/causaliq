# Development Scripts

## Single source of truth

The development scripts that every CausalIQ package carries are **generated**
from the umbrella repository. The canonical implementation lives in:

```
src/causaliq/devtools/
  config.py        # reads [tool.causaliq] from pyproject.toml
  gate.py          # black -> isort -> flake8 -> code rules -> mypy -> pytest
  options.py       # gate command-line switches
  steps.py         # one function per tool
  code_rules.py    # nesting depth and statement counts
  run_checked.py   # launch and wait protocol for long commands
  sync.py          # verify or refresh the generated files
  templates.py     # text templates for the generated scripts
  devenv.py        # umbrella-only: shared development environments
  devenv_check.py  # umbrella-only: verify the shared environments
  devenv_env.py    # umbrella-only: paths, interpreters and pip commands
  devenv_repos.py  # umbrella-only: discover the sibling repositories
```

Everything in `devtools` is stdlib-only, so a package can vendor the modules
and run its gate without installing the umbrella and without network access.
The `devenv*` modules are the one exception: no package imports them, so they
are never vendored.

The umbrella repository runs its own package through thin entry points in
`scripts/`. Packages do not import the umbrella: they receive a vendored copy
of `devtools` under `scripts/_vendor/causaliq_devtools/`.

## Generated files

| File | Purpose |
| ---- | ------- |
| `scripts/check_ci.py` | entry point for the gate |
| `scripts/run_checked.py` | entry point for the run/wait protocol |
| `scripts/sync.py` | entry point for provenance checks and refreshes |
| `scripts/setup_dev_env.py` | umbrella-only entry point for the shared environments |
| `scripts/check_ci.ps1` | PowerShell wrapper for `check_ci.py` |
| `scripts/activate.ps1` | activates one of the package's environments |
| `scripts/setup-env.ps1` | creates and installs the environments |
| `scripts/build-and-publish.ps1` | builds and optionally publishes |
| `scripts/_vendor/causaliq_devtools/` | vendored copy of the modules |
| `scripts/generated.json` | source reference and a SHA-256 per file |

Every generated file begins with a provenance comment:

```text
# generated from causaliq@<sha> <source-path> - do not edit
```

## Never hand-edit a generated file

Hand edits are detected by `sync.py --check`, which recomputes the SHA-256 of
each file and compares it with `scripts/generated.json`. The check is offline
and therefore works in a clone, a fork and a CI job.

```powershell
python scripts/sync.py --check
```

Refresh the files from a clean umbrella checkout:

```powershell
python scripts/sync.py --update --source ..\causaliq
```

`--update` records the umbrella commit in the provenance header. If that
checkout has uncommitted changes, the reference is marked `-dirty` and a
warning is printed: commit the umbrella change first, then regenerate.

## The umbrella itself

The umbrella is the source of the tooling, so it does not vendor a copy of
its own package. It generates only its bootstrap scripts:

```powershell
python scripts/sync.py --update --source . --bootstrap
```

That writes `scripts/activate.ps1`, `scripts/setup-env.ps1`,
`scripts/check_ci.ps1` and `scripts/setup_dev_env.py` with the same provenance
header and manifest as a package. `scripts/check_ci.py`,
`scripts/run_checked.py` and `scripts/sync.py` remain thin canonical entry
points into `causaliq.devtools`; `setup_dev_env.py` is generated because no
package may receive it.

Run the command again after committing, so the recorded reference names the
commit rather than `-dirty`.

## Shared development environments

The umbrella owns two environments, `venv/py312` and `venv/py314`, that hold
every CausalIQ package installed editable in a single resolution. A local
change is therefore visible from every repository, which is the recommended
way to work across packages. A repository-local `venv/` created by
`scripts/setup-env.ps1` remains a convenience for work in one repository and
for OS- or version-specific debugging.

```powershell
python scripts/setup_dev_env.py            # create both environments
python scripts/setup_dev_env.py --check    # verify them
python scripts/setup_dev_env.py --dry-run  # show the commands only
```

| Switch | Effect |
| ------ | ------ |
| `--python 3.12 ...` | versions to manage, repeatable |
| `--extras dev,test` | extras to install, intersected with each package |
| `--repo NAME=PATH` | add or replace a discovered repository |
| `--install-only` | install into existing environments; a missing one fails loudly |
| `--recreate` | pass `--clear` to `python -m venv` for the managed environments |
| `--check` | report each environment, its interpreter and every import |
| `--dry-run` | print the commands without running them |
| `--strict` | stop at the first failing version, and require every import to resolve inside its sibling checkout |
| `--interpreter PATH` | create from this interpreter; requires a single `--python` version |

The versions and extras default to `shared_python_versions` and
`shared_extras`. Every location is derived from the umbrella checkout and
`[tool.causaliq]` - `venv/pyNNN` beside `scripts/` - and no environment
variable is read or set, so the command behaves identically whether or not a
virtual environment is active. Discovery scans the directory above the
umbrella for siblings whose `pyproject.toml` declares `[tool.causaliq]`; a
directory without the section is skipped, as is one whose name ends in
`-template` (the scaffold repository is not a package).

Two caveats keep this set out of the release evidence. It hides undeclared
dependencies, because a package can import something only a sibling declares,
and it can resolve different tool versions from a package's own environment.
Release evidence is the CI job for each repository plus one throwaway
environment that installs the uploaded artefact and smoke-imports it.

## Package configuration

Each package declares its data once, in `pyproject.toml`:

```toml
[tool.causaliq]
distribution = "causaliq-analysis"
package = "causaliq_analysis"
python_versions = ["3.10", "3.11", "3.12", "3.13", "3.14"]
default_python = "3.12"
dev_extras = ["dev", "test", "docs"]
testpaths = ["tests/unit", "tests/functional", "tests/integration"]
fast_testpaths = ["tests/unit", "tests/functional"]
slow_marker = "slow"
extra_steps = []
extra_index_url = ""
```

| Key | Meaning |
| --- | ------- |
| `distribution` | name used by packaging and publishing |
| `package` | import name, also the coverage target |
| `python_versions` | interpreters the generated scripts manage |
| `default_python` | interpreter activated by default |
| `dev_extras` | extras installed by `setup-env.ps1` |
| `shared_python_versions` | umbrella-only: versions of the shared environments |
| `shared_extras` | umbrella-only: extras installed into each shared environment |
| `testpaths` | directories run by the full gate |
| `fast_testpaths` | directories run by `--fast` |
| `slow_marker` | marker excluded unless `--include-slow` is given |
| `extra_steps` | additional commands, run with POSIX-style quoting |
| `extra_index_url` | extra pip index passed to `setup-env.ps1` (empty to omit) |

## Running the gate

On Windows, `CONTRIBUTING.md` keeps its familiar form:

```powershell
.\scripts\check_ci.ps1
```

On every platform, and inside CI:

```powershell
python scripts/check_ci.py
```

| Switch | Effect |
| ------ | ------ |
| `--fix` | black and isort write changes instead of checking |
| `--fast` | unit and functional tests only; no mypy or coverage |
| `--include-slow` | include tests carrying the configured slow marker |
| `--ci` | write JUnit and coverage XML under `build/ci/` |
| `--rules` | run only the code-rules report |
| `--no-tests` | run the quality steps without pytest |

The gate prints the repository root, the interpreter and the selected test
paths before it starts, and refuses to run in another project's environment
unless `--ci` is given.

A gate step runs its tools as `python -X utf8 -m <tool>`, so a non-ASCII
source file is read as UTF-8 even when the process locale is `cp1252` (the
Windows default). CI also sets `PYTHONUTF8=1` for the rest of the job.

The PowerShell wrapper forwards its arguments, so the previous spellings
`-Fast`, `-Fix` and `-IncludeSlow` are still accepted and map to the long
options above.

## Long-running commands

Completion is defined by an artefact, never by console output. The mandated
form is a launch followed by a single blocking wait:

```powershell
python scripts/run_checked.py --log .pytest.log --timeout 3600 -- python -m pytest
python scripts/run_checked.py --wait --log .pytest.log --timeout 3600
```

`run_checked.py` starts a detached supervisor, records the pid in
`<log>.pid`, and has the supervisor write `EXIT_CODE=<n>` to `<log>.exit`
when the child ends. `--wait` blocks once, prints the last lines of the log
and mirrors the recorded exit code. A timeout kills the process tree and
reports exit 124.

Rules that follow from this:

- Never use `Start-Sleep` loops to check whether a command has finished.
- Do not read the log until the process is known to have exited.
- Read the log once, through `--wait --tail`, rather than in a loop.
- Give pytest `--junitxml=<path>` when a machine-readable report is needed;
  the file appearing is itself a completion signal.

The PowerShell brace rule still applies to any hand-written wrapper:
`${LogPath}.exit` is the path, while `$LogPath.exit` is a property access.

## CI consumption

CI runs the same generated copy as the developer:

```yaml
- run: python scripts/sync.py --check
- run: python scripts/check_ci.py --ci
```

The local gate and CI therefore run identical code on every operating system,
and `sync.py --check` fails a pull request that hand-edits a generated file.
`scripts/_vendor/` is part of the generated output and is committed with the
scripts, so `sync.py` and the gate run in a clone without installing the
devtools package.

Shared CI calls the generated gate, so local and CI invocations are the same
command. `addopts` does not carry `-m 'not slow'`: the gate adds the slow-test
filter itself, and a bare `pytest` run executes the full suite. A package whose
integration tests need credentials passes `--include-slow` only when the
workflow can see those credentials (the shared workflow does this for Zenodo),
so the same gate command adapts to the environment without a second code path.

Coverage belongs to the gate as well. `addopts` must not repeat `--cov`: a
duplicated target makes coverage warn that the package was imported before
measurement started (`module-not-measured`).

## Adding or changing a step

1. Change the canonical module in `src/causaliq/devtools/`.
2. Add or update its tests in the umbrella and confirm 100% coverage.
3. Update this page.
4. Run the umbrella gate and commit.
5. Regenerate each package from the committed reference, one repository per
   commit, and run its gate before the change is committed.
