# Standardise package scripts and long-running command checks (Hat 2)

Can we make this change ito each repo one at a time going up the dependency order 
(core --> workflow --> analysis etc)  - so that each repoand  can be checked 
committed by me until we move to the next repo

## Problem

Each package carries its own copies of five development scripts, and the
copies have diverged. Inventory measured on 14 November 2026:

| script | copies | identical? | varies by |
| --- | --- | --- | --- |
| `check_code_rules.py` | 7 | yes, one hash | nothing; absent from research, whatif, zenodo-sync |
| `check_ci.ps1` | 10 | no (4711-5482 B) | coverage target plus capability drift |
| `activate.ps1` | 10 | no (1835-2005 B) | venv layout, Python versions |
| `setup-env.ps1` | 10 | no (6503-7778 B) | deps, extras, sibling editable installs |
| `build-and-publish.ps1` | 10 | no (1683-2076 B) | distribution name |

Capability drift in `check_ci.ps1`:

| repo | code-rules step | `-IncludeSlow` |
| --- | --- | --- |
| analysis, core, data, discovery, knowledge, repo-template | yes | yes |
| research, whatif | no | yes |
| workflow | yes | no |
| zenodo-sync | no | no |

`git log -S IncludeSlow` in `causaliq-workflow` shows the switch never existed
there, so its absence is a fork point rather than a decision. That repo has no
slow-marked tests, so the omission is inert today; `zenodo-sync` has one slow
test and also lacks the switch. Neither is a documented choice.

CI is already consolidated: each package's `ci.yml` is a shim calling
`causaliq/causaliq/.github/workflows/shared-ci.yml@main`. The local PowerShell
gate is therefore a second implementation of the same standard, is Windows-only,
and disagrees with CI on slow tests, because `shared-ci.yml` applies no marker
filter.

`03-test-run.md` already forbids polling and repeated log reads, but a
prohibition is not enforceable while no alternative command exists, and the
terminal cannot observe a command that outlives its capture window (about 20 s).

## Decisions already taken

- No new package. The gate logic lives in the umbrella `causaliq`, which is
  becoming the published ecosystem entry point.
- `causaliq-repo-template` remains the generator: it stamps generated files
  into new and existing packages.
- Generated files carry a provenance header and are verified in CI. Packages
  never call the umbrella by relative path, so clones, forks and offline work
  keep functioning.
- Bootstrap scripts stay repo-local because they must run before anything is
  installed.

## Open decisions

1. CI consumption: run the package's own generated copy (offline, one file, drift
   caught by `sync --check`) or check out the umbrella at a pinned ref.
   Recommendation: generated copy.
2. Slow-test semantics: `-IncludeSlow` everywhere with the default excluding
   `slow`, or drop the switch and always run everything to match CI. Whichever
   wins, `shared-ci.yml` and the local gate must agree.

## Scope

Canonical implementation in the umbrella:

```
src/causaliq/devtools/
  config.py        # reads [tool.causaliq] from the package pyproject.toml
  gate.py          # black -> isort -> flake8 -> code rules -> mypy -> pytest
  code_rules.py    # the existing checker, moved here
  run_checked.py   # launch and wait protocol for long commands
  sync.py          # verify/refresh generated scripts against a template ref
```

Everything in `devtools` is stdlib-only and importable without installing the
umbrella, so it can be vendored.

Per-repo data shrinks to one block in `pyproject.toml`:

```toml
[tool.causaliq]
package = "causaliq_workflow"
testpaths = ["tests/unit", "tests/functional", "tests/integration"]
slow_marker = "slow"
extra_steps = []
```

Generated files, each beginning `# generated from causaliq@<sha> <path> - do not
edit`:

- `scripts/check_ci.py` (gate) and `scripts/run_checked.py`
- `scripts/check_ci.ps1`, a three-line wrapper so `CONTRIBUTING.md` stays true
- `scripts/activate.ps1` and `scripts/setup-env.ps1`, kept local but generated

Deleted: the seven copies of `check_code_rules.py`.

## Long-running command protocol

Completion is defined by an artefact, never by console output:

- `run_checked` launches the command, records the pid, and has the child write
  `EXIT_CODE=<n>` to `<log>.exit` when it ends.
- `wait_checked` blocks once (`WaitForExit(ms)`) and then prints the log tail and
  the recorded exit code. A timeout kills the child and reports exit 124.
- `pytest` runs are given `--junitxml=<temp>/junit.xml`; the XML attributes
  `tests`, `failures` and `errors` are the report, and the file appearing is
  itself a completion signal.
- One read per run. Progress is never tracked by reading logs, by `read_files`
  or by `Start-Sleep` loops.
- `${LogPath}.exit` must be built with braces; `$LogPath.exit` is parsed as a
  property access. The pid must come from `-PassThru`, or it names the shell
  rather than the command.

This replaces the advisory bullets in `03-test-run.md` with a mandated command
that is identical in every package and works on every OS.

## Migration order

1. Umbrella: create the `devtools` modules and tests; add `pyproject.toml` for
   the published package. Run the umbrella tests before and after.
2. Umbrella: add `docs/development_policy/05-scripts.md` (canonical source,
   generated copies, provenance rule, never hand-edit a generated file), link it
   from `index.md`, and make one edit to `CONTRIBUTING.md`.
3. Template: regenerate its own `scripts/` from the umbrella and add the
   `[tool.causaliq]` placeholder block.
4. Pilot `causaliq-workflow` (the drifted copy): run old and new gates on the
   same commit, compare, then delete the old files.
5. Roll out repo by repo; `zenodo-sync` last, because `bump_version.py` needs
   its own decision.
6. `shared-ci.yml`: run `python scripts/check_ci.py --ci`, add
   `sync.py --check`, and stop maintaining the inline gate steps separately.

## Acceptance

- One implementation of each gate; local and CI run the same code on every OS.
- `sync.py --check` fails on any hand-edit of a generated script.
- Parity demonstrated in the pilot package by running the old and new gates on
  the same commit before the old copy is deleted.
- `03-test-run.md` names the mandated command instead of relying on
  prohibitions.

## Out of scope

- Any change to what the gates check, or to runtime code.
- dropping Python 3.9 and adding 3.14 which will be a follow-up "infrastructural
change"

