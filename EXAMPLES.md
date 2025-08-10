# Examples Guide

This guide provides detailed descriptions of all examples in the Mesa Tourism Simulation project, including their purpose, features, usage instructions, and expected outputs.

## Overview

The examples demonstrate various aspects of the tourism simulation system, from basic usage to advanced analysis and visualization capabilities. Each example is designed to showcase specific features and use cases.

## Basic Examples

### 1. Basic Simulation (`basic_simulation.py`)

**Purpose**: Demonstrates the fundamental simulation capabilities with basic data collection and results storage.

**Features**:
- Simple tourism model creation
- Basic simulation execution
- Results collection and storage
- Tourist persona analysis
- Hotspot performance metrics

**Usage**:
```bash
python examples/basic_simulation.py
```

**Output**:
- Timestamped output directory with simulation results
- README file with summary
- Data files (CSV, JSON)
- Console output with key metrics

**Key Metrics Displayed**:
- Final Average Popularity
- Total Visitors
- Social Shares
- Average Satisfaction
- Hotspot performance rankings
- Persona analysis

**Example Output**:
```
📊 SIMULATION RESULTS:
------------------------------
Final Average Popularity: 0.701
Total Visitors: 174
Social Shares: 58
Average Satisfaction: 0.650

🏛️ HOTSPOT PERFORMANCE:
------------------------------
1. Historic Old Town
   Popularity: 0.967
   Visitors: 44
   Category: cultural
```

---

### 2. Basic Simulation with Visualization (`basic_simulation_with_visualization.py`)

**Purpose**: Extends the basic simulation with comprehensive visualization capabilities.

**Features**:
- All basic simulation features
- Automatic chart generation
- Multiple visualization types
- Quick visualization utilities demonstration

**Usage**:
```bash
python examples/basic_simulation_with_visualization.py
```

**Output**:
- All basic simulation outputs
- Visualization charts (PNG files)
- Interactive visualization examples
- Summary reports

**Generated Charts**:
- `popularity_evolution.png` - Hotspot popularity over time
- `satisfaction_by_persona.png` - Tourist satisfaction by persona
- `simulation_dashboard.png` - Comprehensive time series dashboard
- Additional auto-generated charts

**Example Output**:
```
📊 GENERATED CHARTS:
--------------------
• popularity_evolution.png - Hotspot popularity over time
• satisfaction_by_persona.png - Tourist satisfaction by persona
• simulation_dashboard.png - Comprehensive time series dashboard
• Additional auto-generated charts
```

---

### 3. Large Simulation (`large_simulation.py`)

**Purpose**: Demonstrates the system's capability to handle large-scale simulations with thousands of tourists.

**Features**:
- Large-scale simulation (5000 tourists)
- Performance testing
- Scalability demonstration
- Memory management

**Usage**:
```bash
python examples/large_simulation.py
```

**Output**:
- Large-scale simulation results
- Performance metrics
- Memory usage information
- Timestamped output directory

**Key Differences**:
- 5000 tourists instead of 30
- Higher visitor counts
- Different satisfaction patterns
- Performance considerations

**Example Output**:
```
📊 SIMULATION RESULTS:
------------------------------
Final Average Popularity: 0.551
Total Visitors: 28022
Social Shares: 9522
Average Satisfaction: 0.346
```

---

## Analysis Examples

### 4. Custom Analysis (`custom_analysis.py`)

**Purpose**: Demonstrates advanced analysis capabilities with custom scenario creation and comprehensive comparison.

**Features**:
- Custom scenario creation
- Multiple scenario comparison
- Advanced metrics analysis
- Policy recommendations
- Evidence-based insights

**Usage**:
```bash
python examples/custom_analysis.py
```

**Output**:
- Multiple scenario comparisons
- Performance analysis tables
- Policy recommendations
- CSV data exports
- Text analysis reports

**Scenarios Tested**:
- Summer Music Festival (event-driven)
- Luxury Tourism Tax (policy-based)
- Downtown Construction (infrastructure)
- Street Art Festival (custom cultural event)

**Example Output**:
```
📊 COMPREHENSIVE ANALYSIS
========================================

1. PERFORMANCE METRICS COMPARISON:
             Scenario Popularity  Visitors  Shares Satisfaction
             Baseline      0.728       292     104        0.630
Summer Music Festival      0.810       292     104        0.832
   Luxury Tourism Tax      0.740       292     104        0.666
```

---

### 5. Scenario Comparison (`scenario_comparison.py`)

**Purpose**: Original scenario comparison example demonstrating baseline vs. multiple scenarios.

**Features**:
- Baseline vs. scenario comparison
- Impact analysis
- Performance rankings
- Policy recommendations

**Usage**:
```bash
python examples/scenario_comparison.py
```

**Output**:
- Scenario comparison tables
- Impact vs. baseline analysis
- Performance rankings
- Policy recommendations
- Timestamped results

**Scenarios Compared**:
- Baseline (no intervention)
- Summer Music Festival
- Luxury Tourism Tax
- Downtown Construction

**Example Output**:
```
📈 IMPACT vs BASELINE:
----------------------------------------

Summer Music Festival:
  Average Popularity: +0.054 (+7.3%)
  Total Visitors: +0.000 (+0.0%)
  Social Shares: +0.000 (+0.0%)
  Average Satisfaction: +0.220 (+34.8%)
```

---

## Visualization Examples

### 6. Visualization Demo (`visualization_demo.py`)

**Purpose**: Comprehensive demonstration of static visualization capabilities.

**Features**:
- Multiple chart types
- Scenario comparison visualizations
- Time series dashboards
- Hotspot impact analysis
- Automatic chart generation

**Usage**:
```bash
python examples/visualization_demo.py
```

**Output**:
- Multiple PNG chart files
- Scenario comparison charts
- Time series dashboards
- Impact heatmaps
- CSV data exports

**Generated Charts**:
1. `popularity_evolution.png` - Hotspot popularity over time
2. `satisfaction_by_persona.png` - Tourist satisfaction by persona
3. `scenario_comparison.png` - Performance comparison across scenarios
4. `simulation_dashboard.png` - Comprehensive time series dashboard
5. `hotspot_map.png` - Geographic hotspot visualization
6. `hotspot_impact_heatmap.png` - Scenario impact on hotspots

**Example Output**:
```
📊 CHART SUMMARY:
--------------------
1. popularity_evolution.png - Hotspot popularity over time
2. satisfaction_by_persona.png - Tourist satisfaction by persona
3. scenario_comparison.png - Performance comparison across scenarios
4. simulation_dashboard.png - Comprehensive time series dashboard
5. hotspot_map.png - Geographic hotspot visualization
6. hotspot_impact_heatmap.png - Scenario impact on hotspots
```

---

### 7. Interactive Visualization (`interactive_visualization.py`)

**Purpose**: Demonstrates interactive visualization capabilities using Plotly.

**Features**:
- Interactive HTML charts
- Hover tooltips
- Zoom and pan capabilities
- Legend interaction
- Download capabilities
- Responsive design

**Usage**:
```bash
python examples/interactive_visualization.py
```

**Output**:
- Interactive HTML files
- Plotly-based visualizations
- Advanced interactive features
- Responsive charts

**Generated Interactive Charts**:
1. `interactive_popularity.html` - Interactive popularity evolution
2. `interactive_hotspot_map.html` - Interactive geographic hotspot map
3. `interactive_dashboard.html` - Interactive multi-metric dashboard
4. `interactive_scenario_comparison.html` - Interactive scenario comparison
5. `interactive_impact_heatmap.html` - Interactive impact visualization

**Interactive Features**:
- Hover tooltips with detailed information
- Zoom and pan capabilities
- Click to select and highlight data points
- Legend interaction (click to show/hide traces)
- Download as PNG/SVG/PDF
- Responsive design for different screen sizes

**Example Output**:
```
🎯 INTERACTIVE FEATURES:
-------------------------
• Hover tooltips with detailed information
• Zoom and pan capabilities
• Click to select and highlight data points
• Legend interaction (click to show/hide traces)
• Download as PNG/SVG/PDF
• Responsive design for different screen sizes
```

---

## Advanced Scenario Comparison Examples

### 8. Test Scenario Comparison (`test_scenario_comparison.py`)

**Purpose**: Simple test with dramatic effects to verify scenario comparison functionality.

**Features**:
- Dramatic scenario effects
- Clear performance differences
- Simple comparison setup
- Validation testing

**Usage**:
```bash
python examples/test_scenario_comparison.py
```

**Output**:
- Test scenario comparison
- Dramatic effect demonstration
- Validation results
- Timestamped output directory

**Scenarios Tested**:
- Baseline
- High Impact Marketing (dramatic positive effect)
- Construction Disruption (dramatic negative effect)

**Example Output**:
```
🔍 DIFFERENCE ANALYSIS:
------------------------------
High Impact vs Baseline:
   Popularity change: +0.124 (+16.7%)
   Satisfaction change: +0.355 (+56.1%)
Negative Impact vs Baseline:
   Popularity change: -0.201 (-27.1%)
   Satisfaction change: -0.412 (-65.2%)

✅ SUCCESS: High impact scenario shows significant differences!
✅ SUCCESS: Negative impact scenario shows significant differences!
```

---

### 9. Easy Scenario Comparison (`easy_scenario_comparison.py`)

**Purpose**: Demonstrates multiple methods for creating and comparing scenarios using the scenario builder utility.

**Features**:
- Three different comparison methods
- Pre-built comparison sets
- Custom scenario configurations
- Extreme comparison sets
- Scenario builder demonstration

**Usage**:
```bash
python examples/easy_scenario_comparison.py
```

**Output**:
- Multiple comparison sets
- Different scenario configurations
- Custom scenario examples
- Comprehensive results

**Methods Demonstrated**:

#### Method 1: Pre-built Comparison Sets
- Quick comparison set (6 scenarios)
- Standard scenario types
- Easy-to-use templates

#### Method 2: Custom Configurations
- Different intensity levels
- Custom scenario parameters
- Flexible configuration options

#### Method 3: Extreme Comparison Sets
- Dramatic effect scenarios
- Maximum impact demonstrations
- Clear performance differences

**Example Output**:
```
📊 COMPARISON RESULTS SUMMARY:
========================================
Quick Comparison Set:
   🏆 Best: Marketing Campaign (Satisfaction: 0.863, ++36.4%)
   ⚠️  Worst: Construction Disruption (Satisfaction: 0.297, -53.0%)

Custom Comparison Set:
   🏆 Best: Aggressive Marketing (Satisfaction: 1.000, ++58.1%)
   ⚠️  Worst: Severe Construction (Satisfaction: 0.000, -100.0%)
```

---

### 10. Comprehensive Scenario Comparison (`comprehensive_scenario_comparison.py`)

**Purpose**: Full-featured scenario comparison with comprehensive analysis and individual scenario visualizations.

**Features**:
- 6 distinctive scenarios
- Individual scenario visualizations
- Comprehensive analysis reports
- Detailed comparison metrics
- Policy insights

**Usage**:
```bash
python examples/comprehensive_scenario_comparison.py
```

**Output**:
- Comprehensive scenario comparison
- Individual scenario visualizations
- Detailed analysis reports
- Policy recommendations
- Timestamped output directory

**Scenarios Analyzed**:
1. **Baseline** - Standard tourism conditions
2. **Aggressive Marketing** - Massive marketing campaign
3. **Major Festival** - Cultural festival with extensive programming
4. **Construction Disruption** - Major construction project
5. **Luxury Tax** - 15% luxury tax on high-end services
6. **Sustainable Tourism** - Eco-friendly tourism initiative

**Output Structure**:
```
outputs/20250811_000334/
├── charts/                                 # Standard output structure
├── data/                                   # Standard output structure
├── reports/                                # Standard output structure
├── configs/                                # Standard output structure
└── scenario_comparison/                    # Scenario comparison results
    ├── scenario_comparison.png             # Main comparison chart
    ├── scenario_comparison.csv             # Comparison data table
    ├── detailed_comparison.csv             # Detailed metrics
    ├── scenario_analysis_report.txt        # Analysis report
    └── individual_scenarios/               # Individual scenario results
        ├── baseline/
        ├── aggressive_marketing/
        ├── major_festival/
        ├── construction_disruption/
        ├── luxury_tax/
        └── sustainable_tourism/
```

**Example Output**:
```
🎯 SCENARIO INSIGHTS:
------------------------------
🏆 Best Performer: Aggressive Marketing
   Satisfaction: 0.968
   Popularity: 0.799
⚠️  Worst Performer: Construction Disruption
   Satisfaction: 0.000
   Popularity: 0.341
```

---

## Usage Patterns

### Quick Start
For new users, start with:
1. `basic_simulation.py` - Understand the basics
2. `basic_simulation_with_visualization.py` - Add visualization
3. `test_scenario_comparison.py` - Try scenario comparison

### Analysis Workflow
For analysis tasks:
1. `custom_analysis.py` - Advanced analysis
2. `comprehensive_scenario_comparison.py` - Full comparison
3. `visualization_demo.py` - Static visualizations
4. `interactive_visualization.py` - Interactive charts

### Development and Testing
For development:
1. `easy_scenario_comparison.py` - Test different methods
2. `large_simulation.py` - Test scalability
3. `scenario_comparison.py` - Original comparison method

## Output Organization

All examples follow a consistent output organization:

```
outputs/YYYYMMDD_HHMMSS/           # Timestamped directory
├── charts/                        # Generated charts (PNG/HTML)
├── data/                          # Simulation data (CSV/JSON)
├── reports/                       # Analysis reports (TXT/JSON)
├── configs/                       # Configuration files (JSON)
└── README.md                      # Summary report
```

## Key Features Demonstrated

### Simulation Capabilities
- Basic tourism simulation
- Large-scale simulation
- Scenario-aware simulation
- Multi-agent interactions

### Analysis Capabilities
- Performance metrics calculation
- Scenario comparison
- Impact analysis
- Policy recommendations

### Visualization Capabilities
- Static charts (Matplotlib/Seaborn)
- Interactive charts (Plotly)
- Dashboards
- Comparison visualizations

### Data Management
- Results storage
- Timestamped outputs
- Data export (CSV/JSON)
- Configuration management

## Troubleshooting

### Common Issues
1. **Missing Dependencies**: Ensure all requirements are installed
2. **Memory Issues**: Use smaller simulations for limited resources
3. **Display Issues**: Use non-interactive backends for headless environments

### Performance Tips
1. Start with basic examples before moving to complex ones
2. Use appropriate simulation sizes for your hardware
3. Close figures to free memory in long-running scripts

## Next Steps

After running the examples:
1. Explore the generated outputs
2. Modify scenarios for your use case
3. Create custom visualizations
4. Integrate with your own analysis workflows

For more information, see the main README.md and the documentation in the `docs/` directory.
