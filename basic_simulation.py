#!/usr/bin/env python3
"""
Basic Tourism Simulation Example
===============================

This example demonstrates how to run a basic tourism simulation using
the LLM-enhanced tourism simulation system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from data_loader import load_data
from tourism_model import TourismModel
from results_storage import ResultsStorage
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
    print("\n🏗️ Creating tourism model...")
    model = TourismModel(
        personas_data=personas,
        hotspots_data=hotspots,
        business_rules=business_rules,
        num_tourists=30,  # Smaller number for example
        random_seed=42    # For reproducible results
    )

    print(f"✅ Model created with {len(model.tourists)} tourists and {len(model.hotspots)} hotspots")

    # Run simulation
    print("\n🎯 Running simulation for 15 steps...")
    results = model.run_simulation(steps=15)

    # Display results
    print("\n📊 SIMULATION RESULTS:")
    print("-" * 30)

    final_metrics = results.iloc[-1] if len(results) > 0 else {}
    print(f"Final Average Popularity: {final_metrics.get('Average_Popularity', 0):.3f}")
    print(f"Total Visitors: {int(final_metrics.get('Total_Visitors', 0))}")
    print(f"Social Shares: {int(final_metrics.get('Social_Shares', 0))}")
    print(f"Average Satisfaction: {final_metrics.get('Average_Satisfaction', 0):.3f}")

    # Hotspot performance
    print("\n🏛️ HOTSPOT PERFORMANCE:")
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

    # Initialize results storage
    storage = ResultsStorage()
    
    # Save comprehensive results
    print("💾 Saving results to timestamped directory...")
    saved_files = storage.save_simulation_results(
        model_data=results,
        agent_data=model.get_agent_data(),
        hotspot_stats=model.get_hotspot_statistics(),
        persona_stats=model.get_persona_statistics(),
        simulation_config={
            "num_tourists": model.num_tourists,
            "num_hotspots": len(model.hotspots),
            "grid_size": f"{model.grid.width}x{model.grid.height}",
            "random_seed": 42,
            "simulation_steps": 15
        }
    )
    
    # Create README for the output directory
    simulation_info = {
        "duration": "15 steps",
        "steps": 15,
        "num_tourists": model.num_tourists,
        "num_hotspots": len(model.hotspots)
    }
    readme_path = storage.create_readme(simulation_info)

    # Create summary report
    summary = model.get_summary_report()

    print("\n📋 SUMMARY REPORT:")
    print(f"- Simulation completed successfully after {summary['simulation_steps']} steps")
    print(f"- {summary['configuration']['num_tourists']} tourists visited {summary['configuration']['num_hotspots']} hotspots")
    print(f"- Grid size: {summary['configuration']['grid_size']}")

    print(f"\n✅ Basic simulation completed successfully!")
    print(f"📁 Results saved to: {storage.get_output_directory()}")
    print(f"📄 README created at: {readme_path}")
    print(f"🕐 Timestamp: {storage.get_timestamp()}")


if __name__ == "__main__":
    run_basic_simulation()
