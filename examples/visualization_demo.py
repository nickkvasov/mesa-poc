#!/usr/bin/env python3
"""
Visualization Demo Example
==========================

This example demonstrates how to create various visualizations of
tourism simulation results using the built-in visualization utilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, TourismModel, ScenarioAwareTourismModel, TourismScenario, ScenarioManager
from utils import ResultsStorage, analyze_simulation_results
from utils.visualization import (
    create_popularity_chart,
    create_satisfaction_chart,
    create_scenario_comparison,
    create_hotspot_impact_heatmap,
    plot_hotspot_map,
    create_time_series_dashboard,
    save_all_charts
)
import pandas as pd
import matplotlib.pyplot as plt


def run_visualization_demo():
    """Run a demonstration of various visualization capabilities."""

    print("📊 LLM Tourism Simulation - Visualization Demo")
    print("=" * 55)

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

    # Create a simple scenario for comparison
    print("\n🎭 Creating test scenarios...")
    
    # Baseline scenario
    baseline_scenario = TourismScenario(
        name="Baseline",
        category="baseline",
        description="Standard tourism conditions",
        duration_steps=20,
        target_demographics=[]
    )

    # Marketing campaign scenario - more dramatic effects
    marketing_scenario = TourismScenario(
        name="Marketing Campaign",
        category="marketing",
        description="Aggressive marketing campaign targeting all demographics",
        duration_steps=20,
        target_demographics=["Cultural Explorer", "Budget Backpacker", "Adventure Seeker", "Luxury Traveler"]
    )

    # Add more dramatic marketing events
    marketing_scenario.add_event(
        step=3,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.5},  # Increased from 0.3
        description="Major marketing campaign significantly increases overall appeal",
        reasoning="Aggressive promotional activities raise awareness and interest dramatically"
    )

    marketing_scenario.add_event(
        step=8,
        event_type="appeal_boost",
        target="all",
        parameters={"appeal_boost": 0.3},  # Additional boost
        description="Follow-up marketing campaign maintains high appeal",
        reasoning="Sustained marketing efforts keep interest high"
    )

    # Add external factors for marketing
    marketing_scenario.add_external_factor("event_excitement", 0.4)  # Increased from 0.25
    marketing_scenario.add_external_factor("social_media_buzz", 0.3)  # Increased from 0.15

    # Cultural event scenario - more dramatic effects
    cultural_scenario = TourismScenario(
        name="Cultural Festival",
        category="cultural-event",
        description="Major cultural festival in the city center",
        duration_steps=20,
        target_demographics=["Cultural Explorer", "Budget Backpacker"]
    )

    # Add more dramatic cultural events
    cultural_scenario.add_event(
        step=5,
        event_type="appeal_boost",
        target="City Center",
        parameters={"appeal_boost": 0.8},  # Increased from 0.5
        description="Cultural festival dramatically boosts city center appeal",
        reasoning="Major festival creates massive cultural excitement and draws large crowds"
    )

    cultural_scenario.add_event(
        step=5,
        event_type="capacity_boost",
        target="City Center",
        parameters={"capacity_multiplier": 2.0},  # Increased from 1.4
        description="Festival infrastructure dramatically increases capacity",
        reasoning="Major festival utilizes extensive outdoor spaces and temporary facilities"
    )

    cultural_scenario.add_event(
        step=12,
        event_type="appeal_boost",
        target="Art Gallery District",
        parameters={"appeal_boost": 0.6},
        description="Festival spillover effects boost nearby cultural venues",
        reasoning="Festival attendees also visit nearby cultural attractions"
    )

    # Add external factors for cultural festival
    cultural_scenario.add_external_factor("artistic_excitement", 0.5)  # Increased from 0.25
    cultural_scenario.add_external_factor("social_media_buzz", 0.4)  # Increased from 0.15
    cultural_scenario.add_external_factor("cultural_curiosity", 0.6)  # Increased from 0.20

    # Run simulations
    print("\n🎯 Running simulations...")
    scenarios = [baseline_scenario, marketing_scenario, cultural_scenario]
    results_collection = []

    for scenario in scenarios:
        print(f"   Running {scenario.name}...")
        
        model = ScenarioAwareTourismModel(
            scenario=scenario,  # Pass scenario to constructor
            personas_data=personas,
            hotspots_data=hotspots,
            business_rules=business_rules,
            num_tourists=50,
            random_seed=42
        )

        # Run simulation
        model_data = model.run_simulation(steps=20)
        
        # Get statistics
        hotspot_stats = model.get_hotspot_statistics()
        persona_stats = model.get_persona_statistics()
        
        # Analyze results
        analysis = analyze_simulation_results(model_data, hotspot_stats, persona_stats)
        
        # Extract final metrics from performance_metrics
        final_metrics = {
            'avg_popularity': analysis['performance_metrics'].get('final_popularity', 0),
            'total_visitors': analysis['performance_metrics'].get('total_visitors', 0),
            'social_shares': analysis['performance_metrics'].get('total_social_shares', 0),
            'avg_satisfaction': analysis['performance_metrics'].get('final_satisfaction', 0)
        }
        
        results_collection.append({
            'name': scenario.name,
            'scenario': scenario,
            'model_data': model_data,
            'hotspot_stats': hotspot_stats,
            'persona_stats': persona_stats,
            'analysis': analysis,
            'summary': {
                'final_metrics': final_metrics
            }
        })

    # Initialize results storage
    storage = ResultsStorage()
    output_dir = storage.get_output_directory()
    charts_dir = f"{output_dir}/charts"

    print(f"\n📊 Generating visualizations in {charts_dir}...")

    # 1. Popularity Evolution Chart
    print("   1. Creating popularity evolution chart...")
    baseline_data = results_collection[0]['model_data']
    fig1 = create_popularity_chart(
        baseline_data,
        title="Tourism Hotspot Popularity Evolution (Baseline)",
        save_path=f"{charts_dir}/popularity_evolution.png"
    )
    plt.close(fig1)

    # 2. Satisfaction by Persona Chart
    print("   2. Creating satisfaction by persona chart...")
    baseline_persona_stats = results_collection[0]['persona_stats']
    fig2 = create_satisfaction_chart(
        baseline_persona_stats,
        title="Tourist Satisfaction by Persona (Baseline)",
        save_path=f"{charts_dir}/satisfaction_by_persona.png"
    )
    plt.close(fig2)

    # 3. Scenario Comparison Chart
    print("   3. Creating scenario comparison chart...")
    # Convert results to the format expected by create_scenario_comparison
    scenario_results_for_comparison = []
    for result in results_collection:
        scenario_results_for_comparison.append({
            'scenario_name': result['name'],
            'final_metrics': result['summary']['final_metrics']
        })
    
    fig3 = create_scenario_comparison(
        scenario_results_for_comparison,
        metrics=['avg_popularity', 'total_visitors', 'social_shares', 'avg_satisfaction'],
        title="Scenario Performance Comparison",
        save_path=f"{charts_dir}/scenario_comparison.png"
    )
    plt.close(fig3)

    # 4. Time Series Dashboard
    print("   4. Creating time series dashboard...")
    fig4 = create_time_series_dashboard(
        baseline_data,
        title="Tourism Simulation Dashboard (Baseline)",
        save_path=f"{charts_dir}/simulation_dashboard.png"
    )
    plt.close(fig4)

    # 5. Hotspot Map (if location data is available)
    print("   5. Creating hotspot map...")
    try:
        # Create popularity data for hotspots
        popularity_data = {}
        for hotspot in results_collection[0]['hotspot_stats']:
            popularity_data[hotspot['name']] = hotspot['current_popularity']

        # Add mock location data if not present
        hotspots_with_location = []
        for hotspot in hotspots:
            hotspot_dict = hotspot.copy()
            if 'location' not in hotspot_dict:
                # Add mock coordinates for demonstration
                hotspot_dict['location'] = {
                    'x': len(hotspots_with_location) * 10,
                    'y': len(hotspots_with_location) * 8
                }
            hotspots_with_location.append(hotspot_dict)

        fig5 = plot_hotspot_map(
            hotspots_with_location,
            popularity_data=popularity_data,
            title="Tourism Hotspots Map with Popularity",
            save_path=f"{charts_dir}/hotspot_map.png"
        )
        plt.close(fig5)
    except Exception as e:
        print(f"   ⚠️  Could not create hotspot map: {e}")

    # 6. Hotspot Impact Heatmap
    print("   6. Creating hotspot impact heatmap...")
    try:
        # Create impact data for heatmap
        impact_data = []
        baseline_popularity = {h['name']: h['current_popularity'] for h in results_collection[0]['hotspot_stats']}
        
        for result in results_collection[1:]:  # Skip baseline
            scenario_name = result['name']
            scenario_popularity = {h['name']: h['current_popularity'] for h in result['hotspot_stats']}
            
            for hotspot_name in baseline_popularity.keys():
                if hotspot_name in scenario_popularity:
                    baseline = baseline_popularity[hotspot_name]
                    scenario = scenario_popularity[hotspot_name]
                    percent_change = ((scenario - baseline) / baseline * 100) if baseline > 0 else 0
                    
                    impact_data.append({
                        'Hotspot': hotspot_name,
                        'Scenario': scenario_name,
                        'Percent_Change': percent_change
                    })

        if impact_data:
            impact_df = pd.DataFrame(impact_data)
            fig6 = create_hotspot_impact_heatmap(
                impact_df,
                title="Hotspot Impact by Scenario (%)",
                save_path=f"{charts_dir}/hotspot_impact_heatmap.png"
            )
            plt.close(fig6)
    except Exception as e:
        print(f"   ⚠️  Could not create impact heatmap: {e}")

    # 7. Save all charts automatically
    print("   7. Saving all charts automatically...")
    try:
        save_all_charts(results_collection[0], charts_dir)
    except Exception as e:
        print(f"   ⚠️  Error in automatic chart saving: {e}")

    # 8. Create comparison analysis
    print("   8. Creating comparison analysis...")
    
    comparison_data = []
    for result in results_collection:
        metrics = result['summary']['final_metrics']
        comparison_data.append({
            'Scenario': result['name'],
            'Avg_Popularity': metrics.get('avg_popularity', 0),
            'Total_Visitors': metrics.get('total_visitors', 0),
            'Social_Shares': metrics.get('social_shares', 0),
            'Avg_Satisfaction': metrics.get('avg_satisfaction', 0)
        })

    comparison_df = pd.DataFrame(comparison_data)
    comparison_df.to_csv(f"{output_dir}/data/scenario_comparison.csv", index=False)

    # Display results summary
    print("\n📈 VISUALIZATION RESULTS:")
    print("-" * 40)
    print(f"✅ Generated {len(comparison_data)} scenario visualizations")
    print(f"✅ Saved charts to: {charts_dir}/")
    print(f"✅ Saved comparison data to: {output_dir}/data/scenario_comparison.csv")
    
    print("\n📊 CHART SUMMARY:")
    print("-" * 20)
    print("1. popularity_evolution.png - Hotspot popularity over time")
    print("2. satisfaction_by_persona.png - Tourist satisfaction by persona")
    print("3. scenario_comparison.png - Performance comparison across scenarios")
    print("4. simulation_dashboard.png - Comprehensive time series dashboard")
    print("5. hotspot_map.png - Geographic hotspot visualization")
    print("6. hotspot_impact_heatmap.png - Scenario impact on hotspots")
    print("7. Additional auto-generated charts")

    print("\n🎯 SCENARIO PERFORMANCE SUMMARY:")
    print("-" * 40)
    for row in comparison_data:
        print(f"{row['Scenario']}:")
        print(f"   Popularity: {row['Avg_Popularity']:.3f}")
        print(f"   Visitors: {row['Total_Visitors']}")
        print(f"   Satisfaction: {row['Avg_Satisfaction']:.3f}")
        print()

    print("🎉 Visualization demo completed successfully!")
    print(f"📁 All outputs saved to: {output_dir}")
    print(f"🕐 Timestamp: {storage.get_timestamp()}")


def demonstrate_interactive_visualization():
    """Demonstrate how to create interactive visualizations."""
    
    print("\n🖱️ INTERACTIVE VISUALIZATION DEMO:")
    print("=" * 40)
    
    print("To create interactive visualizations, you can use Plotly:")
    print("(Plotly is already included in requirements.txt)")
    
    print("\nExample code for interactive charts:")
    print("""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Interactive line chart
fig = px.line(model_data, x=model_data.index, y='Average_Popularity',
              title='Interactive Popularity Evolution')
fig.show()

# Interactive scatter plot
fig = px.scatter(hotspot_data, x='x_coord', y='y_coord', 
                size='popularity', color='category',
                title='Interactive Hotspot Map')
fig.show()

# Interactive dashboard
fig = make_subplots(rows=2, cols=2, subplot_titles=('Popularity', 'Visitors', 'Satisfaction', 'Shares'))
# Add traces...
fig.show()
    """)


if __name__ == "__main__":
    run_visualization_demo()
    demonstrate_interactive_visualization()
