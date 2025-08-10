"""
Scenario Management System
=========================

This module provides classes and functions for managing what-if scenarios
in the tourism simulation system, enabling policy testing and impact assessment.
"""

import json
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field


@dataclass
class TourismScenario:
    """
    Represents a what-if scenario for tourism policy testing.

    A scenario consists of:
    - Timed events that occur at specific simulation steps
    - Ongoing regulations that persist throughout the simulation  
    - External factors that modify agent behaviors
    """

    name: str
    description: str
    category: str = "general"
    events: List[Dict[str, Any]] = field(default_factory=list)
    regulations: Dict[str, Any] = field(default_factory=dict)
    external_factors: Dict[str, float] = field(default_factory=dict)
    duration_steps: int = 20
    target_demographics: List[str] = field(default_factory=list)
    expected_impacts: Dict[str, str] = field(default_factory=dict)

    def add_event(self, step: int, event_type: str, target: str, parameters: Dict[str, Any], 
                  description: str = "", reasoning: str = ""):
        """
        Add a timed event to the scenario.

        Args:
            step: Simulation step when event occurs
            event_type: Type of event (capacity_boost, appeal_boost, etc.)
            target: Target hotspot or persona type
            parameters: Event-specific parameters
            description: Human-readable event description
            reasoning: LLM-generated reasoning for the event
        """
        event = {
            "step": step,
            "type": event_type,
            "target": target,
            "parameters": parameters,
            "description": description,
            "reasoning": reasoning
        }
        self.events.append(event)

    def add_regulation(self, regulation_type: str, parameters: Dict[str, Any]):
        """
        Add an ongoing regulation to the scenario.

        Args:
            regulation_type: Type of regulation (luxury_tax, capacity_limit, etc.)
            parameters: Regulation-specific parameters
        """
        self.regulations[regulation_type] = parameters

    def add_external_factor(self, factor_name: str, factor_value: float):
        """
        Add an external factor that affects agent behavior.

        Args:
            factor_name: Name of the external factor
            factor_value: Numeric value of the factor effect
        """
        self.external_factors[factor_name] = factor_value

    def get_events_for_step(self, step: int) -> List[Dict[str, Any]]:
        """Get all events that occur at a specific simulation step."""
        return [event for event in self.events if event["step"] == step]

    def get_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of the scenario."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "duration_steps": self.duration_steps,
            "total_events": len(self.events),
            "event_timeline": sorted([e["step"] for e in self.events]),
            "regulations": list(self.regulations.keys()),
            "external_factors": list(self.external_factors.keys()),
            "target_demographics": self.target_demographics,
            "expected_impacts": self.expected_impacts
        }


class ScenarioManager:
    """
    Manages multiple tourism scenarios and provides comparison capabilities.

    The ScenarioManager loads scenarios from JSON configuration files and
    provides tools for scenario selection, comparison, and batch processing.
    """

    def __init__(self, scenarios_file: Optional[str] = None):
        """
        Initialize the scenario manager.

        Args:
            scenarios_file: Path to JSON file containing scenario definitions
        """
        self.scenarios = {}
        self.scenario_history = []

        if scenarios_file:
            self.load_scenarios_from_file(scenarios_file)

    def load_scenarios_from_file(self, file_path: str):
        """
        Load scenarios from a JSON configuration file.

        Args:
            file_path: Path to JSON file with scenario definitions
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            scenarios_data = data.get("scenarios", [])
            for scenario_data in scenarios_data:
                scenario = self._create_scenario_from_dict(scenario_data)
                self.scenarios[scenario.name] = scenario

        except FileNotFoundError:
            print(f"Warning: Scenario file {file_path} not found")
        except json.JSONDecodeError as e:
            print(f"Error parsing scenario file: {e}")

    def _create_scenario_from_dict(self, scenario_data: Dict[str, Any]) -> TourismScenario:
        """Create a TourismScenario instance from dictionary data."""
        scenario = TourismScenario(
            name=scenario_data["name"],
            description=scenario_data["description"],
            category=scenario_data.get("category", "general"),
            duration_steps=scenario_data.get("duration_steps", 20),
            target_demographics=scenario_data.get("target_demographics", []),
            expected_impacts=scenario_data.get("expected_impacts", {})
        )

        # Add events
        for event_data in scenario_data.get("events", []):
            scenario.add_event(
                step=event_data["step"],
                event_type=event_data["type"],
                target=event_data["target"],
                parameters=event_data["parameters"],
                description=event_data.get("description", ""),
                reasoning=event_data.get("reasoning", "")
            )

        # Add regulations
        for reg_type, reg_params in scenario_data.get("regulations", {}).items():
            scenario.add_regulation(reg_type, reg_params)

        # Add external factors
        for factor_name, factor_value in scenario_data.get("external_factors", {}).items():
            if isinstance(factor_value, dict):
                # Handle complex factor definitions
                scenario.add_external_factor(factor_name, factor_value.get("value", 0.0))
            else:
                scenario.add_external_factor(factor_name, factor_value)

        return scenario

    def get_scenario(self, name: str) -> Optional[TourismScenario]:
        """
        Get a scenario by name.

        Args:
            name: Name of the scenario

        Returns:
            TourismScenario instance or None if not found
        """
        return self.scenarios.get(name)

    def list_scenarios(self) -> List[str]:
        """Get list of all available scenario names."""
        return list(self.scenarios.keys())

    def get_scenarios_by_category(self, category: str) -> List[TourismScenario]:
        """
        Get all scenarios in a specific category.

        Args:
            category: Scenario category to filter by

        Returns:
            List of scenarios in the specified category
        """
        return [scenario for scenario in self.scenarios.values() 
                if scenario.category == category]

    def create_scenario(self, name: str, description: str, category: str = "custom") -> TourismScenario:
        """
        Create a new custom scenario.

        Args:
            name: Name for the new scenario
            description: Description of the scenario
            category: Category for the scenario

        Returns:
            New TourismScenario instance
        """
        scenario = TourismScenario(name=name, description=description, category=category)
        self.scenarios[name] = scenario
        return scenario

    def compare_scenarios(self, scenario_names: List[str]) -> Dict[str, Any]:
        """
        Compare multiple scenarios and their characteristics.

        Args:
            scenario_names: List of scenario names to compare

        Returns:
            Dictionary with comparison data
        """
        comparison = {
            "scenarios": [],
            "comparison_matrix": {}
        }

        scenarios_to_compare = []
        for name in scenario_names:
            if name in self.scenarios:
                scenarios_to_compare.append(self.scenarios[name])
            else:
                print(f"Warning: Scenario '{name}' not found")

        if not scenarios_to_compare:
            return comparison

        # Collect scenario summaries
        for scenario in scenarios_to_compare:
            comparison["scenarios"].append(scenario.get_summary())

        # Create comparison matrix
        attributes = ["total_events", "duration_steps", "regulations", "external_factors"]

        for attr in attributes:
            comparison["comparison_matrix"][attr] = {}
            for scenario in scenarios_to_compare:
                summary = scenario.get_summary()
                if attr in ["regulations", "external_factors"]:
                    value = len(summary[attr])
                else:
                    value = summary[attr]
                comparison["comparison_matrix"][attr][scenario.name] = value

        return comparison

    def export_scenario(self, scenario_name: str, file_path: str):
        """
        Export a scenario to a JSON file.

        Args:
            scenario_name: Name of scenario to export
            file_path: Path for the exported file
        """
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found")

        scenario = self.scenarios[scenario_name]

        export_data = {
            "name": scenario.name,
            "description": scenario.description,
            "category": scenario.category,
            "duration_steps": scenario.duration_steps,
            "target_demographics": scenario.target_demographics,
            "expected_impacts": scenario.expected_impacts,
            "events": scenario.events,
            "regulations": scenario.regulations,
            "external_factors": scenario.external_factors
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

    def get_scenario_recommendations(self, objective: str) -> List[str]:
        """
        Get scenario recommendations based on policy objective.

        Args:
            objective: Policy objective (e.g., "increase_satisfaction", "redistribute_tourism")

        Returns:
            List of recommended scenario names
        """
        recommendations = []

        objective_mappings = {
            "increase_satisfaction": ["event-driven"],
            "redistribute_tourism": ["policy-based"],
            "test_disruption": ["infrastructure"],
            "boost_economy": ["event-driven", "policy-based"]
        }

        target_categories = objective_mappings.get(objective, [])

        for scenario in self.scenarios.values():
            if scenario.category in target_categories:
                recommendations.append(scenario.name)

        return recommendations

    def generate_scenario_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report of all available scenarios."""
        categories = {}
        total_events = 0
        total_regulations = 0
        total_factors = 0

        for scenario in self.scenarios.values():
            category = scenario.category
            if category not in categories:
                categories[category] = []
            categories[category].append(scenario.name)

            total_events += len(scenario.events)
            total_regulations += len(scenario.regulations)
            total_factors += len(scenario.external_factors)

        return {
            "total_scenarios": len(self.scenarios),
            "categories": categories,
            "summary_statistics": {
                "total_events": total_events,
                "total_regulations": total_regulations,
                "total_external_factors": total_factors,
                "avg_events_per_scenario": total_events / max(1, len(self.scenarios)),
            },
            "available_scenarios": list(self.scenarios.keys())
        }


def create_festival_scenario(name: str = "Custom Festival") -> TourismScenario:
    """
    Create a template festival scenario for customization.

    Args:
        name: Name for the festival scenario

    Returns:
        TourismScenario instance with festival event template
    """
    scenario = TourismScenario(
        name=name,
        description="Template for festival-based tourism events",
        category="event-driven",
        target_demographics=["Budget Backpacker", "Adventure Seeker"]
    )

    # Add template events
    scenario.add_event(
        step=5,
        event_type="capacity_boost",
        target="TARGET_HOTSPOT",
        parameters={"capacity_multiplier": 1.5},
        description="Festival increases venue capacity",
        reasoning="Temporary infrastructure handles additional visitors"
    )

    scenario.add_external_factor("event_excitement", 0.2)
    scenario.add_external_factor("noise_tolerance", 0.3)

    return scenario


def create_policy_scenario(name: str = "Custom Policy") -> TourismScenario:
    """
    Create a template policy scenario for customization.

    Args:
        name: Name for the policy scenario

    Returns:
        TourismScenario instance with policy template
    """
    scenario = TourismScenario(
        name=name,
        description="Template for tourism policy testing",
        category="policy-based",
        target_demographics=["Luxury Tourist"]
    )

    # Add template regulation
    scenario.add_regulation("example_tax", {
        "tax_rate": 0.10,
        "affected_categories": ["luxury"]
    })

    scenario.add_external_factor("cost_sensitivity", 0.2)

    return scenario
