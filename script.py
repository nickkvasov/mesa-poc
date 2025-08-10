# Create a complete Python project structure for the Tourism Simulation System

import os
import json

# Create the main project structure
project_structure = {
    'llm_tourism_sim/': {
        '__init__.py': '',
        'agents/': {
            '__init__.py': '',
            'tourist.py': '',
            'hotspot.py': ''
        },
        'models/': {
            '__init__.py': '',
            'tourism_model.py': ''
        },
        'scenarios/': {
            '__init__.py': '',
            'scenario_manager.py': ''
        },
        'utils/': {
            '__init__.py': '',
            'data_loader.py': '',
            'visualization.py': '',
            'analysis.py': ''
        },
        'data/': {
            'tourist_personas.json': '',
            'urban_hotspots.json': '',
            'business_rules.json': '',
            'scenarios_events.json': '',
            'master_config.json': ''
        }
    },
    'examples/': {
        'basic_simulation.py': '',
        'scenario_comparison.py': '',
        'custom_analysis.py': ''
    },
    'tests/': {
        '__init__.py': '',
        'test_agents.py': '',
        'test_models.py': '',
        'test_scenarios.py': ''
    },
    'docs/': {
        'README.md': '',
        'USAGE.md': '',
        'API.md': '',
        'CONTRIBUTING.md': ''
    }
}

def create_project_structure(base_path='.', structure=None):
    """Create the project directory structure"""
    if structure is None:
        structure = project_structure
    
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if name.endswith('/'):  # Directory
            os.makedirs(path, exist_ok=True)
            if isinstance(content, dict):
                create_project_structure(path, content)
        else:  # File
            # Create parent directory if it doesn't exist
            parent_dir = os.path.dirname(path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)

# Create the project structure
create_project_structure()

print("✅ Project structure created!")
print("📁 Directory tree:")
print("""
llm_tourism_sim/
├── llm_tourism_sim/          # Main package
│   ├── __init__.py
│   ├── agents/               # Agent classes
│   │   ├── __init__.py
│   │   ├── tourist.py
│   │   └── hotspot.py
│   ├── models/               # Model classes
│   │   ├── __init__.py
│   │   └── tourism_model.py
│   ├── scenarios/            # Scenario management
│   │   ├── __init__.py
│   │   └── scenario_manager.py
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── visualization.py
│   │   └── analysis.py
│   └── data/                 # JSON configuration files
│       ├── tourist_personas.json
│       ├── urban_hotspots.json
│       ├── business_rules.json
│       ├── scenarios_events.json
│       └── master_config.json
├── examples/                 # Example scripts
│   ├── basic_simulation.py
│   ├── scenario_comparison.py
│   └── custom_analysis.py
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_models.py
│   └── test_scenarios.py
└── docs/                     # Documentation
    ├── README.md
    ├── USAGE.md
    ├── API.md
    └── CONTRIBUTING.md
""")