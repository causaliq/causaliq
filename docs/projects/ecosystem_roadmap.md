# CausalIQ Ecosystem - Development Roadmap

*At-a-glance view of development releases across the CausalIQ ecosystem*

Last updated: April 11, 2026

## 🌟 Current Ecosystem Status on PyPI

| Project | Current Release | Project capabilities | Detailed Roadmap |
|---------|-----------------|----------------------|------------------|
| **causaliq** (umbrella)        | 0.1.0 | Ecosystem architecture and development standards defined | n/a |
| **causaliq-analysis** | 0.4.0  | Structural graph merging, metric evaluation and summarisation, and legacy learning traces | [here](https://causaliq.github.io/causaliq-analysis/roadmap/)
| **causaliq-core** | 0.7.0 | Utility functions, graph classes (SDG, PDAG, DAG, PDG), optimal DAG, Bayesian Networks, cache infrastructure and randomised filters | [here](https://causaliq.github.io/causaliq-core/roadmap/) |
| **causaliq-data** | 0.3.0 | Data handling, score functions and independence tests | [here](https://causaliq.github.io/causaliq-data/roadmap/)
| **causaliq-knowledge** | 0.6.0 | PDG generation and workflow integration | [here](https://causaliq.github.io/causaliq-knowledge/roadmap/) |
| **causaliq-repo-template** | 1.0.0 | Repo template for new CausalIQ projects | n/a |
| **causaliq-workflow**      | 0.5.0 | Workflow patterns, multi-step workflows, caches and conservative execution | [here](https://causaliq.github.io/causaliq-workflow/roadmap/) |
| **zenodo-sync**            | 0.1.0 | Follows CausalIQ standards | tbd | 

All other projects not yet released.

**Milestones:**

- end-April 2026: Charts and Tables for CausalIQ LLM-assisted model-averaging paper
- end-September 2026: Experiments and results for another paper
- end-2026: Full reproducibility of key published papers with assets on Zenodo

## 📊 Ecosystem Development Timeline

### April 2026 - Graph evaluation and summarisation

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-analysis** | 0.4.0 |  🚧 Underway | Evaluation and Summarisation: structural evaluation of graphs and result summarisation |
| **causaliq-analysis** | 0.5.0 |  📊 Planned | Publication Assets: table and chart generation for the PGM submission |
| **causaliq-research** | 0.1.0 | 🚧 Underway | PGM Workflows: Models and workflows to support PGM paper |


Code migrated from legacy monolithic repo will be modified to meet CausalIQ quality standards.

CausalIQ packages will implement the CausalIQAction interface and therefore can be included in CausalIQ Workflows


### May 2026 and beyond

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq-analysis** | Non-reference Evaluation | ✨ Envisaged | Evaluation that does not require reference graphs |
| **causaliq-analysis** | Statistical Significance | ✨ Envisaged | Based on January Experience |
| **causaliq-discovery** | Discovery Foundations | ✨ Envisaged | Migration of HC/Tabu-Stable |
| **causaliq-whatif** | Foundation Inference | ✨ Envisaged | Basic PyAgrum Inference |
| **causaliq-workflow** | Comparison capability | ✨ Envisaged | Comparison capability |
| **causaliq-knowledge** | Advanced Queries | ✨ Envisaged | Based on January Experience |


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