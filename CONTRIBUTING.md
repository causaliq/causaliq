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
   git commit -m "Add your descriptive commit message"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style and Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting  
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

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

We aim for comprehensive test coverage. When adding new features:

1. **Write tests first** (TDD approach preferred)
2. **Test edge cases** and error conditions
3. **Mock external dependencies** 
4. **Update test fixtures** if needed

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

### Documentation

- Update docstrings for new/modified functions
- Add type hints to all function signatures
- Update README.md if adding new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format

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