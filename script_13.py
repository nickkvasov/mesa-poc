# Create example scripts

# 1. Basic simulation example
basic_simulation_example = '''#!/usr/bin/env python3
"""
Basic Tourism Simulation Example
===============================

This example demonstrates how to run a basic tourism simulation using
the LLM-enhanced tourism simulation system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from llm_tourism_sim import load_data, TourismModel
import pandas as pd


def run_basic_simulation():
    """Run a basic tourism simulation with LLM-generated data."""
    
    print("🚀 LLM Tourism Simulation - Basic Example")
    print("=" * 50)
    
    # Load LLM-generated data
    print("📁 Loading LLM-generated configuration data...")
    try:
        personas, hotspots, business_rules, scenarios = load_data()
        print(f"✅ Loaded {len(personas)} personas, {len(hotspots)} hotspots")
        print(f"✅ Loaded business rules and {len(scenarios)} scenarios")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Create and configure model
    print("\\n🏗️ Creating tourism model...")
    model = TourismModel(
        personas_data=personas,
        hotspots_data=hotspots,
        business_rules=business_rules,
        num_tourists=30,  # Smaller number for example
        random_seed=42    # For reproducible results
    )
    
    print(f"✅ Model created with {len(model.tourists)} tourists and {len(model.hotspots)} hotspots")
    
    # Run simulation
    print("\\n🎯 Running simulation for 15 steps...")
    results = model.run_simulation(steps=15)
    
    # Display results
    print("\\n📊 SIMULATION RESULTS:")
    print("-" * 30)
    
    final_metrics = results.iloc[-1] if len(results) > 0 else {}
    print(f"Final Average Popularity: {final_metrics.get('Average_Popularity', 0):.3f}")
    print(f"Total Visitors: {int(final_metrics.get('Total_Visitors', 0))}")
    print(f"Social Shares: {int(final_metrics.get('Social_Shares', 0))}")
    print(f"Average Satisfaction: {final_metrics.get('Average_Satisfaction', 0):.3f}")
    
    # Hotspot performance
    print("\\n🏛️ HOTSPOT PERFORMANCE:")
    print("-" * 30)
    hotspot_stats = model.get_hotspot_statistics()
    
    # Sort by popularity
    sorted_hotspots = sorted(hotspot_stats, key=lambda x: x['current_popularity'], reverse=True)
    
    for i, hotspot in enumerate(sorted_hotspots[:5], 1):  # Top 5
        print(f"{i}. {hotspot['name']}")
        print(f"   Popularity: {hotspot['current_popularity']:.3f}")
        print(f"   Visitors: {hotspot['total_visitors']}")
        print(f"   Category: {hotspot['category']}")
        print()
    
    # Persona analysis
    print("👥 PERSONA ANALYSIS:")
    print("-" * 30)
    persona_stats = model.get_persona_statistics()
    
    for persona, stats in persona_stats.items():
        print(f"{persona}:")
        print(f"   Count: {stats['count']}")
        print(f"   Avg Satisfaction: {stats['avg_satisfaction']:.3f}")
        print(f"   Avg Visits: {stats['avg_visits']:.1f}")
        print()
    
    # Save results
    print("💾 Saving results...")
    results.to_csv('basic_simulation_results.csv', index=False)
    
    # Create summary report
    summary = model.get_summary_report()
    
    print("\\n📋 SUMMARY REPORT:")
    print(f"- Simulation completed successfully after {summary['simulation_steps']} steps")
    print(f"- {summary['configuration']['num_tourists']} tourists visited {summary['configuration']['num_hotspots']} hotspots")
    print(f"- Grid size: {summary['configuration']['grid_size']}")
    
    print("\\n✅ Basic simulation completed successfully!")
    print("📁 Results saved to basic_simulation_results.csv")


if __name__ == "__main__":
    run_basic_simulation()
'''

with open('examples/basic_simulation.py', 'w') as f:
    f.write(basic_simulation_example)

print("✅ basic_simulation.py created")