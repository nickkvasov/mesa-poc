#!/usr/bin/env python3
"""
Test Scenario Comparison Visualization
=====================================

This script demonstrates that scenario comparison visualization
is working correctly by creating scenarios with clearly different effects.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, ScenarioAwareTourismModel, TourismScenario
from utils import quick_compare_scenarios
import pandas as pd


def test_scenario_comparison():
    """Test scenario comparison with clearly different scenarios."""
    
    print("🧪 Testing Scenario Comparison Visualization")
    print("=" * 50)

    # Load data
    print("📁 Loading configuration...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Create test scenarios with very different effects
    print("\n🎭 Creating test scenarios with dramatic differences...")
    
    # Baseline scenario
    baseline_scenario = TourismScenario(
        name="Baseline",
        category="baseline",
        description="Standard tourism conditions",
        duration_steps=15,
        target_demographics=[]
    )

    # High Impact Scenario
    high_impact_scenario = TourismScenario(
        name="High Impact Marketing",
        category="marketing",
        description="Extremely aggressive marketing campaign",
        duration_steps=15,
        target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker", "Luxury Traveler"]
    )

    # Add dramatic effects
    high_impact_scenario.add_event(
        step=2,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.8},  # Very high boost
        description="Extremely aggressive marketing campaign",
        reasoning="Massive promotional activities"
    )

    high_impact_scenario.add_event(
        step=6,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.6},  # Additional high boost
        description="Follow-up aggressive marketing",
        reasoning="Sustained massive promotional efforts"
    )

    # Add external factors
    high_impact_scenario.add_external_factor("event_excitement", 0.7)
    high_impact_scenario.add_external_factor("social_media_buzz", 0.6)

    # Negative Impact Scenario
    negative_impact_scenario = TourismScenario(
        name="Construction Disruption",
        category="infrastructure",
        description="Major construction causing disruption",
        duration_steps=15,
        target_demographics=[]
    )

    # Add negative effects
    negative_impact_scenario.add_event(
        step=3,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": -0.4},  # Negative boost
        description="Construction noise and disruption",
        reasoning="Major construction work reduces appeal"
    )

    negative_impact_scenario.add_event(
        step=8,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": -0.3},  # Additional negative effect
        description="Ongoing construction disruption",
        reasoning="Continued construction work maintains negative impact"
    )

    # Add negative external factors
    negative_impact_scenario.add_external_factor("inconvenience_tolerance", -0.5)
    negative_impact_scenario.add_external_factor("noise_tolerance", -0.4)

    # Run simulations
    print("\n🎯 Running simulations...")
    scenarios = [baseline_scenario, high_impact_scenario, negative_impact_scenario]
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

        model_data = model.run_simulation(steps=15)
        
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

    # Display results
    print("\n📊 SIMULATION RESULTS:")
    print("-" * 40)
    for result in results_collection:
        metrics = result['summary']['final_metrics']
        print(f"{result['name']}:")
        print(f"   Popularity: {metrics['avg_popularity']:.3f}")
        print(f"   Visitors: {metrics['total_visitors']}")
        print(f"   Social Shares: {metrics['social_shares']}")
        print(f"   Satisfaction: {metrics['avg_satisfaction']:.3f}")
        print()

    # Generate comparison visualization
    print("📊 Generating scenario comparison visualization...")
    
    # Create timestamped output directory
    from utils import ResultsStorage
    storage = ResultsStorage()
    output_dir = storage.get_output_directory()
    
    comparison_files = quick_compare_scenarios(
        results_collection,
        output_dir=f"{output_dir}/test_scenario_comparison",
        show_plots=False
    )

    print(f"\n✅ Scenario comparison completed!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Scenario comparison saved to: {output_dir}/test_scenario_comparison/")
    print(f"📊 Generated files:")
    for file_type, file_path in comparison_files.items():
        print(f"   • {file_type}: {file_path}")

    # Check if differences are significant
    baseline_metrics = results_collection[0]['summary']['final_metrics']
    high_impact_metrics = results_collection[1]['summary']['final_metrics']
    negative_metrics = results_collection[2]['summary']['final_metrics']

    print(f"\n🔍 DIFFERENCE ANALYSIS:")
    print("-" * 30)
    
    # High Impact vs Baseline
    popularity_diff_high = high_impact_metrics['avg_popularity'] - baseline_metrics['avg_popularity']
    satisfaction_diff_high = high_impact_metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
    
    print(f"High Impact vs Baseline:")
    print(f"   Popularity change: {popularity_diff_high:+.3f} ({popularity_diff_high/baseline_metrics['avg_popularity']*100:+.1f}%)")
    print(f"   Satisfaction change: {satisfaction_diff_high:+.3f} ({satisfaction_diff_high/baseline_metrics['avg_satisfaction']*100:+.1f}%)")
    
    # Negative Impact vs Baseline
    popularity_diff_neg = negative_metrics['avg_popularity'] - baseline_metrics['avg_popularity']
    satisfaction_diff_neg = negative_metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
    
    print(f"Negative Impact vs Baseline:")
    print(f"   Popularity change: {popularity_diff_neg:+.3f} ({popularity_diff_neg/baseline_metrics['avg_popularity']*100:+.1f}%)")
    print(f"   Satisfaction change: {satisfaction_diff_neg:+.3f} ({satisfaction_diff_neg/baseline_metrics['avg_satisfaction']*100:+.1f}%)")

    # Verify that differences are significant
    if abs(popularity_diff_high) > 0.05 and abs(satisfaction_diff_high) > 0.05:
        print(f"\n✅ SUCCESS: High impact scenario shows significant differences!")
    else:
        print(f"\n⚠️  WARNING: High impact scenario differences may be too small")
        
    if abs(popularity_diff_neg) > 0.05 and abs(satisfaction_diff_neg) > 0.05:
        print(f"✅ SUCCESS: Negative impact scenario shows significant differences!")
    else:
        print(f"⚠️  WARNING: Negative impact scenario differences may be too small")

    print(f"\n🎉 Test completed successfully!")


if __name__ == "__main__":
    test_scenario_comparison()
