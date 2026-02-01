# 🧪 CausalIQ Research

CausalIQ Research is a curated collection of experimental setups, benchmark datasets, and published results that enable reproducible research and method comparison in the field of causal discovery and inference.

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-research/)
- [💻 Repository](https://github.com/causaliq/causaliq-research)
- 🚀 Quick Start - coming soon

## Key Features

### 🔄 Reproducibility
- **Complete workflows**: from datasets to results to analysis to assets in published papers
- **Exact replication**: Platform-agnostic deterministic replication of results including of randomisation and information obtained from LLMs

### 🔍 Transparency
- **Open source software**: all software is open source, fully documented and tested on GitHub.
- **Open standard data formats**: results and experiment metadata available in open standard formats e.g. JSON, GraphML, YAML which can therefore be processed by other software
- **Zenodo storage**: all assets used in the complete workflow are publicly available on Zenodo

### 🤖 Automation
- **Ease of use**: a single command can be used to replicate all the experiments and results for a given published paper.
- **Fine-grained control**: alternatively, researchers can opt to look at, or replicate, individual elements of the workflow, for example, run a specific algorithm, or generate an individual chart
- **Dry-run capability**: allows users to see time and resources required to replicate a whole paper or individual asset.
- **Efficiency**: steps within workflows are run in parallel where possible, and users can opt to download results instead of regenerating them.


## Integration with Ecosystem
- 🔍 **CausalIQ Discovery** (causaliq-discovery) is called by this package to perform statistical structure learning.
- 📊 **CausalIQ Analysis** (causaliq-predict) is called by this package to perform results analysis and generate assets for research papers.
- 🔮 **CausalIQ Predict** (causaliq-predict) is called by this package to perform causal prediction.
- 🔄 **Zenodo Synchronisation** (zenodo-sync) is used by this package to download datasets and upload results.
- 🧠 **CausalIQ Knowledge** (causaliq-knowledge) can be integrated into causal discovery, analysis and inference workflows to produce more accurate, transparent and interpretable results.
- 🧪 **CausalIQ Workflow** (causaliq-workflow) orchestrates the steps required for the reproduction of experiments, results and
published paper assets created by the CausalIQ ecosystem.

<br />

---

*CausalIQ Research enables reproducible, transparent causal discovery research by providing curated experimental setups, benchmark datasets, and published results that support method comparison and the advancement of reliable causal inference methodologies.*
