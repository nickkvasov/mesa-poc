#!/usr/bin/env python3
"""
Easy Scenario Comparison Example
================================

This example demonstrates how to easily create and compare multiple
distinctive scenarios using the scenario builder utility.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, ScenarioAwareTourismModel
from utils import quick_compare_scenarios
from utils.scenario_builder import ScenarioBuilder, create_quick_comparison_set, create_extreme_comparison_set
import pandas as pd


def run_easy_comparison():
    """Run an easy comparison of multiple scenarios using the scenario builder."""
    
    print("🎭 Easy Scenario Comparison")
    print("=" * 40)
    
    # Load data
    print("📁 Loading configuration...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Method 1: Use pre-built comparison sets
    print("\n🎯 Method 1: Using pre-built comparison sets")
    print("-" * 45)
    
    # Quick comparison set
    print("📊 Creating quick comparison set...")
    quick_scenarios = create_quick_comparison_set()
    
    print(f"✅ Created {len(quick_scenarios)} scenarios:")
    for scenario in quick_scenarios:
        print(f"   • {scenario.name} ({scenario.category})")
    
    # Run simulations for quick set
    print(f"\n🎯 Running simulations for quick comparison set...")
    quick_results = run_scenarios(quick_scenarios, personas, hotspots, business_rules)
    
    # Create timestamped output directory
    from utils import ResultsStorage
    storage = ResultsStorage()
    output_dir = storage.get_output_directory()
    
    # Generate comparison
    print("📊 Generating quick comparison visualizations...")
    quick_comparison_files = quick_compare_scenarios(
        quick_results,
        output_dir=f"{output_dir}/easy_comparison_quick",
        show_plots=False
    )
    
    # Method 2: Use scenario builder with custom configurations
    print("\n🎯 Method 2: Using scenario builder with custom configurations")
    print("-" * 60)
    
    builder = ScenarioBuilder()
    
    # Add baseline
    builder.add_baseline()
    
    # Add scenarios with different intensities
    builder.add_marketing_scenario(name="Light Marketing", intensity="low")
    builder.add_marketing_scenario(name="Aggressive Marketing", intensity="aggressive")
    
    builder.add_festival_scenario(name="Small Festival", scale="small")
    builder.add_festival_scenario(name="Major Festival", scale="major")
    
    builder.add_construction_scenario(name="Light Construction", severity="light")
    builder.add_construction_scenario(name="Severe Construction", severity="severe")
    
    builder.add_policy_scenario(name="Luxury Tax", policy_type="tax", target="luxury")
    builder.add_policy_scenario(name="Budget Subsidy", policy_type="subsidy", target="budget")
    
    custom_scenarios = builder.get_scenarios()
    
    print(f"✅ Created {len(custom_scenarios)} custom scenarios:")
    for scenario in custom_scenarios:
        print(f"   • {scenario.name} ({scenario.category})")
    
    # Run simulations for custom set
    print(f"\n🎯 Running simulations for custom comparison set...")
    custom_results = run_scenarios(custom_scenarios, personas, hotspots, business_rules)
    
    # Generate comparison
    print("📊 Generating custom comparison visualizations...")
    custom_comparison_files = quick_compare_scenarios(
        custom_results,
        output_dir=f"{output_dir}/easy_comparison_custom",
        show_plots=False
    )
    
    # Method 3: Extreme comparison set
    print("\n🎯 Method 3: Using extreme comparison set")
    print("-" * 40)
    
    extreme_scenarios = create_extreme_comparison_set()
    
    print(f"✅ Created {len(extreme_scenarios)} extreme scenarios:")
    for scenario in extreme_scenarios:
        print(f"   • {scenario.name} ({scenario.category})")
    
    # Run simulations for extreme set
    print(f"\n🎯 Running simulations for extreme comparison set...")
    extreme_results = run_scenarios(extreme_scenarios, personas, hotspots, business_rules)
    
    # Generate comparison
    print("📊 Generating extreme comparison visualizations...")
    extreme_comparison_files = quick_compare_scenarios(
        extreme_results,
        output_dir=f"{output_dir}/easy_comparison_extreme",
        show_plots=False
    )
    
    # Display results summary
    print("\n📊 COMPARISON RESULTS SUMMARY:")
    print("=" * 40)
    
    print("Quick Comparison Set:")
    display_results_summary(quick_results)
    
    print("\nCustom Comparison Set:")
    display_results_summary(custom_results)
    
    print("\nExtreme Comparison Set:")
    display_results_summary(extreme_results)
    
    print(f"\n✅ Easy scenario comparison completed!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Comparison directories:")
    print(f"   • {output_dir}/easy_comparison_quick/")
    print(f"   • {output_dir}/easy_comparison_custom/")
    print(f"   • {output_dir}/easy_comparison_extreme/")


def run_scenarios(scenarios, personas, hotspots, business_rules):
    """Run simulations for a list of scenarios."""
    
    results_collection = []
    
    for scenario in scenarios:
        print(f"   Running {scenario.name}...")
        
        model = ScenarioAwareTourismModel(
            scenario=scenario,
            personas_data=personas,
            hotspots_data=hotspots,
            business_rules=business_rules,
            num_tourists=40,
            random_seed=42  # Same seed for fair comparison
        )
        
        model_data = model.run_simulation(steps=20)
        
        # Get statistics
        hotspot_stats = model.get_hotspot_statistics()
        persona_stats = model.get_persona_statistics()
        
        # Calculate final metrics
        final_metrics = model_data.iloc[-1] if len(model_data) > 0 else {}
        
        results_collection.append({
            'name': scenario.name,
            'scenario': scenario,
            'model_data': model_data,
            'hotspot_stats': hotspot_stats,
            'persona_stats': persona_stats,
            'summary': {
                'final_metrics': {
                    'avg_popularity': final_metrics.get('Average_Popularity', 0),
                    'total_visitors': int(final_metrics.get('Total_Visitors', 0)),
                    'social_shares': int(final_metrics.get('Social_Shares', 0)),
                    'avg_satisfaction': final_metrics.get('Average_Satisfaction', 0)
                }
            }
        })
    
    return results_collection


def display_results_summary(results_collection):
    """Display a summary of scenario results."""
    
    baseline_metrics = results_collection[0]['summary']['final_metrics']
    
    # Find best and worst performers
    sorted_by_satisfaction = sorted(results_collection[1:], 
                                  key=lambda x: x['summary']['final_metrics']['avg_satisfaction'], 
                                  reverse=True)
    
    if sorted_by_satisfaction:
        best_scenario = sorted_by_satisfaction[0]
        worst_scenario = sorted_by_satisfaction[-1]
        
        best_satisfaction = best_scenario['summary']['final_metrics']['avg_satisfaction']
        worst_satisfaction = worst_scenario['summary']['final_metrics']['avg_satisfaction']
        baseline_satisfaction = baseline_metrics['avg_satisfaction']
        
        print(f"   🏆 Best: {best_scenario['name']} (Satisfaction: {best_satisfaction:.3f}, +{(best_satisfaction-baseline_satisfaction)/baseline_satisfaction*100:+.1f}%)")
        print(f"   ⚠️  Worst: {worst_scenario['name']} (Satisfaction: {worst_satisfaction:.3f}, {(worst_satisfaction-baseline_satisfaction)/baseline_satisfaction*100:+.1f}%)")


def demonstrate_custom_scenario():
    """Demonstrate how to create a custom scenario."""
    
    print("\n🎨 CUSTOM SCENARIO EXAMPLE:")
    print("-" * 30)
    
    builder = ScenarioBuilder()
    
    # Create a custom "Digital Nomad Initiative" scenario
    custom_events = [
        {
            "step": 3,
            "type": "appeal_boost",
            "target": "Co-working Spaces",
            "parameters": {"appeal_boost": 0.6},
            "description": "Launch of digital nomad program",
            "reasoning": "Co-working spaces become more appealing to remote workers"
        },
        {
            "step": 8,
            "type": "capacity_boost",
            "target": "Co-working Spaces",
            "parameters": {"capacity_multiplier": 2.0},
            "description": "Expand co-working infrastructure",
            "reasoning": "Increased capacity for digital nomads"
        },
        {
            "step": 12,
            "type": "appeal_boost",
            "target": "all",
            "parameters": {"appeal_boost": 0.3},
            "description": "Digital nomad community effect",
            "reasoning": "Presence of digital nomads increases overall appeal"
        }
    ]
    
    external_factors = {
        "event_excitement": 0.4,
        "social_media_buzz": 0.5,
        "cultural_curiosity": 0.3
    }
    
    custom_scenario = builder.add_custom_scenario(
        name="Digital Nomad Initiative",
        category="policy",
        description="Initiative to attract digital nomads with co-working spaces and community",
        events=custom_events,
        external_factors=external_factors,
        target_demographics=["Adventure Seeker", "Cultural Explorer"],
        duration_steps=20
    )
    
    print(f"✅ Created custom scenario: {custom_scenario.name}")
    print(f"   Category: {custom_scenario.category}")
    print(f"   Description: {custom_scenario.description}")
    print(f"   Events: {len(custom_events)}")
    print(f"   External Factors: {len(external_factors)}")


if __name__ == "__main__":
    run_easy_comparison()
    demonstrate_custom_scenario()
