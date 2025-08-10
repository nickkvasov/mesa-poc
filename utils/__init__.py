"""
Utility Modules
==============

Analysis, visualization, and storage utilities.
"""

from .analysis import analyze_simulation_results, compare_scenarios, generate_policy_recommendations
from .visualization import create_popularity_chart, create_satisfaction_chart, create_scenario_comparison
from .results_storage import ResultsStorage, get_latest_output_dir, list_output_directories
from .quick_visualize import (
    quick_visualize_simulation,
    quick_compare_scenarios,
    quick_summary_report,
    add_visualization_to_existing_simulation
)
from .scenario_builder import (
    ScenarioBuilder,
    create_quick_comparison_set,
    create_extreme_comparison_set
)

__all__ = [
    'analyze_simulation_results',
    'compare_scenarios',
    'generate_policy_recommendations',
    'create_popularity_chart',
    'create_satisfaction_chart', 
    'create_scenario_comparison',
    'ResultsStorage',
    'get_latest_output_dir',
    'list_output_directories',
    'quick_visualize_simulation',
    'quick_compare_scenarios',
    'quick_summary_report',
    'add_visualization_to_existing_simulation',
    'ScenarioBuilder',
    'create_quick_comparison_set',
    'create_extreme_comparison_set'
]
