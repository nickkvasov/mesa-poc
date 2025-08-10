# Usage Guide 📖

This guide provides comprehensive instructions for using the LLM Tourism Simulation System.

## Installation & Setup

### System Requirements
- Python 3.8 or higher
- 4GB RAM (8GB recommended for large simulations)
- 500MB disk space

### Installation Methods

#### Method 1: Direct Installation
```bash
git clone https://github.com/nickkvasov/mesa-poc.git
cd llm-tourism-sim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Method 2: Development Installation
```bash
git clone https://github.com/nickkvasov/mesa-poc.git
cd llm-tourism-sim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with development dependencies
pip install -r requirements.txt
pip install pytest black flake8  # Optional development tools
```

## Quick Start Examples

### 1. Basic Simulation

```python
from sim import load_data, TourismModel
from utils import ResultsStorage

# Load configuration
personas, hotspots, rules, scenarios = load_data()

# Create model
model = TourismModel(
    personas_data=personas,
    hotspots_data=hotspots,
    business_rules=rules,
    num_tourists=30
)

# Run simulation
results = model.run_simulation(steps=15)

# Save results to timestamped directory
storage = ResultsStorage()
saved_files = storage.save_simulation_results(
    model_data=results,
    agent_data=model.get_agent_data(),
    hotspot_stats=model.get_hotspot_statistics(),
    persona_stats=model.get_persona_statistics()
)

print(f"Results saved to: {storage.get_output_directory()}")
print(f"Average satisfaction: {results['Average_Satisfaction'].iloc[-1]:.3f}")
```

### 2. Scenario Testing

```python
from sim import ScenarioAwareTourismModel, ScenarioManager
from utils import ResultsStorage

# Load scenarios
manager = ScenarioManager("scenarios_events.json")
scenario = manager.get_scenario("Summer Music Festival")

# Test scenario
model = ScenarioAwareTourismModel(
    scenario=scenario,
    personas_data=personas,
    hotspots_data=hotspots,
    num_tourists=40
)

results = model.run_simulation(steps=20)

# Save scenario results
storage = ResultsStorage()
saved_files = storage.save_simulation_results(
    model_data=results,
    simulation_config={
        "scenario_name": scenario.name,
        "num_tourists": 40,
        "steps": 20
    }
)
```

### 3. Custom Analysis

```python
from utils import analyze_simulation_results

# Run analysis
analysis = analyze_simulation_results(
    model_data=results,
    hotspot_stats=model.get_hotspot_statistics(),
    persona_stats=model.get_persona_statistics()
)

# Get recommendations
recommendations = analysis['recommendations']
for rec in recommendations:
    print(f"[{rec['priority']}] {rec['recommendation']}")
```

### 4. Results Management

```python
from utils import list_output_directories, get_latest_output_dir

# List all simulation outputs
outputs = list_output_directories()
for output in outputs:
    print(f"📂 {output['timestamp']}: {output['simulation_date']}")

# Get latest output directory
latest_dir = get_latest_output_dir()
print(f"Latest results: {latest_dir}")
```

## Configuration Files

### Tourist Personas (`tourist_personas.json`)

Structure:
```json
{
  "personas": [
    {
      "type": "Budget Backpacker",
      "demographics": {
        "budget_level": "low",
        "age_group": "young"
      },
      "behavioral_traits": {
        "social_influence": 0.8,
        "exploration_tendency": 0.7
      },
      "travel_patterns": {
        "daily_visits": 3,
        "sharing_probability": 0.8
      }
    }
  ]
}
```

### Urban Hotspots (`urban_hotspots.json`)

Structure:
```json
{
  "hotspots": [
    {
      "name": "Historic Old Town",
      "category": "cultural",
      "location": {"x": 5, "y": 8},
      "characteristics": {
        "initial_popularity": 0.7,
        "base_capacity": 100
      },
      "appeal_to_personas": {
        "Cultural Explorer": {
          "appeal_score": 0.9,
          "reasons": ["historical significance"]
        }
      }
    }
  ]
}
```

### Scenarios (`scenarios_events.json`)

Structure:
```json
{
  "scenarios": [
    {
      "name": "Summer Music Festival",
      "category": "event-driven",
      "events": [
        {
          "step": 5,
          "type": "capacity_boost",
          "target": "Riverside Park",
          "parameters": {"capacity_multiplier": 2.0}
        }
      ],
      "external_factors": {
        "event_excitement": {"value": 0.3}
      }
    }
  ]
}
```

## Advanced Features

### Custom Scenario Creation

```python
from sim import TourismScenario

# Create new scenario
scenario = TourismScenario(
    name="Digital Art Exhibition",
    description="Tech-focused art exhibition at gallery",
    category="cultural-tech"
)

# Add events
scenario.add_event(
    step=3,
    event_type="appeal_boost",
    target="Art Gallery District",
    parameters={
        "appeal_boost": 0.4,
        "target_personas": ["Cultural Explorer", "Adventure Seeker"]
    }
)

# Add external factors
scenario.add_external_factor("tech_excitement", 0.25)
```

### Data Visualization

```python
from utils import create_popularity_chart

# Create popularity chart
fig = create_popularity_chart(
    model_data=results,
    title="Tourism Popularity Over Time",
    save_path="popularity_chart.png"
)
```

### Performance Analysis

```python
from utils import compare_scenarios

# Compare multiple scenarios
comparison = compare_scenarios(baseline_results, [scenario1_results, scenario2_results])

# Get ranking
best_scenario = comparison['ranking_analysis']['best_scenario']
print(f"Best performing scenario: {best_scenario}")
```

### Results Storage and Management

```python
from utils import ResultsStorage

# Initialize storage
storage = ResultsStorage()

# Save comprehensive results
saved_files = storage.save_simulation_results(
    model_data=results,
    agent_data=agent_data,
    hotspot_stats=hotspot_stats,
    persona_stats=persona_stats,
    simulation_config={
        "num_tourists": 50,
        "steps": 20,
        "random_seed": 42
    }
)

# Save charts
charts_data = {
    "popularity_chart": fig,
    "satisfaction_chart": fig2
}
chart_files = storage.save_charts(charts_data)

# Create README for the output
simulation_info = {
    "duration": "20 steps",
    "steps": 20,
    "num_tourists": 50,
    "num_hotspots": 7
}
readme_path = storage.create_readme(simulation_info)
```

## Command Line Interface

### Running Examples
```bash
# Basic simulation
python examples/basic_simulation.py

# Scenario comparison
python examples/scenario_comparison.py

# Custom analysis
python examples/custom_analysis.py
```

### Results Management
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

### Data Export
```bash
# Export sample data
python -c "from sim import export_data_sample; export_data_sample()"
```

## Results Storage System

### Output Directory Structure
Each simulation creates a timestamped directory with organized structure:

```
outputs/20250810_214805/
├── README.md                    # Simulation documentation
├── metadata.json               # Simulation metadata and file index
├── data/                       # Raw simulation data
│   ├── model_data.csv         # Time series data (CSV)
│   ├── agent_data.csv         # Agent-level statistics (CSV)
│   ├── hotspot_stats.json     # Hotspot performance (JSON)
│   └── persona_stats.json     # Persona statistics (JSON)
├── charts/                     # Generated visualizations
│   ├── popularity_chart.png   # Matplotlib figures
│   └── chart_metadata.json    # Chart information
├── reports/                    # Analysis reports
│   ├── analysis_summary.json  # Analysis results
│   └── recommendations.json   # Policy recommendations
└── configs/                    # Simulation configurations
    └── simulation_config.json # Model configuration
```

### Loading Previous Results
```python
import pandas as pd
import json
from pathlib import Path

# Load model data
model_data = pd.read_csv('outputs/20250810_214805/data/model_data.csv')

# Load statistics
with open('outputs/20250810_214805/data/hotspot_stats.json', 'r') as f:
    hotspot_stats = json.load(f)

# Load metadata
with open('outputs/20250810_214805/metadata.json', 'r') as f:
    metadata = json.load(f)
```

## Troubleshooting

### Common Issues

**Issue**: Import errors when running examples
**Solution**: Ensure you're running from the project root directory and have activated the virtual environment

**Issue**: JSON file not found errors
**Solution**: Check that data files exist in the data/ directory

**Issue**: Mesa version conflicts  
**Solution**: Install specific version: `pip install mesa==3.2.0`

**Issue**: Results storage directory not created
**Solution**: Ensure you have write permissions in the project directory

### Performance Optimization

- **Large Simulations**: Reduce `num_tourists` or `simulation_steps` for faster execution
- **Memory Usage**: Use smaller grid sizes (`grid_width`, `grid_height`)
- **Reproducibility**: Always set `random_seed` parameter
- **Storage**: Use `storage.save_model_state()` for complete model preservation

## Best Practices

### Simulation Design
1. Start with small simulations (20-30 tourists, 10-15 steps)
2. Use consistent random seeds for comparison
3. Run baseline before testing scenarios
4. Validate results with multiple runs
5. Save results to timestamped directories for reproducibility

### Scenario Testing
1. Test one change at a time for clear attribution
2. Use realistic parameter ranges
3. Document scenario assumptions and rationale
4. Compare against meaningful baselines
5. Save scenario comparison results separately

### Analysis
1. Focus on statistical significance over raw numbers
2. Consider multiple metrics (satisfaction, popularity, visitors)
3. Generate policy recommendations based on evidence
4. Export results for further analysis
5. Use the results storage system for organization

### Results Management
1. Use timestamped directories to avoid overwriting
2. Create README files for each simulation run
3. Organize outputs by type (data, charts, reports)
4. Use the output management utilities for easy access
5. Archive important results for long-term storage

## Next Steps

- Read the [API Documentation](API.md) for detailed function references
- Check [Contributing Guidelines](CONTRIBUTING.md) to extend the system
- Explore the `outputs/` directory for example results
- Join discussions on GitHub for community support
