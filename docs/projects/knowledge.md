# 🧠 CausalIQ Knowledge Project

The CausalIQ Knowledge project represents a novel approach to causal discovery by combining the traditional statistical structure learning algorithms with the contextual understanding and reasoning capabilities of Large Language Models. This integration enables more interpretable, domain-aware, and human-friendly causal discovery workflows.

**Quick Links:**

- [📖 Full Documentation](https://causaliq.github.io/causaliq-knowledge/)
- [💻 Repository](https://github.com/causaliq/causaliq-knowledge)
- 🚀 Quick Start - coming soon

## Possible Key Innovations

### 🧠 LLMs support Causal Discovery and Inference
- initially LLM will work with **graph averaging** to resolve uncertain edges (use entropy to decide edges with uncertain existence or direction)
- integration into **structure learning** algorithms to provide knowledge for "uncertain" areas of the graph
- LLMs analyse learning process and errors to **suggest improved algorithms**
- LLMs used to preprocess **text and visual data** so they can be used as inputs to structure learning

### 🤝 Human Engagement
- **Natural language constraints**: Specify domain knowledge in plain English
- **Expert knowledge incorporation** by converting expert understanding into algorithmic constraints
- LLMs convert **natural language questions** to causal queries
- **Interactive causal discovery** where structure learning or LLMs identify areas of causal uncertainty and can test causal hypotheses through dialogue

### 🪟 Transparency and interpretability
- LLMs **interpret structure learning process** and outputs, including their uncertainties
- LLMs **interpret causal inference** results including uncertainties
- **Contextual graph interpretation** to explain variable meanings and relationships
- **Uncertainty communication** with clear explanation of confidence levels and limitations
- **Report generation including automated research summaries and methodology descriptions

### 🔒 Stability and reproducibility
- **cache queries and responses** so that experiments are stable and repeatable even if LLMs themselves are not
- **stable randomisation** of e.g. data sub-sampling

### 💰 Efficient use of LLM resources (important as an independent researcher)
- **cache queries and results** so that knowledge can be re-used
- evaluation and development of **simple context-adapted LLMs**

## Upcoming Integration with Ecosystem

- 🔍 **CausalIQ Discovery** makes use of this package to learn more 
accurate graphs.
- 🧪 **CausalIQ Analysis** uses this package to explain the learning process, intelligently combine end explain results.
- 🔮 **CausalIq Predict** uses this package to explain predictions made by learnt models.

<br/>

---

*The LLM Knowledge project represents a significant step toward more intelligent, interpretable, and human-collaborative approaches to causal discovery, bridging the gap between statistical rigour and domain expertise.*