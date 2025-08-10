# 2. Scenario comparison example
scenario_comparison_example = '''#!/usr/bin/env python3
"""
Scenario Comparison Example
===========================

This example demonstrates how to run multiple what-if scenarios and
compare their impacts on tourism dynamics.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from llm_tourism_sim import load_data, ScenarioAwareTourismModel
from llm_tourism_sim.scenarios.scenario_manager import ScenarioManager
import pandas as pd


def run_scenario_comparison():
    """Run multiple scenarios and compare their results."""
    
    print("🎭 LLM Tourism Simulation - Scenario Comparison")
    print("=" * 55)
    
    # Load data
    print("📁 Loading configuration data...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Loaded {len(personas)} personas, {len(hotspots)} hotspots, {len(scenarios_data)} scenarios")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Initialize scenario manager
    scenario_manager = ScenarioManager()
    
    # Load scenarios from data
    scenarios = []
    for scenario_data in scenarios_data:
        scenario = scenario_manager._create_scenario_from_dict(scenario_data)
        scenarios.append(scenario)
        scenario_manager.scenarios[scenario.name] = scenario
    
    print(f"✅ Loaded scenarios: {[s.name for s in scenarios]}")
    
    # Run baseline simulation
    print("\\n🏁 Running BASELINE simulation...")
    baseline_model = ScenarioAwareTourismModel(
        scenario=None,  # No scenario = baseline
        personas_data=personas,
        hotspots_data=hotspots,
        business_rules=business_rules,
        num_tourists=40,
        random_seed=42
    )
    
    baseline_results = baseline_model.run_simulation(steps=15)
    baseline_summary = baseline_model.get_summary_report()
    
    print(f"✅ Baseline completed:")
    final_metrics = baseline_summary['final_metrics']
    print(f"   Popularity: {final_metrics['average_popularity']:.3f}")
    print(f"   Visitors: {final_metrics['total_visitors']}")
    print(f"   Satisfaction: {final_metrics['average_satisfaction']:.3f}")
    
    # Run scenario simulations
    scenario_results = []
    
    for scenario in scenarios:
        print(f"\\n🎬 Running scenario: {scenario.name}")
        print(f"   Description: {scenario.description}")
        
        model = ScenarioAwareTourismModel(
            scenario=scenario,
            personas_data=personas,
            hotspots_data=hotspots,
            business_rules=business_rules,
            num_tourists=40,
            random_seed=42  # Same seed for fair comparison
        )
        
        results = model.run_simulation(steps=15)
        summary = model.get_summary_report()
        
        # Store results
        result_data = {
            'scenario_name': scenario.name,
            'model': model,
            'results': results,
            'summary': summary,
            'final_metrics': summary['final_metrics']
        }
        scenario_results.append(result_data)
        
        print(f"✅ {scenario.name} completed:")
        final_metrics = summary['final_metrics']
        print(f"   Popularity: {final_metrics['average_popularity']:.3f}")
        print(f"   Visitors: {final_metrics['total_visitors']}")  
        print(f"   Satisfaction: {final_metrics['average_satisfaction']:.3f}")
    
    # Compare results
    print("\\n📊 SCENARIO COMPARISON ANALYSIS:")
    print("=" * 55)
    
    # Create comparison table
    comparison_data = []
    
    # Add baseline
    baseline_metrics = baseline_summary['final_metrics']
    comparison_data.append({
        'Scenario': 'Baseline',
        'Popularity': baseline_metrics['average_popularity'],
        'Visitors': baseline_metrics['total_visitors'],
        'Social_Shares': baseline_metrics['social_shares'],
        'Satisfaction': baseline_metrics['average_satisfaction']
    })
    
    # Add scenarios
    for result in scenario_results:
        metrics = result['final_metrics']
        comparison_data.append({
            'Scenario': result['scenario_name'],
            'Popularity': metrics['average_popularity'],
            'Visitors': metrics['total_visitors'],
            'Social_Shares': metrics['social_shares'],
            'Satisfaction': metrics['average_satisfaction']
        })
    
    # Create DataFrame for easy comparison
    comparison_df = pd.DataFrame(comparison_data)
    
    print("\\n📋 PERFORMANCE COMPARISON TABLE:")
    print(comparison_df.to_string(index=False, float_format='%.3f'))
    
    # Calculate impacts vs baseline
    print("\\n📈 IMPACT vs BASELINE:")
    print("-" * 40)
    
    baseline_metrics = baseline_summary['final_metrics']
    
    for result in scenario_results:
        scenario_metrics = result['final_metrics']
        scenario_name = result['scenario_name']
        
        print(f"\\n{scenario_name}:")
        
        # Calculate changes
        for metric in ['average_popularity', 'total_visitors', 'social_shares', 'average_satisfaction']:
            baseline_val = baseline_metrics.get(metric, 0)
            scenario_val = scenario_metrics.get(metric, 0)
            
            if baseline_val != 0:
                change = scenario_val - baseline_val
                percent_change = (change / baseline_val) * 100
                print(f"  {metric.replace('_', ' ').title()}: {change:+.3f} ({percent_change:+.1f}%)")
            else:
                print(f"  {metric.replace('_', ' ').title()}: {scenario_val:.3f} (new)")
    
    # Find best and worst scenarios
    print("\\n🏆 SCENARIO RANKINGS:")
    print("-" * 30)
    
    # Rank by satisfaction (primary metric)
    sorted_by_satisfaction = sorted(scenario_results, 
                                  key=lambda x: x['final_metrics']['average_satisfaction'], 
                                  reverse=True)
    
    print("By Satisfaction:")
    for i, result in enumerate(sorted_by_satisfaction, 1):
        satisfaction = result['final_metrics']['average_satisfaction']
        print(f"  {i}. {result['scenario_name']}: {satisfaction:.3f}")
    
    # Save results
    print("\\n💾 Saving comparison results...")
    comparison_df.to_csv('scenario_comparison_results.csv', index=False)
    
    # Generate insights
    print("\\n🔍 KEY INSIGHTS:")
    print("-" * 20)
    
    best_scenario = sorted_by_satisfaction[0]
    worst_scenario = sorted_by_satisfaction[-1]
    
    print(f"• Best performing scenario: {best_scenario['scenario_name']}")
    print(f"  → Achieved {best_scenario['final_metrics']['average_satisfaction']:.3f} satisfaction")
    
    print(f"• Lowest performing scenario: {worst_scenario['scenario_name']}")  
    print(f"  → Achieved {worst_scenario['final_metrics']['average_satisfaction']:.3f} satisfaction")
    
    # Policy recommendations
    print(f"\\n📝 POLICY RECOMMENDATIONS:")
    print("-" * 35)
    
    if best_scenario['final_metrics']['average_satisfaction'] > baseline_metrics['average_satisfaction']:
        print(f"✅ Recommend implementing elements from '{best_scenario['scenario_name']}'")
        print(f"   Expected satisfaction improvement: {((best_scenario['final_metrics']['average_satisfaction'] - baseline_metrics['average_satisfaction']) / baseline_metrics['average_satisfaction'] * 100):+.1f}%")
    
    if worst_scenario['final_metrics']['average_satisfaction'] < baseline_metrics['average_satisfaction']:
        print(f"⚠️  Avoid conditions similar to '{worst_scenario['scenario_name']}'")
        print(f"   Could reduce satisfaction by {((baseline_metrics['average_satisfaction'] - worst_scenario['final_metrics']['average_satisfaction']) / baseline_metrics['average_satisfaction'] * 100):.1f}%")
    
    print("\\n✅ Scenario comparison completed successfully!")
    print("📁 Results saved to scenario_comparison_results.csv")


if __name__ == "__main__":
    run_scenario_comparison()
'''

with open('examples/scenario_comparison.py', 'w') as f:
    f.write(scenario_comparison_example)

print("✅ scenario_comparison.py created")