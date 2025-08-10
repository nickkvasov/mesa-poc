"""
Tourism Model Classes
====================

This module defines the main simulation model classes that orchestrate
the tourism simulation, manage agent interactions, and handle data collection.
"""

import random
import numpy as np
import pandas as pd
from mesa import Model
from mesa.space import MultiGrid
from mesa.model import AgentSet
from mesa.datacollection import DataCollector
from typing import Dict, List, Optional, Any, Tuple

from ..agents.tourist import Tourist, ScenarioAwareTourist
from ..agents.hotspot import Hotspot, ScenarioAwareHotspot
from .scenario_manager import TourismScenario


class TourismModel(Model):
    """
    Base tourism simulation model with LLM-generated agents.

    This model creates and manages tourist and hotspot agents based on
    LLM-generated personas and characteristics, simulating tourism dynamics
    through agent interactions and social influence networks.
    """

    def __init__(self, 
                 personas_data: List[Dict] = None,
                 hotspots_data: List[Dict] = None, 
                 business_rules: Dict = None,
                 num_tourists: int = 50,
                 grid_width: int = 20,
                 grid_height: int = 20,
                 random_seed: int = None):
        """
        Initialize the tourism simulation model.

        Args:
            personas_data: List of LLM-generated persona dictionaries
            hotspots_data: List of LLM-generated hotspot dictionaries
            business_rules: LLM-generated business rules dictionary
            num_tourists: Number of tourist agents to create
            grid_width: Width of the spatial grid
            grid_height: Height of the spatial grid
            random_seed: Random seed for reproducibility
        """
        super().__init__()

        # Set random seed if provided
        if random_seed is not None:
            random.seed(random_seed)
            np.random.seed(random_seed)

        # Store configuration
        self.personas_data = personas_data or []
        self.hotspots_data = hotspots_data or []
        self.business_rules = business_rules or {}
        self.num_tourists = num_tourists

        # Initialize model components
        self.grid = MultiGrid(grid_width, grid_height, torus=False)
        self.running = True
        self.current_step = 0

        # Agent collections
        self.tourists = []
        self.hotspots = []
        self.agent_set = AgentSet([], random=self.random)

        # Data collection
        self._setup_data_collection()

        # Create agents
        self._create_hotspots()
        self._create_tourists()

    def _setup_data_collection(self):
        """Set up comprehensive data collection for analysis."""
        model_reporters = {
            "Average_Popularity": lambda m: np.mean([h.current_popularity for h in m.hotspots]) if m.hotspots else 0,
            "Total_Visitors": lambda m: sum([h.total_visitors + h.visitors_today for h in m.hotspots]),
            "Social_Shares": lambda m: sum([h.social_shares for h in m.hotspots]),
            "Average_Satisfaction": lambda m: np.mean([t.satisfaction for t in m.tourists]) if m.tourists else 0,
            "Active_Tourists": lambda m: len([t for t in m.tourists if t.visits_today < t.daily_visits]),
            "Hotspot_Visits_Today": lambda m: sum([h.visitors_today for h in m.hotspots])
        }

        agent_reporters = {
            "Agent_Type": lambda a: type(a).__name__,
            "Popularity": lambda a: getattr(a, 'current_popularity', None),
            "Visitors_Today": lambda a: getattr(a, 'visitors_today', None),
            "Satisfaction": lambda a: getattr(a, 'satisfaction', None),
            "Persona_Type": lambda a: getattr(a, 'persona_type', None),
            "Visits_Today": lambda a: getattr(a, 'visits_today', None)
        }

        self.datacollector = DataCollector(
            model_reporters=model_reporters,
            agent_reporters=agent_reporters
        )

    def _create_hotspots(self):
        """Create hotspot agents from LLM-generated data."""
        for hotspot_data in self.hotspots_data:
            hotspot = Hotspot(self, hotspot_data)
            self.hotspots.append(hotspot)
            self.agent_set.add(hotspot)

            # Place hotspot on grid
            location = hotspot_data.get("location", {})
            x = location.get("x", random.randrange(self.grid.width))
            y = location.get("y", random.randrange(self.grid.height))

            # Ensure coordinates are within grid bounds
            x = max(0, min(x, self.grid.width - 1))
            y = max(0, min(y, self.grid.height - 1))

            self.grid.place_agent(hotspot, (x, y))

    def _create_tourists(self):
        """Create tourist agents from LLM-generated persona data."""
        if not self.personas_data:
            raise ValueError("No persona data provided for tourist creation")

        for i in range(self.num_tourists):
            # Randomly select persona (could be weighted based on configuration)
            persona_data = random.choice(self.personas_data)
            tourist = Tourist(self, persona_data)
            self.tourists.append(tourist)
            self.agent_set.add(tourist)

            # Place tourist randomly on grid
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(tourist, (x, y))

    def step(self):
        """Execute one step of the simulation."""
        self.datacollector.collect(self)

        # Step all agents
        self.agent_set.do("step")

        self.current_step += 1

    def run_simulation(self, steps: int = 20) -> pd.DataFrame:
        """
        Run the simulation for specified number of steps.

        Args:
            steps: Number of simulation steps to run

        Returns:
            DataFrame with collected model data
        """
        for _ in range(steps):
            self.step()

        return self.get_model_data()

    def get_model_data(self) -> pd.DataFrame:
        """Get collected model data as DataFrame."""
        return self.datacollector.get_model_vars_dataframe()

    def get_agent_data(self) -> pd.DataFrame:
        """Get collected agent data as DataFrame."""
        return self.datacollector.get_agent_vars_dataframe()

    def get_hotspot_statistics(self) -> List[Dict[str, Any]]:
        """Get comprehensive statistics for all hotspots."""
        return [hotspot.get_statistics() for hotspot in self.hotspots]

    def get_persona_statistics(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics grouped by tourist persona type."""
        persona_stats = {}

        for tourist in self.tourists:
            persona = tourist.persona_type
            if persona not in persona_stats:
                persona_stats[persona] = {
                    "count": 0,
                    "total_satisfaction": 0,
                    "total_visits": 0,
                    "total_recommendations": 0
                }

            stats = persona_stats[persona]
            stats["count"] += 1
            stats["total_satisfaction"] += tourist.satisfaction
            stats["total_visits"] += tourist.total_visits
            stats["total_recommendations"] += len(tourist.recommendations_received)

        # Calculate averages
        for persona, stats in persona_stats.items():
            count = stats["count"]
            if count > 0:
                stats["avg_satisfaction"] = stats["total_satisfaction"] / count
                stats["avg_visits"] = stats["total_visits"] / count
                stats["avg_recommendations"] = stats["total_recommendations"] / count

        return persona_stats

    def get_summary_report(self) -> Dict[str, Any]:
        """Generate a comprehensive summary report of simulation results."""
        model_data = self.get_model_data()

        if model_data.empty:
            return {"error": "No simulation data available"}

        final_metrics = model_data.iloc[-1] if len(model_data) > 0 else {}

        return {
            "simulation_steps": len(model_data),
            "final_metrics": {
                "average_popularity": final_metrics.get("Average_Popularity", 0),
                "total_visitors": int(final_metrics.get("Total_Visitors", 0)),
                "social_shares": int(final_metrics.get("Social_Shares", 0)),
                "average_satisfaction": final_metrics.get("Average_Satisfaction", 0)
            },
            "hotspot_statistics": self.get_hotspot_statistics(),
            "persona_statistics": self.get_persona_statistics(),
            "configuration": {
                "num_tourists": self.num_tourists,
                "num_hotspots": len(self.hotspots),
                "grid_size": f"{self.grid.width}x{self.grid.height}"
            }
        }


class ScenarioAwareTourismModel(TourismModel):
    """
    Enhanced tourism model with scenario support for policy testing.

    Extends the base TourismModel with capabilities for testing what-if scenarios,
    including policy changes, events, and external factors that affect tourism dynamics.
    """

    def __init__(self, 
                 scenario: Optional[TourismScenario] = None,
                 personas_data: List[Dict] = None,
                 hotspots_data: List[Dict] = None,
                 business_rules: Dict = None,
                 num_tourists: int = 50,
                 grid_width: int = 20,
                 grid_height: int = 20,
                 random_seed: int = None):
        """
        Initialize scenario-aware tourism model.

        Args:
            scenario: TourismScenario instance for policy testing
            Other args: Same as TourismModel
        """
        self.current_scenario = scenario
        super().__init__(personas_data, hotspots_data, business_rules, 
                        num_tourists, grid_width, grid_height, random_seed)

    def _create_tourists(self):
        """Create scenario-aware tourist agents."""
        if not self.personas_data:
            raise ValueError("No persona data provided for tourist creation")

        self.tourists = []
        for i in range(self.num_tourists):
            persona_data = random.choice(self.personas_data)
            tourist = ScenarioAwareTourist(self, persona_data)
            self.tourists.append(tourist)

            # Place tourist randomly on grid
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(tourist, (x, y))

    def _create_hotspots(self):
        """Create scenario-aware hotspot agents."""
        self.hotspots = []
        for hotspot_data in self.hotspots_data:
            hotspot = ScenarioAwareHotspot(self, hotspot_data)
            self.hotspots.append(hotspot)

            # Place hotspot on grid
            location = hotspot_data.get("location", {})
            x = location.get("x", random.randrange(self.grid.width))
            y = location.get("y", random.randrange(self.grid.height))

            # Ensure coordinates are within grid bounds
            x = max(0, min(x, self.grid.width - 1))
            y = max(0, min(y, self.grid.height - 1))

            self.grid.place_agent(hotspot, (x, y))

    def step(self):
        """Execute one step with scenario processing."""
        self.datacollector.collect(self)

        # Apply scenario effects before agent steps
        if self.current_scenario:
            for agent in self.agents:
                if hasattr(agent, 'apply_scenario_effects'):
                    agent.apply_scenario_effects(self.current_scenario, self.current_step)

        # Step all agents
        for agent in self.agents:
            agent.step()

        self.current_step += 1

    def set_scenario(self, scenario: Optional[TourismScenario]):
        """
        Set or change the active scenario.

        Args:
            scenario: TourismScenario instance or None to clear
        """
        self.current_scenario = scenario

    def get_scenario_impact_summary(self) -> Dict[str, Any]:
        """Generate summary of scenario impacts on the simulation."""
        if not self.current_scenario:
            return {"message": "No active scenario"}

        # Count events that have occurred
        events_occurred = [e for e in self.current_scenario.events 
                          if e["step"] <= self.current_step]

        # Collect hotspot event summaries
        hotspot_events = {}
        for hotspot in self.hotspots:
            if hasattr(hotspot, 'get_event_summary'):
                events = hotspot.get_event_summary()
                if events:
                    hotspot_events[hotspot.name] = events

        return {
            "scenario_name": self.current_scenario.name,
            "description": self.current_scenario.description,
            "events_occurred": len(events_occurred),
            "total_events": len(self.current_scenario.events),
            "active_regulations": list(self.current_scenario.regulations.keys()),
            "external_factors": list(self.current_scenario.external_factors.keys()),
            "hotspot_events": hotspot_events,
            "current_step": self.current_step
        }

    def compare_with_baseline(self, baseline_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare current scenario results with baseline simulation.

        Args:
            baseline_results: Results from baseline simulation

        Returns:
            Dictionary with comparison metrics
        """
        current_results = self.get_summary_report()

        if "final_metrics" not in baseline_results or "final_metrics" not in current_results:
            return {"error": "Insufficient data for comparison"}

        baseline_metrics = baseline_results["final_metrics"]
        current_metrics = current_results["final_metrics"]

        comparison = {}
        for metric, current_value in current_metrics.items():
            baseline_value = baseline_metrics.get(metric, 0)

            if baseline_value != 0:
                change = current_value - baseline_value
                percent_change = (change / baseline_value) * 100
            else:
                change = current_value
                percent_change = 0 if current_value == 0 else 100

            comparison[metric] = {
                "baseline": baseline_value,
                "scenario": current_value,
                "absolute_change": change,
                "percent_change": percent_change
            }

        return {
            "scenario_name": self.current_scenario.name if self.current_scenario else "No Scenario",
            "metrics_comparison": comparison,
            "scenario_summary": self.get_scenario_impact_summary()
        }
