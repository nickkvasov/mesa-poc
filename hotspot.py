"""
Hotspot Agent Classes
====================

This module defines hotspot agent classes representing tourism destinations
with LLM-generated characteristics and scenario adaptations.
"""

import random
import numpy as np
from mesa import Agent
from typing import Dict, List, Optional, Any, Tuple


class Hotspot(Agent):
    """
    Base hotspot agent representing a tourism destination.

    This agent represents a tourism hotspot with LLM-generated characteristics,
    appeal scores, and dynamic popularity based on visitor interactions.
    """

    def __init__(self, model, hotspot_data: Dict[str, Any]):
        """
        Initialize a hotspot agent with LLM-generated data.

        Args:
            model: The Mesa model instance
            hotspot_data: Dictionary containing hotspot characteristics from JSON
        """
        super().__init__(model)

        # Core hotspot attributes from LLM generation
        self.name = hotspot_data["name"]
        self.description = hotspot_data.get("description", "")
        self.category = hotspot_data["category"]

        # Location information
        location = hotspot_data.get("location", {})
        self.x = location.get("x", 0)
        self.y = location.get("y", 0)
        self.pos = (self.x, self.y)  # For Mesa grid compatibility
        self.neighborhood = location.get("neighborhood", "Unknown")

        # Physical characteristics
        characteristics = hotspot_data.get("characteristics", {})
        self.initial_popularity = characteristics.get("initial_popularity", 0.5)
        self.current_popularity = self.initial_popularity
        self.base_capacity = characteristics.get("base_capacity", 100)
        self.capacity = self.base_capacity
        self.accessibility_level = characteristics.get("accessibility_level", "medium")

        # LLM-generated persona appeal scores
        self.appeal_to_personas = hotspot_data.get("appeal_to_personas", {})

        # Amenities and features
        self.amenities = hotspot_data.get("amenities", [])
        self.operating_hours = hotspot_data.get("operating_hours", "09:00-17:00")
        self.seasonal_variation = hotspot_data.get("seasonal_variation", 0.1)

        # Dynamic state tracking
        self.visitors_today = 0
        self.total_visitors = 0
        self.social_shares = 0
        self.popularity_history = [self.current_popularity]
        self.satisfaction_ratings = []

        # Business rule parameters (loaded from configuration)
        self.social_media_boost = 0.1
        self.decay_rate = 0.02
        self.capacity_penalty = 0.5
        self.viral_threshold = 0.8

    def get_persona_appeal(self, persona_type: str) -> float:
        """
        Get the appeal score for a specific persona type.

        Args:
            persona_type: The tourist persona type

        Returns:
            Appeal score between 0 and 1
        """
        if persona_type in self.appeal_to_personas:
            if isinstance(self.appeal_to_personas[persona_type], dict):
                return self.appeal_to_personas[persona_type].get("appeal_score", 0.3)
            else:
                return self.appeal_to_personas[persona_type]
        return 0.3  # Default appeal for unspecified personas

    def get_capacity_factor(self) -> float:
        """
        Calculate capacity utilization factor affecting satisfaction.

        Returns:
            Capacity factor (1.0 = optimal, < 1.0 = overcrowded)
        """
        if self.visitors_today == 0:
            return 1.0
        return min(1.0, self.capacity / max(1, self.visitors_today))

    def record_visit(self):
        """Record a tourist visit to this hotspot."""
        self.visitors_today += 1
        self.total_visitors += 1

    def add_social_boost(self, boost: float):
        """
        Add social media boost to popularity.

        Args:
            boost: Popularity boost amount from social sharing
        """
        self.current_popularity += boost
        self.current_popularity = min(1.0, self.current_popularity)  # Cap at 1.0
        self.social_shares += 1

    def step(self):
        """Execute one step of hotspot dynamics."""
        self.update_popularity()
        self.reset_daily_counters()

    def update_popularity(self):
        """Update popularity based on business rules and visitor activity."""
        # Natural decay
        self.current_popularity *= (1 - self.decay_rate)

        # Capacity penalties for overcrowding
        if self.visitors_today > self.capacity:
            overcrowding_penalty = ((self.visitors_today - self.capacity) / 
                                  self.capacity * self.capacity_penalty)
            self.current_popularity = max(0, self.current_popularity - overcrowding_penalty)

        # Viral boost if above threshold
        if self.current_popularity > self.viral_threshold:
            viral_boost = (self.current_popularity - self.viral_threshold) * 0.1
            self.current_popularity = min(1.0, self.current_popularity + viral_boost)

        # Record popularity history
        self.popularity_history.append(self.current_popularity)

    def reset_daily_counters(self):
        """Reset daily visitor and activity counters."""
        self.total_visitors += self.visitors_today
        self.visitors_today = 0

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive hotspot statistics.

        Returns:
            Dictionary with current hotspot metrics
        """
        return {
            "name": self.name,
            "category": self.category,
            "current_popularity": round(self.current_popularity, 3),
            "visitors_today": self.visitors_today,
            "total_visitors": self.total_visitors,
            "social_shares": self.social_shares,
            "capacity": self.capacity,
            "capacity_utilization": round(self.visitors_today / max(1, self.capacity), 3),
            "avg_popularity": round(np.mean(self.popularity_history), 3) if self.popularity_history else 0
        }


class ScenarioAwareHotspot(Hotspot):
    """
    Enhanced hotspot agent that adapts to scenario conditions.

    Extends the base Hotspot class with scenario-awareness capabilities,
    allowing dynamic adaptation to policy changes and external events.
    """

    def __init__(self, model, hotspot_data: Dict[str, Any]):
        """Initialize scenario-aware hotspot with additional adaptation capabilities."""
        super().__init__(model, hotspot_data)

        # Store original values for scenario resets
        self.base_appeal_to_personas = self.appeal_to_personas.copy()
        self.effective_capacity = self.base_capacity

        # Scenario modifiers
        self.accessibility_modifier = 1.0  # 1.0 = normal, >1.0 = harder access
        self.scenario_appeal_modifiers = {}  # Per-persona appeal changes
        self.scenario_satisfaction_modifiers = {}  # Per-persona satisfaction changes

        # Event tracking
        self.active_events = []
        self.processed_events = []

    def apply_scenario_effects(self, scenario, current_step: int):
        """
        Apply scenario effects to this hotspot.

        Args:
            scenario: TourismScenario instance with events and regulations
            current_step: Current simulation step
        """
        if not scenario:
            return

        # Process new events for this step
        for event in scenario.events:
            if (event["step"] == current_step and 
                event.get("target") == self.name and
                event not in self.processed_events):
                self.process_event(event)
                self.processed_events.append(event)

        # Apply ongoing regulations
        self.apply_regulations(scenario.regulations)

    def process_event(self, event: Dict[str, Any]):
        """
        Process a specific scenario event affecting this hotspot.

        Args:
            event: Event dictionary with type, target, and parameters
        """
        event_type = event["type"]
        params = event["parameters"]

        if event_type == "capacity_boost":
            multiplier = params.get("capacity_multiplier", 1.0)
            self.effective_capacity = self.base_capacity * multiplier
            self.active_events.append(f"Capacity boosted to {self.effective_capacity}")

        elif event_type == "capacity_reset":
            self.effective_capacity = self.base_capacity
            self.active_events.append("Capacity reset to normal")

        elif event_type == "appeal_boost":
            boost = params.get("appeal_boost", 0.0)
            target_personas = params.get("target_personas", [])

            for persona in target_personas:
                if persona in self.appeal_to_personas:
                    original_appeal = self.get_persona_appeal(persona)
                    new_appeal = min(1.0, original_appeal + boost)

                    if isinstance(self.appeal_to_personas[persona], dict):
                        self.appeal_to_personas[persona]["appeal_score"] = new_appeal
                    else:
                        self.appeal_to_personas[persona] = new_appeal

            self.active_events.append(f"Appeal boosted for {', '.join(target_personas)}")

        elif event_type == "appeal_reset":
            self.appeal_to_personas = self.base_appeal_to_personas.copy()
            self.active_events.append("Appeal reset to baseline")

        elif event_type == "accessibility_reduction":
            penalty = params.get("accessibility_penalty", 0.0)
            self.accessibility_modifier = 1.0 + penalty
            self.active_events.append(f"Accessibility reduced by {penalty:.1%}")

        elif event_type == "construction_complete":
            bonus = params.get("accessibility_bonus", 0.0)
            self.accessibility_modifier = max(0.1, 1.0 - bonus)
            self.active_events.append(f"Construction completed, accessibility improved")

        elif event_type == "noise_pollution":
            penalty = params.get("satisfaction_penalty", 0.0)
            # Apply to all personas
            for persona in self.appeal_to_personas.keys():
                self.scenario_satisfaction_modifiers[persona] = -penalty
            self.active_events.append(f"Noise pollution affecting satisfaction")

        elif event_type == "appeal_reduction":
            reduction = params.get("reduction", 0.0)
            for persona in self.appeal_to_personas.keys():
                original_appeal = self.get_persona_appeal(persona)
                new_appeal = max(0.0, original_appeal - reduction)

                if isinstance(self.appeal_to_personas[persona], dict):
                    self.appeal_to_personas[persona]["appeal_score"] = new_appeal
                else:
                    self.appeal_to_personas[persona] = new_appeal

            self.active_events.append(f"Appeal reduced by {reduction:.1%}")

    def apply_regulations(self, regulations: Dict[str, Any]):
        """
        Apply ongoing regulatory effects.

        Args:
            regulations: Dictionary of active regulations
        """
        # Capacity limits
        if "capacity_limit" in regulations:
            reg = regulations["capacity_limit"]
            if reg.get("target") == self.name:
                self.effective_capacity = reg["new_capacity"]

        # Luxury tax effects
        if "luxury_tax" in regulations:
            affected_categories = regulations["luxury_tax"].get("affected_categories", [])
            if self.category in affected_categories:
                tax_rate = regulations["luxury_tax"]["tax_rate"]
                # Convert tax rate to appeal penalty
                tax_penalty = tax_rate * 0.5

                for persona in self.appeal_to_personas.keys():
                    original_appeal = self.base_appeal_to_personas[persona]
                    if isinstance(original_appeal, dict):
                        original_score = original_appeal["appeal_score"]
                    else:
                        original_score = original_appeal

                    new_appeal = max(0.0, original_score - tax_penalty)

                    if isinstance(self.appeal_to_personas[persona], dict):
                        self.appeal_to_personas[persona]["appeal_score"] = new_appeal
                    else:
                        self.appeal_to_personas[persona] = new_appeal

    def get_scenario_appeal_modifier(self, persona_type: str) -> float:
        """
        Get scenario-specific appeal modifier for a persona.

        Args:
            persona_type: The tourist persona type

        Returns:
            Additional appeal modifier from scenarios
        """
        return self.scenario_appeal_modifiers.get(persona_type, 0.0)

    def get_scenario_satisfaction_modifier(self, persona_type: str) -> float:
        """
        Get scenario-specific satisfaction modifier for a persona.

        Args:
            persona_type: The tourist persona type

        Returns:
            Satisfaction modifier from scenarios
        """
        return self.scenario_satisfaction_modifiers.get(persona_type, 0.0)

    def get_capacity_factor(self) -> float:
        """Enhanced capacity factor using effective capacity from scenarios."""
        if self.visitors_today == 0:
            return 1.0
        return min(1.0, self.effective_capacity / max(1, self.visitors_today))

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics including scenario effects."""
        stats = super().get_statistics()

        # Add scenario-specific information
        stats.update({
            "effective_capacity": self.effective_capacity,
            "accessibility_modifier": round(self.accessibility_modifier, 3),
            "active_events": len(self.active_events),
            "processed_events": len(self.processed_events)
        })

        return stats

    def get_event_summary(self) -> List[str]:
        """Get summary of active events affecting this hotspot."""
        return self.active_events.copy()
