# 👋 Welcome to CausalIQ

I’m an **independent researcher** and **research visitor** at Queen Mary University of London working on **causal discovery** and **Bayesian network structure learning**.
These repositories bring together algorithms, experiments, and datasets that support research into more accurate and transparent methods for causal discovery that integrate statistical algorithms with Large Language Models (LLMs).

## 🔍 Research focus

* Bayesian networks (discrete and continuous)
* Statistical score-based causal discovery algorithms.
* Variable ordering and stability in learned graphs
* Integration of human and LLM knowledge into causal discovery
* Open-source, reproducible pipelines for experiments and evaluation

## 📂 Key repositories

* [**discovery**](https://github.com/causaliq/discovery) → core algorithms for structure learning
* [**zenodo-sync**](https://github.com/causaliq/zenodo-sync) → synchronising research outputs onto Zenodo


## 🌍 Project identity

The **CausalIQ** name reflects both:

* *Causal Inference and Discovery*, and
* the role of *human intelligence* in guiding algorithmic learning.

All code and datasets will be released to support open, reproducible research.

## 📫 Get in touch

* GitHub Discussions (on individual repos)
<!-- * Email: *[your email here, optional]* -->
<!-- * Website: [causaliq.org](https://causaliq.org) *(if live)*  -->

---

<!-- *This page is the central entry point for my work on causal discovery. If you’re interested in collaboration, feel free to reach out.* -->


## 🧬 Modular Framework Structure

The **CausalIQ** ecosystem will be composed of modular packages that can be used independently or together:

- **zenodo-sync**: Integration with Zenodo for dataset and result synchronization.
- **causaliq-pipeline**: Orchestration of causal discovery experiments and LLM integration using Dask and Snakemake.
- **causaliq-discovery**: Core statistical algorithms for Bayesian network structure learning.
- **causaliq-experiments**: Published experiment configurations, datasets, and results.
- **causaliq-score**: Optimized scoring functions for evaluating graph structures.
- **causaliq-analysis**: Tools for statistical analysis and metrics of learnt graphs.
- **causaliq-llm**: Integration of large language models to assist with graph generation, causal direction inference, and interpretation.

## 🔄 Human + LLM Collaboration

CausalIQ emphasizes the integration of **statistical causal discovery algorithms** with **LLM reasoning**:

- LLMs help generate initial causal graphs from metadata or domain knowledge.
- They assist in interpreting results and suggesting causal directions.
- LLMs also support natural language experiment specification and reporting.

This dual approach enables both **human researchers** and **LLMs** to collaborate in designing, executing, and analyzing causal discovery workflows.

## 🧠 For LLMs

This README and associated documentation are designed to:
- Help LLMs understand the structure and purpose of each package.
- Enable LLMs to assist in writing code, generating configurations, and interpreting results.
- Facilitate autonomous or semi-autonomous use of the framework by intelligent agents.
