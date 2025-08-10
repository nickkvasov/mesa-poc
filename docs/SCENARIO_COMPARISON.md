# Scenario Comparison Guide

This guide explains how to create and compare multiple distinctive scenarios with clearly different effects on tourism dynamics.

## Overview

The scenario comparison system allows you to:

- **Create Multiple Scenarios**: Build scenarios with different intensities, scales, and effects
- **Compare Performance**: Analyze how different scenarios affect tourism metrics
- **Generate Visualizations**: Create charts and reports comparing scenario outcomes
- **Make Data-Driven Decisions**: Use evidence-based insights for policy planning

## Quick Start

### 1. Using Pre-built Comparison Sets

The easiest way to compare scenarios is using pre-built sets:

```python
from utils.scenario_builder import create_quick_comparison_set, create_extreme_comparison_set

# Quick comparison set (6 scenarios)
scenarios = create_quick_comparison_set()

# Extreme comparison set (6 scenarios with dramatic effects)
extreme_scenarios = create_extreme_comparison_set()
```

### 2. Using the Scenario Builder

For more control, use the ScenarioBuilder class:

```python
from utils.scenario_builder import ScenarioBuilder

builder = ScenarioBuilder()

# Add baseline
builder.add_baseline()

# Add scenarios with different intensities
builder.add_marketing_scenario(name="Light Marketing", intensity="low")
builder.add_marketing_scenario(name="Aggressive Marketing", intensity="aggressive")

builder.add_festival_scenario(name="Small Festival", scale="small")
builder.add_festival_scenario(name="Major Festival", scale="major")

builder.add_construction_scenario(name="Light Construction", severity="light")
builder.add_construction_scenario(name="Severe Construction", severity="severe")

builder.add_policy_scenario(name="Luxury Tax", policy_type="tax", target="luxury")
builder.add_policy_scenario(name="Budget Subsidy", policy_type="subsidy", target="budget")

scenarios = builder.get_scenarios()
```

### 3. Running Comparisons

```python
from sim import load_data, ScenarioAwareTourismModel
from utils import quick_compare_scenarios

# Load data
personas, hotspots, business_rules, scenarios_data = load_data()

# Run simulations
results_collection = []
for scenario in scenarios:
    model = ScenarioAwareTourismModel(
        scenario=scenario,
        personas_data=personas,
        hotspots_data=hotspots,
        business_rules=business_rules,
        num_tourists=50,
        random_seed=42  # Same seed for fair comparison
    )
    
    model_data = model.run_simulation(steps=20)
    
    results_collection.append({
        'name': scenario.name,
        'model_data': model_data,
        'hotspot_stats': model.get_hotspot_statistics(),
        'persona_stats': model.get_persona_statistics(),
        'summary': {
            'final_metrics': {
                'avg_popularity': model_data.iloc[-1].get('Average_Popularity', 0),
                'total_visitors': int(model_data.iloc[-1].get('Total_Visitors', 0)),
                'social_shares': int(model_data.iloc[-1].get('Social_Shares', 0)),
                'avg_satisfaction': model_data.iloc[-1].get('Average_Satisfaction', 0)
            }
        }
    })

# Generate comparison visualizations
from utils import ResultsStorage

# Create timestamped output directory
storage = ResultsStorage()
output_dir = storage.get_output_directory()

comparison_files = quick_compare_scenarios(
    results_collection,
    output_dir=f"{output_dir}/my_scenario_comparison"
)
```

## Available Scenario Types

### 1. Marketing Scenarios

Marketing campaigns with configurable intensity:

```python
builder.add_marketing_scenario(
    name="My Marketing Campaign",
    intensity="high",  # "low", "medium", "high", "aggressive"
    duration_steps=20
)
```

**Intensity Levels:**
- **Low**: Small appeal boosts (0.2, 0.1)
- **Medium**: Moderate appeal boosts (0.4, 0.3, 0.2)
- **High**: Large appeal boosts (0.6, 0.5, 0.3)
- **Aggressive**: Maximum appeal boosts (0.8, 0.6, 0.4)

### 2. Festival Scenarios

Cultural festivals with configurable scale:

```python
builder.add_festival_scenario(
    name="My Festival",
    scale="large",  # "small", "medium", "large", "major"
    duration_steps=20
)
```

**Scale Levels:**
- **Small**: Appeal boost 0.4, capacity 1.5x
- **Medium**: Appeal boost 0.6, capacity 2.0x
- **Large**: Appeal boost 0.8, capacity 2.5x
- **Major**: Appeal boost 1.0, capacity 3.0x

### 3. Construction Scenarios

Infrastructure disruption with configurable severity:

```python
builder.add_construction_scenario(
    name="My Construction Project",
    severity="medium",  # "light", "medium", "heavy", "severe"
    duration_steps=20
)
```

**Severity Levels:**
- **Light**: Small appeal penalties (-0.2, -0.1)
- **Medium**: Moderate appeal penalties (-0.4, -0.3, -0.2)
- **Heavy**: Large appeal penalties (-0.6, -0.5, -0.3)
- **Severe**: Maximum appeal penalties (-0.8, -0.7, -0.5)

### 4. Policy Scenarios

Policy interventions with different types and targets:

```python
builder.add_policy_scenario(
    name="My Policy",
    policy_type="tax",  # "tax", "regulation", "subsidy", "ban"
    target="luxury",    # "luxury", "budget", "all"
    duration_steps=20
)
```

**Policy Types:**
- **Tax**: Reduces appeal of targeted services
- **Regulation**: Adds restrictions and reduces excitement
- **Subsidy**: Increases appeal and excitement
- **Ban**: Significantly reduces appeal and excitement

## Custom Scenarios

Create completely custom scenarios with specific events and factors:

```python
# Define custom events
custom_events = [
    {
        "step": 3,
        "type": "appeal_boost",
        "target": "Co-working Spaces",
        "parameters": {"appeal_boost": 0.6},
        "description": "Launch of digital nomad program",
        "reasoning": "Co-working spaces become more appealing to remote workers"
    },
    {
        "step": 8,
        "type": "capacity_boost",
        "target": "Co-working Spaces",
        "parameters": {"capacity_multiplier": 2.0},
        "description": "Expand co-working infrastructure",
        "reasoning": "Increased capacity for digital nomads"
    }
]

# Define external factors
external_factors = {
    "event_excitement": 0.4,
    "social_media_buzz": 0.5,
    "cultural_curiosity": 0.3
}

# Create custom scenario
custom_scenario = builder.add_custom_scenario(
    name="Digital Nomad Initiative",
    category="policy",
    description="Initiative to attract digital nomads",
    events=custom_events,
    external_factors=external_factors,
    target_demographics=["Adventure Seeker", "Cultural Explorer"],
    duration_steps=20
)
```

## Example Comparisons

### 1. Comprehensive Comparison

Run `examples/comprehensive_scenario_comparison.py` for a full comparison of 6 distinctive scenarios:

```bash
python examples/comprehensive_scenario_comparison.py
```

This creates:
- **Baseline**: No intervention
- **Aggressive Marketing**: High positive impact
- **Major Festival**: Event-driven positive impact
- **Construction Disruption**: Negative impact
- **Luxury Tax**: Policy intervention
- **Sustainable Tourism**: Mixed impact

### 2. Easy Comparison

Run `examples/easy_scenario_comparison.py` for multiple comparison methods:

```bash
python examples/easy_scenario_comparison.py
```

This demonstrates:
- Pre-built comparison sets
- Custom scenario configurations
- Extreme comparison sets

### 3. Test Comparison

Run `examples/test_scenario_comparison.py` for a simple test:

```bash
python examples/test_scenario_comparison.py
```

## Output Structure

Scenario comparisons generate organized output directories within timestamped folders, following the project's standard output organization:

```
outputs/20241210_143022/                    # Timestamped main directory
├── charts/                                 # Standard output structure
├── data/                                   # Standard output structure  
├── reports/                                # Standard output structure
├── configs/                                # Standard output structure
└── my_scenario_comparison/                 # Scenario comparison subdirectory
    ├── scenario_comparison.png             # Main comparison chart
    ├── scenario_comparison.csv             # Comparison data table
    ├── detailed_comparison.csv             # Detailed metrics
    ├── scenario_analysis_report.txt        # Analysis report
    └── individual_scenarios/               # Individual scenario results
        ├── baseline/
        ├── aggressive_marketing/
        └── construction_disruption/
```

## Interpreting Results

### Key Metrics

1. **Average Popularity**: Overall appeal of tourism destinations
2. **Average Satisfaction**: Tourist satisfaction levels
3. **Total Visitors**: Number of tourist visits
4. **Social Shares**: Social media engagement

### Performance Analysis

- **Positive Impact**: Scenarios that increase satisfaction and popularity
- **Negative Impact**: Scenarios that decrease satisfaction and popularity
- **Mixed Impact**: Scenarios with varying effects on different metrics

### Example Results

```
Scenario              Popularity  Satisfaction  Change
Baseline              0.720       0.624         -
Aggressive Marketing  0.799       0.968         +55%
Construction Disrupt  0.341       0.000         -100%
Luxury Tax           0.658       0.454         -27%
```

## Best Practices

### 1. Scenario Design

- **Use Clear Names**: Descriptive scenario names help with interpretation
- **Vary Intensity**: Include scenarios with different effect magnitudes
- **Consider Categories**: Mix different types of interventions
- **Include Baseline**: Always include a baseline for comparison

### 2. Simulation Setup

- **Same Random Seed**: Use identical random seeds for fair comparison
- **Consistent Parameters**: Keep other parameters (tourists, steps) constant
- **Adequate Duration**: Run simulations long enough to see effects

### 3. Analysis

- **Compare to Baseline**: Always measure changes relative to baseline
- **Consider Multiple Metrics**: Don't focus on just one metric
- **Look for Patterns**: Identify which scenario types work best
- **Validate Results**: Ensure results make logical sense

## Advanced Features

### 1. Custom Event Types

Create scenarios with specific event types:

```python
# Appeal boost events
scenario.add_event(step=5, event_type="appeal_boost", target="City Center", 
                  parameters={"appeal_boost": 0.5})

# Capacity boost events
scenario.add_event(step=5, event_type="capacity_boost", target="City Center", 
                  parameters={"capacity_multiplier": 2.0})

# Appeal reset events
scenario.add_event(step=15, event_type="appeal_reset", target="City Center", 
                  parameters={})
```

### 2. External Factors

Add external factors that affect tourist behavior:

```python
# Positive factors
scenario.add_external_factor("event_excitement", 0.5)
scenario.add_external_factor("social_media_buzz", 0.4)
scenario.add_external_factor("cultural_curiosity", 0.3)

# Negative factors
scenario.add_external_factor("inconvenience_tolerance", -0.4)
scenario.add_external_factor("noise_tolerance", -0.3)
scenario.add_external_factor("cost_sensitivity", 0.5)
```

### 3. Target Demographics

Specify which tourist personas are affected:

```python
scenario = TourismScenario(
    name="My Scenario",
    target_demographics=["Cultural Explorer", "Budget Backpacker"]
)
```

## Troubleshooting

### Common Issues

1. **No Effect**: Scenarios may not show effects if:
   - Events target non-existent hotspots
   - Effects are too small to be visible
   - Simulation duration is too short

2. **Identical Results**: If all scenarios show identical results:
   - Check that scenarios are being applied correctly
   - Verify that events are targeting valid locations
   - Ensure external factors are being processed

3. **Extreme Results**: If results are too extreme:
   - Reduce effect magnitudes
   - Use shorter simulation durations
   - Check for unintended interactions

### Performance Tips

1. **Batch Processing**: Run multiple scenarios in one script
2. **Parallel Processing**: Use multiprocessing for large comparisons
3. **Memory Management**: Clear variables between simulations
4. **Output Organization**: Use descriptive directory names

## Integration with Existing Code

### Adding to Existing Simulations

```python
# In your existing simulation code
from utils.scenario_builder import create_quick_comparison_set
from utils import quick_compare_scenarios

# Create scenarios
scenarios = create_quick_comparison_set()

# Run your existing simulation logic for each scenario
results = []
for scenario in scenarios:
    # Your existing simulation code here
    result = run_my_simulation(scenario)
    results.append(result)

# Generate comparison
from utils import ResultsStorage

storage = ResultsStorage()
output_dir = storage.get_output_directory()
comparison_files = quick_compare_scenarios(results, f"{output_dir}/my_comparison")
```

This guide covers the main scenario comparison capabilities. For more advanced features, explore the example files and source code in the `utils/scenario_builder.py` module.
