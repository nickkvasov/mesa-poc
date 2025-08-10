# API Reference 🔧

Complete API documentation for the LLM Tourism Simulation System.

## Project Structure

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

### Import Patterns

```python
# New recommended imports
from sim import TourismModel, load_data, validate_personas_data
from utils import ResultsStorage, analyze_simulation_results

# Legacy imports (still supported)
from tourism_model import TourismModel
from data_loader import load_data
```

## Core Classes

### TourismModel

Main simulation model for basic tourism dynamics.

```python
class TourismModel(Model):
    def __init__(self, personas_data, hotspots_data, business_rules, 
                 num_tourists=50, grid_width=20, grid_height=20, random_seed=None)
```

**Parameters:**
- `personas_data`: List of persona dictionaries from JSON
- `hotspots_data`: List of hotspot dictionaries from JSON  
- `business_rules`: Business rules dictionary from JSON
- `num_tourists`: Number of tourist agents to create
- `grid_width/height`: Spatial grid dimensions
- `random_seed`: For reproducible results

**Methods:**
- `run_simulation(steps)`: Execute simulation for specified steps
- `get_hotspot_statistics()`: Get detailed hotspot metrics
- `get_persona_statistics()`: Get persona-grouped statistics  
- `get_summary_report()`: Generate comprehensive analysis report
- `get_model_data()`: Get time series data from datacollector
- `get_agent_data()`: Get agent-level data from datacollector

### ScenarioAwareTourismModel

Extended model with scenario support for policy testing.

```python
class ScenarioAwareTourismModel(TourismModel):
    def __init__(self, scenario=None, **kwargs)
```

**Additional Parameters:**
- `scenario`: TourismScenario instance for what-if testing

**Additional Methods:**
- `set_scenario(scenario)`: Change active scenario
- `get_scenario_impact_summary()`: Get scenario effect summary
- `compare_with_baseline(baseline_results)`: Compare with baseline simulation

## Agent Classes

### Tourist / ScenarioAwareTourist

Individual tourist agents with persona-driven behavior.

**Key Attributes:**
- `persona_type`: Tourist persona category
- `satisfaction`: Current satisfaction score (0-1)
- `visited_hotspots`: List of visited hotspot IDs
- `recommendations_received`: Social recommendations from other tourists

**Key Methods:**
- `step()`: Execute one step of tourist behavior
- `choose_hotspot()`: Select next destination based on preferences
- `visit_hotspot()`: Visit chosen hotspot and update satisfaction
- `share_experience()`: Post social media about experience
- `make_recommendations()`: Recommend hotspots to nearby tourists

### Hotspot / ScenarioAwareHotspot  

Tourism destination agents with capacity and popularity dynamics.

**Key Attributes:**
- `name`: Hotspot name
- `current_popularity`: Dynamic popularity score (0-1)
- `visitors_today`: Current day visitor count
- `capacity`: Maximum visitor capacity
- `appeal_to_personas`: Dict of persona appeal scores

**Key Methods:**
- `step()`: Update popularity and reset counters
- `record_visit()`: Record tourist visit
- `add_social_boost(boost)`: Apply social media popularity boost
- `get_statistics()`: Get comprehensive hotspot metrics

## Scenario Management

### TourismScenario

Defines what-if scenarios for policy testing.

```python
@dataclass
class TourismScenario:
    name: str
    description: str
    events: List[Dict]
    regulations: Dict
    external_factors: Dict
```

**Methods:**
- `add_event(step, type, target, parameters)`: Add timed event
- `add_regulation(type, parameters)`: Add ongoing regulation  
- `add_external_factor(name, value)`: Add behavioral modifier
- `get_summary()`: Get scenario overview

### ScenarioManager

Manages multiple scenarios and comparisons.

```python
class ScenarioManager:
    def __init__(self, scenarios_file=None)
```

**Methods:**
- `load_scenarios_from_file(path)`: Load scenarios from JSON
- `get_scenario(name)`: Retrieve scenario by name
- `list_scenarios()`: Get all available scenario names
- `create_scenario(name, description)`: Create new custom scenario
- `compare_scenarios(names)`: Compare multiple scenarios

## Results Storage

### ResultsStorage

Manages storage of simulation results in timestamped directories.

```python
class ResultsStorage:
    def __init__(self, base_output_dir="outputs")
```

**Methods:**
- `save_simulation_results(model_data, agent_data=None, hotspot_stats=None, persona_stats=None, simulation_config=None)`: Save comprehensive simulation results
- `save_scenario_comparison(baseline_results, scenario_results, comparison_analysis)`: Save scenario comparison results
- `save_charts(charts_data)`: Save generated visualizations
- `save_model_state(model, filename)`: Save complete model state
- `create_readme(simulation_info)`: Create README for output directory
- `get_output_directory()`: Get current output directory path
- `get_timestamp()`: Get current timestamp string

### Utility Functions

```python
# Get latest output directory
latest_dir = get_latest_output_dir(base_output_dir="outputs")

# List all output directories
outputs = list_output_directories(base_output_dir="outputs")
```

## Utility Functions

### Data Loading

```python
# Load all configuration data
personas, hotspots, rules, scenarios = load_data(data_dir=None)

# Load individual components
personas = load_personas(file_path=None)
hotspots = load_hotspots(file_path=None)  
rules = load_business_rules(file_path=None)
scenarios = load_scenarios(file_path=None)

# Validate data
is_valid = validate_personas_data(personas)
is_valid = validate_hotspots_data(hotspots)
```

### Analysis Functions

```python
# Comprehensive analysis
analysis = analyze_simulation_results(model_data, hotspot_stats, persona_stats)

# Scenario comparison
comparison = compare_scenarios(baseline_results, scenario_results)

# Policy recommendations
recommendations = generate_policy_recommendations(analysis_results)

# Satisfaction metrics
metrics = calculate_satisfaction_metrics(satisfaction_data)
```

### Visualization Functions

```python
# Popularity evolution chart
fig = create_popularity_chart(model_data, title="Popularity Over Time")

# Satisfaction by persona
fig = create_satisfaction_chart(persona_stats, title="Tourist Satisfaction")

# Scenario comparison
fig = create_scenario_comparison(scenario_results, metrics=['satisfaction'])

# Hotspot impact heatmap  
fig = create_hotspot_impact_heatmap(impact_data, title="Scenario Impacts")

# Tourism hotspot map
fig = plot_hotspot_map(hotspots_data, popularity_data)

# Comprehensive dashboard
fig = create_time_series_dashboard(model_data, title="Simulation Dashboard")
```

## Data Structures

### Persona Dictionary Structure

```python
{
    "type": "Budget Backpacker",
    "description": "Young, cost-conscious travelers...",
    "demographics": {
        "budget_level": "low",
        "age_group": "young", 
        "origin": "Europe",
        "typical_group_size": 1
    },
    "behavioral_traits": {
        "social_influence": 0.8,
        "recommendation_trust": 0.9,
        "exploration_tendency": 0.7,
        "price_sensitivity": 0.9
    },
    "travel_patterns": {
        "daily_visits": 3,
        "movement_speed": 2,
        "sharing_probability": 0.8,
        "influence_on_similar_personas": 0.7,
        "influence_on_different_personas": 0.3
    }
}
```

### Hotspot Dictionary Structure

```python
{
    "name": "Historic Old Town",
    "description": "Charming historic district...",
    "category": "cultural",
    "location": {
        "x": 5,
        "y": 8,
        "neighborhood": "Heritage District"
    },
    "characteristics": {
        "initial_popularity": 0.7,
        "base_capacity": 100,
        "accessibility_level": "high"
    },
    "appeal_to_personas": {
        "Cultural Explorer": {
            "appeal_score": 0.9,
            "reasons": ["historical significance", "cultural immersion"]
        },
        "Budget Backpacker": {
            "appeal_score": 0.7,
            "reasons": ["free walking areas", "authentic culture"]
        }
    },
    "amenities": ["guided tours", "street performers", "historical markers"]
}
```

### Event Dictionary Structure

```python
{
    "step": 5,
    "type": "capacity_boost",
    "target": "Riverside Park", 
    "parameters": {
        "capacity_multiplier": 2.0
    },
    "description": "Festival infrastructure doubles park capacity",
    "reasoning": "Temporary stages and seating increase venue capacity"
}
```

### Results Storage Structure

```python
# Output directory structure
{
    "timestamp": "20250810_214805",
    "simulation_date": "2025-08-10T21:48:05.872631",
    "files_saved": {
        "model_data": "outputs/20250810_214805/data/model_data.csv",
        "agent_data": "outputs/20250810_214805/data/agent_data.csv",
        "hotspot_stats": "outputs/20250810_214805/data/hotspot_stats.json",
        "persona_stats": "outputs/20250810_214805/data/persona_stats.json",
        "metadata": "outputs/20250810_214805/metadata.json"
    },
    "model_steps": 15,
    "total_agents": 555,
    "hotspots_count": 7,
    "personas_count": 5
}
```

## Event Types

### Hotspot Events
- `capacity_boost`: Increase hotspot capacity temporarily
- `capacity_reset`: Return capacity to baseline
- `appeal_boost`: Increase appeal to specific personas
- `appeal_reset`: Return appeal to baseline
- `accessibility_reduction`: Make hotspot harder to reach
- `construction_complete`: Improve accessibility after construction
- `noise_pollution`: Reduce satisfaction due to noise
- `appeal_reduction`: Decrease appeal to all personas

### Persona Events  
- `satisfaction_penalty`: Reduce satisfaction for persona type
- `appeal_boost`: Increase persona appeal sensitivity

### Regulation Types
- `luxury_tax`: Tax on luxury category hotspots
- `capacity_limit`: Hard capacity limits on specific hotspots
- `restricted_access`: Limited access during certain periods

### External Factor Types
- `cost_sensitivity`: Increased price awareness
- `event_excitement`: General excitement and mood boost
- `inconvenience_tolerance`: Tolerance for disruption
- `noise_tolerance`: Tolerance for crowding and noise
- `luxury_stigma`: Social pressure against luxury consumption
- `alternative_seeking`: Tendency to explore alternatives

## Error Handling

### Common Exceptions

```python
# Data loading errors
try:
    personas, hotspots, rules, scenarios = load_data()
except FileNotFoundError:
    print("Data files not found - check data directory")
except json.JSONDecodeError:
    print("Invalid JSON format in data files")

# Model creation errors  
try:
    model = TourismModel(personas_data=personas, hotspots_data=hotspots)
except ValueError as e:
    print(f"Invalid model configuration: {e}")

# Simulation errors
try:
    results = model.run_simulation(steps=20)
except Exception as e:
    print(f"Simulation error: {e}")

# Results storage errors
try:
    storage = ResultsStorage()
    saved_files = storage.save_simulation_results(model_data=results)
except PermissionError:
    print("Permission denied - check write access to outputs directory")
```

### Validation Functions

```python
# Validate data integrity
from sim import validate_personas_data, validate_hotspots_data

is_valid = validate_personas_data(personas)
if not is_valid:
    print("Persona data validation failed")

is_valid = validate_hotspots_data(hotspots)  
if not is_valid:
    print("Hotspot data validation failed")
```

## Performance Considerations

### Memory Usage
- Tourist agents: ~1KB each
- Hotspot agents: ~0.5KB each  
- Model overhead: ~10MB base
- Total: ~50MB for typical simulation (50 tourists, 7 hotspots)

### Execution Speed
- Basic step: ~1ms per tourist per step
- Scenario processing: +20% overhead
- Data collection: +10% overhead
- Typical simulation (50 tourists, 20 steps): ~2-5 seconds

### Storage Requirements
- Model data CSV: ~1KB per step
- Agent data CSV: ~5KB per step
- Statistics JSON: ~2KB per simulation
- Total per simulation: ~100-500KB

### Optimization Tips
```python
# For large simulations, disable some data collection
model.datacollector = None

# Use smaller grids for faster neighbor searches  
model = TourismModel(grid_width=10, grid_height=10)

# Reduce social interaction range
business_rules["recommendation_mechanics"]["word_of_mouth_range"] = 1

# Use efficient results storage
storage = ResultsStorage()
storage.save_simulation_results(
    model_data=results,
    # Only save essential data for large simulations
    agent_data=None,
    simulation_config={"num_tourists": 100, "steps": 50}
)
```

## Command Line Interface

### Output Management Commands
```bash
# List all simulation outputs
python utils/list_outputs.py list

# Show latest output information
python utils/list_outputs.py latest

# Explore output directory contents
python utils/list_outputs.py explore

# Explore specific output directory
python utils/list_outputs.py explore 20250810_214805
```

### Simulation Commands
```bash
# Run basic simulation
python examples/basic_simulation.py

# Run scenario comparison
python examples/scenario_comparison.py

# Run tests
python tests/test_basic.py
```
