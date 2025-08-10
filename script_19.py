# Create basic test file
test_file = '''#!/usr/bin/env python3
"""
Basic Test Suite for LLM Tourism Simulation System
=================================================

This module provides basic tests to verify system functionality.
For comprehensive testing, use pytest with the full test suite.
"""

import sys
import os
import unittest
import tempfile
import json

# Add package to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from llm_tourism_sim import load_data, TourismModel, ScenarioAwareTourismModel
    from llm_tourism_sim.scenarios.scenario_manager import TourismScenario, ScenarioManager
    from llm_tourism_sim.utils.data_loader import validate_personas_data, validate_hotspots_data
    from llm_tourism_sim.utils.analysis import analyze_simulation_results
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Import failed: {e}")
    IMPORTS_AVAILABLE = False


@unittest.skipUnless(IMPORTS_AVAILABLE, "Package imports not available")
class TestDataLoading(unittest.TestCase):
    """Test data loading functionality."""
    
    def test_load_data(self):
        """Test loading all configuration data."""
        try:
            personas, hotspots, business_rules, scenarios = load_data()
            
            self.assertIsInstance(personas, list)
            self.assertIsInstance(hotspots, list)
            self.assertIsInstance(business_rules, dict)
            self.assertIsInstance(scenarios, list)
            
            self.assertGreater(len(personas), 0)
            self.assertGreater(len(hotspots), 0)
            
        except Exception as e:
            self.fail(f"Data loading failed: {e}")
    
    def test_data_validation(self):
        """Test data validation functions."""
        try:
            personas, hotspots, _, _ = load_data()
            
            personas_valid = validate_personas_data(personas)
            hotspots_valid = validate_hotspots_data(hotspots)
            
            self.assertTrue(personas_valid, "Personas data validation failed")
            self.assertTrue(hotspots_valid, "Hotspots data validation failed")
            
        except Exception as e:
            self.fail(f"Data validation failed: {e}")


@unittest.skipUnless(IMPORTS_AVAILABLE, "Package imports not available")
class TestBasicSimulation(unittest.TestCase):
    """Test basic simulation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            self.personas, self.hotspots, self.business_rules, _ = load_data()
        except Exception:
            self.skipTest("Could not load test data")
    
    def test_model_creation(self):
        """Test creating a basic tourism model."""
        model = TourismModel(
            personas_data=self.personas,
            hotspots_data=self.hotspots,
            business_rules=self.business_rules,
            num_tourists=10,
            random_seed=42
        )
        
        self.assertEqual(len(model.tourists), 10)
        self.assertEqual(len(model.hotspots), len(self.hotspots))
        self.assertTrue(model.running)
    
    def test_simulation_execution(self):
        """Test running a basic simulation."""
        model = TourismModel(
            personas_data=self.personas,
            hotspots_data=self.hotspots,
            business_rules=self.business_rules,
            num_tourists=5,
            random_seed=42
        )
        
        results = model.run_simulation(steps=3)
        
        self.assertEqual(len(results), 3)
        self.assertIn('Average_Popularity', results.columns)
        self.assertIn('Average_Satisfaction', results.columns)
        self.assertIn('Total_Visitors', results.columns)
    
    def test_statistics_collection(self):
        """Test statistics collection."""
        model = TourismModel(
            personas_data=self.personas,
            hotspots_data=self.hotspots,
            business_rules=self.business_rules,
            num_tourists=5,
            random_seed=42
        )
        
        model.run_simulation(steps=2)
        
        hotspot_stats = model.get_hotspot_statistics()
        persona_stats = model.get_persona_statistics()
        summary = model.get_summary_report()
        
        self.assertIsInstance(hotspot_stats, list)
        self.assertIsInstance(persona_stats, dict)
        self.assertIsInstance(summary, dict)
        
        self.assertGreater(len(hotspot_stats), 0)
        self.assertIn('final_metrics', summary)


@unittest.skipUnless(IMPORTS_AVAILABLE, "Package imports not available")
class TestScenarioSystem(unittest.TestCase):
    """Test scenario management and execution."""
    
    def test_scenario_creation(self):
        """Test creating a custom scenario."""
        scenario = TourismScenario(
            name="Test Scenario",
            description="Test scenario for unit testing",
            category="test"
        )
        
        scenario.add_event(5, "appeal_boost", "Test Target", {"boost": 0.1})
        scenario.add_regulation("test_regulation", {"param": "value"})
        scenario.add_external_factor("test_factor", 0.2)
        
        self.assertEqual(scenario.name, "Test Scenario")
        self.assertEqual(len(scenario.events), 1)
        self.assertEqual(len(scenario.regulations), 1)
        self.assertEqual(len(scenario.external_factors), 1)
    
    def test_scenario_manager(self):
        """Test scenario manager functionality."""
        manager = ScenarioManager()
        
        # Create test scenario
        scenario = manager.create_scenario("Test", "Test description", "test")
        self.assertIn("Test", manager.scenarios)
        
        # Test scenario retrieval
        retrieved = manager.get_scenario("Test")
        self.assertEqual(retrieved.name, "Test")
        
        # Test scenario listing
        scenarios = manager.list_scenarios()
        self.assertIn("Test", scenarios)


@unittest.skipUnless(IMPORTS_AVAILABLE, "Package imports not available")  
class TestAnalysis(unittest.TestCase):
    """Test analysis and visualization functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        try:
            personas, hotspots, business_rules, _ = load_data()
            
            model = TourismModel(
                personas_data=personas,
                hotspots_data=hotspots,
                business_rules=business_rules,
                num_tourists=5,
                random_seed=42
            )
            
            self.model_data = model.run_simulation(steps=3)
            self.hotspot_stats = model.get_hotspot_statistics()
            self.persona_stats = model.get_persona_statistics()
            
        except Exception:
            self.skipTest("Could not set up test data")
    
    def test_simulation_analysis(self):
        """Test comprehensive simulation analysis."""
        analysis = analyze_simulation_results(
            self.model_data,
            self.hotspot_stats,
            self.persona_stats
        )
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('simulation_overview', analysis)
        self.assertIn('performance_metrics', analysis)
        self.assertIn('hotspot_analysis', analysis)
        self.assertIn('persona_analysis', analysis)
        self.assertIn('recommendations', analysis)


def run_tests():
    """Run all tests and display results."""
    print("🧪 LLM Tourism Simulation - Test Suite")
    print("=" * 45)
    
    if not IMPORTS_AVAILABLE:
        print("❌ Package imports failed - cannot run tests")
        print("   Please ensure the package is properly installed")
        return False
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDataLoading,
        TestBasicSimulation, 
        TestScenarioSystem,
        TestAnalysis
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Display summary
    print("\\n" + "=" * 45)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if result.errors:
        print("\\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\\n✅ All tests passed successfully!")
    else:
        print("\\n❌ Some tests failed - check output above")
    
    return success


if __name__ == "__main__":
    run_tests()
'''

with open('tests/test_basic.py', 'w') as f:
    f.write(test_file)

# Create contributing guidelines  
contributing_doc = '''# Contributing to LLM Tourism Simulation System 🤝

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git fork https://github.com/llm-tourism-sim/llm-tourism-sim.git
   git clone https://github.com/YOUR_USERNAME/llm-tourism-sim.git
   cd llm-tourism-sim
   ```

2. **Install Development Dependencies**
   ```bash
   pip install -e .[dev,examples,docs]
   ```

3. **Run Tests**
   ```bash
   python tests/test_basic.py
   # Or with pytest (if installed)
   pytest tests/
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
black llm_tourism_sim/

# Check style (if flake8 is installed)  
flake8 llm_tourism_sim/
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
- Update `docs/API.md` for new public functions
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
   - Add to `llm_tourism_sim/data/tourist_personas.json`
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

## 📦 Pull Request Process

### Before Submitting

1. **Code Quality**
   ```bash
   # Run tests
   python tests/test_basic.py
   
   # Check imports work
   python -c "import llm_tourism_sim; print('✅ Import successful')"
   
   # Test examples
   python examples/basic_simulation.py
   ```

2. **Documentation**
   - Update relevant documentation files
   - Add docstrings to new functions
   - Include examples for new features

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Existing tests pass
- [ ] New tests added for new functionality
- [ ] Examples updated if needed

## Documentation
- [ ] Code includes docstrings
- [ ] API documentation updated
- [ ] README updated if needed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes (or clearly documented)
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

Every contribution is valuable and appreciated! 🙏

---

*For questions about these guidelines, please open a GitHub Discussion or contact the maintainers.*
'''

with open('docs/CONTRIBUTING.md', 'w') as f:
    f.write(contributing_doc)

print("✅ tests/test_basic.py created")
print("✅ docs/CONTRIBUTING.md created")