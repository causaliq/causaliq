# ⚙️ CausalIQ Core Project

The CausalIQ Core project provides the foundational infrastructure shared across the CausalIQ ecosystem. It contains graph classes, Bayesian Network support, caching infrastructure, and the action provider framework that enables workflow integration.

**Current Version**: v0.7.0

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-core/)
- [💻 Repository](https://github.com/causaliq/causaliq-core)

## Key Components

### 📊 Graph Classes
Typed graph representations — DAG, PDAG, PDG (probabilistic), and SDG (undirected) — with conversion utilities, validation, and I/O support for Tetrad CSV, Bayesys CSV, and GraphML formats.

### 🔢 Bayesian Networks
Parameterised Bayesian Network support with CPT parameters for discrete and continuous variables, and DSC/XDSL file format I/O.

### 💾 Caching Infrastructure
SQLite-backed `TokenCache` with a shared token dictionary and pluggable compressors (JSON tokenisation achieving 50–70% size reduction, and GraphML serialisation).

### 🤖 Action Provider Framework
Base class and type-safe interfaces for CausalIQ Workflow actions, with formalised CREATE, UPDATE, and AGGREGATE execution patterns and automatic entry-point discovery.

### 🔍 Filter and Weight Expressions
Safe expression evaluation against cache entry metadata, supporting logical filters, `random()` sampling, and metadata-driven aggregation weights.

### 🛠️ Utilities
Shared cross-cutting concerns including stable cross-platform RNG, mathematical helpers, timing tools, environment detection, and enhanced enumerations.

## Usage Across Ecosystem

CausalIQ Core is a dependency of most CausalIQ packages:

| Package | Core Usage |
|---------|------------|
| **causaliq-knowledge** | TokenCache for LLM response caching, graph classes |
| **causaliq-analysis** | Graph classes, BN support, caching, filter expressions |
| **causaliq-workflow** | Action provider framework, caching, filter evaluation |
| **causaliq-data** | Graph classes, caching infrastructure |
| **causaliq-discovery** | Graph classes, BN support |

<br/>

---

*CausalIQ Core provides the foundational building blocks that enable consistent, efficient, and interoperable functionality across the entire CausalIQ ecosystem.*
