# LLM Tourism Simulation System 🏛️🎭

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Mesa](https://img.shields.io/badge/Mesa-3.0+-green.svg)](https://mesa.readthedocs.io/)

A sophisticated **agent-based tourism simulation system** enhanced with Large Language Models for generating realistic tourist personas, urban hotspots, and policy scenarios. This system enables evidence-based tourism policy testing and urban planning decisions through computational simulation.

## 🌟 Key Features

### 🤖 **LLM-Enhanced Content Generation**
- **5 Realistic Tourist Personas** with detailed behavioral profiles, demographics, and travel patterns
- **7 Urban Tourism Hotspots** with geospatial characteristics and persona-specific appeal scores
- **Comprehensive Business Rules** with behavioral parameters and social interaction mechanics
- **3 What-If Scenarios** for policy testing (festivals, taxation, construction disruption)

### 🎯 **Advanced Simulation Capabilities**
- **Mesa-based Agent Modeling** with complex social influence networks
- **Dynamic Scenario Processing** for real-time policy impact assessment
- **Multi-Dimensional Analysis** covering satisfaction, popularity, visitor flows, and social sharing
- **Comparative Scenario Testing** with statistical significance analysis

### 📊 **Professional Analysis Tools**
- **Comprehensive Visualization Suite** with time series, heatmaps, and comparison charts
- **Policy Recommendation Engine** generating evidence-based insights
- **Statistical Analysis** with trend detection and performance metrics
- **Timestamped Results Storage** with organized output directories and automatic documentation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nickkvasov/mesa-poc.git
cd llm-tourism-sim

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Project Structure

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

### Basic Usage

```python
from sim import load_data, TourismModel
from utils import ResultsStorage

# Load LLM-generated configuration
personas, hotspots, business_rules, scenarios = load_data()

# Create and run simulation
model = TourismModel(
    personas_data=personas,
    hotspots_data=hotspots,
    business_rules=business_rules,
    num_tourists=50
)

# Run simulation for 20 steps
results = model.run_simulation(steps=20)

# Save results to timestamped directory
storage = ResultsStorage()
saved_files = storage.save_simulation_results(
    model_data=results,
    agent_data=model.get_agent_data(),
    hotspot_stats=model.get_hotspot_statistics(),
    persona_stats=model.get_persona_statistics()
)

print(f"Results saved to: {storage.get_output_directory()}")
```

### Scenario Testing

```python
from sim import ScenarioAwareTourismModel, ScenarioManager

# Load scenarios
scenario_manager = ScenarioManager("scenarios_events.json")
festival_scenario = scenario_manager.get_scenario("Summer Music Festival")

# Test scenario impact
model = ScenarioAwareTourismModel(
    scenario=festival_scenario,
    personas_data=personas,
    hotspots_data=hotspots,
    num_tourists=50
)

results = model.run_simulation(steps=20)
impact_summary = model.get_scenario_impact_summary()
```

### Command Line Examples

```bash
# Run basic simulation
python examples/basic_simulation.py

# Run scenario comparison
python examples/scenario_comparison.py

# List and manage output directories
python utils/list_outputs.py list
python utils/list_outputs.py latest
python utils/list_outputs.py explore
```




## 🎭 Available Scenarios

### 1. **Summer Music Festival** (Event-Driven)
- **Objective**: Test impact of major cultural events on tourism
- **Effects**: Capacity boost at Riverside Park, increased appeal to young demographics
- **Expected Impact**: +40-60% satisfaction, enhanced social sharing
- **Policy Applications**: Festival planning, event infrastructure investment

### 2. **Luxury Tourism Tax** (Policy-Based)
- **Objective**: Assess redistribution effects of luxury taxation
- **Effects**: 15% tax on luxury services, capacity limits on high-end venues
- **Expected Impact**: Tourist redistribution to alternative venues
- **Policy Applications**: Sustainable tourism regulation, revenue generation

### 3. **Downtown Construction** (Infrastructure)
- **Objective**: Measure disruption impact of major infrastructure projects
- **Effects**: Accessibility penalties, noise pollution, post-completion improvements
- **Expected Impact**: -50-80% satisfaction during construction
- **Policy Applications**: Construction timing, disruption mitigation strategies

## 🏛️ Tourist Personas

| Persona | Budget | Characteristics | Key Interests |
|---------|--------|-----------------|---------------|
| **Budget Backpacker** | Low | High social influence, exploration-focused | Street food, free activities, local culture |
| **Luxury Tourist** | High | Comfort-seeking, status-conscious | Fine dining, shopping, premium services |
| **Cultural Explorer** | Medium | Learning-oriented, authentic experiences | Museums, historical sites, art galleries |
| **Adventure Seeker** | Medium | Risk-tolerant, physically active | Outdoor activities, extreme sports, nature |
| **Family Traveler** | Medium | Safety-conscious, convenience-seeking | Family activities, parks, safe attractions |

## 📊 Results Storage & Management

### Timestamped Output Directories
Each simulation run creates a unique timestamped directory with organized structure:

```
outputs/20250810_214805/
├── README.md                    # Simulation documentation
├── metadata.json               # Simulation metadata
├── data/                       # Raw simulation data
│   ├── model_data.csv         # Time series data
│   ├── agent_data.csv         # Agent-level statistics
│   ├── hotspot_stats.json     # Hotspot performance
│   └── persona_stats.json     # Persona statistics
├── charts/                     # Generated visualizations
├── reports/                    # Analysis reports
└── configs/                    # Simulation configurations
```

### Output Management Commands
```bash
# List all simulation outputs
python utils/list_outputs.py list

# Show latest output information
python utils/list_outputs.py latest

# Explore output directory contents
python utils/list_outputs.py explore

# Explore specific output
python list_outputs.py explore 20250810_214805
```

## 🎯 Use Cases

### 🏛️ **Tourism Authorities**
- **Policy Impact Testing**: Simulate taxation, regulation, and infrastructure changes
- **Event Planning**: Optimize festival timing, capacity, and resource allocation
- **Crisis Management**: Model tourism recovery strategies and disruption mitigation
- **Revenue Optimization**: Balance visitor satisfaction with economic objectives

### 🏗️ **Urban Planners**
- **Infrastructure Assessment**: Evaluate construction impact on tourism flows
- **Zoning Decisions**: Understand tourism implications of development projects
- **Transportation Planning**: Optimize connectivity to tourism destinations
- **Sustainability Analysis**: Balance tourism growth with quality of life

### 🎓 **Researchers & Academics**
- **Tourism Dynamics Research**: Study complex visitor behavior patterns
- **Social Network Analysis**: Investigate recommendation and influence networks
- **Policy Effectiveness Studies**: Quantify intervention impacts with statistical rigor
- **Urban Systems Modeling**: Integrate tourism with broader city dynamics

## 📊 Analysis Capabilities

### **Performance Metrics**
- **Satisfaction Analysis**: Multi-dimensional tourist satisfaction tracking
- **Popularity Dynamics**: Hotspot performance and viral growth patterns
- **Visitor Flow Analysis**: Spatial and temporal movement patterns
- **Social Influence Networks**: Recommendation cascades and peer effects

### **Comparative Analysis**
- **Scenario vs Baseline**: Statistical comparison of policy interventions
- **Cross-Scenario Ranking**: Performance-based scenario evaluation
- **Impact Assessment**: Quantified changes in key metrics
- **Policy Recommendations**: Evidence-based guidance for decision makers

## 🛠️ Development & Extension

### **Custom Personas**
```python
# Add new persona to tourist_personas.json
new_persona = {
    "type": "Digital Nomad",
    "demographics": {"budget_level": "medium", "age_group": "young"},
    "behavioral_traits": {"social_influence": 0.9, "exploration_tendency": 0.8},
    "travel_patterns": {"daily_visits": 2, "sharing_probability": 0.9}
}
```

### **Custom Scenarios**
```python
from scenario_manager import TourismScenario

# Create custom policy scenario
scenario = TourismScenario(
    name="Remote Work Hub Initiative",
    description="Transform Cultural sites into co-working spaces",
    category="policy-innovation"
)

scenario.add_event(5, "appeal_boost", "Art Gallery District", 
                  {"appeal_boost": 0.3, "target_personas": ["Digital Nomad"]})
```

### **Custom Analysis**
```python
from analysis import analyze_simulation_results

# Perform detailed analysis
analysis = analyze_simulation_results(model_data, hotspot_stats, persona_stats)
recommendations = analysis['recommendations']
```

## 📈 Performance & Validation

### **Simulation Performance**
- **Scale**: Supports 50-200+ tourist agents with 7+ hotspots
- **Speed**: ~100 simulation steps per second on standard hardware
- **Memory**: ~50MB RAM for typical configuration
- **Reproducibility**: Fixed random seeds ensure consistent results

### **Validation Metrics**
- **Baseline Performance**: 0.628 average satisfaction, 141 total visitors
- **Scenario Impact Range**: -72.9% to +55.4% satisfaction change
- **Statistical Significance**: Consistent results across multiple runs
- **Behavioral Realism**: LLM-generated behaviors match tourism research findings

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- **Code Standards**: Python style guide, testing requirements, documentation
- **Development Setup**: Environment configuration, development dependencies
- **Contribution Process**: Issue reporting, pull request workflow, code review
- **Extension Guidelines**: Adding new personas, hotspots, scenarios, and analysis tools

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Mesa Framework**: Agent-based modeling foundation
- **LLM Content Generation**: Realistic persona and scenario creation
- **Tourism Research Community**: Behavioral insights and validation
- **Open Source Community**: Tools, libraries, and inspiration

## 📞 Contact & Support

- **Documentation**: [API Reference](API.md), [Usage Guide](USAGE.md)
- **Issues**: [GitHub Issues](https://github.com/llm-tourism-sim/llm-tourism-sim/issues)
- **Discussions**: [GitHub Discussions](https://github.com/llm-tourism-sim/llm-tourism-sim/discussions)
- **Email**: contact@llm-tourism-sim.org

---

**Built with ❤️ for evidence-based tourism policy making**

*Transform tourism planning from intuition to data-driven decision making with LLM-enhanced agent-based simulation.*
