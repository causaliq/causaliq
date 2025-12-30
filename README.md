# 👋 Welcome to CausalIQ

I’m an **independent researcher** and **research visitor** at Queen Mary University of London working on **causal discovery** and **Bayesian network structure learning**.
The CausalIQ ecosystem brings together algorithms, experiments, and datasets that support research into more accurate and transparent methods for causal discovery that integrate statistical algorithms with Large Language Models (LLMs).

## 🔍 Research focus

* Bayesian networks (discrete and continuous)
* Statistical score-based causal discovery algorithms.
* Variable ordering and stability in learned graphs
* Integration of human and LLM knowledge into causal discovery
* Open-source, reproducible workflows for experiments and evaluation

## 📂 Constituent Projects

Currently underway:

* [**CausalIQ Analysis**](https://github.com/causaliq/causaliq-analysis) → provides tools to evaluate structure learning experiments and generate publication-ready charts and tables.
* [**CausalIQ Data**](https://github.com/causaliq/causaliq-data) → optimised data handling, statistical testing, and scoring infrastructure for causal discovery and Bayesian network operations.
* [**CausalIQ Workflow**](https://github.com/causaliq/causaliq-workflow) → orchestration of causal discovery and inference, and analysis with LLM integration.
* [**Zenodo Sync**](https://github.com/causaliq/zenodo-sync) → synchronise local research data and results with Zenodo for reproducible science. CLI and API to upload, publish and download assets.

Coming soon:

* **CausalIQ Discovery** → provides algorithms for learning causal graph structures from observational data. There is a focus on simple, stable and competitive algorithms.
* **CausalIQ Knowledge** → combines the traditional statistical structure learning algorithms with the contextual understanding and reasoning capabilities of Large Language Models. This integration enables more interpretable, domain-aware, and human-friendly causal discovery workflows.
* **CausalIQ Papers** → uses the other projects to reproduce all experiments and results in published CausalIQ papers.


## 🌍 Project identity

The **CausalIQ** name reflects both:

* *Causal Inference and Discovery*, and
* the role of *human intelligence* in guiding algorithmic learning.

All code and datasets will be released to support open, reproducible research.

## 📫 Get in touch

* GitHub Discussions (on individual repos)
* Email: info@causaliq.org
* Website: [causaliq.org](https://causaliq.org)

---

<!-- *This page is the central entry point for my work on causal discovery. If you’re interested in collaboration, feel free to reach out.* -->


## 🧬 Modular Ecosystem Structure

The **CausalIQ** ecosystem will be provided as a set of Python packages (each with its own associated GitHub repo) which can be used independently or together as desired.

Under development:

- [**causaliq**](https://github.com/causaliq/causaliq) - public website providing documentation entry point to the CausalIQ ecossystem.
- [**causaliq-analysis**](https://github.com/causaliq/causaliq-analysis) - Tools for statistical analysis and metrics of learnt graphs.
- [**causaliq-core**](https://github.com/causaliq/causaliq-core) - common software used by other CausalIQ packages. Currently includes classes for graphs as well as utility methods.
- [**causaliq-data**](https://github.com/causaliq/causaliq-data) - development just beginning
- [**causaliq-workflow**](https://github.com/causaliq/causaliq-workflow) - supports Continuous Integration testing style workflows, but not yet integrated with any other CausalIQ packages.
- [**zenodo-sync**](https://github.com/causaliq/zenodo-sync) - Zenodo upload being developed

Starting soon:

- **causaliq-discovery** - Core statistical algorithms for Bayesian network structure learning.
- **causaliq-knowledge** - Integration of large language models, human expertise etc. to assist with graph generation, causal direction inference, and interpretation.
- **causaliq-papers** - Experiment configurations, datasets, and results for published papers.

Legacy code:

- [**discovery**](https://github.com/causaliq/discovery) - a monolithic legacy codebase underlying the currently published work which is being migrated into the individual CausalIQ packages.


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
