#!/usr/bin/env python3
"""
Basic Tourism Simulation with Visualization
==========================================

This example demonstrates how to run a basic tourism simulation and
automatically generate visualizations of the results.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, TourismModel
from utils import ResultsStorage, add_visualization_to_existing_simulation
import pandas as pd


def run_basic_simulation_with_visualization():
    """Run a basic tourism simulation with automatic visualization."""

    print("🚀 LLM Tourism Simulation - Basic Example with Visualization")
    print("=" * 65)

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

    # Display basic results
    print("\n📊 SIMULATION RESULTS:")
    print("-" * 30)

    final_metrics = results.iloc[-1] if len(results) > 0 else {}
    print(f"Final Average Popularity: {final_metrics.get('Average_Popularity', 0):.3f}")
    print(f"Total Visitors: {int(final_metrics.get('Total_Visitors', 0))}")
    print(f"Social Shares: {int(final_metrics.get('Social_Shares', 0))}")
    print(f"Average Satisfaction: {final_metrics.get('Average_Satisfaction', 0):.3f}")

    # Get statistics for visualization
    hotspot_stats = model.get_hotspot_statistics()
    persona_stats = model.get_persona_statistics()

    # Initialize results storage
    storage = ResultsStorage()
    
    # Save comprehensive results with storage system
    print("\n💾 Saving results to timestamped directory...")
    saved_files = storage.save_simulation_results(
        model_data=results,
        agent_data=model.get_agent_data(),
        hotspot_stats=hotspot_stats,
        persona_stats=persona_stats,
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

    # ADD VISUALIZATION HERE
    print("\n🎨 Generating visualizations...")
    output_dir = storage.get_output_directory()
    visualization_files = add_visualization_to_existing_simulation(
        model_data=results,
        hotspot_stats=hotspot_stats,
        persona_stats=persona_stats,
        output_dir=f"{output_dir}/visualization"
    )

    # Display visualization results
    print("\n📈 VISUALIZATION OUTPUTS:")
    print("-" * 30)
    print(f"✅ Charts saved to: {output_dir}/visualization/charts/")
    print(f"✅ Data files saved to: {output_dir}/visualization/data/")
    print(f"✅ Summary report saved to: {output_dir}/visualization/reports/")
    
    print("\n📊 GENERATED CHARTS:")
    print("-" * 20)
    print("• popularity_evolution.png - Hotspot popularity over time")
    print("• satisfaction_by_persona.png - Tourist satisfaction by persona")
    print("• simulation_dashboard.png - Comprehensive time series dashboard")
    print("• Additional auto-generated charts")

    # Display summary
    print("\n📋 SUMMARY:")
    print("-" * 10)
    summary = model.get_summary_report()
    print(f"- Simulation completed successfully after {summary['simulation_steps']} steps")
    print(f"- {summary['configuration']['num_tourists']} tourists visited {summary['configuration']['num_hotspots']} hotspots")
    print(f"- Grid size: {summary['configuration']['grid_size']}")

    print(f"\n✅ Basic simulation with visualization completed successfully!")
    print(f"📁 Results saved to: {storage.get_output_directory()}")
    print(f"📄 README created at: {readme_path}")
    print(f"🎨 Visualizations saved to: {output_dir}/visualization/")
    print(f"🕐 Timestamp: {storage.get_timestamp()}")


def demonstrate_quick_visualization():
    """Demonstrate the quick visualization utilities."""
    
    print("\n⚡ QUICK VISUALIZATION DEMO:")
    print("=" * 35)
    
    print("You can also use the quick visualization utilities directly:")
    print("""
from utils import quick_visualize_simulation, quick_summary_report

# Quick visualization
chart_files = quick_visualize_simulation(
    model_data=results,
    hotspot_stats=hotspot_stats,
    persona_stats=persona_stats,
    output_dir="my_charts",
    show_plots=True  # Display charts interactively
)

# Quick summary report
summary_file = quick_summary_report(
    model_data=results,
    hotspot_stats=hotspot_stats,
    persona_stats=persona_stats,
    output_file="my_summary.txt"
)
    """)


if __name__ == "__main__":
    run_basic_simulation_with_visualization()
    demonstrate_quick_visualization()
