# 🔢 CausalIQ Data Project

The CausalIQ Data project provides the data-related capabilities that causal
discovery requires. These are:

 - **data import and caching** - data can be imported from standard 
tabular formats (comma-separated variables) and cached for high performance
 - **graph scoring** - provide graph score derived from the data which is
 the objective function used by *score-based* structure learning algorithms. This is 
 based upon how likely the data is to be seen for a given graph, typically
 modified by a penalty for complex graphs (e.g. BIC score), or modified
 by a prior belief about the graph strcuture (e.g. BDeu score)
 - **independence tests** - used to determine conditional independence tests
 which are intrinsic to the operataion of *constraint-based* structure
 learning algorithms.


**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-data/)
- [💻 Repository](https://github.com/causaliq/causaliq-data)
- 🚀 Quick Start - coming soon

## Upcoming Key Innovations

### 🧩 Plugin Architecture
- **use by third-party software** - ability to use these data capabilities in third party structure learning algorithms so that comparisons are based on a common scoring or conditional independence framework, and performance optimisations speed up third-party algorithms.

### 🏛️ Stability Integration
- **Stable scores** - stable resolution of equal-score situations for unstable algorithms e.g. Tabu

### 🧠 LLM-assisted Causal Discovery
- **Data values** - Data values and variable names may provide part of the context for
LLM-assisted causal discovery
- **Knowledge integration** - incorporation of LLM and human expertise in scores and priors via the CausalIQ Knowledge package. 
- **Relationship explanations**: Natural language descriptions of relationships in data

### ⚡Optimised Performance
- **GPU Data provider** - support for optimised data handling on GPU hardware
- **Intelligent data scanning** - reduce number of full-row data scans

### 🎲 Enhanced Distribution Support
- **Mixed Types**: scores and independence tests that support mixtures of continuous and categorical variables


## Integration with CausalIQ Ecosystem

- 🔍 **CausalIQ Discovery** makes use of this package to provide objective functions and conditional independence
tests for structure learning algorithms.
- 🧪 **CausalIQ Analysis** uses score functions as part of the evaluation of learnt graphs.
- 💎 **CausalIQ Core** makes use of the BNFit interface to estimate parameters based on data.
- 🤖 **CausalIQ Workflow** uses the in-memory randomisation of this package for stability experiments.


<br/>

---

*CausalIQ Data represents the foundational data processing layer that enables robust, high-performance causal discovery through optimized scoring functions, conditional independence testing, and seamless integration across the entire CausalIQ ecosystem.*