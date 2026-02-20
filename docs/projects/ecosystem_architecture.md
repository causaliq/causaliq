# CausalIQ Ecosystem Architecture

## Overview

The CausalIQ ecosystem is designed as a modular framework for causal discovery research that seamlessly integrates statistical algorithms with Large Language Models (LLMs). The architecture emphasizes modularity, reproducibility, and human-AI collaboration to advance the field of causal inference and Bayesian network structure learning.

## Architecture Principles

### 🔧 Modularity
Each project can be used independently, allowing researchers to adopt specific components without requiring the entire ecosystem.

### 🔗 Interoperability
Projects integrate seamlessly through standardized APIs, data formats, and shared configuration patterns.

### 🔬 Reproducibility
Open-source design with versioned datasets, experiment configurations, and results synchronized via Zenodo.

### 🤝 Human-AI Collaboration
Statistical causal discovery algorithms are enhanced by LLM reasoning for interpretation, direction inference, and domain knowledge integration.

## Ecosystem Components

### Core Projects

```
causaliq-research (Datasets, experiments and results for papers)
├── causaliq-workflow (Orchestration & workflow management)
├── causaliq-discovery (Statistical algorithms & structure learning)
├── causaliq-data (Optimized data caching, score functions and independence tests)
├── causaliq-analysis (Metrics & statistical analysis)
├── causaliq-knowledge (LLM integration & reasoning)
├── causaliq-predict (Using causal models for prediction)
├── causaliq-core (Graphs, Bayesian Networks and utilities)
└── zenodo-sync (Dataset & result synchronization)
```

### Project Responsibilities

| Project | Purpose | Key Features |
|---------|---------|--------------|
| **causaliq-discovery** | Core statistical algorithms | Statististical algorithms to learn causal models |
| **causaliq-data** | Data related functions | Data caching, scoring and indepedence tests |
| **causaliq-analysis** | Result analysis | Metrics, stability analysis, graph comparison |
| **causaliq-knowledge** | LLM integration | Graph generation, causal direction inference |
| **causaliq-workflow** | Workflow orchestration | CI workflow inspired, DASK task management |
| **causaliq-research** | Research outputs | Published configurations, datasets, results |
| **causaliq-predict**  | Causal prediction | Using causal models to predict and answer counterfactuals |
| **causaliq-core** | Shared code | Graph representations and utility functions |
| **zenodo-sync** | Data management | Automated synchronization with Zenodo |

## Data Flow Architecture

### 1. Input Stage
- **Raw datasets**: Observational and experimental data
- **Domain knowledge**: Expert-provided causal relationships
- **LLM priors**: Generated initial graphs from metadata
- **Configuration**: Experiment parameters and algorithm settings

### 2. Processing Stage
- **Statistical learning**: Score-based structure learning algorithms
- **LLM guidance**: Causal direction suggestions and constraint generation
- **Hybrid reasoning**: Integration of statistical evidence with domain knowledge
- **Optimization**: Graph search and scoring function evaluation

### 3. Evaluation Stage
- **Scoring**: BIC, AIC, BDeu, and custom metrics
- **Stability analysis**: Bootstrap sampling and edge confidence
- **Comparison**: Against ground truth and baseline methods
- **Validation**: Cross-validation and holdout testing

### 4. Output Stage
- **Learned graphs**: Final Bayesian network structures
- **Metrics**: Performance statistics and confidence measures
- **Interpretations**: LLM-generated explanations and insights
- **Reports**: Automated analysis summaries

### 5. Storage Stage
- **Version control**: Git-based experiment tracking
- **Zenodo sync**: Automated dataset and result archival
- **Metadata**: Rich annotations for reproducibility

## Integration Patterns

### API Standards
- **Graph representation**: NetworkX-compatible formats
- **Data interfaces**: Pandas DataFrame standards
- **Configuration**: YAML/JSON schema validation
- **Scoring**: Consistent function signatures

### Communication Protocols
- **Inter-project**: REST APIs and message queues
- **LLM integration**: OpenAI-compatible interfaces
- **Workflow**: Dask distributed computing
- **Storage**: Cloud-native object storage

### Shared Data Structures
```python
# Example graph representation
graph = {
    "nodes": ["X1", "X2", "X3"],
    "edges": [("X1", "X2"), ("X2", "X3")],
    "metadata": {
        "algorithm": "pc",
        "score": "bic",
        "confidence": 0.95
    }
}
```

## LLM Integration Architecture

### 🧠 LLM Capabilities
- **Graph generation**: Initial structures from domain descriptions
- **Causal direction**: Arrow orientation suggestions
- **Interpretation**: Natural language explanations
- **Constraint generation**: Domain-informed restrictions
- **Report writing**: Automated experimental summaries

### 🔄 Human-LLM Workflow
1. **Human specification**: Natural language experiment description
2. **LLM parsing**: Structured configuration generation
3. **Statistical learning**: Algorithm execution with LLM constraints
4. **LLM interpretation**: Results explanation and insights
5. **Human validation**: Expert review and refinement

## Deployment Patterns

### 🔬 Research Environment
- **Local development**: Individual project installation
- **Jupyter integration**: Interactive analysis notebooks
- **Academic clusters**: HPC job submission

### ☁️ Cloud Deployment
- **Container orchestration**: Docker/Kubernetes
- **Serverless functions**: Event-driven processing
- **Managed services**: Cloud-native ML platforms

### 🏢 Enterprise Integration
- **API gateways**: Secure external access
- **Data pipelines**: ETL/ELT integration
- **Monitoring**: Observability and logging

## Caching Architecture

CausalIQ uses a unified caching strategy to avoid redundant computation,
reduce costs, and ensure reproducibility of results over time.

### Design Goals

| Goal | Description |
|------|-------------|
| **Avoid re-computation** | Expensive operations (LLM queries, structure learning) are cached |
| **Reproducibility** | Cached results can be replicated years later despite LLM evolution |
| **Compact storage** | SQLite with tokenised encoding minimises filesystem footprint |
| **Fast lookup** | Quick existence checks support conservative workflow execution |
| **Open formats** | Import/export to JSON, GraphML, CSV for archival and sharing |
| **Flexibility** | Single cache can hold multiple entry types without schema changes |

### Cache Types

| Cache | Purpose | Typical Size |
|-------|---------|--------------|
| **LLM Cache** | Store LLM request/response pairs to reduce API costs | 10K-100K entries |
| **Workflow Cache** | Store workflow step results (graphs, metrics, traces) | 1K-10K entries |

Note: "Workflow Cache" refers specifically to caches storing workflow results,
as distinct from LLM Caches which store API request/response pairs.

### Common Infrastructure

All caches share common infrastructure in `causaliq-core`:

- **TokenCache**: SQLite-backed storage with shared token dictionary
- **EntryEncoder**: Abstract interface for type-specific encoding
- **JsonEncoder**: Tokenised JSON compression (50-70% compression)

Type-specific encoders (e.g., `LLMEntryEncoder`, `GraphEntryEncoder`) extend
the base infrastructure for domain-specific data structures.

### Cache Entry Structure

Each cache entry consists of:

- **Hash key + sequence**: `(hash, seq)` composite key handles rare hash collisions
- **Original key JSON**: Stored for collision detection and verification
- **Data blobs**: One or more type-specific encoded objects (graph, trace, etc.)
- **Metadata blob**: JSON with provenance, metrics, and type-specific attributes

### Hash Collision Handling

Cache keys use truncated SHA-256 hashes (64-bit). While collisions are rare,
all caches handle them safely:

- `seq` column allows multiple entries with same hash
- `key_json` stores original key for exact matching
- On insert: match existing key → update; hash collision → use next `seq`
- On lookup: scan entries with matching hash, return exact key match

### Import/Export

Caches support round-trip conversion to open formats:

- **Export**: Convert cache entries to directories of JSON, GraphML, CSV files
- **Import**: Populate caches from open format files (e.g., test fixtures)

This bridges the tension between efficient internal storage and standards-based
archival formats suitable for Zenodo publication.

## Quality Assurance

### Testing Strategy
- **Unit tests**: Individual function validation
- **Integration tests**: Cross-project compatibility
- **Performance tests**: Scalability benchmarks
- **Reproducibility tests**: Result consistency validation

### Documentation Standards
- **API documentation**: OpenAPI specifications
- **User guides**: Getting started tutorials
- **Developer docs**: Contribution guidelines
- **Research papers**: Algorithmic foundations

## Future Extensions

### Planned Enhancements
- **Real-time learning**: Streaming data processing
- **Federated learning**: Distributed causal discovery
- **Multi-modal data**: Text, images, time series
- **Causal reasoning**: Counterfactual inference

### Research Directions
- **LLM fine-tuning**: Domain-specific causal models
- **Active learning**: Experimental design optimization
- **Uncertainty quantification**: Bayesian model averaging
- **Scalability**: Large-scale graph learning

---

*This architecture document provides the blueprint for the CausalIQ ecosystem, enabling both human researchers and LLMs to understand and contribute to the framework's development and application.*