# 🧠 CausalIQ Knowledge Project

The CausalIQ Knowledge project represents a novel approach to causal discovery by combining the traditional statistical structure learning algorithms with the contextual understanding and reasoning capabilities of Large Language Models. This integration enables more interpretable, domain-aware, and human-friendly causal discovery workflows.

**Current Version**: v0.6.0

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-knowledge/)
- [💻 Repository](https://github.com/causaliq/causaliq-knowledge)

## Key Features

### 🧠 LLM Graph Generation (`generate_graph`)
Generate causal PDGs from network context specifications using any of 7 LLM providers (OpenAI, Anthropic, Groq, DeepSeek, Mistral, Gemini, Ollama), with multi-sampling via `llm_seed` and semantic variable name disguising. Available as CLI and workflow action.

### 💾 Response Caching
SQLite-based query and response caching for stable, reproducible LLM experiments, with provider-specific limits, CLI cache management tools, and automatic recovery from malformed LLM responses.

### 🔌 Direct Vendor API Clients
Lightweight LLM integration using direct vendor APIs via `httpx` — no LiteLLM or LangChain wrappers — for full control and easy debugging.

## Future Directions

### 🤝 Human Engagement
- **Natural language constraints**: Specify domain knowledge in plain English
- **Expert knowledge incorporation** by converting expert understanding into algorithmic constraints
- LLMs convert **natural language questions** to causal queries
- **Interactive causal discovery** where structure learning or LLMs identify areas of causal uncertainty and can test causal hypotheses through dialogue

### 🪟 Transparency and Interpretability
- LLMs **interpret structure learning process** and outputs, including their uncertainties
- LLMs **interpret causal inference** results including uncertainties
- **Contextual graph interpretation** to explain variable meanings and relationships
- **Uncertainty communication** with clear explanation of confidence levels and limitations
- **Report generation** including automated research summaries and methodology descriptions

### 🔒 Stability and Reproducibility
- **Stable randomisation** of e.g. data sub-sampling
- Evaluation and development of **simple context-adapted LLMs**

## Integration with Ecosystem

- 🔍 **CausalIQ Discovery** makes use of this package to learn more accurate graphs.
- 📊 **CausalIQ Analysis** uses graph averaging from causaliq-analysis to resolve uncertain edges identified by this package.
- 🔮 **CausalIQ WhatIf** uses this package to explain predictions made by learnt models.
- 🤖 **CausalIQ Workflow** executes graph generation as workflow steps with cache integration.

<br/>

---

*CausalIQ Knowledge bridges the gap between statistical rigour and domain expertise, enabling more intelligent, interpretable, and human-collaborative approaches to causal discovery.*