# CausalIQ Ecosystem - Development Roadmap

*At-a-glance view of development releases across the CausalIQ ecosystem*

Last updated: February 01, 2026

## 🌟 Current Ecosystem Status

| Project | Current Release | Project capabilities | Detailed Roadmap |
|---------|-----------------|----------------------|------------------|
| **causaliq** (umbrella)        | 0.1 Architecture | Ecosystem architecture and development standards defined | n/a |
| **causaliq-analysis** | 0.2 Legacy trace | Structural graph metrics and legacy learning traces | [here](https://causaliq.github.io/causaliq-analysis/roadmap/)
| **causaliq-core** | 0.3 Bayesian Networks | Utility functions, graph classes (SDG, PDAG, DAG) and Bayesian Networks | [here](https://causaliq.github.io/causaliq-core/roadmap/) |
| **causaliq-data** | 0.3 Independence Tests | Data handling, score functions and independence tests | [here](https://causaliq.github.io/causaliq-data/roadmap/)
| **causaliq-knowledge** | 0.3 LLM Caching | LLM query and response caching | [here](https://causaliq.github.io/causaliq-knowledge/roadmap/) |
| **causaliq-repo-template** | 1.0 Foundation | Repo template for new CausalIQ projects | n/a |
| **causaliq-workflow**      | 0.1 Workflow Foundations | Basic workflow framework | [here](https://causaliq.github.io/causaliq-workflow/roadmap/) |
| **zenodo-sync**            | 0.1 Foundation | Follows CausalIQ standards | tbd | 

All other projects not yet released.

**Milestones:**

- end-March 2026: CausalIQ LLM-assisted model-averaging experiments & results for conference paper
- end-April 2026: Charts and Tables for CausalIQ LLM-assisted model-averaging paper
- end-September 2026: Experiments and results for another paper
- end-2026: Full reproducibility of key published papers with assets on Zenodo

## 📊 Ecosystem Development Timeline

### February 2026 - Graph averaging and LLM Knowledge

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-analysis** | 0.3 Graph Averaging | 📊 Planned | Probabilistic graph averaging |
| **causaliq-analysis** | 0.4 Averaging Analysis | ✨ Envisaged | Basic analysis of graph averaging |
| **causaliq-core** | 0.4 Caching and GraphML | 📊 Planned | Generic caching and GraphML support |
| **causaliq-research** | 0.1 Foundation Models | 🚧 Underway | Models to support PGM paper |
| **causaliq-workflow** | 0.2 Knowledge Workflows | 📊 Planned | LLM graph generation workflow |
| **causaliq-workflow** | 0.3 Result Caching | 📊 Planned | Graph generation results cached |
| **causaliq-workflow** | 0.4 Analysis Workflows | 📊 Planned | Graph evaluation and averaging workflows |

Code migrated from legacy monolithic repo will be modified to meet CausalIQ quality standards.

CausalIQ packages will implement the CausalIQAction interface and therefore can be included in CausalIQ Workflows


### March 2026 - LLM Context and Averaging Evaluation

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-analysis** | 0.5 Non-reference Evaluation | ✨ Envisaged | Evaluation that does not require reference graphs |
| **causaliq-knowledge** | 0.4 LLM Context | ✨ Envisaged | Variable, domain and literature context |


### April 2026 - Graph Averaging Analysis

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-analysis** | 0.6 Analysis Plots | ✨ Envisaged | Based on January Experience |
| **causaliq-discovery** | 0.1 Discovery Foundations | ✨ Envisaged | Migration of HC/Tabu-Stable |
| **causal-predict** | 0.1 Foundation Inference | ✨ Envisaged | Basic PyAgrum Inference |
| **causaliq-workflow** | 0.5 Enhanced Workflow | 🔄 Background | Comparison and dry-run capability |

### Q2 2026 - Graph Averaging Production

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-knowledge** | 0.5 Advanced Queries | ✨ Envisaged | Based on January Experience |


### H2 2026 - Complete Legacy Support


## 🚀 Future Vision Post 2026

### Research Platform Features
- **LLM Integration:** Model averaging, hypothesis generation with causal reasoning
- **Web Interface:** Browser-based workflow designer for non-technical researchers  
- **Publication Support:** Reproducible research outputs with automated documentation

### Advanced Capabilities
- **Workflow Marketplace:** Sharing and discovering research workflow templates
- **Interactive Notebooks:** Jupyter integration with workflow execution
- **Multi-machine Execution:** Distributed workflows across compute clusters
- **AI-assisted Optimisation:** Automated hyperparameter and workflow tuning
- **Integration Ecosystem:** Plugins for major research tools and platforms

### Performance & Scale
- **High-performance Computing:** GPU acceleration for large-scale structure learning
- **Distributed Storage:** Cloud-native knowledge bases with global accessibility
- **Real-time Analytics:** Live causal discovery with streaming data sources
- **Enterprise Features:** Security, compliance, and enterprise-grade deployment

---

*This roadmap is updated weekly and reflects current development priorities. For detailed project-specific roadmaps, see individual project documentation.*