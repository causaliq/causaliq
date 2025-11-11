# LLM Development Support Guidelines

This guide outlines how Large Language Models (LLMs) should assist with software development across the CausalIQ ecosystem, emphasizing incremental development and clear communication.

## 🔄 Incremental Development Approach

### Core Philosophy
- **Small, focused changes** that address one concern at a time
- **Explain all changes** clearly before and during implementation  
- **Break down complex problems** into reviewable steps
- **Respect developer preference** for understanding each modification

### Change Sizing Principles

**Prefer Small Changes (<50 lines):**
- Single function modifications
- Bug fixes in isolated components
- Documentation updates
- Simple refactoring improvements

**When Larger Changes Are Necessary:**
- Critical security vulnerabilities affecting multiple files
- Performance bottlenecks requiring architectural changes
- API consistency improvements across projects
- Breaking changes that must be coordinated

**Always explain WHY larger changes are needed and ASK before implementing**

### Change Communication Requirements

For every proposed change, provide:
- **What**: Exactly what code is being modified
- **Why**: The problem being solved or improvement being made
- **Impact**: What other functionality might be affected
- **Alternatives**: Whether incremental approaches were considered

## 📋 Providing Context to LLMs

When requesting coding assistance, provide these documents for optimal results:

**Essential Context:**
1. **This LLM Development Guide** - Development principles and standards
2. **CausalIQ Ecosystem Architecture** - Overall system design and integration
3. **Package README** - Specific package purpose, installation, basic usage
4. **Package Design Notes** - Detailed technical decisions and patterns

**Additional Helpful Context:**
- **Relevant source files** - Current implementation being modified
- **Test files** - Existing test patterns and coverage
- **Error messages** - If debugging or fixing issues
- **Related issues** - GitHub issues or design discussions

**Context Sizing Tips:**
- Paste documents directly (most efficient for LLMs)
- For large codebases, focus on relevant modules/files
- Include type definitions and key interfaces
- Provide examples of existing patterns to follow

## 🎯 Development Principles

### Core Values
- **Augmentation, not replacement**: Enhance human developer capabilities
- **Transparency**: Clear explanations for all suggestions
- **Quality**: Maintain high standards while respecting incremental approach
- **Learning**: Help developers understand patterns and decisions

## 📋 Essential Quality Standards

### Code Generation Checklist
- [ ] **Type hints**: All parameters and return values typed
- [ ] **Docstrings**: Clear documentation with examples  
- [ ] **Error handling**: Appropriate exceptions and validation
- [ ] **Testing**: Generate corresponding test cases
- [ ] **Incremental**: Changes broken into logical steps
- [ ] **British English**: Use British spelling in all documentation
- [ ] **MkDocs formatting**: Include blank lines before bullet point lists

### Example: Good Incremental Development
```python
# Step 1: Add basic function signature with types
def calculate_bic_score(
    graph: Dict[str, List[str]], 
    data: pd.DataFrame
) -> float:
    """Calculate BIC score for a given graph structure."""
    pass

# Step 2: Add implementation (next change)
# Step 3: Add error handling (separate change)  
# Step 4: Add comprehensive tests (separate change)
```

## 🧪 Testing Guidelines

### Test Categories

**Unit Tests**
- Test one or small number of functions in isolation
- Mock external dependencies and functions outside the package
- No access to filesystem, databases, or external services
- Fast execution (milliseconds)

**Functional Tests**  
- Test code with local machine resources
- Can access filesystem, local databases, local Python/non-Python software
- Test real file I/O, local API calls, subprocess execution
- Moderate execution time (seconds)

**Integration Tests**
- Test interactions with remote systems/services
- Examples: Zenodo API, cloud services, remote databases
- May require network access and authentication
- Slower execution (seconds to minutes)

### Test Structure Requirements

**Use pytest exclusively** - avoid unittest classes and methods

**Prefer individual test functions** over test classes:
```python
# ✅ Preferred: Individual functions
def test_bic_score_returns_float():
    """Test BIC score calculation returns float."""
    pass

def test_bic_score_handles_empty_graph():
    """Test BIC score with empty graph."""
    pass

# ❌ Avoid: Classes unless strictly necessary
class TestBICScoring:  # Only if shared setup is complex
    pass
```

### Test Data & Structure

**Permanent test files** (tracked in GitHub):
```
tests/data/functional/{module}/{scenario}.csv
tests/data/integration/{service}/{test_case}.json
```

**One-line test comments** for VS Code outline:
```python
# Test BIC score calculation returns correct float type
def test_bic_score_returns_float():
    pass
```

## 🛠️ Code Quality Standards

### CI Validation Tools
Generated code must pass these automated checks:

**Black** (code formatting):
- 79 character line limit (not 88)
- Double quotes for strings
- Trailing commas in multi-line structures

**isort** (import sorting):
- Group imports: stdlib, third-party, local
- Alphabetical within groups
- Single line imports preferred

**mypy** (type checking):
- Complete type hints for all functions
- Use `typing` imports for complex types
- No `# type: ignore` unless absolutely necessary

**flake8** (style checking):
- No unused imports or variables
- Proper indentation and spacing
- Descriptive variable names
- British English spelling in comments and strings

### Documentation Standards

**Language and Formatting Requirements**:

- **British English**: Use British spelling throughout (optimise, colour, analyse)
- **MkDocs compatibility**: Always include blank line before bullet point lists
- **Google-style docstrings**: Complete with examples and type information
- **Markdown formatting**: Ensure proper rendering in documentation website

**Example Documentation**:
```python
def optimise_graph_structure(data: pd.DataFrame) -> Dict[str, List[str]]:
    """Optimise causal graph structure using statistical methods.
    
    This function analyses the input data to discover optimal causal 
    relationships between variables.
    
    Args:
        data: Input dataset for analysis
        
    Returns:
        Dictionary representing optimised graph structure
        
    Note:
        The algorithm supports several optimisation strategies:
        
        - Constraint-based learning with independence tests
        - Score-based optimisation using BIC criteria  
        - Hybrid approaches combining both methods
        
    """
    pass
```

### Code Style Example
```python
from typing import Dict, List, Optional
import json
from pathlib import Path

import pandas as pd
import numpy as np

from causaliq.scoring import calculate_bic_score


def learn_structure(
    data: pd.DataFrame,
    algorithm: str = "pc", 
    alpha: float = 0.05,
    max_iterations: Optional[int] = None
) -> Dict[str, List[str]]:
    """Learn causal structure from observational data.
    
    Args:
        data: Dataset with variables as columns
        algorithm: Structure learning algorithm to use
        alpha: Significance threshold for independence tests
        max_iterations: Maximum algorithm iterations
        
    Returns:
        Adjacency dictionary representing learned DAG
        
    Raises:
        ValueError: If data contains missing values
    """
    if data.isnull().any().any():
        raise ValueError("Data contains missing values")
    
    # Implementation following 79-char limit
    result = _execute_algorithm(
        data=data,
        algorithm=algorithm,
        alpha=alpha,
        max_iterations=max_iterations
    )
    
    return result
```

---

## 📖 Reference Examples

### Complete Function Example
```python
def calculate_bic_score(graph: Dict[str, List[str]], 
                       data: pd.DataFrame) -> float:
    """Calculate BIC score for graph structure.
    
    Args:
        graph: Adjacency dict representing DAG structure
        data: Dataset with variables as columns
        
    Returns:
        BIC score (higher is better)
    """
    if not _is_dag(graph):
        raise ValueError("Graph must be directed acyclic")
    
    try:
        log_likelihood = _calculate_log_likelihood(graph, data)
        penalty = _calculate_parameter_penalty(graph, data)
        return log_likelihood - penalty
    except Exception as e:
        raise ValueError(f"BIC calculation failed: {e}")
```

### Test Example
```python
# Test BIC score calculation with valid DAG structure
def test_bic_score_valid_dag():
    data_path = Path("tests/data/functional/scoring/sample.csv")
    data = pd.read_csv(data_path)
    graph = {"A": ["B"], "B": []}
    
    score = calculate_bic_score(graph, data)
    
    assert isinstance(score, float)
    assert np.isfinite(score)
```

---

*These guidelines ensure LLM assistance maintains high standards while respecting developer preferences for incremental, understandable changes across the CausalIQ ecosystem.*

---

**Document Location**: This guide is maintained in the umbrella `causaliq/causaliq` repository and should be referenced when working on any CausalIQ project (causaliq-discovery, causaliq-guide, causaliq-pipeline, etc.).