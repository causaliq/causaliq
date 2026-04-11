# 🧪 CausalIQ Research

CausalIQ Research is a curated collection of experimental setups, benchmark datasets, and published results that enable reproducible research and method comparison in the field of causal discovery and inference.

> **Early Development** — This package has initial project scaffolding (CLI, docs, CI) but no completed feature releases yet. Release v0.1.0 (Graph Averaging) is in development.

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-research/)
- [💻 Repository](https://github.com/causaliq/causaliq-research)

## Repository Structure

The repository is organised around research concepts rather than file types:

```
causaliq-research/
├── src/              # Minimal code (CLI, utilities)
├── models/           # Bayesian model specifications — by model
│   └── asia/
│   └── sachs/
├── experiments/      # Workflows + results — by experiment series
│   └── llm-benchmark-2026/
│       ├── workflow.yaml
│       └── results.db
├── papers/           # Generated assets — by paper
│   └── llm-priors-2026/
│       ├── tables/
│       └── figures/
└── scratch/          # Gitignored working directory
```

## Key Features

### 🔄 Reproducibility
Complete workflows from datasets through results to published paper assets, with platform-agnostic deterministic replication including stable randomisation and cached LLM responses.

### 🔍 Transparency
All software is open source on GitHub, results use open standard formats (JSON, GraphML, YAML), and assets will be publicly available on Zenodo.

### 🤖 Automation
A single command replicates all experiments for a published paper, with fine-grained control over individual steps, dry-run capability, and parallel execution.


## Integration with Ecosystem
- 🔍 **CausalIQ Discovery** (causaliq-discovery) is called by this package to perform statistical structure learning.
- 📊 **CausalIQ Analysis** (causaliq-analysis) is called by this package to perform results analysis and generate assets for research papers.
- 🔮 **CausalIQ WhatIf** (causaliq-whatif) is called by this package to perform causal prediction.
- 🔄 **Zenodo Synchronisation** (zenodo-sync) is used by this package to download datasets and upload results.
- 🧠 **CausalIQ Knowledge** (causaliq-knowledge) can be integrated into causal discovery, analysis and inference workflows to produce more accurate, transparent and interpretable results.
- 🤖 **CausalIQ Workflow** (causaliq-workflow) orchestrates the steps required for the reproduction of experiments, results, and published paper assets.

<br />

---

*CausalIQ Research enables reproducible, transparent causal discovery research by providing curated experimental setups, benchmark datasets, and published results that support method comparison and the advancement of reliable causal inference methodologies.*
