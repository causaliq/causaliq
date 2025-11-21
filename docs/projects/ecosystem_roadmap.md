# CausalIQ Ecosystem - Development Roadmap

*At-a-glance view of development releases across the CausalIQ ecosystem*

Last updated: November 21, 2025

## 🌟 Current Ecosystem Status

| Project | Current Release | Project capabilities | Detailed Roadmap |
|---------|-----------------|----------------------|------------------|
| **causaliq** (Main)        | 0.1 Architecture | Architecture and development standards defined | n/a |
| **causaliq-workflow**      | 0.2 Basic CLI | Basic CLI with real-time execution feedback | [here](https://causaliq.github.io/causaliq-workflow/roadmap/) |
| **zenodo-sync**            | 0.1 Foundation | Follows CausalIQ standards | tbd | 
| **causaliq-repo-template** | 1.0 Foundation |Defines standardised project docs, structure and CI testing | n/a |

All other projects not yet started.

**Milestones:**

- end-March 2026: CausalIQ LLM-assisted model-averaging experiments & results for conference paper
- end-April 2026: Charts and Tables for CausalIQ LLM-assisted model-averaging paper
- end-September 2026: Experiments and results for another paper
- end-2026: Full reproducibility of key published papers with assets on Zenodo

## 📊 Ecosystem Development Timeline

### November 2025 - Reproducible Development, Monolith Migration and Workflow started

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causaliq** | 0.1 Foundation | ✅ Complete | Architecture and development standards defined |
| **causal-core** | 0.1 Foundation | 📝 Planned | Common path, enum, random, math functions from monolith |
| **causal-core** | 0.2 Graphs | 📝 Planned | General, PDAG and DAGs from monolith ||
| **causaliq-workflow** | 0.2 Basic CLI | ✅ Complete | Command-line interface, Action registry, Workflow execution |
| **causaliq-workflow** | 0.3 Enhanced Workflow | 📝 Planned | Conservative execution and dry-run capability |
| **zenodo-sync** | 0.1 Foundation | ✅ Complete | Follows CausalIQ standards, Deposit constructor |
| **causaliq-repo-template** | 1.0 Foundation | ✅ Complete | MkDocs, Project structure & CI Testing Template |

Code migrated from legacy monolithic repo will be modifiied to meet CausalIQ quality standards.

### December 2025 - Graph Metrics and Averaging 

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causal-analysis** | 0.1 Foundation | ✨ Envisaged | Action interface supported |
| **causal-analysis** | 0.2 Structural Metrics | ✨ Envisaged | Structural graph metrics from monolith |
| **causal-analysis** | 0.3 Graph Averaging | ✨ Envisaged | Probabilistic graph averaging |
| **causal-core** | 0.3 Input/Output | 📝 Planned | Graph file formats including GraphML |
| **causal-papers** | 0.1 Import graph | ✨ Envisaged | Import graphs from monolithic repo |
| **causaliq-workflow** | 0.4 Progress and Summary | ✨ Envisaged | Real-time progress tracking and execution summary |

CausalIQ packages (excluding core) will implement the CausalIQ Action interface and therefore can be included in CausalIQ Workflows

### January 2026 - LLM Causal Knowledge I

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causal-analysis** | 0.4 Averaging Analysis | ✨ Envisaged | Basic analysis of graph averaging |
| **causal-knowledge** | 0.1 Foundation | ✨ Envisaged | Requirements and technical architecture |
| **causal-knowledge** | 0.2 LLM APIs | ✨ Envisaged | Some LLMs integrated |
| **causal-knowledge** | 0.3 Simple Edge Queries | ✨ Envisaged | Simple Edge Queries - existence/orientation |
| **causal-knowledge** | 0.4 Query Database | ✨ Envisaged | Query, context, response stored |
| **causaliq-workflow** | 0.5 Advanced Features | ✨ Envisaged | Metadata, compare mode, timeouts, estimated completion |


### February 2026 - LLM Causal Knowledge II

| Project | Release | Status | Key Deliverables |
|---------|---------|--------|------------------|
| **causal-analysis** | 0.4 LLM Analysis | ✨ Envisaged | Based on January Experience |
| **causal-knowledge** | 0.5 Advanced Queries | ✨ Envisaged | Based on January Experience |

## 🚀 Future Vision Post February 2026

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