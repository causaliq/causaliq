# LLM Development Support Guidelines

This guide outlines how Large Language Models (LLMs) should assist with software development across the CausalIQ ecosystem, emphasizing incremental development and clear communication.

## 📋 Single Source of Truth for Project Planning

**CRITICAL**: All development planning and progress tracking is centralised in:
👉 **[docs/roadmap.md](docs/roadmap.md)** - Complete roadmap with delivery specifications

**LLM Responsibility**: Always reference roadmap.md for current status, next milestones, and feature specifications. Do not duplicate roadmap content in other documents.

## 🎯 Progress Tracking Standards

**CRITICAL**: Progress percentages must be mathematically accurate, not aspirational.

**Calculation Method:**
- Count completed tasks within each feature area
- Calculate percentage based on actual implementation status
- Verify progress calculations before updating any documentation

**Common LLM Errors to Avoid:**
- ❌ Counting design documents as implementation progress
- ❌ Optimistic rounding or aspirational percentages  
- ❌ Claiming high completion when only infrastructure exists
- ❌ Duplicating progress tracking across multiple documents

**Always verify progress calculations and maintain single source of truth in roadmap.md**

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

## 📚 Documentation Architecture Patterns

### Single Source of Truth Principle

**CRITICAL**: Each type of information should have exactly one authoritative location.

**Documentation Structure for CausalIQ Projects:**
```
├── README.md                      # Project gateway - brief overview, links to detailed docs
├── docs/roadmap.md                # Single source for features and progress
├── docs/technical_architecture.md # System design and development patterns  
├── docs/example_workflows.md      # Concrete usage examples
└── docs/design/...                # Contains design notes for specific areas
```

The [ecosystem-wide development standards](https://github.com/causaliq/causaliq/blob/main/LLM_DEVELOPMENT_GUIDE.md) (this document) is maintained in the causaliq/causaliq umbrella repo.

**Information Ownership:**
- **README.md**: Project description, quick start, documentation index
- **roadmap.md**: All feature specifications and progress tracking
- **technical_architecture.md**: System design, architectural decisions, and project-specific development patterns
- **[LLM_DEVELOPMENT_GUIDE_ENHANCED.md](https://github.com/causaliq/causaliq/blob/main/LLM_DEVELOPMENT_GUIDE.md)**: Ecosystem-wide standards (this document)

### Documentation Consolidation Patterns

**Common Documentation Duplication Problems:**
- ❌ Multiple "feature lists" across README, planning docs, and guides
- ❌ Development standards scattered across project-specific guides
- ❌ Progress tracking in multiple inconsistent locations
- ❌ Architecture decisions repeated across multiple documents

**Consolidation Strategy:**
1. **Audit existing documentation** for duplication and inconsistency
2. **Identify single sources of truth** for each information type
3. **Move content to proper locations** based on information architecture
4. **Update all references** to point to consolidated sources
5. **Remove redundant documents** that add maintenance overhead

**Example: causaliq-pipeline Documentation Consolidation (November 2025)**
- Removed `docs/llm_communication_guide.md` (90% duplication with this guide)
- Removed `docs/development_practices.md` (development patterns moved to technical architecture)
- Consolidated all progress tracking into `docs/roadmap.md`
- Updated README.md to reference detailed docs rather than duplicating content

**Benefits Achieved:**
- ✅ Eliminated maintenance overhead from duplicate content
- ✅ Single sources of truth for each information type
- ✅ Cleaner, more focused documentation structure
- ✅ Proper information architecture with clear ownership

### LLM Communication About Documentation

**When working on documentation:**
- Always ask "Does this information exist elsewhere?"
- Prefer linking to authoritative sources over duplication
- Update the single source of truth, not copies
- Remove redundant content when consolidating

**Documentation Maintenance Requirements:**
- Update roadmap.md when completing features
- Add architectural decisions to technical_architecture.md
- Keep README.md brief and gateway-focused
- Reference this guide for ecosystem standards, not project-specific copies

## 🎯 Development Principles

### Core Values
- **Augmentation, not replacement**: Enhance human developer capabilities
- **Transparency**: Clear explanations for all suggestions
- **Quality**: Maintain high standards while respecting incremental approach
- **Learning**: Help developers understand patterns and decisions

## 🏗️ Environment Management

### CausalIQ Standard Environment Setup
**CRITICAL**: Never use `pip install` directly. Always use project setup scripts.

**For package development:**
```powershell
# Use provided environment setup script
.\scripts\setup-env.ps1

# Verify environment with CI checks
.\scripts\check_ci.ps1
```

**For LLM assistance:**
- Inform LLM about environment management: "Use scripts/setup-env.ps1 for dependencies, not pip install"
- Always run CI checks after dependency changes
- Include environment setup in implementation explanations

### Terminal Session and Virtual Environment Management
**CRITICAL**: Virtual environments must be maintained within the same terminal session.

**Common LLM Error Pattern:**
```powershell
# ❌ WRONG: Each command starts a new terminal session
Terminal 1: .\scripts\activate.ps1 311
Terminal 2: python -m mkdocs serve    # Fails - no venv activated
```

**Correct LLM Approach:**
```powershell
# ✅ CORRECT: Run activation and commands in same session
.\scripts\activate.ps1 311; python -m mkdocs serve --dev-addr=127.0.0.1:8000
```

**LLM Best Practices:**
- **Sequential commands**: Use semicolon (`;`) to run activation + command in one call
- **Session awareness**: Remember that `run_in_terminal` starts fresh sessions
- **Environment verification**: Check for `(py311)` prompt prefix before running Python tools
- **Documentation tools**: MkDocs, pytest, and other tools require activated venv

**Environment-Dependent Tools:**
- `mkdocs serve` - Requires venv for mkdocstrings-python handler
- `pytest` with coverage - Uses venv-installed packages
- `black`, `isort`, `flake8`, `mypy` - Should use venv versions for consistency

## 📋 Essential Quality Standards

### Code Generation Checklist
- [ ] **Type hints**: All parameters and return values typed
- [ ] **Docstrings**: Clear documentation with examples  
- [ ] **Error handling**: Appropriate exceptions and validation
- [ ] **Testing**: Generate corresponding test cases
- [ ] **Incremental**: Changes broken into logical steps
- [ ] **British English**: Use British spelling in all documentation
- [ ] **MkDocs formatting**: Include blank lines before bullet point lists
- [ ] **API Documentation**: Satisfactory documentation available before commit
- [ ] **Design Documentation**: Significant decisions documented in technical_architecture.md
- [ ] **Progress Tracking**: Update roadmap.md with completed tasks before commit

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

**Test Classification Rules:**
- **Unit tests**: Pure logic, no filesystem/external dependencies
- **Functional tests**: Filesystem access, local resources (use `tests/data/functional/`)
- **Integration tests**: Remote services, network dependencies

## 🛠️ Code Quality Standards

### CI Validation Tools
Generated code must pass these automated checks:

**Black** (code formatting):
- **79 character line limit** (not 88) - CRITICAL CausalIQ standard
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

### Line Length Management
**CRITICAL**: Follow 79-character limit from the start, not retrospectively:
```python
# ✅ Good: Written to 79-char limit
def process_configuration_data(
    workflow_config: Dict[str, Any],
    validation_schema: Dict[str, Any]
) -> ProcessedConfig:
    """Process workflow configuration with validation."""
    pass

# ❌ Bad: Long lines requiring later reformatting
def process_configuration_data(workflow_config: Dict[str, Any], validation_schema: Dict[str, Any]) -> ProcessedConfig:
```

### Documentation Standards

**Language and Formatting Requirements**:

- **British English**: Use British spelling throughout (optimise, colour, analyse)
- **MkDocs compatibility**: Always include blank line before bullet point lists
- **Google-style docstrings**: Complete with examples and type information
- **Markdown formatting**: Ensure proper rendering in documentation website

**API Documentation Requirements**:

- **Pre-commit documentation**: Ensure satisfactory API documentation is available before each commit
- **Design documentation**: Significant design decisions must be documented in `technical_architecture.md` or separate design notes
- **Public API exposure**: All user-facing classes and functions properly documented

**Roadmap Maintenance Requirements**:

- **Task completion updates**: Mark tasks as completed (✅) in roadmap.md when implementation is done
- **Progress recalculation**: Update overall progress percentages using accurate mathematical calculation
- **Status transitions**: Change feature areas from ⏸️ to 🚧 when starting, 🚧 to ✅ when complete
- **Milestone identification**: Update 🎯 next milestone indicators as priorities shift
- **Commit synchronisation**: Roadmap updates should be included in the same commit as the feature implementation

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

## ⚠️ Common Standards Violations to Avoid

### Testing Violations
- ❌ Using test classes when individual functions suffice
- ❌ Putting filesystem tests in unit tests (belongs in functional)
- ❌ Missing permanent test files in `tests/data/functional/`
- ❌ Missing one-line test comments for VS Code outline

### Code Quality Violations
- ❌ Writing long lines and fixing retrospectively (write to 79 chars)
- ❌ Missing type hints or incomplete docstrings
- ❌ Using American spelling in comments/strings
- ❌ Incomplete API documentation before commit

### Environment Violations
- ❌ Using `pip install` directly instead of `scripts/setup-env.ps1`
- ❌ Not running CI checks before claiming completion
- ❌ Missing dependency declarations in project files
- ❌ **Starting new terminal sessions without venv activation**
- ❌ **Running Python tools (mkdocs, pytest) without proper environment**
- ❌ **Forgetting semicolon syntax for sequential commands in PowerShell**

### Documentation Violations
- ❌ Missing design documentation for significant decisions
- ❌ Incomplete API documentation before commit
- ❌ Missing blank lines before bullet points in MkDocs
- ❌ Failing to update roadmap.md when completing tasks
- ❌ Inaccurate progress calculations in roadmap.md
- ❌ Creating duplicate documentation instead of referencing single sources of truth
- ❌ Maintaining redundant project-specific guides that duplicate ecosystem standards
- ❌ Scattering feature lists and progress tracking across multiple documents

---

*These guidelines ensure LLM assistance maintains high standards while respecting developer preferences for incremental, understandable changes across the CausalIQ ecosystem.*

---

**Document Location**: This guide is maintained in the umbrella `causaliq/causaliq` repository and should be referenced when working on any CausalIQ project (causaliq-discovery, causaliq-guide, causaliq-pipeline, etc.).