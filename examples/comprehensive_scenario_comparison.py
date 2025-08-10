#!/usr/bin/env python3
"""
Comprehensive Scenario Comparison Example
========================================

This example demonstrates how to create and compare multiple distinctive
scenarios with clearly different effects on tourism dynamics.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, ScenarioAwareTourismModel, TourismScenario
from utils import quick_compare_scenarios, add_visualization_to_existing_simulation
import pandas as pd


def create_distinctive_scenarios():
    """Create multiple distinctive scenarios with clear, different effects."""
    
    scenarios = []
    
    # 1. BASELINE - No intervention
    baseline = TourismScenario(
        name="Baseline",
        category="baseline",
        description="Standard tourism conditions without any interventions",
        duration_steps=20,
        target_demographics=[]
    )
    scenarios.append(baseline)
    
    # 2. AGGRESSIVE MARKETING - High positive impact
    aggressive_marketing = TourismScenario(
        name="Aggressive Marketing",
        category="marketing",
        description="Massive marketing campaign targeting all demographics",
        duration_steps=20,
        target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker", "Luxury Traveler"]
    )
    
    # Multiple marketing events
    aggressive_marketing.add_event(
        step=3,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.7},
        description="Major marketing campaign launch",
        reasoning="Aggressive promotional activities raise awareness dramatically"
    )
    
    aggressive_marketing.add_event(
        step=8,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.5},
        description="Follow-up marketing campaign",
        reasoning="Sustained marketing efforts maintain high interest"
    )
    
    aggressive_marketing.add_event(
        step=15,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.3},
        description="Final marketing push",
        reasoning="Final promotional activities before campaign end"
    )
    
    # External factors
    aggressive_marketing.add_external_factor("event_excitement", 0.6)
    aggressive_marketing.add_external_factor("social_media_buzz", 0.5)
    aggressive_marketing.add_external_factor("cultural_curiosity", 0.4)
    
    scenarios.append(aggressive_marketing)
    
    # 3. MAJOR FESTIVAL - Event-driven positive impact
    major_festival = TourismScenario(
        name="Major Festival",
        category="cultural-event",
        description="Major cultural festival with extensive programming",
        duration_steps=20,
        target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker"]
    )
    
    # Festival events
    major_festival.add_event(
        step=5,
        event_type="appeal_boost",
        target="City Center",
        parameters={"appeal_boost": 0.9},
        description="Festival opening ceremony",
        reasoning="Major festival creates massive cultural excitement"
    )
    
    major_festival.add_event(
        step=5,
        event_type="capacity_boost",
        target="City Center",
        parameters={"capacity_multiplier": 2.5},
        description="Festival infrastructure deployment",
        reasoning="Extensive outdoor spaces and temporary facilities"
    )
    
    major_festival.add_event(
        step=10,
        event_type="appeal_boost",
        target="Art Gallery District",
        parameters={"appeal_boost": 0.6},
        description="Festival spillover effects",
        reasoning="Festival attendees visit nearby cultural venues"
    )
    
    major_festival.add_event(
        step=15,
        event_type="appeal_reset",
        target="City Center",
        parameters={},
        description="Festival ends",
        reasoning="Festival concludes, appeal returns to baseline"
    )
    
    # External factors
    major_festival.add_external_factor("artistic_excitement", 0.8)
    major_festival.add_external_factor("social_media_buzz", 0.7)
    major_festival.add_external_factor("cultural_curiosity", 0.6)
    
    scenarios.append(major_festival)
    
    # 4. CONSTRUCTION DISRUPTION - Negative impact
    construction_disruption = TourismScenario(
        name="Construction Disruption",
        category="infrastructure",
        description="Major construction project causing significant disruption",
        duration_steps=20,
        target_demographics=[]
    )
    
    # Construction events
    construction_disruption.add_event(
        step=3,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": -0.5},
        description="Construction begins",
        reasoning="Major construction work reduces overall appeal"
    )
    
    construction_disruption.add_event(
        step=8,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": -0.4},
        description="Ongoing construction disruption",
        reasoning="Continued construction work maintains negative impact"
    )
    
    construction_disruption.add_event(
        step=15,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": -0.2},
        description="Construction winding down",
        reasoning="Construction work is completing, impact lessening"
    )
    
    # External factors
    construction_disruption.add_external_factor("inconvenience_tolerance", -0.6)
    construction_disruption.add_external_factor("noise_tolerance", -0.5)
    construction_disruption.add_external_factor("event_excitement", -0.3)
    
    scenarios.append(construction_disruption)
    
    # 5. LUXURY TAX - Policy intervention
    luxury_tax = TourismScenario(
        name="Luxury Tax",
        category="policy",
        description="15% luxury tax on high-end tourism services",
        duration_steps=20,
        target_demographics=["Luxury Traveler"]
    )
    
    # Tax events
    luxury_tax.add_event(
        step=5,
        event_type="appeal_boost",
        target="Luxury Hotel District",
        parameters={"appeal_boost": -0.4},
        description="Luxury tax implementation",
        reasoning="Tax reduces appeal of luxury services"
    )
    
    luxury_tax.add_event(
        step=5,
        event_type="appeal_boost",
        target="Fine Dining District",
        parameters={"appeal_boost": -0.3},
        description="Luxury tax on dining",
        reasoning="Tax affects high-end dining establishments"
    )
    
    luxury_tax.add_event(
        step=10,
        event_type="appeal_boost",
        target="Budget Accommodation",
        parameters={"appeal_boost": 0.2},
        description="Shift to budget options",
        reasoning="Some tourists shift to more affordable options"
    )
    
    # External factors
    luxury_tax.add_external_factor("cost_sensitivity", 0.4)
    luxury_tax.add_external_factor("event_excitement", -0.2)
    
    scenarios.append(luxury_tax)
    
    # 6. SUSTAINABLE TOURISM INITIATIVE - Mixed impact
    sustainable_initiative = TourismScenario(
        name="Sustainable Tourism",
        category="policy",
        description="Sustainable tourism initiative with eco-friendly focus",
        duration_steps=20,
        target_demographics=["Adventure Seeker", "Cultural Explorer"]
    )
    
    # Sustainable events
    sustainable_initiative.add_event(
        step=4,
        event_type="appeal_boost",
        target="Nature Reserve",
        parameters={"appeal_boost": 0.6},
        description="Eco-tourism promotion",
        reasoning="Sustainable practices attract eco-conscious tourists"
    )
    
    sustainable_initiative.add_event(
        step=4,
        event_type="capacity_boost",
        target="Nature Reserve",
        parameters={"capacity_multiplier": 1.8},
        description="Eco-infrastructure development",
        reasoning="Sustainable infrastructure increases capacity"
    )
    
    sustainable_initiative.add_event(
        step=8,
        event_type="appeal_boost",
        target="Local Markets",
        parameters={"appeal_boost": 0.4},
        description="Local business promotion",
        reasoning="Support for local, sustainable businesses"
    )
    
    sustainable_initiative.add_event(
        step=12,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.2},
        description="Overall sustainability appeal",
        reasoning="General appeal of sustainable tourism practices"
    )
    
    # External factors
    sustainable_initiative.add_external_factor("cultural_curiosity", 0.5)
    sustainable_initiative.add_external_factor("event_excitement", 0.3)
    sustainable_initiative.add_external_factor("social_media_buzz", 0.4)
    
    scenarios.append(sustainable_initiative)
    
    return scenarios


def run_comprehensive_comparison():
    """Run comprehensive comparison of multiple distinctive scenarios."""
    
    print("🎭 Comprehensive Scenario Comparison")
    print("=" * 50)
    
    # Load data
    print("📁 Loading configuration...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Create distinctive scenarios
    print("\n🎭 Creating distinctive scenarios...")
    scenarios = create_distinctive_scenarios()
    
    print(f"✅ Created {len(scenarios)} distinctive scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"   {i}. {scenario.name} ({scenario.category})")
        print(f"      {scenario.description}")
    
    # Run simulations
    print(f"\n🎯 Running simulations for {len(scenarios)} scenarios...")
    results_collection = []
    
    for scenario in scenarios:
        print(f"   Running {scenario.name}...")
        
        model = ScenarioAwareTourismModel(
            scenario=scenario,
            personas_data=personas,
            hotspots_data=hotspots,
            business_rules=business_rules,
            num_tourists=50,
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
    
    # Display results summary
    print("\n📊 SCENARIO PERFORMANCE SUMMARY:")
    print("-" * 50)
    
    baseline_metrics = results_collection[0]['summary']['final_metrics']
    
    for result in results_collection:
        metrics = result['summary']['final_metrics']
        popularity_diff = metrics['avg_popularity'] - baseline_metrics['avg_popularity']
        satisfaction_diff = metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
        
        print(f"{result['name']}:")
        print(f"   Popularity: {metrics['avg_popularity']:.3f} ({popularity_diff:+.3f})")
        print(f"   Satisfaction: {metrics['avg_satisfaction']:.3f} ({satisfaction_diff:+.3f})")
        print(f"   Visitors: {metrics['total_visitors']}")
        print(f"   Social Shares: {metrics['social_shares']}")
        print()
    
    # Generate comprehensive visualizations
    print("📊 Generating comprehensive visualizations...")
    
    # Create timestamped output directory
    from utils import ResultsStorage
    storage = ResultsStorage()
    output_dir = storage.get_output_directory()
    scenario_comparison_dir = f"{output_dir}/scenario_comparison"
    
    # 1. Scenario comparison chart
    comparison_files = quick_compare_scenarios(
        results_collection,
        output_dir=scenario_comparison_dir,
        show_plots=False
    )
    
    # 2. Individual scenario visualizations
    for i, result in enumerate(results_collection):
        scenario_name = result['name'].replace(' ', '_').lower()
        output_dir = f"{scenario_comparison_dir}/{scenario_name}"
        
        print(f"   Generating visualizations for {result['name']}...")
        visualization_files = add_visualization_to_existing_simulation(
            model_data=result['model_data'],
            hotspot_stats=result['hotspot_stats'],
            persona_stats=result['persona_stats'],
            output_dir=output_dir
        )
    
    # 3. Create summary analysis
    print("\n📈 CREATING SUMMARY ANALYSIS...")
    create_summary_analysis(results_collection, scenario_comparison_dir)
    
    print(f"\n✅ Comprehensive scenario comparison completed!")
    print(f"📁 Results saved to: {output_dir}")
    print(f"📊 Scenario comparison saved to: {scenario_comparison_dir}")
    print(f"📊 Generated comparison files:")
    for file_type, file_path in comparison_files.items():
        print(f"   • {file_type}: {file_path}")
    
    print(f"\n🎯 SCENARIO INSIGHTS:")
    print("-" * 30)
    
    # Find best and worst performers
    sorted_by_satisfaction = sorted(results_collection[1:], 
                                  key=lambda x: x['summary']['final_metrics']['avg_satisfaction'], 
                                  reverse=True)
    
    best_scenario = sorted_by_satisfaction[0]
    worst_scenario = sorted_by_satisfaction[-1]
    
    print(f"🏆 Best Performer: {best_scenario['name']}")
    print(f"   Satisfaction: {best_scenario['summary']['final_metrics']['avg_satisfaction']:.3f}")
    print(f"   Popularity: {best_scenario['summary']['final_metrics']['avg_popularity']:.3f}")
    
    print(f"⚠️  Worst Performer: {worst_scenario['name']}")
    print(f"   Satisfaction: {worst_scenario['summary']['final_metrics']['avg_satisfaction']:.3f}")
    print(f"   Popularity: {worst_scenario['summary']['final_metrics']['avg_popularity']:.3f}")
    
    print(f"\n🎉 Analysis completed successfully!")


def create_summary_analysis(results_collection, output_dir):
    """Create a comprehensive summary analysis of all scenarios."""
    
    baseline_metrics = results_collection[0]['summary']['final_metrics']
    
    # Create detailed comparison table
    comparison_data = []
    for result in results_collection:
        metrics = result['summary']['final_metrics']
        popularity_diff = metrics['avg_popularity'] - baseline_metrics['avg_popularity']
        satisfaction_diff = metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
        
        comparison_data.append({
            'Scenario': result['name'],
            'Category': result['scenario'].category,
            'Popularity': metrics['avg_popularity'],
            'Popularity_Change': popularity_diff,
            'Popularity_Change_Pct': (popularity_diff / baseline_metrics['avg_popularity'] * 100) if baseline_metrics['avg_popularity'] > 0 else 0,
            'Satisfaction': metrics['avg_satisfaction'],
            'Satisfaction_Change': satisfaction_diff,
            'Satisfaction_Change_Pct': (satisfaction_diff / baseline_metrics['avg_satisfaction'] * 100) if baseline_metrics['avg_satisfaction'] > 0 else 0,
            'Visitors': metrics['total_visitors'],
            'Social_Shares': metrics['social_shares']
        })
    
    # Save detailed comparison
    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv(f"{output_dir}/detailed_comparison.csv", index=False)
    
    # Create summary report
    with open(f"{output_dir}/scenario_analysis_report.txt", 'w') as f:
        f.write("COMPREHENSIVE SCENARIO ANALYSIS REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("EXECUTIVE SUMMARY:\n")
        f.write("-" * 20 + "\n")
        f.write(f"• Total scenarios analyzed: {len(results_collection)}\n")
        f.write(f"• Baseline popularity: {baseline_metrics['avg_popularity']:.3f}\n")
        f.write(f"• Baseline satisfaction: {baseline_metrics['avg_satisfaction']:.3f}\n\n")
        
        # Top performers
        sorted_by_satisfaction = sorted(results_collection[1:], 
                                      key=lambda x: x['summary']['final_metrics']['avg_satisfaction'], 
                                      reverse=True)
        
        f.write("TOP PERFORMERS BY SATISFACTION:\n")
        f.write("-" * 35 + "\n")
        for i, result in enumerate(sorted_by_satisfaction[:3], 1):
            metrics = result['summary']['final_metrics']
            satisfaction_diff = metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
            f.write(f"{i}. {result['name']}\n")
            f.write(f"   Satisfaction: {metrics['avg_satisfaction']:.3f} ({satisfaction_diff:+.3f})\n")
            f.write(f"   Category: {result['scenario'].category}\n\n")
        
        # Impact analysis
        f.write("IMPACT ANALYSIS:\n")
        f.write("-" * 15 + "\n")
        for result in results_collection[1:]:
            metrics = result['summary']['final_metrics']
            popularity_diff = metrics['avg_popularity'] - baseline_metrics['avg_popularity']
            satisfaction_diff = metrics['avg_satisfaction'] - baseline_metrics['avg_satisfaction']
            
            f.write(f"{result['name']}:\n")
            f.write(f"   Popularity Impact: {popularity_diff:+.1%}\n")
            f.write(f"   Satisfaction Impact: {satisfaction_diff:+.1%}\n")
            f.write(f"   Overall Rating: {'Positive' if satisfaction_diff > 0 else 'Negative'}\n\n")
        
        f.write("RECOMMENDATIONS:\n")
        f.write("-" * 15 + "\n")
        best_scenario = sorted_by_satisfaction[0]
        f.write(f"• Best performing scenario: {best_scenario['name']}\n")
        f.write(f"• Recommended for implementation based on satisfaction gains\n")
        f.write(f"• Consider combining elements from top performers\n")
        f.write(f"• Monitor long-term effects of chosen interventions\n")


if __name__ == "__main__":
    run_comprehensive_comparison()
