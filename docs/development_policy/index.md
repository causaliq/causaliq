# Development Policies

These pages are the **single source of truth** for engineering standards across
the CausalIQ ecosystem. They are written so that both human contributors and
LLM/Cline agents follow the same rules, and they apply to every CausalIQ
package (discovery, knowledge, whatif, analysis, workflow, data and core).

Individual repositories must **reference** these policies rather than
restating them. The contribution process itself - setting up an environment,
branching, commit conventions and reviews - is described in
[CONTRIBUTING.md](https://github.com/causaliq/causaliq/blob/main/CONTRIBUTING.md).

## The "Two Hats" Principle

Every task is either a **feature/fix** (Hat 1) or a **refactor** (Hat 2). The
two are never mixed in the same change, so that behavioural changes and
structural changes can be reviewed independently.

- **Hat 1 - Features and fixes**: work within the existing structure and apply
  the sizing limits to new code only.
- **Hat 2 - Refactoring**: restructure code only when explicitly asked, apply
  the limits to everything you touch, and never change runtime behaviour or
  public APIs.

## Policy Documents

Follow the documents in order, as they mirror the development lifecycle:

1. **[Plan Phase](00-plan.md)** - assigning work to the right package, task
   isolation and scoping.
2. **[Coding](01-code.md)** - module and method limits, naming, docstrings and
   quality gates.
3. **[Writing Tests](02-test-write.md)** - test framework, granularity,
   directory layout and the "two hats" rules for tests.
4. **[Running Tests](03-test-run.md)** - terminal setup, environment
   confirmation and the test workflow.
5. **[Documentation](04-docs.md)** - formatting, British English and
   single-source-of-truth rules.

## For LLM and Cline Agents

Each policy also acts as an automation rule: a `paths` header scopes it to the
files it governs, so an agent loads the planning rules when working on a task
plan, the coding rules when editing `src/`, the test rules when editing
`tests/`, and the documentation rules when editing `docs/`.
