# Contributing to LLM Tourism Simulation System 🤝

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git fork https://github.com/llm-tourism-sim/llm-tourism-sim.git
   git clone https://github.com/YOUR_USERNAME/llm-tourism-sim.git
   cd llm-tourism-sim
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Development Tools (Optional)**
   ```bash
   pip install pytest black flake8
   ```

5. **Run Tests**
   ```bash
   python tests/test_basic.py
   # Or with pytest (if installed)
   pytest tests/test_basic.py
   ```

## 📋 Types of Contributions

### 🐛 Bug Reports
- Use GitHub Issues with the "bug" label
- Include system information, error messages, and reproduction steps
- Provide minimal code example that demonstrates the issue

### 💡 Feature Requests  
- Use GitHub Issues with the "enhancement" label
- Describe the problem the feature would solve
- Provide use cases and examples
- Consider implementation complexity

### 📝 Documentation Improvements
- Fix typos, clarify explanations, add examples
- Update API documentation for code changes
- Improve installation and usage guides

### 🔧 Code Contributions
- Bug fixes, performance improvements, new features
- Follow coding standards and include tests
- Update documentation as needed

## 📁 Project Structure

The project is organized into logical packages for better maintainability:

```
mesa-poc/
├── data/                    # Configuration data files
│   ├── tourist_personas.json
│   ├── urban_hotspots.json
│   ├── business_rules.json
│   └── scenarios_events.json
├── sim/                     # Core simulation modules
│   ├── models/             # Simulation models
│   ├── agents/             # Tourist and hotspot agents
│   └── data_loader.py      # Data loading utilities
├── utils/                   # Analysis and utility modules
│   ├── analysis.py         # Statistical analysis
│   ├── visualization.py    # Charts and plots
│   └── results_storage.py  # Results management
├── examples/                # Example scripts
├── tests/                   # Test suite
└── docs/                    # Documentation
```

### Where to Add New Code

- **New simulation models**: `sim/models/`
- **New agent types**: `sim/agents/`
- **New analysis functions**: `utils/`
- **New example scripts**: `examples/`
- **New tests**: `tests/`
- **New data files**: `data/`

## 🛠️ Development Guidelines

### Code Style

**Python Standards:**
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Include docstrings for all public functions and classes
- Maximum line length: 100 characters

**Formatting Tools:**
```bash
# Format code (if black is installed)
black .

# Check style (if flake8 is installed)  
flake8 .
```

### Testing Requirements

**Test Coverage:**
- Write tests for all new functionality
- Maintain existing test coverage
- Test both success and failure cases

**Test Structure:**
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        # Test setup
        pass

    def test_basic_functionality(self):
        # Test basic use case
        pass

    def test_edge_cases(self):
        # Test edge cases and error conditions
        pass
```

### Documentation Standards

**Code Documentation:**
```python
def new_function(param1: str, param2: int = 10) -> dict:
    """
    Brief description of what the function does.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is invalid

    Example:
        >>> result = new_function("test", 5)
        >>> print(result)
        {'key': 'value'}
    """
```

**API Documentation:**
- Update `API.md` for new public functions
- Include examples and parameter descriptions
- Document any breaking changes

## 🎯 Specific Contribution Areas

### Adding New Tourist Personas

1. **Define Persona Profile**
   ```json
   {
     "type": "New Persona Type",
     "description": "Detailed description",
     "demographics": {...},
     "behavioral_traits": {...},
     "travel_patterns": {...}
   }
   ```

2. **Add to Configuration**
   - Add to `tourist_personas.json`
   - Update appeal scores in hotspot definitions
   - Add to business rules if needed

3. **Update Documentation**
   - Add persona description to README.md
   - Update API documentation
   - Include in examples

### Adding New Hotspot Types

1. **Define Hotspot Characteristics**
   ```json
   {
     "name": "New Hotspot",
     "category": "new_category",
     "location": {...},
     "characteristics": {...},
     "appeal_to_personas": {...}
   }
   ```

2. **Integration Requirements**
   - Add appeal scores for all existing personas
   - Consider spatial distribution
   - Update visualization if needed

### Creating New Scenarios

1. **Scenario Design**
   ```python
   scenario = TourismScenario(
       name="Descriptive Name",
       description="Clear description of scenario",
       category="appropriate_category"
   )
   ```

2. **Event Definition**
   - Use realistic timing and parameters
   - Include clear reasoning for each event
   - Test impact on different personas

3. **Validation**
   - Test scenario produces expected effects
   - Compare against baseline
   - Document expected outcomes

### Extending Analysis Tools

1. **New Metrics**
   - Define clear calculation method
   - Include statistical significance tests
   - Provide interpretation guidelines

2. **Visualization Enhancements**
   - Follow existing chart style
   - Include appropriate legends and labels
   - Test with different data sizes

### Extending Results Storage

1. **New Storage Formats**
   - Add support for new file formats
   - Include metadata and documentation
   - Maintain backward compatibility

2. **Output Management**
   - Add new utility functions
   - Improve directory organization
   - Enhance search and filtering

## 📦 Pull Request Process

### Before Submitting

1. **Code Quality**
   ```bash
   # Run tests
   python tests/test_basic.py

   # Check imports work
   python -c "from sim import TourismModel, load_data; print('✅ Import successful')"

   # Test examples
   python examples/basic_simulation.py
   python examples/scenario_comparison.py
   ```

2. **Documentation**
   - Update relevant documentation files
   - Add docstrings to new functions
   - Include examples for new features

3. **Results Storage**
   - Test with results storage system
   - Verify output directory structure
   - Check metadata generation

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Results storage enhancement

## Testing
- [ ] Existing tests pass
- [ ] New tests added for new functionality
- [ ] Examples updated if needed
- [ ] Results storage tested if applicable

## Documentation
- [ ] Code includes docstrings
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Usage examples updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes (or clearly documented)
- [ ] Virtual environment setup documented
```

### Review Process

1. **Automated Checks**
   - Tests must pass
   - Code style compliance
   - Import validation

2. **Manual Review**
   - Code quality and design
   - Documentation completeness
   - Test coverage
   - Results storage integration

3. **Approval**
   - At least one maintainer approval required
   - Address review feedback
   - Merge when approved

## 🔄 Release Process

### Version Numbering
- Follow semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Release notes prepared
- [ ] Results storage system tested

## 🌟 Recognition

### Contributors
- All contributors listed in CONTRIBUTORS.md
- Significant contributions acknowledged in releases
- Optional: Join core team for major contributors

### Attribution
- Maintain attribution for LLM-generated content
- Credit original ideas and implementations
- Acknowledge feedback and suggestions

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Email**: contact@llm-tourism-sim.org

### Code Review
- Submit draft PRs early for feedback
- Ask specific questions in PR comments
- Reference relevant issues and discussions

### Development Questions
- Check existing documentation first
- Search closed issues for similar problems
- Provide context and code examples

## 🎉 Thank You!

Your contributions help make this project better for everyone. Whether you're:
- Reporting bugs
- Suggesting features  
- Improving documentation
- Contributing code
- Providing feedback
- Enhancing results storage

Every contribution is valuable and appreciated! 🙏

---

*For questions about these guidelines, please open a GitHub Discussion or contact the maintainers.*
