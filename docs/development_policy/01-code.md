---
paths:
  - "src/**"
---
# Rules for Coding Functionality

## The "Two Hats" Rule
- **Hat 1 (Features & Fixes):**
  - Work strictly within existing module structures and only apply "New Module and Method Constraints" to **new code** 
- **Hat 2 (Refactoring):**
  - Perform structural refactoring or file splitting ONLY when explicitly given a refactoring command on a **specific module**.
  - Module and method constraints **must** be applied to all re-structured sub-modules
  - Refactoring MUST NOT alter runtime behaviour or public APIs.

## New Module and Method Constraints
- **Counting Rules:** All limits below use these definitions.
  - **Statement:** one executable statement of the function body, including
    nested statements. A statement spanning several lines counts once.
    Docstrings, comments, blank lines and `# pragma: no cover` blocks do not
    count.
  - **Nesting Depth:** the number of enclosing blocks around a line, counting
    blocks below the function body. A block is `if`/`elif`/`else`,
    `for`/`while`, `try`/`except` or `with`. A guard clause that exits the
    current block (`continue`, `break`, `return`, `raise`) does not increment
    the count, so `for` + `if` is compliant while `for` + `if` + `try` is not.
    Comprehensions and conditional expressions are never blocks.
- **Module Limits:** Do not exceed ~200 executable statements per module.
  Extract sub-modules if approaching this threshold.
- **Method Limits:** Keep functions and methods within 5–15 statements (hard
  maximum 30).
- **Indentation & Nesting:** Limit nesting to 2 blocks below the function body,
  as defined in the counting rules above.
- **Legacy Code:** Limits apply to new modules and to any function or module
  being restructured. Pre-existing breaches are quarantined — bring the
  functions you touch within the limits rather than rewriting untouched code.
- **Enforcement:** `python scripts/check_code_rules.py` runs with the other
  quality gates and reports nesting depth and statement counts per function
  and statements per module. New and re-structured files must report zero
  breaches.
- **79-Character Line Limit**: Enforce strictly from initial generation.
- **Docstrings**: Google-style, British English spelling (*optimise*, *analyse*), blank lines before list items for MkDocs compatibility.


## Naming & Semantics
- **Public API:** Use explicit, action-oriented `verb_noun` naming (e.g., `compute_backdoor_adjustment`, `parse_json_to_dag`).
- **Internal Logic:** Prefix non-public helper functions and methods with a single leading underscore `_`.
- **Booleans:** Prefix predicate functions returning booleans with `is_`, `has_`, or `can_`.
- **Self-Documentation:** Prefer descriptive function names over multi-line docstrings for minor internal helpers.

## Quality Standards
Code must pass: `black` (79 chars), `isort`, `mypy` (100% typed), `flake8`, and achieve 100% `pytest` coverage.