"""
Tourist Agent Classes
====================

This module defines tourist agent classes with LLM-generated persona behaviors
and scenario-aware adaptations.
"""

import random
import numpy as np
from mesa import Agent
from typing import Dict, List, Optional, Any


class Tourist(Agent):
    """
    Base tourist agent with LLM-generated persona characteristics.

    This agent represents a tourist with specific behavioral traits, preferences,
    and interaction patterns based on LLM-generated persona profiles.
    """

    def __init__(self, model, persona_data: Dict[str, Any]):
        """
        Initialize a tourist agent with LLM-generated persona data.

        Args:
            model: The Mesa model instance
            persona_data: Dictionary containing persona characteristics from JSON
        """
        super().__init__(model)

        # Core persona attributes from LLM generation
        self.persona_type = persona_data["type"]
        self.description = persona_data.get("description", "")

        # Demographics
        demographics = persona_data.get("demographics", {})
        self.budget_level = demographics.get("budget_level", "medium")
        self.age_group = demographics.get("age_group", "adult")
        self.origin = demographics.get("origin", "Unknown")
        self.group_size = demographics.get("typical_group_size", 1)

        # Interests and preferences
        self.interests = persona_data.get("interests", [])

        # Behavioral traits
        traits = persona_data.get("behavioral_traits", {})
        self.social_influence = traits.get("social_influence", 0.5)
        self.recommendation_trust = traits.get("recommendation_trust", 0.5)
        self.exploration_tendency = traits.get("exploration_tendency", 0.5)
        self.price_sensitivity = traits.get("price_sensitivity", 0.5)

        # Travel patterns
        patterns = persona_data.get("travel_patterns", {})
        self.daily_visits = patterns.get("daily_visits", 2)
        self.movement_speed = patterns.get("movement_speed", 1)
        self.sharing_probability = patterns.get("sharing_probability", 0.5)
        self.influence_on_similar = patterns.get("influence_on_similar_personas", 0.5)
        self.influence_on_different = patterns.get("influence_on_different_personas", 0.3)

        # Dynamic state
        self.current_hotspot = None
        self.visited_hotspots = []
        self.satisfaction = 0.5
        self.recommendations_received = []
        self.visits_today = 0
        self.total_visits = 0

    def step(self):
        """Execute one step of tourist behavior."""
        if self.visits_today < self.daily_visits:
            self.choose_hotspot()
            self.visit_hotspot()
            self.share_experience()
            self.make_recommendations()

    def choose_hotspot(self):
        """
        Choose next hotspot based on persona preferences and social influences.

        Uses LLM-generated appeal scores and behavioral parameters to make
        realistic destination choices.
        """
        available_hotspots = [agent for agent in self.model.agents 
                            if hasattr(agent, 'appeal_to_personas')]

        if not available_hotspots:
            return

        scores = {}
        for hotspot in available_hotspots:
            # Base appeal from LLM-generated persona-hotspot mappings
            base_score = hotspot.get_persona_appeal(self.persona_type)

            # Popularity influence
            popularity_score = hotspot.current_popularity * 0.3

            # Social recommendations
            rec_score = 0
            for rec in self.recommendations_received:
                if rec["hotspot_id"] == hotspot.unique_id:
                    rec_score += rec["strength"] * self.recommendation_trust

            # Distance penalty
            if hasattr(self, 'pos') and self.pos and hasattr(hotspot, 'pos'):
                distance = np.sqrt((self.pos[0] - hotspot.pos[0])**2 + 
                                 (self.pos[1] - hotspot.pos[1])**2)
                distance_penalty = distance * 0.05
            else:
                distance_penalty = 0

            # Exploration bonus
            exploration_bonus = 0.2 if hotspot.unique_id not in self.visited_hotspots else 0
            exploration_bonus *= self.exploration_tendency

            total_score = base_score + popularity_score + rec_score - distance_penalty + exploration_bonus
            scores[hotspot.unique_id] = max(0, total_score)

        # Probabilistic choice based on scores
        if scores and sum(scores.values()) > 0:
            hotspot_ids = list(scores.keys())
            weights = list(scores.values())
            chosen_id = np.random.choice(hotspot_ids, p=np.array(weights)/sum(weights))

            self.current_hotspot = chosen_id
            chosen_hotspot = next(h for h in available_hotspots if h.unique_id == chosen_id)

            # Move to hotspot location if grid exists
            if hasattr(self.model, 'grid') and hasattr(chosen_hotspot, 'pos'):
                self.model.grid.move_agent(self, chosen_hotspot.pos)

    def visit_hotspot(self):
        """Visit the chosen hotspot and calculate satisfaction."""
        if not self.current_hotspot:
            return

        hotspot = next((agent for agent in self.model.agents 
                       if hasattr(agent, 'unique_id') and agent.unique_id == self.current_hotspot), None)

        if not hotspot:
            return

        # Record visit
        self.visited_hotspots.append(self.current_hotspot)
        self.visits_today += 1
        self.total_visits += 1
        hotspot.record_visit()

        # Calculate satisfaction based on LLM-generated appeal and capacity
        base_appeal = hotspot.get_persona_appeal(self.persona_type)
        capacity_factor = hotspot.get_capacity_factor()

        self.satisfaction = base_appeal * capacity_factor
        self.satisfaction = max(0, min(1, self.satisfaction))

    def share_experience(self):
        """Share experience on social media based on satisfaction and persona traits."""
        if not self.current_hotspot:
            return

        if random.random() < self.sharing_probability:
            hotspot = next((agent for agent in self.model.agents 
                           if hasattr(agent, 'unique_id') and agent.unique_id == self.current_hotspot), None)

            if hotspot:
                # Boost popularity based on satisfaction and social influence
                boost = self.satisfaction * self.social_influence * 0.1  # Social media boost factor
                hotspot.add_social_boost(boost)

    def make_recommendations(self):
        """Make word-of-mouth recommendations to nearby tourists."""
        if not self.current_hotspot or self.satisfaction < 0.6:
            return

        # Find nearby tourists within word-of-mouth range
        if hasattr(self.model, 'grid'):
            neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=3)

            for neighbor in neighbors:
                if isinstance(neighbor, Tourist) and neighbor != self:
                    # Recommendation strength based on persona similarity
                    if neighbor.persona_type == self.persona_type:
                        strength = self.influence_on_similar
                    else:
                        strength = self.influence_on_different

                    strength *= self.satisfaction

                    # Add recommendation
                    neighbor.recommendations_received.append({
                        "hotspot_id": self.current_hotspot,
                        "strength": strength,
                        "from_persona": self.persona_type,
                        "step": self.model.schedule.steps if hasattr(self.model.schedule, 'steps') else 0
                    })

    def reset_daily_counters(self):
        """Reset daily activity counters."""
        self.visits_today = 0


class ScenarioAwareTourist(Tourist):
    """
    Enhanced tourist agent that adapts behavior based on scenario conditions.

    Extends the base Tourist class with scenario-awareness capabilities,
    allowing dynamic adaptation to policy changes and external events.
    """

    def __init__(self, model, persona_data: Dict[str, Any]):
        """Initialize scenario-aware tourist with additional adaptation capabilities."""
        super().__init__(model, persona_data)

        # Scenario-related modifiers
        self.scenario_modifiers = {
            "satisfaction_modifier": 0.0,
            "appeal_sensitivity": 1.0, 
            "cost_sensitivity": 1.0,
            "crowding_tolerance": 1.0,
            "sharing_boost": 1.0
        }

    def apply_scenario_effects(self, scenario, current_step: int):
        """
        Apply scenario effects to modify tourist behavior.

        Args:
            scenario: TourismScenario instance with events and factors
            current_step: Current simulation step
        """
        if not scenario:
            return

        # Reset modifiers
        self.scenario_modifiers = {
            "satisfaction_modifier": 0.0,
            "appeal_sensitivity": 1.0,
            "cost_sensitivity": 1.0,
            "crowding_tolerance": 1.0,
            "sharing_boost": 1.0
        }

        # Process persona-specific events
        for event in scenario.events:
            if (event["step"] == current_step and 
                event.get("target") == self.persona_type):
                self._process_persona_event(event)

        # Apply external factors
        for factor_name, factor_value in scenario.external_factors.items():
            self._apply_external_factor(factor_name, factor_value)

    def _process_persona_event(self, event: Dict[str, Any]):
        """Process events targeting this persona type."""
        event_type = event["type"]
        params = event["parameters"]

        if event_type == "satisfaction_penalty":
            penalty = params.get("penalty", 0.0)
            self.scenario_modifiers["satisfaction_modifier"] -= penalty
        elif event_type == "appeal_boost":
            boost = params.get("boost", 0.0)
            self.scenario_modifiers["appeal_sensitivity"] += boost

    def _apply_external_factor(self, factor_name: str, factor_value: float):
        """Apply external scenario factors to behavior modifiers."""
        factor_mappings = {
            "cost_sensitivity": "cost_sensitivity",
            "event_excitement": "satisfaction_modifier",
            "inconvenience_tolerance": "satisfaction_modifier", 
            "noise_tolerance": "crowding_tolerance"
        }

        if factor_name in factor_mappings:
            modifier_name = factor_mappings[factor_name]
            if modifier_name == "satisfaction_modifier":
                self.scenario_modifiers[modifier_name] += factor_value
            else:
                self.scenario_modifiers[modifier_name] = 1.0 + factor_value

    def visit_hotspot(self):
        """Enhanced visit with scenario-aware satisfaction calculation."""
        if not self.current_hotspot:
            return

        hotspot = next((agent for agent in self.model.agents 
                       if hasattr(agent, 'unique_id') and agent.unique_id == self.current_hotspot), None)

        if not hotspot:
            return

        # Record visit
        self.visited_hotspots.append(self.current_hotspot)
        self.visits_today += 1
        self.total_visits += 1
        hotspot.record_visit()

        # Calculate satisfaction with scenario modifiers
        base_appeal = hotspot.get_persona_appeal(self.persona_type)
        base_appeal *= self.scenario_modifiers["appeal_sensitivity"]

        capacity_factor = hotspot.get_capacity_factor()
        # Apply crowding tolerance modifier
        capacity_factor = (capacity_factor - 1.0) * self.scenario_modifiers["crowding_tolerance"] + 1.0

        # Apply scenario-specific modifiers
        scenario_satisfaction = hotspot.get_scenario_satisfaction_modifier(self.persona_type)

        self.satisfaction = (base_appeal * capacity_factor + 
                           scenario_satisfaction + 
                           self.scenario_modifiers["satisfaction_modifier"])
        self.satisfaction = max(0, min(1, self.satisfaction))

    def share_experience(self):
        """Enhanced sharing with scenario-modified probability."""
        if not self.current_hotspot:
            return

        modified_sharing_prob = self.sharing_probability * self.scenario_modifiers["sharing_boost"]

        if random.random() < modified_sharing_prob:
            hotspot = next((agent for agent in self.model.agents 
                           if hasattr(agent, 'unique_id') and agent.unique_id == self.current_hotspot), None)

            if hotspot:
                boost = self.satisfaction * self.social_influence * 0.1
                hotspot.add_social_boost(boost)
