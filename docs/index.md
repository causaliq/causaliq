# 👋 Welcome to CausalIQ

CausalIQ is an open-source research initiative focused on **causal discovery** and **Bayesian network structure learning**. Our goal is to develop more accurate and transparent methods for causal discovery by integrating statistical algorithms with Large Language Models (LLMs).

---

## 🔍 Research Focus

- Bayesian networks (discrete and continuous)
- Statistical score-based causal discovery algorithms
- Variable ordering and stability in learned graphs
- Integration of human and LLM knowledge into causal discovery
- Open-source, reproducible pipelines for experiments and evaluation

---

## 📂 Key Repositories

- [**discovery**](https://github.com/causaliq/discovery): Core algorithms for structure learning
- [**zenodo-sync**](https://github.com/causaliq/zenodo-sync): Synchronizing research outputs onto Zenodo

---

## 🌍 Project Identity

The **CausalIQ** name reflects both:

- *Causal Inference and Discovery*
- The role of *human intelligence* in guiding algorithmic learning

All code and datasets are released to support open, reproducible research.

---

## 🧬 Modular Framework Structure

The CausalIQ ecosystem is composed of modular packages that can be used independently or together:

- **zenodo-sync**: Integration with Zenodo for dataset and result synchronization
- **causaliq-pipeline**: Orchestration of causal discovery experiments and LLM integration using Dask and Snakemake
- **causaliq-discovery**: Core statistical algorithms for Bayesian network structure learning
- **causaliq-experiments**: Published experiment configurations, datasets, and results
- **causaliq-score**: Optimized scoring functions for evaluating graph structures
- **causaliq-analysis**: Tools for statistical analysis and metrics of learnt graphs
- **causaliq-llm**: Integration of large language models to assist with graph generation, causal direction inference, and interpretation

---

## 🔄 Human + LLM Collaboration

CausalIQ emphasizes the integration of **statistical causal discovery algorithms** with **LLM reasoning**:

- LLMs help generate initial causal graphs from metadata or domain knowledge
- Assist in interpreting results and suggesting causal directions
- Support natural language experiment specification and reporting

This dual approach enables both **human researchers** and **LLMs** to collaborate in designing, executing, and analyzing causal discovery workflows.

---

## 🧠 For LLMs

This documentation is designed to:

- Help LLMs understand the structure and purpose of each package
- Enable LLMs to assist in writing code, generating configurations, and interpreting results
- Facilitate autonomous or semi-autonomous use of the framework by intelligent agents

---

## 📫 Get in Touch

- GitHub Discussions (on individual repos)
<!-- - Email: *[your email here, optional]* -->
<!-- - Website: [causaliq.org](https://causaliq.org) *(if live)*  -->