# Create the data loader utility
data_loader = '''"""
Data Loading Utilities
=====================

This module provides functions for loading LLM-generated configuration data
from JSON files, including personas, hotspots, business rules, and scenarios.
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


# Default data directory relative to this module
DEFAULT_DATA_DIR = Path(__file__).parent.parent / "data"


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}")


def load_personas(file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load LLM-generated tourist personas from JSON file.
    
    Args:
        file_path: Path to personas JSON file. If None, uses default location.
        
    Returns:
        List of persona dictionaries with behavioral profiles
    """
    if file_path is None:
        file_path = DEFAULT_DATA_DIR / "tourist_personas.json"
    
    data = load_json_file(str(file_path))
    return data.get("personas", [])


def load_hotspots(file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load LLM-generated urban hotspots from JSON file.
    
    Args:
        file_path: Path to hotspots JSON file. If None, uses default location.
        
    Returns:
        List of hotspot dictionaries with characteristics and appeal scores
    """
    if file_path is None:
        file_path = DEFAULT_DATA_DIR / "urban_hotspots.json"
    
    data = load_json_file(str(file_path))
    return data.get("hotspots", [])


def load_business_rules(file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load LLM-generated business rules from JSON file.
    
    Args:
        file_path: Path to business rules JSON file. If None, uses default location.
        
    Returns:
        Dictionary with business rules and behavioral parameters
    """
    if file_path is None:
        file_path = DEFAULT_DATA_DIR / "business_rules.json"
    
    return load_json_file(str(file_path))


def load_scenarios(file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Load LLM-generated scenarios from JSON file.
    
    Args:
        file_path: Path to scenarios JSON file. If None, uses default location.
        
    Returns:
        List of scenario dictionaries with events and regulations
    """
    if file_path is None:
        file_path = DEFAULT_DATA_DIR / "scenarios_events.json"
    
    data = load_json_file(str(file_path))
    return data.get("scenarios", [])


def load_master_config(file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load master configuration file with system metadata.
    
    Args:
        file_path: Path to master config JSON file. If None, uses default location.
        
    Returns:
        Dictionary with system configuration and metadata
    """
    if file_path is None:
        file_path = DEFAULT_DATA_DIR / "master_config.json"
    
    return load_json_file(str(file_path))


def load_data(data_dir: Optional[str] = None) -> Tuple[List[Dict], List[Dict], Dict[str, Any], List[Dict]]:
    """
    Load all LLM-generated data files for tourism simulation.
    
    This convenience function loads personas, hotspots, business rules, and scenarios
    from their default locations or a specified directory.
    
    Args:
        data_dir: Directory containing JSON data files. If None, uses default location.
        
    Returns:
        Tuple of (personas, hotspots, business_rules, scenarios)
    """
    if data_dir:
        data_path = Path(data_dir)
    else:
        data_path = DEFAULT_DATA_DIR
    
    try:
        personas = load_personas(data_path / "tourist_personas.json")
        hotspots = load_hotspots(data_path / "urban_hotspots.json")
        business_rules = load_business_rules(data_path / "business_rules.json")
        scenarios = load_scenarios(data_path / "scenarios_events.json")
        
        return personas, hotspots, business_rules, scenarios
        
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Please ensure all JSON data files are present in the data directory:")
        print(f"  - {data_path}/tourist_personas.json")
        print(f"  - {data_path}/urban_hotspots.json")
        print(f"  - {data_path}/business_rules.json")
        print(f"  - {data_path}/scenarios_events.json")
        raise


def validate_personas_data(personas: List[Dict[str, Any]]) -> bool:
    """
    Validate that persona data contains required fields.
    
    Args:
        personas: List of persona dictionaries
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["type", "demographics", "behavioral_traits", "travel_patterns"]
    
    for persona in personas:
        for field in required_fields:
            if field not in persona:
                print(f"Missing required field '{field}' in persona: {persona.get('type', 'Unknown')}")
                return False
        
        # Check nested required fields
        if "budget_level" not in persona.get("demographics", {}):
            print(f"Missing budget_level in persona: {persona.get('type', 'Unknown')}")
            return False
            
        traits = persona.get("behavioral_traits", {})
        required_traits = ["social_influence", "recommendation_trust", "exploration_tendency"]
        for trait in required_traits:
            if trait not in traits:
                print(f"Missing trait '{trait}' in persona: {persona.get('type', 'Unknown')}")
                return False
    
    return True


def validate_hotspots_data(hotspots: List[Dict[str, Any]]) -> bool:
    """
    Validate that hotspot data contains required fields.
    
    Args:
        hotspots: List of hotspot dictionaries
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["name", "category", "location", "characteristics", "appeal_to_personas"]
    
    for hotspot in hotspots:
        for field in required_fields:
            if field not in hotspot:
                print(f"Missing required field '{field}' in hotspot: {hotspot.get('name', 'Unknown')}")
                return False
        
        # Check location coordinates
        location = hotspot.get("location", {})
        if "x" not in location or "y" not in location:
            print(f"Missing x/y coordinates in hotspot: {hotspot.get('name', 'Unknown')}")
            return False
        
        # Check characteristics
        characteristics = hotspot.get("characteristics", {})
        required_characteristics = ["initial_popularity", "base_capacity"]
        for char in required_characteristics:
            if char not in characteristics:
                print(f"Missing characteristic '{char}' in hotspot: {hotspot.get('name', 'Unknown')}")
                return False
    
    return True


def validate_business_rules_data(business_rules: Dict[str, Any]) -> bool:
    """
    Validate that business rules contain required parameters.
    
    Args:
        business_rules: Dictionary with business rules
        
    Returns:
        True if valid, False otherwise
    """
    required_sections = ["recommendation_mechanics", "persona_interaction_rules"]
    
    for section in required_sections:
        if section not in business_rules:
            print(f"Missing required section '{section}' in business rules")
            return False
    
    # Check recommendation mechanics
    rec_mechanics = business_rules.get("recommendation_mechanics", {})
    required_params = ["social_media_boost", "word_of_mouth_range", "viral_threshold", "decay_rate"]
    for param in required_params:
        if param not in rec_mechanics:
            print(f"Missing parameter '{param}' in recommendation_mechanics")
            return False
    
    return True


def get_data_summary(data_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a summary of loaded data for validation and overview.
    
    Args:
        data_dir: Directory containing data files
        
    Returns:
        Dictionary with data summary statistics
    """
    try:
        personas, hotspots, business_rules, scenarios = load_data(data_dir)
        
        # Count persona types
        persona_types = {}
        for persona in personas:
            ptype = persona.get("type", "Unknown")
            persona_types[ptype] = persona_types.get(ptype, 0) + 1
        
        # Count hotspot categories  
        hotspot_categories = {}
        for hotspot in hotspots:
            category = hotspot.get("category", "Unknown")
            hotspot_categories[category] = hotspot_categories.get(category, 0) + 1
        
        # Count scenario types
        scenario_categories = {}
        for scenario in scenarios:
            category = scenario.get("category", "Unknown")
            scenario_categories[category] = scenario_categories.get(category, 0) + 1
        
        return {
            "data_validation": {
                "personas_valid": validate_personas_data(personas),
                "hotspots_valid": validate_hotspots_data(hotspots),
                "business_rules_valid": validate_business_rules_data(business_rules)
            },
            "data_counts": {
                "total_personas": len(personas),
                "total_hotspots": len(hotspots),
                "total_scenarios": len(scenarios),
                "business_rule_sections": len([k for k in business_rules.keys() if k != "metadata"])
            },
            "persona_distribution": persona_types,
            "hotspot_distribution": hotspot_categories,
            "scenario_distribution": scenario_categories,
            "data_quality": "All data files loaded successfully"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "data_quality": "Error loading data files"
        }


def export_data_sample(output_dir: str = "sample_data", num_personas: int = 2, num_hotspots: int = 3):
    """
    Export a sample of the data for testing or demonstration purposes.
    
    Args:
        output_dir: Directory to save sample files
        num_personas: Number of personas to include in sample
        num_hotspots: Number of hotspots to include in sample
    """
    try:
        personas, hotspots, business_rules, scenarios = load_data()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Sample personas
        sample_personas = {
            "metadata": {
                "version": "1.0",
                "description": "Sample tourist personas for testing",
                "total_personas": min(num_personas, len(personas))
            },
            "personas": personas[:num_personas]
        }
        
        # Sample hotspots
        sample_hotspots = {
            "metadata": {
                "version": "1.0", 
                "description": "Sample urban hotspots for testing",
                "total_hotspots": min(num_hotspots, len(hotspots))
            },
            "hotspots": hotspots[:num_hotspots]
        }
        
        # Save sample files
        with open(f"{output_dir}/sample_personas.json", 'w') as f:
            json.dump(sample_personas, f, indent=2)
            
        with open(f"{output_dir}/sample_hotspots.json", 'w') as f:
            json.dump(sample_hotspots, f, indent=2)
            
        with open(f"{output_dir}/sample_business_rules.json", 'w') as f:
            json.dump(business_rules, f, indent=2)
        
        print(f"Sample data exported to {output_dir}/")
        print(f"  - {num_personas} personas")
        print(f"  - {num_hotspots} hotspots") 
        print(f"  - Complete business rules")
        
    except Exception as e:
        print(f"Error exporting sample data: {e}")
'''

# Write data_loader.py
with open('llm_tourism_sim/utils/data_loader.py', 'w') as f:
    f.write(data_loader)

print("✅ Data Loader utility created!")
print("   - Comprehensive JSON loading functions")
print("   - Data validation and error handling")
print("   - Sample data export capabilities")