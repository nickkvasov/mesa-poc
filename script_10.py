# Create JSON data files directly in the data directory

import json

# 1. Create tourist personas
tourist_personas_data = {
    "metadata": {
        "version": "1.0",
        "generated_by": "LLM Tourism Simulation System",
        "description": "LLM-generated tourist personas with rich behavioral profiles",
        "total_personas": 5,
        "generation_date": "2025-08-10"
    },
    "personas": [
        {
            "id": 1,
            "type": "Budget Backpacker",
            "description": "Young, cost-conscious travelers seeking authentic local experiences",
            "demographics": {
                "budget_level": "low",
                "age_group": "young",
                "origin": "Europe",
                "typical_group_size": 1
            },
            "interests": ["street food", "free activities", "hostels", "local culture", "walking tours"],
            "behavioral_traits": {
                "social_influence": 0.8,
                "recommendation_trust": 0.9,
                "exploration_tendency": 0.7,
                "price_sensitivity": 0.9
            },
            "travel_patterns": {
                "daily_visits": 3,
                "movement_speed": 2,
                "sharing_probability": 0.8,
                "influence_on_similar_personas": 0.7,
                "influence_on_different_personas": 0.3
            }
        },
        {
            "id": 2,
            "type": "Luxury Tourist",
            "description": "Affluent travelers seeking premium experiences and comfort",
            "demographics": {
                "budget_level": "high",
                "age_group": "middle_aged",
                "origin": "North America",
                "typical_group_size": 2
            },
            "interests": ["fine dining", "shopping", "spas", "premium hotels", "private tours"],
            "behavioral_traits": {
                "social_influence": 0.6,
                "recommendation_trust": 0.5,
                "exploration_tendency": 0.4,
                "price_sensitivity": 0.2
            },
            "travel_patterns": {
                "daily_visits": 2,
                "movement_speed": 1,
                "sharing_probability": 0.4,
                "influence_on_similar_personas": 0.8,
                "influence_on_different_personas": 0.2
            }
        },
        {
            "id": 3,
            "type": "Cultural Explorer",
            "description": "Knowledge-seeking travelers focused on history, art, and cultural understanding",
            "demographics": {
                "budget_level": "medium",
                "age_group": "senior",
                "origin": "Asia",
                "typical_group_size": 3
            },
            "interests": ["museums", "historical sites", "art galleries", "local traditions", "guided tours"],
            "behavioral_traits": {
                "social_influence": 0.4,
                "recommendation_trust": 0.7,
                "exploration_tendency": 0.8,
                "learning_orientation": 0.9
            },
            "travel_patterns": {
                "daily_visits": 4,
                "movement_speed": 1,
                "sharing_probability": 0.6,
                "influence_on_similar_personas": 0.9,
                "influence_on_different_personas": 0.4
            }
        },
        {
            "id": 4,
            "type": "Adventure Seeker",
            "description": "Active travelers pursuing exciting outdoor activities and new challenges",
            "demographics": {
                "budget_level": "medium",
                "age_group": "young",
                "origin": "Australia",
                "typical_group_size": 2
            },
            "interests": ["outdoor activities", "extreme sports", "nature exploration", "hiking", "adventure tours"],
            "behavioral_traits": {
                "social_influence": 0.9,
                "recommendation_trust": 0.8,
                "exploration_tendency": 0.9,
                "risk_tolerance": 0.9
            },
            "travel_patterns": {
                "daily_visits": 2,
                "movement_speed": 3,
                "sharing_probability": 0.9,
                "influence_on_similar_personas": 0.8,
                "influence_on_different_personas": 0.5
            }
        },
        {
            "id": 5,
            "type": "Family Traveler",
            "description": "Family groups seeking safe, entertaining activities suitable for all ages",
            "demographics": {
                "budget_level": "medium",
                "age_group": "middle_aged",
                "origin": "North America",
                "typical_group_size": 4
            },
            "interests": ["family activities", "parks", "safe attractions", "restaurants", "entertainment"],
            "behavioral_traits": {
                "social_influence": 0.7,
                "recommendation_trust": 0.8,
                "exploration_tendency": 0.5,
                "safety_consciousness": 0.9
            },
            "travel_patterns": {
                "daily_visits": 3,
                "movement_speed": 1,
                "sharing_probability": 0.7,
                "influence_on_similar_personas": 0.8,
                "influence_on_different_personas": 0.6
            }
        }
    ]
}

with open('llm_tourism_sim/data/tourist_personas.json', 'w') as f:
    json.dump(tourist_personas_data, f, indent=2)

print("✅ tourist_personas.json created")