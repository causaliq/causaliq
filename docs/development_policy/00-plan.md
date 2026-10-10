---
paths:
  - "docs/current_task.md"
---
# Rules for Plan Phase

## Package Structure Assignment
Ensure functionality is assigned to the correct CausalIQ package:
- **discovery**: Causal discovery algorithms.
- **knowledge**: Human or LLM knowledge integration.
- **whatif**: Causal inference capabilities.
- **analysis**: Results, graph analysis, summarisation, and plotting.
- **workflow**: Orchestration across discovery, inference, and analysis.
- **data**: Data input, conditional independence tests, and scoring.
- **core**: Shared foundational capabilities.

## Scope & Task Isolation (The "Two Hats" Rule)
- **Strict Separation:** Never mix Feature/Fix Implementation (Hat 1) with Refactoring (Hat 2) in the same task plan.
- **Plan Budgeting:**
  - **Hat 1 (Feature/Fix):** Scope tasks strictly around existing code structures. If technical debt is identified, log it as a follow-up refactoring item; do not include it in the immediate action plan.
  - **Hat 2 (Refactor):** Create standalone plans dedicated solely to file splitting, structural moves, or architectural reorganisation. Ensure the plan includes running existing tests before and after execution. Always design `__init__.py` to re-export public interfaces so existing package imports remain unbroken.
- **New Module Architectural Standard:** Plans for newly created modules must
  immediately incorporate the standard limits defined in `01-code.md`.
- **Re-structured Code:** Moved or split code is measured against the same
  limits as new code. A plan that moves code must state the intended
  decomposition up front and expect the moved functions to be flattened or
  split within the same step. Flattening and splitting inside a move is Hat 2
  work and does not count as mixing hats.

## Sub-package & Module Structure
- **Limits:** Sizing and nesting limits, and the counting rules for them, are
  defined once in `01-code.md` and are not restated here.

## LLMs should NOT commit changes
- LLMs **SHOULD NEVER** commit changes: this should remain in the control of the user 

## Communication & Planning
- **Explicit Rationale**: Always state **What**, **Why**, **Impact**, and **Alternatives** in responses.
- **Comprehensive Scoping**: Ensure plans account for coding, tests, and documentation.

## Searching Code
- avoid searching the very large venv and cache folders