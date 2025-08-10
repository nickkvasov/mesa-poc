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
git clone https://github.com/llm-tourism-sim/llm-tourism-sim.git
cd llm-tourism-sim
pip install -e .
```

#### Method 2: Development Installation
```bash
git clone https://github.com/llm-tourism-sim/llm-tourism-sim.git
cd llm-tourism-sim
pip install -e .[dev,examples,docs]
```

## Quick Start Examples

### 1. Basic Simulation

```python
from llm_tourism_sim import load_data, TourismModel

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
print(f"Average satisfaction: {results['Average_Satisfaction'].iloc[-1]:.3f}")
```

### 2. Scenario Testing

```python
from llm_tourism_sim import ScenarioAwareTourismModel
from llm_tourism_sim.scenarios.scenario_manager import ScenarioManager

# Load scenarios
manager = ScenarioManager("llm_tourism_sim/data/scenarios_events.json")
scenario = manager.get_scenario("Summer Music Festival")

# Test scenario
model = ScenarioAwareTourismModel(
    scenario=scenario,
    personas_data=personas,
    hotspots_data=hotspots,
    num_tourists=40
)

results = model.run_simulation(steps=20)
```

### 3. Custom Analysis

```python
from llm_tourism_sim.utils.analysis import analyze_simulation_results

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
from llm_tourism_sim.scenarios.scenario_manager import TourismScenario

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
from llm_tourism_sim.utils.visualization import create_popularity_chart

# Create popularity chart
fig = create_popularity_chart(
    model_data=results,
    title="Tourism Popularity Over Time",
    save_path="popularity_chart.png"
)
```

### Performance Analysis

```python
from llm_tourism_sim.utils.analysis import compare_scenarios

# Compare multiple scenarios
comparison = compare_scenarios(baseline_results, [scenario1_results, scenario2_results])

# Get ranking
best_scenario = comparison['ranking_analysis']['best_scenario']
print(f"Best performing scenario: {best_scenario}")
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

### Data Export
```bash
# Export sample data
python -c "from llm_tourism_sim.utils.data_loader import export_data_sample; export_data_sample()"
```

## Troubleshooting

### Common Issues

**Issue**: Import errors when running examples
**Solution**: Ensure you're running from the project root directory or install with `pip install -e .`

**Issue**: JSON file not found errors
**Solution**: Check that data files exist in `llm_tourism_sim/data/` directory

**Issue**: Mesa version conflicts  
**Solution**: Install specific version: `pip install mesa==3.2.0`

### Performance Optimization

- **Large Simulations**: Reduce `num_tourists` or `simulation_steps` for faster execution
- **Memory Usage**: Use smaller grid sizes (`grid_width`, `grid_height`)
- **Reproducibility**: Always set `random_seed` parameter

## Best Practices

### Simulation Design
1. Start with small simulations (20-30 tourists, 10-15 steps)
2. Use consistent random seeds for comparison
3. Run baseline before testing scenarios
4. Validate results with multiple runs

### Scenario Testing
1. Test one change at a time for clear attribution
2. Use realistic parameter ranges
3. Document scenario assumptions and rationale
4. Compare against meaningful baselines

### Analysis
1. Focus on statistical significance over raw numbers
2. Consider multiple metrics (satisfaction, popularity, visitors)
3. Generate policy recommendations based on evidence
4. Export results for further analysis

## Next Steps

- Read the [API Documentation](API.md) for detailed function references
- Check [Contributing Guidelines](CONTRIBUTING.md) to extend the system
- Explore advanced examples in the `examples/` directory
- Join discussions on GitHub for community support
