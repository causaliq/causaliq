# Drop Python 3.9 support and add 3.14 support

Remove Python 3.9 support, add 3.14 support to all packages, and make 3.12 the 
default Python version.

I have installed Python 3.14.10 on the local system at @c:\dev\python3.14.10

I suggest we do it in dependency order:

umbrella -> core -> workflow -> data -> knowledge -> analysis -> discovery -> whatif -> research -> zenodo-sync

I would also suggest we first do the bare minimum to support 3.14 on each repo,
and then have a second refactoring round optimising the code to take account
of no longer having to support 3.9. This include being more deliberate about
the tooling (e.g. mypy) and dependency (e.g. pandas) versions, and not
including 3.9 "workarounds". All documentation should correctly refer to 
support for 3.10 to 3.14.

After completing this, I would then manually release each package on 
production PyPI with a 0.x.0 (no dev) version number

## Status (November 2026)

- Stage 1 (drop 3.9, add 3.14, default 3.12) is committed and green in every
  repository.
- Stage 2 (typing, tooling, dependency and documentation refactor) is complete
  for the umbrella. The remaining repositories follow in dependency order.
- Umbrella round-2 items landed: UTF-8 gate invocation, `extra_index_url`,
  `-ExistingOnly`, PEP 639 licence metadata, isort capped below 9, the legacy
  `setup_venv.ps1` removed, and an ecosystem co-install CI job.

---

## Known issues and round-2 backlog

### isort 9 skips non-ASCII files on Windows (deferred)

Every repository that declares `isort>=5.10.0` without an upper bound (the
umbrella, core, workflow, analysis, discovery, whatif, research and
zenodo-sync) now resolves isort 9.x. isort 9 reads and writes files using the
process locale encoding, which is `cp1252` on a default Windows install, so a
source file containing non-ASCII text (`→`, `α`, `🎉`) cannot be encoded and
is skipped with a warning:

```text
UserWarning: Unable to parse file tests\unit\graph\test_graph.py due to
'charmap' codec can't encode character '\u2192' in position 111
```

`causaliq-data` and `causaliq-knowledge` are unaffected because they pin
`isort>=5.10.0,<9.0.0`. The check still exits 0, so the gate passes, but on
Windows those files are not import-checked and `check_ci.ps1 -Fix` leaves them
unsorted while reporting success. Linux and macOS use a UTF-8 locale, so the
matrix still checks the files; the gap is Windows-only.

Verified locally:

```powershell
$py = '.\venv\py312\Scripts\python.exe'

# warning, exit 0 (file skipped)
& $py -m isort --check-only tests\unit\graph\test_graph.py

# no warning, exit 0 (file checked)
& $py -X utf8 -m isort --check-only tests\unit\graph\test_graph.py
```

Immediate local workaround: `$env:PYTHONUTF8 = '1'` before running the gate.

Round-2 fix, as one change:

1. run the gate's tools in UTF-8 mode: `devtools/steps.py::_module_command`
   returns `(sys.executable, "-X", "utf8", "-m", module, *paths)`, with
   `tests/unit/test_steps.py` updated to match;
2. set `PYTHONUTF8: "1"` in the shared CI job environment, beside
   `PYTHONIOENCODING`;
3. decide the isort bound deliberately: adopt 9 everywhere (with 1 and 2) or
   cap every package below 9 like `causaliq-data`, rather than leaving the
   ecosystem split.

### Other deferred items

- `causaliq-workflow`: remove the `sys.version_info >= (3, 10)` entry-point
  branch in `registry.py` and its Python 3.9 mock test.
- `scripts/setup_venv.ps1`: legacy single-environment script, hard-coded to
  3.11. `-Install` in `CONTRIBUTING.md` and the package READMEs abbreviates
  the generated `-InstallOnly`, so it skips missing environments instead of
  creating them.
- `scripts/setup-env.ps1` and CI disagree on package indexes. CI passes
  `extra-index-url: https://test.pypi.org/simple/` (workflow, data,
  knowledge, analysis, discovery), where the dev builds live
  (`causaliq-core 0.8.0.devN`, `causaliq-workflow 0.6.0.devN`; they are not
  on production PyPI), but the generated setup script installs
  `-e ".[extras]"` against production PyPI only. A from-scratch venv rebuild
  therefore fails with "Could not find a version that satisfies the
  requirement causaliq-core>=0.8.0.dev16", while pre-existing venvs keep
  working because the dev builds are already installed. Add an
  `extra_index_url` key to `[tool.causaliq]` (empty for core, whatif and
  zenodo-sync) that the template passes to pip, so a clean clone and a clean
  CI job resolve identically. Workaround meanwhile:
  `$env:PIP_EXTRA_INDEX_URL = 'https://test.pypi.org/simple/'`. The mismatch
  disappears once the stable 0.x.0 releases satisfy the dev pins.
- Provenance: keep the commit-hash reference (status quo), which costs a
  second umbrella commit per tooling change.
- Dependency and tooling versions: SPEC 0 minimums and badge; replace
  `license = {text = "MIT"}` with an SPDX string in `causaliq` and
  `zenodo-sync` (setuptools drops support on 2027-02-18).

---

## Stage 2 - refactor for a 3.10-3.14 floor

Stage 1 is committed in every repository: `requires-python` is `>=3.10`, the
environments and CI matrices cover 3.10-3.14, 3.12 is the default, the docs
refer to 3.10-3.14, and the generated scripts are pinned to the umbrella
commit that carries the change. Every package gate passes on Python 3.14
except `causaliq-discovery` (see below).

Order remains: umbrella -> core -> workflow -> data -> knowledge -> analysis
-> discovery -> whatif -> research -> zenodo-sync.

### First steps in the new session

1. Push the stage 1 commits and confirm CI is green on 3.10-3.14 for every
   repository (3.10 runs on `ubuntu-24.04` via `legacy-python-versions`).
2. Confirm the local environment strategy (below) and create the shared
   environments before touching code.
3. Clear the `causaliq-discovery` 3.14 item so the baseline is fully green.
4. Change the umbrella first: the tooling items regenerate every package's
   scripts, so they must land before the per-package work.
5. Then one repository at a time, in dependency order, one commit each.

### Outstanding before stage 2 starts

`causaliq-discovery` on 3.14 (local `venv\py314` and its CI job) fails while
pip tries to build matplotlib. The published `causaliq-analysis 0.5.0.dev6`
still pins `matplotlib<3.10,>=3.9`, and matplotlib 3.9 has no cp314 wheel, so
pip falls back to a source build. CI shows the failure on macOS and Windows
while generating matplotlib's metadata; only ubuntu passes, because its image
carries the FreeType and libpng build dependencies. Three ways to clear it, in
increasing permanence:

1. publish a new `causaliq-analysis` dev build with the corrected pin (for
   example `0.5.0.dev7`); discovery needs no change, and the next CI run
   resolves it because `>=0.5.0.dev5` prefers the newer build;
2. for local work, install the sibling packages editable before the extras;
3. release `causaliq-analysis 0.5.0` (pin already
   `matplotlib>=3.10.7,<3.11`) before discovery and research - the permanent
   fix, and it follows the release order.

`causaliq-research` depends on analysis as well, so its 3.14 job would fail
the same way once its workflow is re-enabled.

```powershell
$py = '.\venv\py314\Scripts\python.exe'
& $py -m pip install -e ..\causaliq-core -e ..\causaliq-workflow `
    -e ..\causaliq-data -e ..\causaliq-knowledge -e ..\causaliq-analysis
& $py -m pip install -e ".[dev,test,docs]"
```

### Scope

1. Remove the 3.9 workarounds: workflow's `sys.version_info >= (3, 10)`
   entry-point branch and its mocked 3.9 test; the `scipy-stubs`
   `python_version>='3.10'` marker in data. Record, rather than assume, the
   decisions that depend on the floor: the `StrEnum` backport and the custom
   `[tool.causaliq]` parser both need a 3.11 floor, so they stay while 3.10
   remains supported.
2. Typing: adopt PEP 604/585 (`X | None`, `list[str]`, `dict[str, int]`) and
   remove `Optional`, `List` and `Dict`; drop `from __future__ import
   annotations` where it no longer earns its keep; raise mypy's
   `python_version` to 3.12 and review `warn_unused_ignores` per repository.
3. Tooling versions, decided once: one isort major for the whole ecosystem
   plus the UTF-8 gate fix recorded above; refresh the stale `pre-commit`
   `rev` pins (black 23.3.0, flake8 6.0.0, mypy 1.3.0); confirm the black and
   mypy bounds; add `PYTHONUTF8: "1"` to the shared CI job environment.
4. Dependency floors (SPEC 0): raise the numpy, pandas, scipy, scikit-learn,
   matplotlib and seaborn minimums to the SPEC 0 window, add the SPEC 0
   badge, and revisit the `pandas<3.1` and `matplotlib<3.11` caps now that
   the newer behaviour is understood.
5. Packaging metadata: replace `license = {text = "MIT"}` with an SPDX
   string in `causaliq` and `zenodo-sync`, drop the MIT licence classifier,
   and align `license-files` across packages (setuptools removes support for
   the table form on 2027-02-18).
6. Scripts and provenance: remove `scripts/setup_venv.ps1`; settle the
   `-Install` versus `-InstallOnly` spelling so the legacy form cannot
   silently skip environments; add the `extra_index_url` key so local setup
   and CI resolve identically; keep the commit-hash provenance (two commits
   per tooling change).
7. CI gap: nothing checks that the packages are co-installable at their
   released versions, which is what users of several packages do. Add one job
   that installs the whole ecosystem from the index into a single
   environment.
8. Documentation: close the "Adopt SPEC 0 minimum dependency versions and
   badge" roadmap item when 4 lands and refresh the badges then, and remove
   any remaining pre-3.10 statements in READMEs and user guides, leaving
   historical CHANGELOG entries alone.

### Local environment strategy (confirm before coding)

Every repository currently keeps `venv\py310` ... `venv\py314` - fifty
environments - each installing the package editable with the dev, test and
docs extras and resolving siblings from Test PyPI. That repeats the
scientific stack in every environment, and dependent repositories test the
*published* sibling builds rather than the working tree; the matplotlib
source build and the `pandas-stubs` mypy surprise both came from this.

- **Per repository (status quo).** Matches the gate's ownership check and CI
  exactly, and exposes undeclared dependencies and pin conflicts; costs fifty
  environments and hides local sibling edits.
- **One shared set in the umbrella.** Two or three environments (3.12 and
  3.14) with every package installed editable. Fast, and local edits are
  visible across repositories; but it masks missing dependency declarations
  and the gate rejects a foreign interpreter unless `--ci` is given.
- **Hybrid (recommended).** Two shared environments in the umbrella (3.12 and
  3.14) with every package installed editable; each package's gate runs
  against them with `--ci`. Repo-local environments are optional
  conveniences (gate without `--ci`, `activate.ps1`, OS/version-specific
  debugging), not part of the release process. Release evidence comes from CI
  (index-resolved install per repo) plus one throwaway environment that
  installs the uploaded artifact from Test PyPI and smoke-imports it.

Two caveats still apply to the shared set, and they are why it is not release
evidence: it hides undeclared dependencies (discovery's mypy only failed
because the shared env had `pandas-stubs`, which discovery does not declare),
and it can resolve different tool versions - the same work had isort 8.0.1 in
the shared env and isort 9.0.2 in core's own env, which is why one reported
"Unable to parse file" warnings and the other did not.

Creating the shared set (manual, until `scripts/setup_dev_env.py` exists):

```powershell
# from the folder that contains every repository
py -3.12 -m venv causaliq\venv\py312
& .\causaliq\venv\py312\Scripts\python.exe -m pip install `
    -e 'causaliq[dev]' -e 'causaliq-core[dev,test]' `
    -e 'causaliq-workflow[dev,test]' -e 'causaliq-data[dev,test]' `
    -e 'causaliq-knowledge[dev,test]' -e 'causaliq-analysis[dev,test]' `
    -e 'causaliq-discovery[dev,test]' -e 'causaliq-whatif[dev,test]' `
    -e 'causaliq-research[dev,test]' -e 'zenodo-sync[dev,test]'
```

Repeat with `py -3.14` and `venv\py314`. No Test PyPI index is needed: every
CausalIQ package is installed editable in a single resolution, which is the
local-side benefit of the hybrid. With the shared set in place the fifty
per-repository environments can be deleted.

`scripts/setup_dev_env.py` is planned to automate this (sibling discovery via
`[tool.causaliq]`, environment creation, one pip resolve, smoke imports). It
is a new capability (Hat 1), so it is a separate task and must not be mixed
into stage 2.

Release check - one throwaway environment, recreated per release, run from
the folder that contains every repository:

```powershell
py -3.12 -m venv causaliq\venv\release-check
& .\causaliq\venv\release-check\Scripts\python.exe -m pip install `
    --index-url https://test.pypi.org/simple/ `
    --extra-index-url https://pypi.org/simple/ `
    causaliq-analysis==0.5.0
& .\causaliq\venv\release-check\Scripts\python.exe `
    -c "import causaliq_analysis"
```

If the hybrid is adopted, consider teaching the gate to accept a shared
environment: instead of requiring `sys.prefix` to sit inside the repository,
verify that the installed `config.package` distribution resolves into this
repository's `src` tree. That keeps the guard - the gate must test this
repository's code - without forcing one environment per repository.

### Process

- LLMs never stage, commit or push; edits stay in the working tree and the
  user commits, one repository per commit.
- A repository is committed only when its gate passes; run the gate on 3.12
  and 3.14 locally and treat CI as authoritative for 3.10, 3.11 and 3.13.
- Regenerate the generated scripts after the umbrella change: `python
  scripts/sync.py --update --source . --bootstrap --ref causaliq@<sha>` in
  the umbrella, then `python scripts/sync.py --update --source ..\causaliq
  --ref causaliq@<sha>` in each package, and commit the regenerated files.
- Keep `docs/development_policy/` authoritative: stage 2 is Hat 2 work and
  must not be bundled with feature or fix changes.

---

## Task: setup_dev_env (Hat 1 - umbrella development environments)

A new capability, separate from stage 2 and to be completed first: it makes
the shared development environments reproducible. Implement it as its own
commits; do not mix it with the stage 2 refactor.

### Goal

One command creates and maintains the shared environments described under
"Local environment strategy" - every CausalIQ package installed editable in a
single resolution - and can verify them.

### Decisions taken

- Default versions: 3.12 and 3.14 (`shared_python_versions`), overridable.
- Extras: `dev,test` by default (`shared_extras`); `docs` is opt-in through
  `--extras`.
- `devtools/devenv.py` is excluded from vendoring, because no package ever
  runs it (see Design).

### Interface

```text
python scripts/setup_dev_env.py [--python 3.12 ...] [--extras dev,test]
    [--repo NAME=PATH] [--install-only] [--recreate] [--check] [--dry-run]
    [--strict] [--interpreter PATH]
```

`--check` is the "confirm the strategy" step used by the stage 2 first steps:
it reports each environment, its interpreter and the importability of every
discovered package, and exits non-zero when incomplete. `--dry-run` prints
the commands without executing them.

### Design

- `src/causaliq/devtools/devenv.py`, stdlib only:
  - `discover(root)` scans sibling directories for a `pyproject.toml` with a
    `[tool.causaliq]` section and reuses `config.read_section` and
    `build_config` for `distribution`, `package` and `dev_extras`; no new
    manifest. `--repo NAME=PATH` adds or overrides an entry.
  - `resolve_interpreter(version)` uses `py -<ver>` on Windows and
    `python<ver>` then `python3` on POSIX; `--interpreter` overrides. A
    missing interpreter fails loudly, naming `py -0p`, instead of skipping.
  - `venv_command()` and `install_command()` build argument lists so they can
    be asserted without executing anything.
  - One `pip install -e` invocation for the whole ecosystem, then an import
    smoke check over every discovered package.
  - Nothing is deleted: removing old environments stays manual.
- Generated entry point `scripts/setup_dev_env.py`, rendered only when
  `sync.py --bootstrap` runs, so packages never receive a script that would
  try to install their siblings.
- `sync.py::_vendor_files` skips `devenv.py`, with a comment explaining that
  it is umbrella-only tooling which packages never import, so vendoring it
  would place an unused copy in ten repositories. A test asserts the
  exclusion.

  Note: this exclusion avoids an unused file, it does not avoid the
  regeneration pass. `sync.py` itself (bootstrap rendering plus the
  exclusion) and `config.py` (the new keys) are vendored, so every package's
  `scripts/_vendor/causaliq_devtools/` changes and must be regenerated - the
  usual two umbrella commits, then one commit per package.
- Config: `shared_python_versions = ["3.12", "3.14"]` and
  `shared_extras = ["dev", "test"]` in the umbrella `[tool.causaliq]`, with
  code defaults when the keys are absent.

### Tests and validation

- Unit: discovery over a temporary sibling tree, config parsing, interpreter
  resolution with `os.name` monkeypatched, and command construction.
- Functional: `--dry-run` and `--check` over fake repositories, asserting the
  planned commands and the exit codes.
- 100 % coverage of `devenv.py`, as the umbrella gate requires.
- Manual acceptance on this machine: build both environments from scratch,
  run one package gate from the shared set with `--ci`, then delete every
  per-repository `venv/`.

### Acceptance criteria

1. `python scripts/setup_dev_env.py` builds `venv/py312` and `venv/py314`
   with every package editable and smoke-imports each one.
2. `--check` exits zero only when both environments are complete.
3. `--dry-run` shows the exact commands, and `--install-only` never skips a
   missing environment silently.
4. The umbrella gate is green on 3.12 and 3.14, and `check_ci.py --ci` runs a
   package gate against the shared set.
5. `sync.py --check` is green in every repository after regeneration.

### Files expected to change

- `src/causaliq/devtools/devenv.py` (new)
- `src/causaliq/devtools/sync.py` (bootstrap-only entry point, vendoring
  exclusion)
- `src/causaliq/devtools/config.py` (two optional keys)
- `tests/unit/test_devenv.py`, `tests/functional/test_devenv.py` (new), plus
  a case in `tests/functional/test_sync.py`
- `pyproject.toml` (the two keys)
- `docs/development_policy/05-scripts.md`, `CONTRIBUTING.md`
- regenerated `scripts/` in the umbrella and all ten packages

### Out of scope

Changing `scripts/setup-env.ps1`, the gate's environment check or CI;
deleting environments; installing the docs extras by default.

