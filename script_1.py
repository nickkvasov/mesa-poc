# Create the main package __init__.py
main_init = '''"""
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
from .models.tourism_model import TourismModel, ScenarioAwareTourismModel
from .agents.tourist import Tourist, ScenarioAwareTourist
from .agents.hotspot import Hotspot, ScenarioAwareHotspot
from .scenarios.scenario_manager import ScenarioManager, TourismScenario
from .utils.data_loader import load_data, load_personas, load_hotspots, load_business_rules, load_scenarios
from .utils.visualization import create_popularity_chart, create_satisfaction_chart, create_scenario_comparison
from .utils.analysis import analyze_simulation_results, compare_scenarios, generate_policy_recommendations

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
    'create_popularity_chart',
    'create_satisfaction_chart',
    'create_scenario_comparison',
    'analyze_simulation_results',
    'compare_scenarios',
    'generate_policy_recommendations'
]
'''

# Write main __init__.py
with open('llm_tourism_sim/__init__.py', 'w') as f:
    f.write(main_init)

# Create agents __init__.py
agents_init = '''"""
Agent Classes for Tourism Simulation
====================================

This module contains the core agent classes that represent tourists and hotspots
in the tourism simulation system.

Classes:
    Tourist: Base tourist agent with persona-driven behavior
    ScenarioAwareTourist: Enhanced tourist that responds to scenarios
    Hotspot: Base hotspot agent representing tourism destinations
    ScenarioAwareHotspot: Enhanced hotspot that adapts to policy changes
"""

from .tourist import Tourist, ScenarioAwareTourist
from .hotspot import Hotspot, ScenarioAwareHotspot

__all__ = ['Tourist', 'ScenarioAwareTourist', 'Hotspot', 'ScenarioAwareHotspot']
'''

with open('llm_tourism_sim/agents/__init__.py', 'w') as f:
    f.write(agents_init)

# Create models __init__.py
models_init = '''"""
Model Classes for Tourism Simulation
====================================

This module contains the main simulation model classes that orchestrate
the tourism simulation and manage agent interactions.

Classes:
    TourismModel: Base tourism simulation model
    ScenarioAwareTourismModel: Enhanced model with scenario support
"""

from .tourism_model import TourismModel, ScenarioAwareTourismModel

__all__ = ['TourismModel', 'ScenarioAwareTourismModel']
'''

with open('llm_tourism_sim/models/__init__.py', 'w') as f:
    f.write(models_init)

# Create scenarios __init__.py
scenarios_init = '''"""
Scenario Management for Tourism Simulation
==========================================

This module provides classes and functions for managing what-if scenarios
in the tourism simulation system.

Classes:
    TourismScenario: Defines a tourism policy scenario
    ScenarioManager: Manages multiple scenarios and comparisons
"""

from .scenario_manager import ScenarioManager, TourismScenario

__all__ = ['ScenarioManager', 'TourismScenario']
'''

with open('llm_tourism_sim/scenarios/__init__.py', 'w') as f:
    f.write(scenarios_init)

# Create utils __init__.py
utils_init = '''"""
Utility Functions for Tourism Simulation
========================================

This module provides utility functions for data loading, visualization,
and analysis of tourism simulation results.

Functions:
    Data Loading: load_data, load_personas, load_hotspots, etc.
    Visualization: create_popularity_chart, create_satisfaction_chart, etc.
    Analysis: analyze_simulation_results, compare_scenarios, etc.
"""

from .data_loader import (
    load_data, load_personas, load_hotspots, 
    load_business_rules, load_scenarios
)
from .visualization import (
    create_popularity_chart, create_satisfaction_chart,
    create_scenario_comparison, plot_hotspot_map
)
from .analysis import (
    analyze_simulation_results, compare_scenarios,
    generate_policy_recommendations, calculate_satisfaction_metrics
)

__all__ = [
    'load_data', 'load_personas', 'load_hotspots', 'load_business_rules', 'load_scenarios',
    'create_popularity_chart', 'create_satisfaction_chart', 'create_scenario_comparison', 'plot_hotspot_map',
    'analyze_simulation_results', 'compare_scenarios', 'generate_policy_recommendations', 'calculate_satisfaction_metrics'
]
'''

with open('llm_tourism_sim/utils/__init__.py', 'w') as f:
    f.write(utils_init)

print("✅ Package __init__.py files created!")
print("   - Main package initialization with API exports")
print("   - Subpackage initializations for agents, models, scenarios, utils")
print("   - Comprehensive docstrings and version information")