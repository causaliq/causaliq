# 🤖 CausalIQ Workflow

The CausalIQ Workflow framework provides a comprehensive solution for designing, executing, and reproducing causal discovery experiments at scale. Using a GitHub Actions-inspired YAML syntax, it enables researchers to conduct rigorous, reproducible studies while managing complex experimental configurations.

**Current Version**: v0.5.0

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-workflow/)
- [💻 Repository](https://github.com/causaliq/causaliq-workflow)

## Key Features

### 🔄 Workflow Orchestration
GitHub Actions-inspired YAML workflows with matrix expansion for systematic parameter sweeps, multi-step sequential execution, and template variable validation.

### ⚡ Action Framework
Three formalised action patterns — CREATE, UPDATE, and AGGREGATE — with conservative execution that automatically skips completed work. Use `--mode=force` to bypass skip checks.

### 🔍 Filter Expressions
Logical expressions evaluated against flattened entry metadata, with template variable resolution, `random()` sampling, and relaxed numeric suffix matching (k, M, G, T).

### 💾 Workflow Caching
SQLite-based result storage with SHA-256 matrix keys, null wildcards for flexible matching, and CLI commands for cache export/import.

### 🔌 Plug-in Actions
Auto-discovery system for registering action providers from any CausalIQ package, with type-safe `ActionInput`/`ActionResult` interfaces built on causaliq-core.

## Future Directions

- **Step output chaining**: Step output references and cache restoration for resumable workflows
- **Dry and comparison runs**: Runtime estimation and processing summaries
- **Discovery integration**: Structure learning algorithms as workflow actions
- **CI testing**: Workflow specification syntax validation
- **Distributed computing**: Scalable parallel processing

## Integration with Ecosystem

- 🔍 **CausalIQ Discovery** (causaliq-discovery) is called by this package to perform structure learning.
- 📊 **CausalIQ Analysis** (causaliq-analysis) is called by this package to perform results analysis and generate assets for research papers.
- 🧠 **CausalIQ Knowledge** (causaliq-knowledge) provides LLM graph generation as a workflow action with cache integration.
- 🔮 **CausalIQ WhatIf** (causaliq-whatif) is called by this package to perform causal prediction.
- 🔄 **Zenodo Synchronisation** (zenodo-sync) is used by this package to download datasets and upload results.
- 🧪 **CausalIQ Research** (causaliq-research) experiments are defined as CausalIQ Workflows, allowing full reproduction of experiments, results, and published paper assets.

<br />

---

*The CausalIQ Workflow framework enables reproducible, scalable causal discovery research by providing comprehensive tools for experiment design, execution, and analysis, supporting the advancement of reliable causal inference methodologies.*
