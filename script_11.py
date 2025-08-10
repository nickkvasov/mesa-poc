# 2. Create urban hotspots
urban_hotspots_data = {
    "metadata": {
        "version": "1.0",
        "generated_by": "LLM Tourism Simulation System",
        "description": "LLM-generated urban tourism hotspots with geospatial characteristics",
        "total_hotspots": 7,
        "grid_dimensions": {"width": 20, "height": 20},
        "generation_date": "2025-08-10"
    },
    "hotspots": [
        {
            "id": 1,
            "name": "Historic Old Town",
            "description": "Charming historic district with cobblestone streets and cultural landmarks",
            "category": "cultural",
            "location": {"x": 5, "y": 8, "neighborhood": "Heritage District"},
            "characteristics": {
                "initial_popularity": 0.7,
                "base_capacity": 100,
                "accessibility_level": "high"
            },
            "appeal_to_personas": {
                "Cultural Explorer": {"appeal_score": 0.9, "reasons": ["historical significance", "cultural immersion"]},
                "Budget Backpacker": {"appeal_score": 0.7, "reasons": ["free walking areas", "authentic culture"]},
                "Family Traveler": {"appeal_score": 0.6, "reasons": ["safe areas", "educational value"]},
                "Luxury Tourist": {"appeal_score": 0.4, "reasons": ["cultural prestige"]},
                "Adventure Seeker": {"appeal_score": 0.3, "reasons": ["exploration opportunities"]}
            },
            "amenities": ["guided tours", "street performers", "historical markers"]
        },
        {
            "id": 2,
            "name": "Central Shopping District",
            "description": "Bustling commercial center with shops, restaurants, and entertainment",
            "category": "commercial",
            "location": {"x": 10, "y": 10, "neighborhood": "Downtown Core"},
            "characteristics": {
                "initial_popularity": 0.8,
                "base_capacity": 150,
                "accessibility_level": "excellent"
            },
            "appeal_to_personas": {
                "Luxury Tourist": {"appeal_score": 0.9, "reasons": ["high-end shopping", "premium dining"]},
                "Family Traveler": {"appeal_score": 0.6, "reasons": ["variety of shops", "entertainment"]},
                "Cultural Explorer": {"appeal_score": 0.4, "reasons": ["urban culture"]},
                "Budget Backpacker": {"appeal_score": 0.3, "reasons": ["window shopping"]},
                "Adventure Seeker": {"appeal_score": 0.2, "reasons": ["urban exploration"]}
            },
            "amenities": ["shopping malls", "restaurants", "public transport"]
        },
        {
            "id": 3,
            "name": "Riverside Park",
            "description": "Large green space with walking paths and recreational facilities",
            "category": "nature",
            "location": {"x": 15, "y": 5, "neighborhood": "Waterfront"},
            "characteristics": {
                "initial_popularity": 0.6,
                "base_capacity": 200,
                "accessibility_level": "high"
            },
            "appeal_to_personas": {
                "Family Traveler": {"appeal_score": 0.9, "reasons": ["safe play areas", "outdoor activities"]},
                "Adventure Seeker": {"appeal_score": 0.8, "reasons": ["jogging paths", "water sports"]},
                "Budget Backpacker": {"appeal_score": 0.8, "reasons": ["free recreation", "scenic views"]},
                "Cultural Explorer": {"appeal_score": 0.5, "reasons": ["peaceful environment"]},
                "Luxury Tourist": {"appeal_score": 0.4, "reasons": ["scenic beauty"]}
            },
            "amenities": ["walking paths", "playgrounds", "sports facilities"]
        },
        {
            "id": 4,
            "name": "Food Market Quarter",
            "description": "Vibrant culinary district with street food and authentic dining",
            "category": "food",
            "location": {"x": 8, "y": 15, "neighborhood": "Culinary District"},
            "characteristics": {
                "initial_popularity": 0.5,
                "base_capacity": 80,
                "accessibility_level": "medium"
            },
            "appeal_to_personas": {
                "Budget Backpacker": {"appeal_score": 0.9, "reasons": ["affordable food", "authentic cuisine"]},
                "Cultural Explorer": {"appeal_score": 0.8, "reasons": ["culinary traditions"]},
                "Adventure Seeker": {"appeal_score": 0.7, "reasons": ["food challenges", "local discoveries"]},
                "Family Traveler": {"appeal_score": 0.5, "reasons": ["variety of options"]},
                "Luxury Tourist": {"appeal_score": 0.3, "reasons": ["unique experiences"]}
            },
            "amenities": ["food stalls", "local markets", "seating areas"]
        },
        {
            "id": 5,
            "name": "Luxury Hotel Zone",
            "description": "Upscale hospitality district with premium services",
            "category": "luxury",
            "location": {"x": 12, "y": 12, "neighborhood": "Premium Quarter"},
            "characteristics": {
                "initial_popularity": 0.4,
                "base_capacity": 60,
                "accessibility_level": "excellent"
            },
            "appeal_to_personas": {
                "Luxury Tourist": {"appeal_score": 0.9, "reasons": ["premium accommodations", "exclusive services"]},
                "Family Traveler": {"appeal_score": 0.5, "reasons": ["high-quality services"]},
                "Cultural Explorer": {"appeal_score": 0.3, "reasons": ["architectural elegance"]},
                "Budget Backpacker": {"appeal_score": 0.1, "reasons": ["aspirational experiences"]},
                "Adventure Seeker": {"appeal_score": 0.2, "reasons": ["premium adventure services"]}
            },
            "amenities": ["luxury hotels", "spas", "fine restaurants"]
        },
        {
            "id": 6,
            "name": "Art Gallery District",
            "description": "Creative quarter with contemporary galleries and exhibitions",
            "category": "cultural",
            "location": {"x": 7, "y": 12, "neighborhood": "Arts Quarter"},
            "characteristics": {
                "initial_popularity": 0.3,
                "base_capacity": 70,
                "accessibility_level": "good"
            },
            "appeal_to_personas": {
                "Cultural Explorer": {"appeal_score": 0.9, "reasons": ["contemporary art", "cultural exhibitions"]},
                "Luxury Tourist": {"appeal_score": 0.6, "reasons": ["exclusive collections"]},
                "Budget Backpacker": {"appeal_score": 0.4, "reasons": ["free exhibitions"]},
                "Family Traveler": {"appeal_score": 0.3, "reasons": ["educational value"]},
                "Adventure Seeker": {"appeal_score": 0.2, "reasons": ["creative challenges"]}
            },
            "amenities": ["art galleries", "artist studios", "exhibition halls"]
        },
        {
            "id": 7,
            "name": "Adventure Sports Center",
            "description": "Specialized facility for extreme sports and outdoor activities",
            "category": "adventure",
            "location": {"x": 18, "y": 8, "neighborhood": "Sports Complex"},
            "characteristics": {
                "initial_popularity": 0.2,
                "base_capacity": 40,
                "accessibility_level": "medium"
            },
            "appeal_to_personas": {
                "Adventure Seeker": {"appeal_score": 0.9, "reasons": ["extreme sports", "adrenaline rush"]},
                "Budget Backpacker": {"appeal_score": 0.5, "reasons": ["adventure experiences"]},
                "Family Traveler": {"appeal_score": 0.3, "reasons": ["family adventure options"]},
                "Cultural Explorer": {"appeal_score": 0.2, "reasons": ["local sports culture"]},
                "Luxury Tourist": {"appeal_score": 0.3, "reasons": ["exclusive adventure packages"]}
            },
            "amenities": ["climbing walls", "adventure courses", "equipment rental"]
        }
    ]
}

with open('llm_tourism_sim/data/urban_hotspots.json', 'w') as f:
    json.dump(urban_hotspots_data, f, indent=2)

print("✅ urban_hotspots.json created")