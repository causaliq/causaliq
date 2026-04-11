# 🤖 CausalIQ Workflow

The CausalIQ Workflow framework provides a comprehensive solution for designing, executing, and reproducing causal discovery experiments at scale. Built on modern workflow orchestration tools, it enables researchers to conduct rigorous, reproducible studies while managing complex experimental configurations and large-scale computations.


**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-workflow/)
- [💻 Repository](https://github.com/causaliq/causaliq-workflow)
- 🚀 Quick Start - coming soon

## Key Features

### 🔄 Workflow Orchestration
- **Continuous Integration (CI) testing**: Workflow specification syntax
- **Dask distributed computing**: Scalable parallel processing
- **Dependency management**: Automatic handling of data and processing dependencies
- **Error recovery**: Robust handling of failures and restarts

### 📊 Experiment Management
- **Configuration management**: YAML-based experiment specifications
- **Parameter sweeps**: Systematic exploration of algorithm parameters
- **Version control**: Git-based tracking of experiments and results
- **Reproducibility**: Deterministic execution with seed management

### 📈 Results Tracking
- **Automated metrics**: Comprehensive evaluation of learned structures
- **Comparison frameworks**: Statistical comparison across methods
- **Visualization**: Interactive plots and publication-ready figures
- **Report generation**: Automated experimental summaries


## Integration with Ecosystem

- 🔍 **CausalIQ Discovery** (causaliq-discovery) is called by this package to perform structure learning.
- 📊 **CausalIQ Analysis** (causaliq-analysis) is called by this package to perform results analysis and generate assets for research papers.
- 🔮 **CausalIQ WhatIf** (causaliq-whatif) is called by this package to perform causal prediction.
- 🔄 **Zenodo Synchronisation** (zenodo-sync) is used by this package to download datasets and upload results.
- 🧠 **CausalIQ Knowledge** (causaliq-knowledge) can be integrated into causal discovery, analysis and inference workflows to produce more accurate, transparent and interpretable results.
- 🧪 **CausalIQ Research** (causaliq-research) are defined in terms of CausalIQ Workflows allowing the reproduction of experiments, results and
published paper assets created by the CausalIQ ecosystem.

<br />

---

*The CausalIQ Workflow framework enables reproducible, scalable causal discovery research by providing comprehensive tools for experiment design, execution, and analysis, supporting the advancement of reliable causal inference methodologies.*
