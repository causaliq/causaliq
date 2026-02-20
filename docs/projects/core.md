# ⚙️ CausalIQ Core Project

The CausalIQ Core project provides the foundational infrastructure shared across the CausalIQ ecosystem. It contains graph classes, Bayesian Network support, caching infrastructure, and the action provider framework that enables workflow integration.

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-core/)
- [💻 Repository](https://github.com/causaliq/causaliq-core)

## Key Components

### 📊 Graph Classes
Typed graph representations for causal discovery:

- **DAG** (Directed Acyclic Graph): Fully directed causal graphs
- **PDAG** (Partially Directed Acyclic Graph): Mixed directed/undirected edges representing Markov equivalence classes
- **SDG** (Summary Dependence Graph): Undirected graphs representing conditional dependencies
- **Conversion utilities**: Transform between graph types with validation
- **I/O support**: Read/write Tetrad and Bayesys CSV formats

### 🔢 Bayesian Networks
Support for parameterised Bayesian Networks:

- **BN class**: Bayesian Network structure with CPT parameters
- **Distribution types**: Discrete and continuous variable support
- **I/O formats**: DSC and XDSL file format support

### 💾 Caching Infrastructure
Token-based caching with compression for efficient storage:

- **TokenCache**: SQLite-backed cache with shared token dictionary
- **Compressor framework**: Pluggable compression for different data types
- **JsonCompressor**: Tokenised JSON compression (50-70% size reduction)
- **GraphMLCompressor**: Efficient graph serialisation

### 🤖 Action Provider Framework
Infrastructure for CausalIQ Workflow integration:

- **CausalIQActionProvider**: Base class for workflow actions
- **ActionInput/ActionOutput**: Typed action parameters
- **ActionResult**: Standardised action return values
- **Entry point discovery**: Automatic action registration

## Usage Across Ecosystem

CausalIQ Core is a dependency of most CausalIQ packages:

| Package | Core Usage |
|---------|------------|
| **causaliq-knowledge** | TokenCache for LLM response caching, graph classes |
| **causaliq-analysis** | Graph classes, BN support, caching |
| **causaliq-workflow** | Action provider framework |
| **causaliq-data** | Graph classes, caching infrastructure |
| **causaliq-discovery** | Graph classes, BN support |

## Quick Start

```python
from causaliq_core.graph import PDAG, DAG, read, write

# Create a partially directed graph
pdag = PDAG(
    ['X', 'Y', 'Z'],
    [('X', '->', 'Y'), ('Y', '--', 'Z')]
)

# Convert to DAG (if possible)
dag = pdag.to_dag()

# Save and load graphs
write(pdag, "my_graph.csv")  # Bayesys format
loaded = read("my_graph.csv")
```

```python
from causaliq_core.cache import TokenCache

# Create persistent cache
with TokenCache("my_cache.db") as cache:
    cache.put("key1", "type", b"data")
    data = cache.get("key1", "type")
```

<br/>

---

*CausalIQ Core provides the foundational building blocks that enable consistent, efficient, and interoperable functionality across the entire CausalIQ ecosystem.*
