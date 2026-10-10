# Contributing to CausalIQ

Thank you for your interest in contributing to CausalIQ! We welcome contributions from the community and are excited to see what you'll bring to this project.

This document describes the **contribution process** - repository setup, development workflow, commit conventions and review - that applies across all the CausalIQ repos. Please also refer to any additional project-specific guidelines that might apply.

**Engineering standards are defined once**, in the umbrella [development policies](docs/development_policy/index.md). Please read them before contributing, and do not restate or override them in individual repositories.

**Note**: When following these instructions, replace <package-name> with the name of a specific repo e.g. "causaliq-discovery".

## Engineering Standards

The ecosystem-wide engineering standards live in the umbrella repository and apply to every CausalIQ package. They are written for both human contributors and AI assistants (such as Cline), and follow a "Two Hats" model that keeps feature/fix work strictly separate from refactoring.

| Area | Policy document |
| ---- | --------------- |
| Planning and task scoping | [Plan Phase](docs/development_policy/00-plan.md) |
| Coding standards and limits | [Coding](docs/development_policy/01-code.md) |
| Writing tests | [Writing Tests](docs/development_policy/02-test-write.md) |
| Running tests and terminals | [Running Tests](docs/development_policy/03-test-run.md) |
| Documentation | [Documentation](docs/development_policy/04-docs.md) |

Read the relevant policy before you start, and make sure your change satisfies its requirements. The quality gates are:

- `black` formatting with 79-character lines
- `isort` import ordering
- `mypy` type checking on fully typed code
- `flake8` linting
- `pytest` with 100% coverage

Run them all with:

```bash
.\scripts\check_ci.ps1
```

The script automatically activates the correct Python environment (3.11) and runs each gate.

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
   - Write code following the [coding policy](docs/development_policy/01-code.md)
   - Add tests following the [test-writing policy](docs/development_policy/02-test-write.md)
   - Update documentation following the [documentation policy](docs/development_policy/04-docs.md)

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

### Running Tests

Prefer targeted test modules while developing:

```bash
python -m pytest tests/unit          # Unit tests only
python -m pytest tests/functional    # Functional tests only
python -m pytest tests/integration   # Integration tests
```

Use `.\scripts\check_ci.ps1` to run the full suite with coverage before
submitting. Integration tests typically have package-specific prerequisites.
See the [test-running policy](docs/development_policy/03-test-run.md) for
terminal, environment and session guidance.

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

New packages should use the following `pyproject.toml` template. Keep the configuration aligned with the [development policies](docs/development_policy/index.md).

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
    "pytest-mock>=3.0.0",
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
addopts = "--strict-markers --cov=src --cov-report=term-missing --cov-fail-under=100"
```

### Documentation

Follow the [documentation policy](docs/development_policy/04-docs.md). In addition:

- Update docstrings for new or modified functions.
- Update README.md when adding new features.
- Update CHANGELOG.md following the [Keep a Changelog](https://keepachangelog.com/) format.

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
│   ├── unit/                 # Unit tests (only uses package's own code, possibly with mocks)
│   ├── functional/           # Functional tests (internal dependencies such as filesystem or third party packages)
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
- **Expected behaviour** vs actual behaviour
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
