#!/usr/bin/env python3
"""
Custom Analysis Example
=======================

This example demonstrates advanced analysis capabilities and custom
scenario creation for specialized tourism policy testing.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from llm_tourism_sim import load_data, ScenarioAwareTourismModel, analyze_simulation_results
from llm_tourism_sim.scenarios.scenario_manager import TourismScenario, ScenarioManager
from llm_tourism_sim.utils.analysis import compare_scenarios, generate_policy_recommendations
import pandas as pd


def create_custom_scenario():
    """Create a custom scenario for testing."""

    print("🛠️ Creating custom 'Street Art Festival' scenario...")

    scenario = TourismScenario(
        name="Street Art Festival",
        category="cultural-event",
        description="Pop-up street art festival transforms Art Gallery District for 1 week",
        duration_steps=20,
        target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker"]
    )

    # Add events
    scenario.add_event(
        step=3,
        event_type="appeal_boost", 
        target="Art Gallery District",
        parameters={
            "appeal_boost": 0.4,
            "target_personas": ["Cultural Explorer", "Budget Backpacker", "Adventure Seeker"]
        },
        description="Street art festival significantly boosts appeal to cultural and adventurous tourists",
        reasoning="Street art appeals to culture seekers and budget travelers seeking authentic experiences"
    )

    scenario.add_event(
        step=3,
        event_type="capacity_boost",
        target="Art Gallery District", 
        parameters={"capacity_multiplier": 1.3},
        description="Outdoor installations increase effective venue capacity",
        reasoning="Street art utilizes outdoor spaces, expanding beyond indoor gallery limitations"
    )

    scenario.add_event(
        step=10,
        event_type="appeal_reset",
        target="Art Gallery District",
        parameters={},
        description="Festival ends, appeal returns to baseline",
        reasoning="Temporary art installations removed, regular programming resumes"
    )

    scenario.add_event(
        step=10,
        event_type="capacity_reset", 
        target="Art Gallery District",
        parameters={},
        description="Capacity returns to normal after festival",
        reasoning="Outdoor spaces no longer utilized for art displays"
    )

    # Add external factors
    scenario.add_external_factor("artistic_excitement", 0.25)
    scenario.add_external_factor("social_media_buzz", 0.15)
    scenario.add_external_factor("cultural_curiosity", 0.20)

    print("✅ Custom scenario created with 4 events and 3 external factors")

    return scenario


def run_advanced_analysis():
    """Run advanced analysis with custom scenarios and detailed insights."""

    print("🔬 LLM Tourism Simulation - Advanced Analysis")
    print("=" * 50)

    # Load data
    print("📁 Loading configuration...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Initialize scenario manager
    scenario_manager = ScenarioManager()

    # Load existing scenarios
    existing_scenarios = []
    for scenario_data in scenarios_data:
        scenario = scenario_manager._create_scenario_from_dict(scenario_data)
        existing_scenarios.append(scenario)

    # Create custom scenario
    custom_scenario = create_custom_scenario()
    all_scenarios = existing_scenarios + [custom_scenario]

    print(f"\n🎭 Testing {len(all_scenarios)} scenarios:")
    for s in all_scenarios:
        print(f"   • {s.name} ({s.category})")

    # Run comprehensive comparison
    print("\n🚀 Running comprehensive simulation analysis...")

    results_collection = []

    # Baseline
    print("\n1️⃣ Baseline simulation...")
    baseline_model = ScenarioAwareTourismModel(
        personas_data=personas, hotspots_data=hotspots, 
        business_rules=business_rules, num_tourists=50, random_seed=123
    )
    baseline_results = baseline_model.run_simulation(steps=18)
    baseline_summary = baseline_model.get_summary_report()

    results_collection.append({
        'name': 'Baseline',
        'model_data': baseline_results,
        'summary': baseline_summary,
        'hotspot_stats': baseline_model.get_hotspot_statistics(),
        'persona_stats': baseline_model.get_persona_statistics()
    })

    print(f"✅ Baseline: {baseline_summary['final_metrics']['average_satisfaction']:.3f} satisfaction")

    # Test each scenario
    for i, scenario in enumerate(all_scenarios, 2):
        print(f"\n{i}️⃣ {scenario.name}...")

        model = ScenarioAwareTourismModel(
            scenario=scenario, personas_data=personas, hotspots_data=hotspots,
            business_rules=business_rules, num_tourists=50, random_seed=123
        )

        results = model.run_simulation(steps=18)
        summary = model.get_summary_report()

        results_collection.append({
            'name': scenario.name,
            'model_data': results,
            'summary': summary,
            'hotspot_stats': model.get_hotspot_statistics(),
            'persona_stats': model.get_persona_statistics(),
            'scenario': scenario
        })

        print(f"✅ {scenario.name}: {summary['final_metrics']['average_satisfaction']:.3f} satisfaction")

    # Perform detailed analysis
    print("\n📊 COMPREHENSIVE ANALYSIS")
    print("=" * 40)

    # 1. Performance comparison
    print("\n1. PERFORMANCE METRICS COMPARISON:")
    comparison_table = []

    for result in results_collection:
        metrics = result['summary']['final_metrics']
        comparison_table.append({
            'Scenario': result['name'],
            'Popularity': f"{metrics['average_popularity']:.3f}",
            'Visitors': metrics['total_visitors'],
            'Shares': metrics['social_shares'],
            'Satisfaction': f"{metrics['average_satisfaction']:.3f}"
        })

    df = pd.DataFrame(comparison_table)
    print(df.to_string(index=False))

    # 2. Individual analysis for each result
    print("\n2. DETAILED INDIVIDUAL ANALYSIS:")
    print("-" * 40)

    for result in results_collection[1:]:  # Skip baseline
        print(f"\n📋 {result['name'].upper()}:")

        analysis = analyze_simulation_results(
            result['model_data'],
            result['hotspot_stats'],
            result['persona_stats']
        )

        # Performance summary
        perf = analysis['performance_metrics']
        print(f"   Final Popularity: {perf['final_popularity']:.3f}")
        print(f"   Total Visitors: {perf['total_visitors']}")
        print(f"   Satisfaction Change: {perf['satisfaction_change']:+.3f}")

        # Top hotspot
        hotspot_analysis = analysis['hotspot_analysis']
        if 'top_performers' in hotspot_analysis and hotspot_analysis['top_performers']['most_popular']:
            top_hotspot = hotspot_analysis['top_performers']['most_popular']
            print(f"   Top Hotspot: {top_hotspot['name']} ({top_hotspot['popularity']:.3f})")

        # Best persona
        persona_analysis = analysis['persona_analysis'] 
        if 'persona_rankings' in persona_analysis and persona_analysis['persona_rankings']['highest_satisfaction']:
            best_persona = persona_analysis['persona_rankings']['highest_satisfaction']
            print(f"   Best Persona: {best_persona['persona']} ({best_persona['satisfaction']:.3f})")

    # 3. Scenario impact comparison
    print("\n3. SCENARIO IMPACT vs BASELINE:")
    print("-" * 40)

    baseline_metrics = results_collection[0]['summary']['final_metrics']

    impact_analysis = []
    for result in results_collection[1:]:
        scenario_metrics = result['summary']['final_metrics']

        satisfaction_impact = scenario_metrics['average_satisfaction'] - baseline_metrics['average_satisfaction']
        visitor_impact = scenario_metrics['total_visitors'] - baseline_metrics['total_visitors']
        popularity_impact = scenario_metrics['average_popularity'] - baseline_metrics['average_popularity']

        impact_analysis.append({
            'Scenario': result['name'],
            'Satisfaction_Impact': f"{satisfaction_impact:+.3f}",
            'Visitor_Impact': f"{visitor_impact:+d}",
            'Popularity_Impact': f"{popularity_impact:+.3f}",
            'Overall_Rating': 'Positive' if satisfaction_impact > 0 else 'Negative'
        })

    impact_df = pd.DataFrame(impact_analysis)
    print(impact_df.to_string(index=False))

    # 4. Policy recommendations
    print("\n4. EVIDENCE-BASED POLICY RECOMMENDATIONS:")
    print("-" * 50)

    # Find best performing scenario
    best_result = max(results_collection[1:], 
                     key=lambda x: x['summary']['final_metrics']['average_satisfaction'])

    best_satisfaction = best_result['summary']['final_metrics']['average_satisfaction']
    baseline_satisfaction = baseline_metrics['average_satisfaction']
    improvement = best_satisfaction - baseline_satisfaction

    print(f"\n🏆 BEST SCENARIO: {best_result['name']}")
    print(f"   Satisfaction: {best_satisfaction:.3f} (+{improvement:.3f} vs baseline)")
    print(f"   Improvement: {(improvement/baseline_satisfaction*100):+.1f}%")

    if 'scenario' in best_result:
        scenario = best_result['scenario']
        print(f"   Category: {scenario.category}")
        print(f"   Target Demographics: {', '.join(scenario.target_demographics)}")

        if hasattr(scenario, 'external_factors') and scenario.external_factors:
            print(f"   Key Factors: {', '.join(scenario.external_factors.keys())}")

    # Generate automated recommendations
    best_analysis = analyze_simulation_results(
        best_result['model_data'],
        best_result['hotspot_stats'], 
        best_result['persona_stats']
    )

    recommendations = best_analysis.get('recommendations', [])
    if recommendations:
        print(f"\n📝 AUTOMATED RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. [{rec['priority'].upper()}] {rec['recommendation']}")
            print(f"      → {rec['rationale']}")

    # 5. Save comprehensive results
    print("\n💾 SAVING RESULTS:")
    print("-" * 20)

    # Save comparison data
    df.to_csv('advanced_analysis_comparison.csv', index=False)
    impact_df.to_csv('scenario_impact_analysis.csv', index=False)

    # Save detailed analysis for best scenario
    with open('best_scenario_analysis.txt', 'w') as f:
        f.write(f"BEST SCENARIO ANALYSIS: {best_result['name']}\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Satisfaction Score: {best_satisfaction:.3f}\n")
        f.write(f"Improvement over Baseline: {improvement:.3f} ({(improvement/baseline_satisfaction*100):+.1f}%)\n\n")

        if recommendations:
            f.write("RECOMMENDATIONS:\n")
            for rec in recommendations:
                f.write(f"- [{rec['priority'].upper()}] {rec['recommendation']}\n")
                f.write(f"  Rationale: {rec['rationale']}\n\n")

    print("✅ advanced_analysis_comparison.csv")
    print("✅ scenario_impact_analysis.csv") 
    print("✅ best_scenario_analysis.txt")

    print("\n🎉 Advanced analysis completed successfully!")
    print(f"\n📊 KEY FINDING: '{best_result['name']}' scenario shows {(improvement/baseline_satisfaction*100):+.1f}% satisfaction improvement")


if __name__ == "__main__":
    run_advanced_analysis()
