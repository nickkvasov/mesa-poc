# Visualization Guide

This guide explains how to add visualization capabilities to your tourism simulation results.

## Overview

The tourism simulation system includes comprehensive visualization tools that can generate:

- **Static Charts**: PNG images using Matplotlib and Seaborn
- **Interactive Charts**: HTML files using Plotly
- **Dashboards**: Multi-panel visualizations
- **Comparison Charts**: Scenario and hotspot comparisons
- **Maps**: Geographic hotspot visualizations

## Quick Start

### 1. Basic Visualization

Add visualization to any simulation with a single function call:

```python
from utils import add_visualization_to_existing_simulation

# After running your simulation
visualization_files = add_visualization_to_existing_simulation(
    model_data=results,
    hotspot_stats=model.get_hotspot_statistics(),
    persona_stats=model.get_persona_statistics(),
    output_dir="my_visualization"
)
```

### 2. Quick Visualization

For simple charts without complex setup:

```python
from utils import quick_visualize_simulation

chart_files = quick_visualize_simulation(
    model_data=results,
    hotspot_stats=hotspot_stats,
    persona_stats=persona_stats,
    output_dir="quick_charts",
    show_plots=True  # Display charts interactively
)
```

### 3. Scenario Comparison

Compare multiple scenarios:

```python
from utils import quick_compare_scenarios

comparison_files = quick_compare_scenarios(
    scenario_results=results_collection,
    output_dir="scenario_comparison"
)
```

## Available Chart Types

### 1. Popularity Evolution Chart

Shows how hotspot popularity changes over time:

```python
from utils.visualization import create_popularity_chart

fig = create_popularity_chart(
    model_data,
    title="Hotspot Popularity Evolution",
    save_path="popularity_chart.png"
)
```

### 2. Satisfaction by Persona Chart

Displays tourist satisfaction levels by persona type:

```python
from utils.visualization import create_satisfaction_chart

fig = create_satisfaction_chart(
    persona_stats,
    title="Tourist Satisfaction by Persona",
    save_path="satisfaction_chart.png"
)
```

### 3. Time Series Dashboard

Comprehensive dashboard with multiple metrics:

```python
from utils.visualization import create_time_series_dashboard

fig = create_time_series_dashboard(
    model_data,
    title="Tourism Simulation Dashboard",
    save_path="dashboard.png"
)
```

### 4. Scenario Comparison Chart

Compare performance across different scenarios:

```python
from utils.visualization import create_scenario_comparison

fig = create_scenario_comparison(
    scenario_results,
    metrics=['avg_popularity', 'total_visitors', 'social_shares', 'avg_satisfaction'],
    title="Scenario Performance Comparison",
    save_path="scenario_comparison.png"
)
```

### 5. Hotspot Map

Geographic visualization of hotspots:

```python
from utils.visualization import plot_hotspot_map

fig = plot_hotspot_map(
    hotspots_data,
    popularity_data=popularity_dict,
    title="Tourism Hotspots Map",
    save_path="hotspot_map.png"
)
```

### 6. Impact Heatmap

Shows how scenarios impact different hotspots:

```python
from utils.visualization import create_hotspot_impact_heatmap

fig = create_hotspot_impact_heatmap(
    impact_data,
    title="Hotspot Impact by Scenario",
    save_path="impact_heatmap.png"
)
```

## Interactive Visualizations

### Using Plotly

Create interactive HTML charts:

```python
import plotly.express as px
import plotly.graph_objects as go

# Interactive line chart
fig = px.line(model_data, x=model_data.index, y='Average_Popularity',
              title='Interactive Popularity Evolution')
fig.write_html("interactive_popularity.html")

# Interactive scatter plot
fig = px.scatter(hotspot_data, x='x_coord', y='y_coord', 
                size='popularity', color='category',
                title='Interactive Hotspot Map')
fig.write_html("interactive_map.html")
```

### Interactive Dashboard

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Popularity', 'Visitors', 'Satisfaction', 'Shares')
)

# Add traces...
fig.update_layout(title="Interactive Dashboard")
fig.write_html("interactive_dashboard.html")
```

## Examples

### 1. Basic Simulation with Visualization

Run `examples/basic_simulation_with_visualization.py`:

```bash
python examples/basic_simulation_with_visualization.py
```

This demonstrates how to add visualization to a basic simulation.

### 2. Comprehensive Visualization Demo

Run `examples/visualization_demo.py`:

```bash
python examples/visualization_demo.py
```

This shows all available chart types and features.

### 3. Interactive Visualization Demo

Run `examples/interactive_visualization.py`:

```bash
python examples/interactive_visualization.py
```

This demonstrates interactive Plotly charts.

## Output Structure

When you use visualization functions, they create organized output directories:

```
outputs/
├── 20241201_143022/           # Timestamped simulation run
│   ├── data/                  # Raw simulation data
│   │   ├── model_data.csv
│   │   ├── agent_data.csv
│   │   ├── hotspot_stats.json
│   │   └── persona_stats.json
│   ├── charts/                # Generated charts
│   │   ├── popularity_evolution.png
│   │   ├── satisfaction_by_persona.png
│   │   ├── simulation_dashboard.png
│   │   ├── scenario_comparison.png
│   │   ├── hotspot_map.png
│   │   └── impact_heatmap.png
│   ├── reports/               # Text reports
│   │   └── simulation_summary.txt
│   └── README.md              # Run documentation
└── visualization/             # Additional visualization outputs
    ├── charts/
    ├── data/
    └── reports/
```

## Customization

### Chart Styling

Customize chart appearance:

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Custom colors
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
```

### Custom Metrics

Add your own metrics to charts:

```python
# Add custom metric to model data
model_data['Custom_Metric'] = model_data['Average_Popularity'] * model_data['Average_Satisfaction']

# Use in visualization
fig = create_popularity_chart(
    model_data,
    title="Custom Metric Evolution",
    save_path="custom_metric.png"
)
```

### Advanced Plotly Features

```python
# Animated charts
fig = px.line(model_data, x='step', y='popularity', 
              animation_frame='scenario')

# 3D visualizations
fig = px.scatter_3d(data, x='x', y='y', z='popularity',
                   color='category')

# Range sliders
fig.update_xaxes(rangeslider_visible=True)

# Custom hover templates
fig.update_traces(hovertemplate='<b>%{fullData.name}</b><br>' +
                                 'Step: %{x}<br>' +
                                 'Popularity: %{y:.3f}<br>' +
                                 '<extra></extra>')
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Ensure all required packages are installed:
   ```bash
   pip install matplotlib seaborn plotly pandas numpy
   ```

2. **Display Issues**: For headless environments, use:
   ```python
   import matplotlib
   matplotlib.use('Agg')  # Non-interactive backend
   ```

3. **Memory Issues**: Close figures after saving:
   ```python
   plt.savefig("chart.png")
   plt.close()  # Free memory
   ```

4. **Data Format**: Ensure your data is in the correct format:
   ```python
   # Model data should be a DataFrame with time series
   # Hotspot stats should be a list of dictionaries
   # Persona stats should be a dictionary
   ```

### Performance Tips

1. **Batch Processing**: Generate multiple charts in one run
2. **Figure Management**: Close figures to free memory
3. **File Formats**: Use PNG for static charts, HTML for interactive
4. **Resolution**: Adjust DPI for different quality needs

## Integration with Existing Code

### Adding to Basic Simulation

```python
# In your existing simulation code
results = model.run_simulation(steps=15)

# Add these lines for visualization
from utils import add_visualization_to_existing_simulation

visualization_files = add_visualization_to_existing_simulation(
    model_data=results,
    hotspot_stats=model.get_hotspot_statistics(),
    persona_stats=model.get_persona_statistics(),
    output_dir="my_visualization"
)
```

### Adding to Scenario Analysis

```python
# After running multiple scenarios
from utils import quick_compare_scenarios

comparison_files = quick_compare_scenarios(
    scenario_results=results_collection,
    output_dir="scenario_analysis"
)
```

## Best Practices

1. **Organize Outputs**: Use timestamped directories for different runs
2. **Save Data**: Always save raw data alongside charts
3. **Documentation**: Include README files with run information
4. **Version Control**: Keep charts out of version control (add to .gitignore)
5. **Naming**: Use descriptive names for chart files
6. **Quality**: Use appropriate DPI and formats for your needs

## Advanced Features

### Custom Chart Types

Create your own visualization functions:

```python
def create_custom_chart(data, **kwargs):
    """Create a custom visualization."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Your custom plotting code here
    
    if kwargs.get('save_path'):
        plt.savefig(kwargs['save_path'], dpi=300, bbox_inches='tight')
    
    return fig
```

### Automated Reporting

Generate comprehensive reports:

```python
from utils import quick_summary_report

summary_file = quick_summary_report(
    model_data=results,
    hotspot_stats=hotspot_stats,
    persona_stats=persona_stats,
    output_file="comprehensive_report.txt"
)
```

This guide covers the main visualization capabilities. For more advanced features, explore the example files and source code in the `utils/visualization.py` module.
