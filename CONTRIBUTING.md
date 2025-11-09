# Contributing to CausalIQ

Thank you for your interest in contributing to CausalIQ! We welcome contributions from the community and are excited to see what you'll bring to this project.

This document describes contribution guidelines that apply across all the CausalIQ repos - please then refer to any additional project specific guidelines that might apply.

**Note**: When following these instructions, replace <package-name> with the name of a specific repo e.g. "causaliq-discovery".

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/<package-name>.git
   cd <package-name>
   ```

2. **Set up the development environment**:
   ```bash
   # Windows - create all Python environments and install package
   .\scripts\setup-env.ps1 -Install
   
   # Or step by step:
   .\scripts\setup-env.ps1                  # Create environments only
   .\scripts\setup-env.ps1 -InstallOnly     # Install package
   ```

3. **Activate your development environment**:
   ```bash
   .\scripts\activate.ps1        # Activates Python 3.11 (default)
   .\scripts\activate.ps1 310    # Or Python 3.10 for testing
   ```

## Development Workflow

### Making Changes

1. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code following our style guide
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests and checks**:
   ```bash
   .\scripts\check_ci.ps1        # Runs all CI checks locally
   .\scripts\check_ci.ps1 -Fast  # Skip slower checks
   .\scripts\check_ci.ps1 -Fix   # Auto-fix formatting issues
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add descriptive commit message"
   ```

#### Commit Guidelines

**Commit Message Format**:

- **One line only**: Keep commit messages to a single line
- **Start with prefix**: Use conventional commit prefixes
- **Present tense**: Write as if completing "This commit will..."

**Accepted prefixes**:

- `feat:` - New features or functionality
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Adding or modifying tests
- `refactor:` - Code restructuring without functionality changes
- `perf:` - Performance improvements
- `style:` - Code style changes (formatting, missing semicolons, etc.)
- `chore:` - Maintenance tasks (dependency updates, build changes)

**Examples**:
```bash
git commit -m "feat: implement PC algorithm with independence testing"
git commit -m "fix: resolve numerical instability in BIC scoring"
git commit -m "docs: add API documentation for graph learning functions"
git commit -m "test: add comprehensive tests for constraint-based methods"
git commit -m "refactor: simplify graph validation logic"
```

**Commit Sizing**:

- **Small, focused commits**: Each commit should address a single logical change
- **Complete functionality**: Don't commit broken or incomplete features
- **Related changes together**: Group related modifications in one commit
- **Separate concerns**: Don't mix refactoring with new features

**Good commit sizes**:
```bash
git commit -m "feat: add basic PC algorithm structure"        # Just the skeleton
git commit -m "feat: implement independence testing in PC"   # Add one component  
git commit -m "test: add unit tests for PC algorithm"        # Add corresponding tests
```

**Avoid**:
```bash
git commit -m "feat: complete PC algorithm with tests and docs"  # Too large
git commit -m "fix typo"                                         # Missing prefix
git commit -m "Update code"                                      # Too vague
```

5. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style and Quality

We maintain high code quality standards using these tools:

- **Black**: Code formatting with 79-character line length
- **isort**: Import sorting  
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing with 100% coverage target

#### Python Code Standards

**Formatting**:
- Black with 79-character line length
- Google-style docstrings for all public APIs
- Complete type annotations using modern Python typing
- UTF-8 encoding for all text files

**Example Code Style**:
```python
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from causaliq_discovery import independence_test


def learn_structure(
    data: pd.DataFrame,
    algorithm: str = "pc",
    alpha: float = 0.05,
    max_conditioning_set_size: Optional[int] = None,
) -> Tuple[Dict[str, List[str]], float]:
    """Learn causal graph structure from observational data.
    
    Args:
        data: Observational dataset with variables as columns.
        algorithm: Structure learning algorithm to use.
        alpha: Significance level for conditional independence tests.
        max_conditioning_set_size: Maximum size of conditioning sets.
        
    Returns:
        Tuple of (adjacency dict, confidence score).
        
    Raises:
        ValueError: If algorithm is not supported.
        
    Example:
        >>> data = pd.DataFrame(np.random.randn(100, 3), columns=["A", "B", "C"])
        >>> graph, score = learn_structure(data, algorithm="pc")
        >>> len(graph)
        3
    """
    if data.empty:
        raise ValueError("Empty dataset provided")
    
    # Implementation with proper error handling
    try:
        result = _execute_algorithm(data, algorithm, alpha)
        return result, _calculate_confidence(result)
    except Exception as e:
        raise ValueError(f"Structure learning failed: {e}")
```

**Dependencies**:
- **Core**: NumPy, Pandas, NetworkX for all projects
- **Testing**: pytest, pytest-cov, hypothesis
- **Development**: pre-commit, black, isort, flake8, mypy

Run all checks:
```bash
.\scripts\check_ci.ps1
```

The script automatically:
- Activates the correct Python environment (3.11)
- Runs formatting checks with Black and isort
- Performs linting with flake8
- Runs type checking with MyPy
- Executes all tests with coverage reporting

### Testing

We aim for 100% test coverage. When adding new features:

1. **Write tests first** (TDD approach preferred)
2. **Test edge cases** and error conditions
3. **Mock external dependencies** 
4. **Update test fixtures** if needed

#### Testing Standards

**Test Structure Requirements**:

**Use pytest exclusively** - avoid unittest classes and methods

**Prefer individual test functions** over test classes:
```python
# tests/unit/test_structure_learning.py
import pytest
import pandas as pd
from unittest.mock import patch

from causaliq_discovery import learn_structure


# ✅ Preferred: Individual test functions
def test_empty_data_raises_error():
    """Empty datasets should raise ValueError."""
    with pytest.raises(ValueError, match="Empty dataset"):
        learn_structure(pd.DataFrame())

def test_algorithm_integration():
    """Test algorithm integration with mocked dependencies."""
    with patch('causaliq_discovery._execute_algorithm') as mock_execute:
        mock_execute.return_value = {"A": ["B"], "B": []}
        data = pd.DataFrame([[1, 2], [3, 4]], columns=["A", "B"])
        
        graph, score = learn_structure(data)
        
        assert isinstance(graph, dict)
        assert isinstance(score, float)
        mock_execute.assert_called_once()

def test_valid_data_returns_graph():
    """Test with valid input data."""
    data = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["A", "B", "C"])
    graph, score = learn_structure(data)
    
    assert isinstance(graph, dict)
    assert isinstance(score, float)
    assert len(graph) == 3

# ❌ Avoid: Classes unless strictly necessary for shared setup
class TestComplexSetup:  # Only if absolutely needed
    """Use classes only when complex shared setup is required."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        # Complex setup that can't be done with simple fixtures
        pass
```

**Test Categories**:
- **Unit tests**: Test individual functions with mocked dependencies
- **Functional tests**: Test with local system resources (filesystem, etc.)
- **Integration tests**: Test with external systems (APIs, databases)

**Test Data Management**:
- **Use permanent test files** tracked in GitHub (not generated on-the-fly)
- **File organization**: `tests/data/{category}/{module}/{scenario}.csv`
- **One-line comments**: Add before each test function for VS Code outline visibility

```python
# Test BIC score calculation returns correct float type
def test_bic_score_returns_float():
    data_path = Path("tests/data/functional/scoring/sample.csv")
    data = pd.read_csv(data_path)
    # ... test implementation
```

**Coverage Requirements**:
- **Target**: 100% code coverage
- **Minimum acceptable**: 95% coverage for new contributions
- **Tools**: pytest-cov for coverage reporting

**Test Categories**:
- **Unit tests**: Test individual functions with mocked dependencies
- **Functional tests**: Test with local system resources (filesystem, etc.)
- **Integration tests**: Test with external systems (APIs, databases)

Run tests:
```bash
.\scripts\check_ci.ps1               # Full test suite with coverage
python -m pytest tests/unit          # Unit tests only
python -m pytest tests/functional    # Unit tests only
python -m pytest tests/integration   # Integration tests
```

**Note**: Integration tests typically have package-specific prerequisites.

### Multi-Version Testing

Since CausalIQ supports Python 3.9-3.12, we encourage testing across versions:

```bash
# Test with different Python versions
.\scripts\activate.ps1 39    # Python 3.9
python -m pytest tests/unit/

.\scripts\activate.ps1 310   # Python 3.10  
python -m pytest tests/unit/

.\scripts\activate.ps1 311   # Python 3.11 (default)
python -m pytest tests/unit/

.\scripts\activate.ps1 312   # Python 3.12
python -m pytest tests/unit/
```

### Adding Dependencies

When adding new dependencies:

1. **Add to `pyproject.toml`** in the appropriate section
2. **Update all environments**:
   ```bash
   .\scripts\setup-env.ps1 -InstallOnly
   ```
3. **Test across Python versions** to ensure compatibility

#### Project Configuration

Use this template for `pyproject.toml` configuration:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "causaliq-[component]"
version = "0.1.0"
description = "Component description"
authors = [{name = "CausalIQ", email = "contact@causaliq.org"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "numpy>=1.21.0",
    "pandas>=1.3.0",
    "networkx>=2.6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[tool.black]
line-length = 79
target-version = ["py39"]

[tool.isort]
profile = "black"
line_length = 79

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--strict-markers --cov=src --cov-report=term-missing --cov-fail-under=95"
```

### Documentation

- Update docstrings for new/modified functions using Google-style format
- Add complete type hints to all function signatures
- Update README.md if adding new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format

#### Documentation Standards

**Language and Formatting**:

- **Use British English** throughout all documentation (e.g., "optimise" not "optimize", "colour" not "color")
- **MkDocs formatting**: Always include a blank line before bullet point lists to ensure proper rendering

**Example of proper MkDocs formatting**:
```markdown
The algorithm supports several options:

- Statistical validation using independence tests
- Domain knowledge integration through constraints
- Bootstrap sampling for confidence intervals

This ensures bullet points render correctly in the documentation.
```

#### Performance Guidelines

When implementing algorithms, follow these optimization principles:

**Vectorization**:
```python
import numpy as np
from functools import lru_cache

# ✅ Preferred: NumPy vectorized operations
def compute_correlations(data: pd.DataFrame) -> np.ndarray:
    """Compute all pairwise correlations efficiently."""
    return np.corrcoef(data.T)

# ❌ Avoid: Python loops for numerical computations
def compute_correlations_slow(data: pd.DataFrame) -> np.ndarray:
    """Inefficient correlation computation."""
    n_vars = len(data.columns)
    correlations = np.zeros((n_vars, n_vars))
    for i in range(n_vars):
        for j in range(n_vars):
            correlations[i, j] = data.iloc[:, i].corr(data.iloc[:, j])
    return correlations

@lru_cache(maxsize=128)
def expensive_computation(data_hash: str) -> float:
    """Cache expensive computations to avoid recomputation."""
    # Implementation here
    pass
```

**Profiling Tools**:
- Use `cProfile` and `line_profiler` for performance analysis
- Monitor memory usage with `memory_profiler`
- Consider `joblib` for parallel processing when appropriate

## Project Structure common across all repos

```
<package-name>/
├── docs/                     # Documentation
│   ├── architecture.md       # Package architecture
│   ├── index.md              # Documentation entry point
│   ├── ...                   # Package-specific design and usage documentation
├── scripts/                  # Development scripts
│   ├── activate.ps1          # Environment activation
│   ├── setup-env.ps1         # Environment management  
│   ├── check_ci.ps1          # Local CI validation
│   ├── bump_version.py       # Version management
│   └── build-and-publish.ps1 # Package publishing
├── src/package-name/         # Main package code
│   ├── __init__.py           # Package initialization
│   └── ...                   # Other modules are specific to each package
├── tests/                    # Test files
│   ├── unit/                 # Unit tests (only uses packages's own code, possibly with mocks)    
│   ├── functional/           # Functional tests (internal dependencies such as filesystem or third party packages )
│   └── integration/          # Integration tests (access external systems)
├── .pre-commit-config.yaml   # Automated code checks before commits
├── CHANGELOG.md              # Log of software changes
├── CONTRIBUTING.md           # Package-specific contribution guidelines
├── mkdocs.yml                # Documentation configuration
├── pyproject.toml            # Package configuration
└── README.md                 # Project documentation
```

## Types of Contributions

### Bug Reports

When filing bug reports, please include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **System information** (OS, Python version, package version)
- **Error messages** and stack traces if applicable

### Feature Requests

For feature requests:

- **Describe the use case** and problem you're solving
- **Explain the proposed solution** in detail
- **Consider alternatives** and trade-offs
- **Check existing issues** to avoid duplicates

### Code Contributions

We welcome:

- **Bug fixes**
- **New features** (please discuss in an issue first)
- **Performance improvements**
- **Documentation improvements**
- **Test improvements**

## Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality, backwards compatible
- **PATCH**: Bug fixes, backwards compatible

## Review Process

All contributions go through code review:

1. **Automated checks** must pass (GitHub Actions)
2. **Manual review** by maintainers
3. **Discussion and refinement** if needed
4. **Merge** when approved

## Community Guidelines

- **Be respectful** and constructive
- **Help others** learn and contribute
- **Ask questions** if something is unclear
- **Share knowledge** and best practices

## Recognition

Contributors will be:

- **Listed in CONTRIBUTORS.md** (coming soon)
- **Mentioned in release notes** for significant contributions
- **Tagged** in relevant GitHub issues and PRs

## Getting Help

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Code Review**: Request feedback on your contributions

## License

By contributing to CausalIQ, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CausalIQ projects! 🚀