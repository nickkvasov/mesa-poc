# 3. Create business rules
business_rules_data = {
    "metadata": {
        "version": "1.0",
        "generated_by": "LLM Tourism Simulation System",
        "description": "LLM-generated business rules governing agent behavior and social dynamics",
        "generation_date": "2025-08-10"
    },
    "recommendation_mechanics": {
        "description": "Core mechanics governing how recommendations spread and popularity evolves",
        "social_media_boost": {
            "value": 0.1,
            "description": "Popularity increase per satisfied tourist social media share",
            "reasoning": "Modern tourists heavily influence destination popularity through social sharing"
        },
        "word_of_mouth_range": {
            "value": 3,
            "description": "Grid cell radius for direct tourist-to-tourist recommendations",
            "reasoning": "Physical proximity enables face-to-face recommendations with higher trust"
        },
        "viral_threshold": {
            "value": 0.8,
            "description": "Popularity threshold above which viral amplification effects occur",
            "reasoning": "Destinations reaching critical mass experience self-reinforcing popularity growth"
        },
        "decay_rate": {
            "value": 0.02,
            "description": "Daily popularity decay rate without fresh visitor activity",
            "reasoning": "Destination popularity naturally fades without continuous positive reinforcement"
        },
        "capacity_penalty": {
            "value": 0.5,
            "description": "Popularity reduction multiplier when destination exceeds capacity",
            "reasoning": "Overcrowding significantly reduces visitor satisfaction and future recommendations"
        }
    },
    "persona_interaction_rules": {
        "Budget Backpacker": {
            "sharing_probability": 0.8,
            "influence_on_similar": 0.7,
            "influence_on_different": 0.3,
            "movement_speed": 2,
            "daily_visits": 3
        },
        "Luxury Tourist": {
            "sharing_probability": 0.4,
            "influence_on_similar": 0.8,
            "influence_on_different": 0.2,
            "movement_speed": 1,
            "daily_visits": 2
        },
        "Cultural Explorer": {
            "sharing_probability": 0.6,
            "influence_on_similar": 0.9,
            "influence_on_different": 0.4,
            "movement_speed": 1,
            "daily_visits": 4
        },
        "Adventure Seeker": {
            "sharing_probability": 0.9,
            "influence_on_similar": 0.8,
            "influence_on_different": 0.5,
            "movement_speed": 3,
            "daily_visits": 2
        },
        "Family Traveler": {
            "sharing_probability": 0.7,
            "influence_on_similar": 0.8,
            "influence_on_different": 0.6,
            "movement_speed": 1,
            "daily_visits": 3
        }
    }
}

with open('llm_tourism_sim/data/business_rules.json', 'w') as f:
    json.dump(business_rules_data, f, indent=2)

# 4. Create scenarios events
scenarios_data = {
    "metadata": {
        "version": "1.0",
        "generated_by": "LLM Tourism Simulation System",
        "description": "LLM-generated what-if scenarios for policy testing",
        "total_scenarios": 3,
        "generation_date": "2025-08-10"
    },
    "scenarios": [
        {
            "id": 1,
            "name": "Summer Music Festival",
            "category": "event-driven",
            "description": "A major 3-day music festival is held at Riverside Park, attracting younger tourists",
            "duration_steps": 20,
            "target_demographics": ["Budget Backpacker", "Adventure Seeker"],
            "events": [
                {
                    "step": 5,
                    "type": "capacity_boost",
                    "target": "Riverside Park",
                    "parameters": {"capacity_multiplier": 2.0},
                    "description": "Festival infrastructure doubles park capacity"
                },
                {
                    "step": 5,
                    "type": "appeal_boost",
                    "target": "Riverside Park",
                    "parameters": {
                        "appeal_boost": 0.3,
                        "target_personas": ["Budget Backpacker", "Adventure Seeker"]
                    },
                    "description": "Festival increases appeal to young demographics"
                },
                {
                    "step": 8,
                    "type": "capacity_reset",
                    "target": "Riverside Park",
                    "parameters": {},
                    "description": "Festival ends, capacity returns to normal"
                },
                {
                    "step": 8,
                    "type": "appeal_reset",
                    "target": "Riverside Park",
                    "parameters": {},
                    "description": "Appeal returns to baseline after festival"
                }
            ],
            "regulations": {},
            "external_factors": {
                "noise_tolerance": {"value": 0.4, "description": "Higher tolerance for crowding during festival"},
                "event_excitement": {"value": 0.3, "description": "General excitement boost from festival"}
            }
        },
        {
            "id": 2,
            "name": "Luxury Tourism Tax",
            "category": "policy-based",
            "description": "City introduces a 15% tourism tax on luxury experiences",
            "duration_steps": 20,
            "target_demographics": ["Luxury Tourist"],
            "events": [
                {
                    "step": 3,
                    "type": "satisfaction_penalty",
                    "target": "Luxury Tourist",
                    "parameters": {"penalty": 0.2},
                    "description": "Luxury tourists experience reduced satisfaction due to tax"
                },
                {
                    "step": 3,
                    "type": "appeal_reduction",
                    "target": "Luxury Hotel Zone",
                    "parameters": {"reduction": 0.3},
                    "description": "Luxury venues become less appealing due to higher costs"
                }
            ],
            "regulations": {
                "luxury_tax": {
                    "tax_rate": 0.15,
                    "affected_categories": ["luxury"],
                    "description": "15% tax on luxury tourism services"
                },
                "capacity_limit": {
                    "target": "Luxury Hotel Zone",
                    "new_capacity": 40,
                    "description": "Reduced luxury accommodation capacity"
                }
            },
            "external_factors": {
                "cost_sensitivity": {"value": 0.4, "description": "Increased cost awareness"},
                "luxury_stigma": {"value": 0.2, "description": "Social pressure against luxury consumption"}
            }
        },
        {
            "id": 3,
            "name": "Downtown Construction",
            "category": "infrastructure",
            "description": "Major construction disrupts Central Shopping District access",
            "duration_steps": 20,
            "target_demographics": ["all"],
            "events": [
                {
                    "step": 4,
                    "type": "accessibility_reduction",
                    "target": "Central Shopping District",
                    "parameters": {"accessibility_penalty": 0.4},
                    "description": "Construction barriers reduce accessibility"
                },
                {
                    "step": 6,
                    "type": "noise_pollution",
                    "target": "Central Shopping District", 
                    "parameters": {"satisfaction_penalty": 0.2},
                    "description": "Construction noise reduces visitor satisfaction"
                },
                {
                    "step": 12,
                    "type": "construction_complete",
                    "target": "Central Shopping District",
                    "parameters": {"accessibility_bonus": 0.2},
                    "description": "Construction completion improves accessibility"
                }
            ],
            "regulations": {
                "restricted_access": {
                    "affected_hotspots": ["Central Shopping District"],
                    "description": "Limited access during construction"
                }
            },
            "external_factors": {
                "inconvenience_tolerance": {"value": -0.2, "description": "Reduced tolerance for disruption"},
                "alternative_seeking": {"value": 0.3, "description": "Higher tendency to seek alternatives"}
            }
        }
    ]
}

with open('llm_tourism_sim/data/scenarios_events.json', 'w') as f:
    json.dump(scenarios_data, f, indent=2)

# 5. Create master config
master_config_data = {
    "system_metadata": {
        "name": "LLM-Enhanced Tourism Simulation System",
        "version": "1.0",
        "created_date": "2025-08-10",
        "description": "Complete agent-based tourism simulation with LLM-generated content",
        "technology_stack": ["Mesa 3.2.0", "Python", "LLM-generated content"],
        "license": "MIT"
    },
    "asset_files": {
        "tourist_personas": {
            "filename": "tourist_personas.json",
            "description": "LLM-generated tourist personas with behavioral profiles",
            "record_count": 5
        },
        "urban_hotspots": {
            "filename": "urban_hotspots.json",
            "description": "LLM-generated urban tourism destinations",
            "record_count": 7
        },
        "business_rules": {
            "filename": "business_rules.json",
            "description": "LLM-generated behavioral rules",
            "rule_categories": 2
        },
        "scenarios_events": {
            "filename": "scenarios_events.json",
            "description": "LLM-generated what-if scenarios",
            "scenario_count": 3
        }
    },
    "simulation_configuration": {
        "default_parameters": {
            "grid_size": {"width": 20, "height": 20},
            "default_tourist_count": 50,
            "simulation_steps": 15,
            "random_seed": 42
        },
        "persona_distribution": {
            "Budget Backpacker": 0.30,
            "Luxury Tourist": 0.20,
            "Cultural Explorer": 0.16,
            "Adventure Seeker": 0.14,
            "Family Traveler": 0.20
        }
    },
    "technical_requirements": {
        "python_version": ">=3.8",
        "required_packages": ["mesa>=3.0", "pandas", "numpy", "matplotlib"]
    }
}

with open('llm_tourism_sim/data/master_config.json', 'w') as f:
    json.dump(master_config_data, f, indent=2)

print("✅ business_rules.json created")
print("✅ scenarios_events.json created") 
print("✅ master_config.json created")
print("\n📁 All JSON data files created successfully!")
print("   - tourist_personas.json (5 personas)")
print("   - urban_hotspots.json (7 hotspots)")
print("   - business_rules.json (comprehensive rules)")
print("   - scenarios_events.json (3 scenarios)")
print("   - master_config.json (system configuration)")