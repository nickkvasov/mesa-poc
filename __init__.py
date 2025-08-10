"""
LLM Tourism Simulation System
============================

A sophisticated agent-based tourism simulation system enhanced with Large Language Models
for generating realistic tourist personas, urban hotspots, and policy scenarios.

Key Features:
- LLM-generated tourist personas with rich behavioral profiles
- Dynamic urban hotspots with geospatial characteristics
- What-if scenario testing for tourism policy analysis
- Mesa-based agent modeling with social influence networks
- Comprehensive data visualization and analysis tools

Quick Start:
    from llm_tourism_sim import TourismModel, load_data
    
    # Load LLM-generated configuration
    personas, hotspots, rules = load_data()
    
    # Create and run simulation
    model = TourismModel(num_tourists=50)
    model.run_simulation(steps=20)
    
    # Analyze results
    results = model.get_analysis()
    model.visualize_results()

For detailed usage examples, see the examples/ directory.
"""

__version__ = "1.0.0"
__author__ = "LLM Tourism Simulation Team"
__email__ = "contact@llm-tourism-sim.org"
__license__ = "MIT"

# Import main classes for easy access
from tourism_model import TourismModel, ScenarioAwareTourismModel
from tourist import Tourist, ScenarioAwareTourist
from hotspot import Hotspot, ScenarioAwareHotspot
from scenario_manager import ScenarioManager, TourismScenario
from data_loader import load_data, load_personas, load_hotspots, load_business_rules, load_scenarios, validate_personas_data, validate_hotspots_data
from visualization import create_popularity_chart, create_satisfaction_chart, create_scenario_comparison, plot_hotspot_map
from analysis import analyze_simulation_results, compare_scenarios, generate_policy_recommendations, calculate_satisfaction_metrics
from results_storage import ResultsStorage, get_latest_output_dir, list_output_directories

# Main API functions
__all__ = [
    'TourismModel',
    'ScenarioAwareTourismModel', 
    'Tourist',
    'ScenarioAwareTourist',
    'Hotspot',
    'ScenarioAwareHotspot',
    'ScenarioManager',
    'TourismScenario',
    'load_data',
    'load_personas',
    'load_hotspots', 
    'load_business_rules',
    'load_scenarios',
    'validate_personas_data',
    'validate_hotspots_data',
    'create_popularity_chart',
    'create_satisfaction_chart',
    'create_scenario_comparison',
    'plot_hotspot_map',
    'analyze_simulation_results',
    'compare_scenarios',
    'generate_policy_recommendations',
    'calculate_satisfaction_metrics',
    'ResultsStorage',
    'get_latest_output_dir',
    'list_output_directories'
]
