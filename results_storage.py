"""
Results Storage Utilities
========================

This module provides functions for storing simulation results in timestamped files
within an organized outputs directory structure.
"""

import os
import json
import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import pickle


class ResultsStorage:
    """
    Manages storage of simulation results in timestamped files.
    
    Creates organized output directories and stores results with timestamps
    for easy tracking and comparison of different simulation runs.
    """
    
    def __init__(self, base_output_dir: str = "outputs"):
        """
        Initialize the results storage system.
        
        Args:
            base_output_dir: Base directory for storing outputs
        """
        self.base_output_dir = Path(base_output_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.base_output_dir / self.timestamp
        
        # Create output directory structure
        self._create_directory_structure()
    
    def _create_directory_structure(self):
        """Create the output directory structure."""
        # Create main output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different types of outputs
        (self.output_dir / "data").mkdir(exist_ok=True)
        (self.output_dir / "charts").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)
        (self.output_dir / "configs").mkdir(exist_ok=True)
    
    def save_simulation_results(self, 
                              model_data: pd.DataFrame,
                              agent_data: Optional[pd.DataFrame] = None,
                              hotspot_stats: Optional[List[Dict]] = None,
                              persona_stats: Optional[Dict] = None,
                              simulation_config: Optional[Dict] = None) -> Dict[str, str]:
        """
        Save comprehensive simulation results to timestamped files.
        
        Args:
            model_data: Time series data from the model
            agent_data: Agent-level data (optional)
            hotspot_stats: Hotspot statistics (optional)
            persona_stats: Persona statistics (optional)
            simulation_config: Simulation configuration (optional)
            
        Returns:
            Dictionary with paths to saved files
        """
        saved_files = {}
        
        # Save model time series data
        if not model_data.empty:
            model_data_path = self.output_dir / "data" / "model_data.csv"
            model_data.to_csv(model_data_path, index=False)
            saved_files["model_data"] = str(model_data_path)
        
        # Save agent data
        if agent_data is not None and not agent_data.empty:
            agent_data_path = self.output_dir / "data" / "agent_data.csv"
            agent_data.to_csv(agent_data_path, index=False)
            saved_files["agent_data"] = str(agent_data_path)
        
        # Save hotspot statistics
        if hotspot_stats:
            hotspot_stats_path = self.output_dir / "data" / "hotspot_stats.json"
            with open(hotspot_stats_path, 'w', encoding='utf-8') as f:
                json.dump(hotspot_stats, f, indent=2, ensure_ascii=False)
            saved_files["hotspot_stats"] = str(hotspot_stats_path)
        
        # Save persona statistics
        if persona_stats:
            persona_stats_path = self.output_dir / "data" / "persona_stats.json"
            with open(persona_stats_path, 'w', encoding='utf-8') as f:
                json.dump(persona_stats, f, indent=2, ensure_ascii=False)
            saved_files["persona_stats"] = str(persona_stats_path)
        
        # Save simulation configuration
        if simulation_config:
            config_path = self.output_dir / "configs" / "simulation_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(simulation_config, f, indent=2, ensure_ascii=False)
            saved_files["simulation_config"] = str(config_path)
        
        # Create summary metadata
        metadata = {
            "timestamp": self.timestamp,
            "simulation_date": datetime.now().isoformat(),
            "files_saved": saved_files,
            "model_steps": len(model_data) if not model_data.empty else 0,
            "total_agents": len(agent_data) if agent_data is not None else 0,
            "hotspots_count": len(hotspot_stats) if hotspot_stats else 0,
            "personas_count": len(persona_stats) if persona_stats else 0
        }
        
        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        saved_files["metadata"] = str(metadata_path)
        
        return saved_files
    
    def save_scenario_comparison(self, 
                               baseline_results: Dict[str, Any],
                               scenario_results: List[Dict[str, Any]],
                               comparison_analysis: Dict[str, Any]) -> Dict[str, str]:
        """
        Save scenario comparison results.
        
        Args:
            baseline_results: Baseline simulation results
            scenario_results: List of scenario simulation results
            comparison_analysis: Analysis comparing scenarios
            
        Returns:
            Dictionary with paths to saved files
        """
        saved_files = {}
        
        # Save baseline results
        baseline_path = self.output_dir / "data" / "baseline_results.json"
        with open(baseline_path, 'w', encoding='utf-8') as f:
            json.dump(baseline_results, f, indent=2, ensure_ascii=False)
        saved_files["baseline_results"] = str(baseline_path)
        
        # Save scenario results
        scenarios_path = self.output_dir / "data" / "scenario_results.json"
        with open(scenarios_path, 'w', encoding='utf-8') as f:
            json.dump(scenario_results, f, indent=2, ensure_ascii=False)
        saved_files["scenario_results"] = str(scenarios_path)
        
        # Save comparison analysis
        comparison_path = self.output_dir / "reports" / "scenario_comparison.json"
        with open(comparison_path, 'w', encoding='utf-8') as f:
            json.dump(comparison_analysis, f, indent=2, ensure_ascii=False)
        saved_files["comparison_analysis"] = str(comparison_path)
        
        # Create comparison summary
        summary = {
            "timestamp": self.timestamp,
            "baseline_metrics": baseline_results.get("final_metrics", {}),
            "scenario_count": len(scenario_results),
            "scenario_names": [s.get("scenario_name", "Unknown") for s in scenario_results],
            "best_scenario": comparison_analysis.get("best_scenario", "Unknown"),
            "worst_scenario": comparison_analysis.get("worst_scenario", "Unknown")
        }
        
        summary_path = self.output_dir / "reports" / "comparison_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        saved_files["comparison_summary"] = str(summary_path)
        
        return saved_files
    
    def save_charts(self, charts_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Save generated charts and visualizations.
        
        Args:
            charts_data: Dictionary containing chart objects and metadata
            
        Returns:
            Dictionary with paths to saved chart files
        """
        saved_files = {}
        charts_dir = self.output_dir / "charts"
        
        for chart_name, chart_info in charts_data.items():
            if hasattr(chart_info, 'savefig'):
                # Matplotlib figure
                chart_path = charts_dir / f"{chart_name}.png"
                chart_info.savefig(chart_path, dpi=300, bbox_inches='tight')
                saved_files[chart_name] = str(chart_path)
            elif isinstance(chart_info, dict):
                # Chart metadata or data
                chart_path = charts_dir / f"{chart_name}.json"
                with open(chart_path, 'w', encoding='utf-8') as f:
                    json.dump(chart_info, f, indent=2, ensure_ascii=False)
                saved_files[chart_name] = str(chart_path)
        
        return saved_files
    
    def save_model_state(self, model, filename: str = "model_state.pkl") -> str:
        """
        Save the complete model state for later analysis.
        
        Args:
            model: The simulation model instance
            filename: Name of the pickle file
            
        Returns:
            Path to the saved model state file
        """
        model_path = self.output_dir / "data" / filename
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        return str(model_path)
    
    def get_output_directory(self) -> str:
        """Get the current output directory path."""
        return str(self.output_dir)
    
    def get_timestamp(self) -> str:
        """Get the current timestamp string."""
        return self.timestamp
    
    def create_readme(self, simulation_info: Dict[str, Any]) -> str:
        """
        Create a README file for the output directory.
        
        Args:
            simulation_info: Information about the simulation run
            
        Returns:
            Path to the created README file
        """
        readme_content = f"""# Simulation Results - {self.timestamp}

## Simulation Information
- **Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Duration**: {simulation_info.get('duration', 'Unknown')}
- **Steps**: {simulation_info.get('steps', 'Unknown')}
- **Tourists**: {simulation_info.get('num_tourists', 'Unknown')}
- **Hotspots**: {simulation_info.get('num_hotspots', 'Unknown')}

## Directory Structure
```
{self.timestamp}/
├── data/           # Raw simulation data (CSV, JSON)
├── charts/         # Generated visualizations (PNG, JSON)
├── reports/        # Analysis reports and summaries
└── configs/        # Simulation configurations
```

## Files Description
- `model_data.csv`: Time series data from the simulation
- `agent_data.csv`: Agent-level statistics
- `hotspot_stats.json`: Hotspot performance metrics
- `persona_stats.json`: Tourist persona statistics
- `metadata.json`: Simulation metadata and file index

## Usage
To load and analyze these results:
```python
import pandas as pd
import json

# Load model data
model_data = pd.read_csv('data/model_data.csv')

# Load statistics
with open('data/hotspot_stats.json', 'r') as f:
    hotspot_stats = json.load(f)
```

Generated on: {datetime.now().isoformat()}
"""
        
        readme_path = self.output_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return str(readme_path)


def get_latest_output_dir(base_output_dir: str = "outputs") -> Optional[str]:
    """
    Get the path to the most recent output directory.
    
    Args:
        base_output_dir: Base directory for outputs
        
    Returns:
        Path to the latest output directory, or None if no outputs exist
    """
    base_path = Path(base_output_dir)
    if not base_path.exists():
        return None
    
    # Find all timestamped directories
    output_dirs = [d for d in base_path.iterdir() 
                  if d.is_dir() and d.name.replace('_', '').replace('-', '').isdigit()]
    
    if not output_dirs:
        return None
    
    # Return the most recent one
    latest_dir = max(output_dirs, key=lambda x: x.name)
    return str(latest_dir)


def list_output_directories(base_output_dir: str = "outputs") -> List[Dict[str, str]]:
    """
    List all output directories with their timestamps and metadata.
    
    Args:
        base_output_dir: Base directory for outputs
        
    Returns:
        List of dictionaries with directory information
    """
    base_path = Path(base_output_dir)
    if not base_path.exists():
        return []
    
    output_dirs = []
    for d in base_path.iterdir():
        if d.is_dir() and d.name.replace('_', '').replace('-', '').isdigit():
            metadata_path = d / "metadata.json"
            metadata = {}
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                except:
                    pass
            
            output_dirs.append({
                "directory": str(d),
                "timestamp": d.name,
                "simulation_date": metadata.get("simulation_date", "Unknown"),
                "model_steps": metadata.get("model_steps", 0),
                "total_agents": metadata.get("total_agents", 0)
            })
    
    # Sort by timestamp (newest first)
    output_dirs.sort(key=lambda x: x["timestamp"], reverse=True)
    return output_dirs
