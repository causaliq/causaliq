# � CausalIQ Analysis Project

The CausalIQ Analysis project provides tools for analysing causal discovery
results, including structural evaluation metrics, graph merging, optimal DAG
extraction, and metric summarisation.

**Current Version**: v0.4.0

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-analysis/)
- [💻 Repository](https://github.com/causaliq/causaliq-analysis)

## Key Features

### 📏 Structural Evaluation (`evaluate_graph`)
Compare learned graphs against ground truth using standard metrics (F1, precision, recall, SHD) and equivalence class metrics, with support for multiple graph formats. Available as CLI and workflow action.

### 🎯 Optimal DAG Extraction (`best_graph`)
Extract the best DAG from a Probabilistic Dependency Graph using a greedy algorithm with configurable edge probability thresholds. Available as CLI and workflow action.

### 📊 Metric Summarisation (`summarise`)
Aggregate metrics across experiments into publication-ready CSV tables with configurable summary statistics and filter expressions. Available as CLI and workflow action.

### 🔗 Graph Merging (`merge_graphs`)
Combine multiple learned graphs into a single PDG using average, noisy-OR, or max strategies with optional metadata-driven weights. Available as CLI and workflow action.

### 🔄 Trace Migration (`migrate_trace`)
Convert legacy experiment traces (pickle format) to modern GraphML and JSON metadata, with filtering by sample size and seeds. Available as CLI and workflow action.

### 📐 Foundation Metrics
CausalIQ and Bayesys structural graph metrics and KL divergence metric.

## Upcoming Key Innovations

### 🧠 LLM-assisted Graph Averaging
- **Uncertain or conflicting edges** — resolved using LLM queries

### 📊 Publication-ready chart generation
- **Seaborn charts** — flexible, standardised publication-ready chart generation

### ▦ Publication-ready table generation
- **LaTeX tables** — converts tabular analysis data into publication-ready LaTeX tables

## Integration with CausalIQ Ecosystem

- 🔍 **CausalIQ Discovery** generates causal graphs which this package evaluates and visualises.
- 🤖 **CausalIQ Workflow** can access all features of this package (through the Action interface) so that analysis and visualisation are incorporated into CausalIQ workflows.
- 🧪 **CausalIQ Research** uses the analysis, table and chart features of this package to generate published paper assets.

<br/>

---

*CausalIQ Analysis provides the analytical foundation for evaluating, comparing, and summarising causal discovery results across the entire CausalIQ ecosystem.*