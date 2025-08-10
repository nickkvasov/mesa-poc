"""
Simulation Package
=================

Core simulation modules for the LLM Tourism Simulation System.
"""

# Import data loader functions first (no heavy dependencies)
from .data_loader import (
    load_data, load_personas, load_hotspots, load_business_rules, load_scenarios,
    validate_personas_data, validate_hotspots_data, validate_business_rules_data
)

# Import heavy modules only when needed
try:
    from .models.tourism_model import TourismModel, ScenarioAwareTourismModel
    from .models.scenario_manager import ScenarioManager, TourismScenario
    from .agents.tourist import Tourist, ScenarioAwareTourist
    from .agents.hotspot import Hotspot, ScenarioAwareHotspot
    HEAVY_IMPORTS_AVAILABLE = True
except ImportError:
    HEAVY_IMPORTS_AVAILABLE = False

# Base exports (always available)
__all__ = [
    'load_data',
    'load_personas',
    'load_hotspots',
    'load_business_rules',
    'load_scenarios',
    'validate_personas_data',
    'validate_hotspots_data',
    'validate_business_rules_data'
]

# Add heavy imports if available
if HEAVY_IMPORTS_AVAILABLE:
    __all__.extend([
        'TourismModel',
        'ScenarioAwareTourismModel',
        'ScenarioManager', 
        'TourismScenario',
        'Tourist',
        'ScenarioAwareTourist',
        'Hotspot',
        'ScenarioAwareHotspot'
    ])
