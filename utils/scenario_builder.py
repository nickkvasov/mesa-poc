"""
Scenario Builder Utilities
==========================

This module provides utilities for easily creating and comparing
multiple distinctive scenarios with different effects and characteristics.
"""

from typing import List, Dict, Any, Optional
from sim.models.scenario_manager import TourismScenario


class ScenarioBuilder:
    """
    Utility class for building and managing multiple scenarios for comparison.
    """
    
    def __init__(self):
        self.scenarios = []
    
    def add_baseline(self, name: str = "Baseline", duration_steps: int = 20) -> TourismScenario:
        """Add a baseline scenario with no interventions."""
        baseline = TourismScenario(
            name=name,
            category="baseline",
            description="Standard tourism conditions without any interventions",
            duration_steps=duration_steps,
            target_demographics=[]
        )
        self.scenarios.append(baseline)
        return baseline
    
    def add_marketing_scenario(self, 
                             name: str = "Marketing Campaign",
                             intensity: str = "medium",
                             duration_steps: int = 20) -> TourismScenario:
        """
        Add a marketing scenario with configurable intensity.
        
        Args:
            name: Scenario name
            intensity: "low", "medium", "high", or "aggressive"
            duration_steps: Simulation duration
        """
        intensity_configs = {
            "low": {"appeal_boosts": [0.2, 0.1], "external_factors": {"event_excitement": 0.2}},
            "medium": {"appeal_boosts": [0.4, 0.3, 0.2], "external_factors": {"event_excitement": 0.4, "social_media_buzz": 0.3}},
            "high": {"appeal_boosts": [0.6, 0.5, 0.3], "external_factors": {"event_excitement": 0.6, "social_media_buzz": 0.5, "cultural_curiosity": 0.4}},
            "aggressive": {"appeal_boosts": [0.8, 0.6, 0.4], "external_factors": {"event_excitement": 0.8, "social_media_buzz": 0.7, "cultural_curiosity": 0.6}}
        }
        
        config = intensity_configs.get(intensity, intensity_configs["medium"])
        
        scenario = TourismScenario(
            name=name,
            category="marketing",
            description=f"{intensity.title()} marketing campaign targeting all demographics",
            duration_steps=duration_steps,
            target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker", "Luxury Traveler"]
        )
        
        # Add marketing events
        for i, boost in enumerate(config["appeal_boosts"]):
            step = 3 + i * 5
            scenario.add_event(
                step=step,
                event_type="appeal_boost",
                target="all",
                parameters={"appeal_boost": boost},
                description=f"Marketing campaign phase {i+1}",
                reasoning=f"Promotional activities with {boost:.1f} appeal boost"
            )
        
        # Add external factors
        for factor, value in config["external_factors"].items():
            scenario.add_external_factor(factor, value)
        
        self.scenarios.append(scenario)
        return scenario
    
    def add_festival_scenario(self,
                            name: str = "Cultural Festival",
                            scale: str = "medium",
                            duration_steps: int = 20) -> TourismScenario:
        """
        Add a festival scenario with configurable scale.
        
        Args:
            name: Scenario name
            scale: "small", "medium", "large", or "major"
            duration_steps: Simulation duration
        """
        scale_configs = {
            "small": {"appeal_boost": 0.4, "capacity_multiplier": 1.5, "external_factors": {"artistic_excitement": 0.3}},
            "medium": {"appeal_boost": 0.6, "capacity_multiplier": 2.0, "external_factors": {"artistic_excitement": 0.5, "social_media_buzz": 0.4}},
            "large": {"appeal_boost": 0.8, "capacity_multiplier": 2.5, "external_factors": {"artistic_excitement": 0.7, "social_media_buzz": 0.6, "cultural_curiosity": 0.5}},
            "major": {"appeal_boost": 1.0, "capacity_multiplier": 3.0, "external_factors": {"artistic_excitement": 0.9, "social_media_buzz": 0.8, "cultural_curiosity": 0.7}}
        }
        
        config = scale_configs.get(scale, scale_configs["medium"])
        
        scenario = TourismScenario(
            name=name,
            category="cultural-event",
            description=f"{scale.title()} cultural festival with extensive programming",
            duration_steps=duration_steps,
            target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker"]
        )
        
        # Festival opening
        scenario.add_event(
            step=5,
            event_type="appeal_boost",
            target="City Center",
            parameters={"appeal_boost": config["appeal_boost"]},
            description="Festival opening ceremony",
            reasoning=f"Major festival creates {config['appeal_boost']:.1f} appeal boost"
        )
        
        scenario.add_event(
            step=5,
            event_type="capacity_boost",
            target="City Center",
            parameters={"capacity_multiplier": config["capacity_multiplier"]},
            description="Festival infrastructure deployment",
            reasoning=f"Extensive facilities with {config['capacity_multiplier']:.1f}x capacity"
        )
        
        # Spillover effects
        scenario.add_event(
            step=10,
            event_type="appeal_boost",
            target="Art Gallery District",
            parameters={"appeal_boost": config["appeal_boost"] * 0.7},
            description="Festival spillover effects",
            reasoning="Festival attendees visit nearby cultural venues"
        )
        
        # Festival ends
        scenario.add_event(
            step=15,
            event_type="appeal_reset",
            target="City Center",
            parameters={},
            description="Festival ends",
            reasoning="Festival concludes, appeal returns to baseline"
        )
        
        # Add external factors
        for factor, value in config["external_factors"].items():
            scenario.add_external_factor(factor, value)
        
        self.scenarios.append(scenario)
        return scenario
    
    def add_construction_scenario(self,
                                name: str = "Construction Disruption",
                                severity: str = "medium",
                                duration_steps: int = 20) -> TourismScenario:
        """
        Add a construction disruption scenario with configurable severity.
        
        Args:
            name: Scenario name
            severity: "light", "medium", "heavy", or "severe"
            duration_steps: Simulation duration
        """
        severity_configs = {
            "light": {"appeal_penalties": [-0.2, -0.1], "external_factors": {"inconvenience_tolerance": -0.2}},
            "medium": {"appeal_penalties": [-0.4, -0.3, -0.2], "external_factors": {"inconvenience_tolerance": -0.4, "noise_tolerance": -0.3}},
            "heavy": {"appeal_penalties": [-0.6, -0.5, -0.3], "external_factors": {"inconvenience_tolerance": -0.6, "noise_tolerance": -0.5, "event_excitement": -0.3}},
            "severe": {"appeal_penalties": [-0.8, -0.7, -0.5], "external_factors": {"inconvenience_tolerance": -0.8, "noise_tolerance": -0.7, "event_excitement": -0.5}}
        }
        
        config = severity_configs.get(severity, severity_configs["medium"])
        
        scenario = TourismScenario(
            name=name,
            category="infrastructure",
            description=f"{severity.title()} construction project causing significant disruption",
            duration_steps=duration_steps,
            target_demographics=[]
        )
        
        # Construction phases
        for i, penalty in enumerate(config["appeal_penalties"]):
            step = 3 + i * 5
            scenario.add_event(
                step=step,
                event_type="appeal_boost",
                target="all",
                parameters={"appeal_boost": penalty},
                description=f"Construction phase {i+1}",
                reasoning=f"Construction work with {abs(penalty):.1f} appeal penalty"
            )
        
        # Add external factors
        for factor, value in config["external_factors"].items():
            scenario.add_external_factor(factor, value)
        
        self.scenarios.append(scenario)
        return scenario
    
    def add_policy_scenario(self,
                          name: str = "Policy Intervention",
                          policy_type: str = "tax",
                          target: str = "luxury",
                          duration_steps: int = 20) -> TourismScenario:
        """
        Add a policy intervention scenario.
        
        Args:
            name: Scenario name
            policy_type: "tax", "regulation", "subsidy", or "ban"
            target: "luxury", "budget", "all", or specific target
            duration_steps: Simulation duration
        """
        policy_configs = {
            "tax": {
                "luxury": {"appeal_penalty": -0.4, "external_factors": {"cost_sensitivity": 0.4}},
                "budget": {"appeal_penalty": -0.2, "external_factors": {"cost_sensitivity": 0.6}},
                "all": {"appeal_penalty": -0.3, "external_factors": {"cost_sensitivity": 0.5}}
            },
            "regulation": {
                "luxury": {"appeal_penalty": -0.3, "external_factors": {"event_excitement": -0.2}},
                "budget": {"appeal_penalty": -0.1, "external_factors": {"event_excitement": -0.1}},
                "all": {"appeal_penalty": -0.2, "external_factors": {"event_excitement": -0.15}}
            },
            "subsidy": {
                "luxury": {"appeal_boost": 0.2, "external_factors": {"event_excitement": 0.2}},
                "budget": {"appeal_boost": 0.4, "external_factors": {"event_excitement": 0.3}},
                "all": {"appeal_boost": 0.3, "external_factors": {"event_excitement": 0.25}}
            },
            "ban": {
                "luxury": {"appeal_penalty": -0.6, "external_factors": {"event_excitement": -0.4}},
                "budget": {"appeal_penalty": -0.3, "external_factors": {"event_excitement": -0.2}},
                "all": {"appeal_penalty": -0.5, "external_factors": {"event_excitement": -0.3}}
            }
        }
        
        config = policy_configs.get(policy_type, {}).get(target, {"appeal_penalty": -0.3, "external_factors": {}})
        
        scenario = TourismScenario(
            name=name,
            category="policy",
            description=f"{policy_type.title()} policy targeting {target} tourism",
            duration_steps=duration_steps,
            target_demographics=["Luxury Traveler"] if target == "luxury" else ["Budget Backpacker"] if target == "budget" else []
        )
        
        # Policy implementation
        scenario.add_event(
            step=5,
            event_type="appeal_boost",
            target="all",
            parameters={"appeal_boost": config.get("appeal_penalty", 0) or config.get("appeal_boost", 0)},
            description=f"{policy_type.title()} implementation",
            reasoning=f"Policy affects {target} tourism with {abs(config.get('appeal_penalty', 0) or config.get('appeal_boost', 0)):.1f} impact"
        )
        
        # Add external factors
        for factor, value in config["external_factors"].items():
            scenario.add_external_factor(factor, value)
        
        self.scenarios.append(scenario)
        return scenario
    
    def add_custom_scenario(self,
                          name: str,
                          category: str,
                          description: str,
                          events: List[Dict[str, Any]],
                          external_factors: Dict[str, float],
                          target_demographics: List[str] = None,
                          duration_steps: int = 20) -> TourismScenario:
        """
        Add a custom scenario with user-defined events and factors.
        
        Args:
            name: Scenario name
            category: Scenario category
            description: Scenario description
            events: List of event dictionaries
            external_factors: Dictionary of external factors
            target_demographics: List of target demographics
            duration_steps: Simulation duration
        """
        scenario = TourismScenario(
            name=name,
            category=category,
            description=description,
            duration_steps=duration_steps,
            target_demographics=target_demographics or []
        )
        
        # Add custom events
        for event in events:
            scenario.add_event(
                step=event.get("step", 5),
                event_type=event.get("type", "appeal_boost"),
                target=event.get("target", "all"),
                parameters=event.get("parameters", {}),
                description=event.get("description", "Custom event"),
                reasoning=event.get("reasoning", "User-defined event")
            )
        
        # Add external factors
        for factor, value in external_factors.items():
            scenario.add_external_factor(factor, value)
        
        self.scenarios.append(scenario)
        return scenario
    
    def get_scenarios(self) -> List[TourismScenario]:
        """Get all created scenarios."""
        return self.scenarios
    
    def clear_scenarios(self):
        """Clear all scenarios."""
        self.scenarios = []
    
    def create_comparison_set(self, 
                            include_baseline: bool = True,
                            marketing_intensity: str = "medium",
                            festival_scale: str = "medium",
                            construction_severity: str = "medium") -> List[TourismScenario]:
        """
        Create a standard comparison set of scenarios.
        
        Args:
            include_baseline: Whether to include baseline scenario
            marketing_intensity: Intensity of marketing scenario
            festival_scale: Scale of festival scenario
            construction_severity: Severity of construction scenario
        """
        self.clear_scenarios()
        
        if include_baseline:
            self.add_baseline()
        
        self.add_marketing_scenario(intensity=marketing_intensity)
        self.add_festival_scenario(scale=festival_scale)
        self.add_construction_scenario(severity=construction_severity)
        self.add_policy_scenario(name="Luxury Tax", policy_type="tax", target="luxury")
        self.add_policy_scenario(name="Sustainable Initiative", policy_type="subsidy", target="budget")
        
        return self.get_scenarios()


def create_quick_comparison_set() -> List[TourismScenario]:
    """
    Create a quick set of scenarios for comparison.
    
    Returns:
        List of TourismScenario objects
    """
    builder = ScenarioBuilder()
    return builder.create_comparison_set()


def create_extreme_comparison_set() -> List[TourismScenario]:
    """
    Create a set of scenarios with extreme effects for dramatic comparison.
    
    Returns:
        List of TourismScenario objects
    """
    builder = ScenarioBuilder()
    builder.clear_scenarios()
    
    builder.add_baseline()
    builder.add_marketing_scenario(name="Aggressive Marketing", intensity="aggressive")
    builder.add_festival_scenario(name="Major Festival", scale="major")
    builder.add_construction_scenario(name="Severe Construction", severity="severe")
    builder.add_policy_scenario(name="Luxury Ban", policy_type="ban", target="luxury")
    builder.add_policy_scenario(name="Budget Subsidy", policy_type="subsidy", target="budget")
    
    return builder.get_scenarios()
