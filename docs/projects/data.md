# � CausalIQ Data Project

The CausalIQ Data project provides the data handling, statistical testing, and scoring infrastructure that causal discovery requires. It delivers plug-in data adapters, comprehensive score functions, and conditional independence tests used by structure learning algorithms.

**Current Version**: v0.3.0

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-data/)
- [💻 Repository](https://github.com/causaliq/causaliq-data)

## Key Features

### 🔌 Plug-in Data Adapters
Abstract `Data` base class with Pandas, NumPy, and Oracle (synthetic) adapters, supporting CSV I/O, data randomisation, and categorical/continuous variable types.

### 📊 Score Functions
Comprehensive scoring framework with entropy-based (BIC, AIC, log-likelihood), Bayesian (BDE, K2, BDJ, BDS), and Gaussian (BGE, BIC-g, loglik-g) score types, evaluated at node, DAG, or full network level.

### 🧪 Independence Tests
Chi-squared and Mutual Information tests for conditional independence (X ⊥ Y | Z), designed for constraint-based algorithms such as PC and FCI.

### 🔧 Preprocessing and Utilities
Data cleaning utilities, BNFit interface for Bayesian Network parameter fitting, and marginal computation.

## Future Directions

### 🧩 Plugin Architecture
- **Third-party integration**: Ability to use these data capabilities in third-party structure learning algorithms so that comparisons are based on a common scoring or conditional independence framework

### 🏛️ Stability Integration
- **Stable scores**: Stable resolution of equal-score situations for unstable algorithms (e.g. Tabu)

### 🧠 LLM-assisted Causal Discovery
- **Data context**: Data values and variable names as context for LLM-assisted causal discovery
- **Knowledge integration**: Incorporation of LLM and human expertise in scores and priors via CausalIQ Knowledge

### ⚡ Optimised Performance
- **GPU data provider**: Support for optimised data handling on GPU hardware
- **Intelligent data scanning**: Reduce number of full-row data scans

### 🎲 Enhanced Distribution Support
- **Mixed types**: Scores and independence tests supporting mixtures of continuous and categorical variables

## Integration with CausalIQ Ecosystem

- 🔍 **CausalIQ Discovery** makes use of this package to provide objective functions and conditional independence tests for structure learning algorithms.
- 📊 **CausalIQ Analysis** uses score functions as part of the evaluation of learnt graphs.
- 💎 **CausalIQ Core** makes use of the BNFit interface to estimate parameters based on data.
- 🤖 **CausalIQ Workflow** uses the in-memory randomisation of this package for stability experiments.

<br/>

---

*CausalIQ Data provides the foundational data processing layer that enables robust, high-performance causal discovery through optimised scoring functions, conditional independence testing, and seamless integration across the entire CausalIQ ecosystem.*