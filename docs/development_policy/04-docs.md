---
paths:
  - "docs/**"
---
# Rules for Documentation

## Formatting Guidelines
- **British English**: Standardise spelling across all documentation.
- **MkDocs Compatibility**: Precede bullet point lists with a blank line.
- **Single Source of Truth**: Keep status tracking in `docs/roadmap.md` and
  design decisions in the architecture documentation (`docs/architecture/` in
  each package; `docs/projects/ecosystem_architecture.md` in the umbrella
  repository). Avoid duplicating feature lists across files.
- **Policy Documents**: The umbrella `docs/development_policy/` files are the
  single source of truth for engineering standards. Package documentation must
  reference them rather than restating their contents.