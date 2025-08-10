#!/usr/bin/env python3
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
    # Import validation functions (should work without numpy)
    from sim import validate_personas_data, validate_hotspots_data, load_data
    VALIDATION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Validation imports failed: {e}")
    VALIDATION_AVAILABLE = False

try:
    # Import heavy modules (may fail without numpy)
    from sim import TourismModel, ScenarioAwareTourismModel, TourismScenario, ScenarioManager
    from utils import analyze_simulation_results
    HEAVY_IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Heavy imports failed: {e}")
    HEAVY_IMPORTS_AVAILABLE = False

IMPORTS_AVAILABLE = VALIDATION_AVAILABLE or HEAVY_IMPORTS_AVAILABLE


@unittest.skipUnless(VALIDATION_AVAILABLE, "Validation functions not available")
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


@unittest.skipUnless(HEAVY_IMPORTS_AVAILABLE, "Heavy imports not available")
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


@unittest.skipUnless(HEAVY_IMPORTS_AVAILABLE, "Heavy imports not available")
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


@unittest.skipUnless(HEAVY_IMPORTS_AVAILABLE, "Heavy imports not available")  
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
    print("\n" + "=" * 45)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\n')[-2]}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\n')[-2]}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ Some tests failed - check output above")

    return success


if __name__ == "__main__":
    run_tests()
