#!/usr/bin/env python3
"""
Interactive Visualization Example
================================

This example demonstrates how to create interactive visualizations
using Plotly for enhanced user experience and exploration of
tourism simulation results.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from sim import load_data, TourismModel, ScenarioAwareTourismModel, TourismScenario
from utils import ResultsStorage, analyze_simulation_results
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo


def create_interactive_popularity_chart(model_data: pd.DataFrame, title: str = "Interactive Popularity Evolution"):
    """Create an interactive line chart showing popularity evolution."""
    
    fig = px.line(model_data, x=model_data.index, y='Average_Popularity',
                  title=title,
                  labels={'index': 'Simulation Step', 'Average_Popularity': 'Average Popularity'},
                  template='plotly_white')
    
    fig.update_layout(
        hovermode='x unified',
        xaxis_title="Simulation Step",
        yaxis_title="Average Popularity",
        showlegend=True
    )
    
    return fig


def create_interactive_hotspot_map(hotspots_data: list, popularity_data: dict = None, 
                                 title: str = "Interactive Hotspot Map"):
    """Create an interactive scatter plot map of hotspots."""
    
    # Prepare data
    map_data = []
    for hotspot in hotspots_data:
        location = hotspot.get('location', {})
        hotspot_name = hotspot.get('name', 'Unknown')
        
        data_point = {
            'name': hotspot_name,
            'x': location.get('x', 0),
            'y': location.get('y', 0),
            'category': hotspot.get('category', 'unknown'),
            'popularity': popularity_data.get(hotspot_name, 0.5) if popularity_data else 0.5
        }
        map_data.append(data_point)
    
    df = pd.DataFrame(map_data)
    
    fig = px.scatter(df, x='x', y='y', 
                    size='popularity',
                    color='category',
                    hover_name='name',
                    hover_data=['popularity'],
                    title=title,
                    template='plotly_white',
                    size_max=30)
    
    fig.update_layout(
        xaxis_title="X Coordinate",
        yaxis_title="Y Coordinate",
        showlegend=True
    )
    
    return fig


def create_interactive_dashboard(model_data: pd.DataFrame, title: str = "Interactive Simulation Dashboard"):
    """Create an interactive dashboard with multiple charts."""
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Popularity Evolution', 'Visitor Count', 'Social Shares', 'Satisfaction'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Add traces
    if 'Average_Popularity' in model_data.columns:
        fig.add_trace(
            go.Scatter(x=model_data.index, y=model_data['Average_Popularity'],
                      mode='lines+markers', name='Popularity',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )
    
    if 'Total_Visitors' in model_data.columns:
        fig.add_trace(
            go.Scatter(x=model_data.index, y=model_data['Total_Visitors'],
                      mode='lines+markers', name='Visitors',
                      line=dict(color='green', width=2)),
            row=1, col=2
        )
    
    if 'Social_Shares' in model_data.columns:
        fig.add_trace(
            go.Scatter(x=model_data.index, y=model_data['Social_Shares'],
                      mode='lines+markers', name='Social Shares',
                      line=dict(color='orange', width=2)),
            row=2, col=1
        )
    
    if 'Average_Satisfaction' in model_data.columns:
        fig.add_trace(
            go.Scatter(x=model_data.index, y=model_data['Average_Satisfaction'],
                      mode='lines+markers', name='Satisfaction',
                      line=dict(color='red', width=2)),
            row=2, col=2
        )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    return fig


def create_interactive_scenario_comparison(scenario_results: list, 
                                         title: str = "Interactive Scenario Comparison"):
    """Create an interactive comparison chart for multiple scenarios."""
    
    # Prepare data
    comparison_data = []
    for result in scenario_results:
        metrics = result.get('summary', {}).get('final_metrics', {})
        comparison_data.append({
            'Scenario': result.get('name', 'Unknown'),
            'Popularity': metrics.get('avg_popularity', 0),
            'Visitors': metrics.get('total_visitors', 0),
            'Social_Shares': metrics.get('social_shares', 0),
            'Satisfaction': metrics.get('avg_satisfaction', 0)
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Create subplots for different metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Average Popularity', 'Total Visitors', 'Social Shares', 'Average Satisfaction'),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Add bar charts
    fig.add_trace(
        go.Bar(x=df['Scenario'], y=df['Popularity'], name='Popularity',
               marker_color='lightblue'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=df['Scenario'], y=df['Visitors'], name='Visitors',
               marker_color='lightgreen'),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Bar(x=df['Scenario'], y=df['Social_Shares'], name='Social Shares',
               marker_color='lightcoral'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Bar(x=df['Scenario'], y=df['Satisfaction'], name='Satisfaction',
               marker_color='lightyellow'),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title=title,
        template='plotly_white',
        height=600,
        showlegend=False
    )
    
    return fig


def create_interactive_heatmap(impact_data: pd.DataFrame, 
                             title: str = "Interactive Hotspot Impact Heatmap"):
    """Create an interactive heatmap showing scenario impacts."""
    
    # Pivot data for heatmap
    pivot_data = impact_data.pivot(index='Hotspot', columns='Scenario', values='Percent_Change')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='RdYlBu_r',
        zmid=0,
        text=pivot_data.values.round(1),
        texttemplate="%{text}%",
        textfont={"size": 10},
        colorbar=dict(title="Percent Change (%)")
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Scenario",
        yaxis_title="Hotspot",
        template='plotly_white'
    )
    
    return fig


def run_interactive_visualization_demo():
    """Run a demonstration of interactive visualization capabilities."""
    
    print("🖱️ LLM Tourism Simulation - Interactive Visualization Demo")
    print("=" * 60)

    # Load data
    print("📁 Loading configuration...")
    try:
        personas, hotspots, business_rules, scenarios_data = load_data()
        print(f"✅ Configuration loaded successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Create test scenarios
    print("\n🎭 Creating test scenarios...")
    
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
        description="Aggressive marketing campaign with dramatic effects",
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
    marketing_scenario.add_external_factor("event_excitement", 0.4)
    marketing_scenario.add_external_factor("social_media_buzz", 0.3)

    # Run simulations
    print("\n🎯 Running simulations...")
    scenarios = [baseline_scenario, marketing_scenario]
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

        model_data = model.run_simulation(steps=20)
        hotspot_stats = model.get_hotspot_statistics()
        persona_stats = model.get_persona_statistics()
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

    print(f"\n📊 Generating interactive visualizations...")

    # 1. Interactive Popularity Chart
    print("   1. Creating interactive popularity chart...")
    baseline_data = results_collection[0]['model_data']
    fig1 = create_interactive_popularity_chart(
        baseline_data,
        title="Interactive Tourism Hotspot Popularity Evolution"
    )
    fig1.write_html(f"{charts_dir}/interactive_popularity.html")

    # 2. Interactive Hotspot Map
    print("   2. Creating interactive hotspot map...")
    try:
        popularity_data = {h['name']: h['current_popularity'] for h in results_collection[0]['hotspot_stats']}
        
        # Add mock location data if not present
        hotspots_with_location = []
        for hotspot in hotspots:
            hotspot_dict = hotspot.copy()
            if 'location' not in hotspot_dict:
                hotspot_dict['location'] = {
                    'x': len(hotspots_with_location) * 10,
                    'y': len(hotspots_with_location) * 8
                }
            hotspots_with_location.append(hotspot_dict)

        fig2 = create_interactive_hotspot_map(
            hotspots_with_location,
            popularity_data=popularity_data,
            title="Interactive Tourism Hotspots Map"
        )
        fig2.write_html(f"{charts_dir}/interactive_hotspot_map.html")
    except Exception as e:
        print(f"   ⚠️  Could not create interactive hotspot map: {e}")

    # 3. Interactive Dashboard
    print("   3. Creating interactive dashboard...")
    fig3 = create_interactive_dashboard(
        baseline_data,
        title="Interactive Tourism Simulation Dashboard"
    )
    fig3.write_html(f"{charts_dir}/interactive_dashboard.html")

    # 4. Interactive Scenario Comparison
    print("   4. Creating interactive scenario comparison...")
    # Convert results to the format expected by create_interactive_scenario_comparison
    scenario_results_for_comparison = []
    for result in results_collection:
        scenario_results_for_comparison.append({
            'scenario_name': result['name'],
            'final_metrics': result['summary']['final_metrics']
        })
    
    fig4 = create_interactive_scenario_comparison(
        scenario_results_for_comparison,
        title="Interactive Scenario Performance Comparison"
    )
    fig4.write_html(f"{charts_dir}/interactive_scenario_comparison.html")

    # 5. Interactive Impact Heatmap
    print("   5. Creating interactive impact heatmap...")
    try:
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
            fig5 = create_interactive_heatmap(
                impact_df,
                title="Interactive Hotspot Impact by Scenario"
            )
            fig5.write_html(f"{charts_dir}/interactive_impact_heatmap.html")
    except Exception as e:
        print(f"   ⚠️  Could not create interactive impact heatmap: {e}")

    # Display results
    print("\n📈 INTERACTIVE VISUALIZATION RESULTS:")
    print("-" * 45)
    print(f"✅ Generated {len(results_collection)} scenario interactive visualizations")
    print(f"✅ Saved interactive charts to: {charts_dir}/")
    
    print("\n📊 INTERACTIVE CHART SUMMARY:")
    print("-" * 30)
    print("1. interactive_popularity.html - Interactive popularity evolution")
    print("2. interactive_hotspot_map.html - Interactive geographic hotspot map")
    print("3. interactive_dashboard.html - Interactive multi-metric dashboard")
    print("4. interactive_scenario_comparison.html - Interactive scenario comparison")
    print("5. interactive_impact_heatmap.html - Interactive impact visualization")

    print("\n🎯 INTERACTIVE FEATURES:")
    print("-" * 25)
    print("• Hover tooltips with detailed information")
    print("• Zoom and pan capabilities")
    print("• Click to select and highlight data points")
    print("• Legend interaction (click to show/hide traces)")
    print("• Download as PNG/SVG/PDF")
    print("• Responsive design for different screen sizes")

    print("\n🌐 VIEWING INSTRUCTIONS:")
    print("-" * 25)
    print("1. Open any .html file in your web browser")
    print("2. Use mouse to interact with charts")
    print("3. Right-click for additional options")
    print("4. Use browser's back/forward buttons to navigate")

    print("\n🎉 Interactive visualization demo completed successfully!")
    print(f"📁 All outputs saved to: {output_dir}")
    print(f"🕐 Timestamp: {storage.get_timestamp()}")


def demonstrate_advanced_interactive_features():
    """Demonstrate advanced interactive visualization features."""
    
    print("\n🚀 ADVANCED INTERACTIVE FEATURES:")
    print("=" * 40)
    
    print("Advanced Plotly features you can add:")
    print("""
# 1. Animated charts
fig = px.line(model_data, x='step', y='popularity', 
              animation_frame='scenario', 
              title='Animated Popularity Evolution')

# 2. 3D visualizations
fig = px.scatter_3d(data, x='x', y='y', z='popularity',
                   color='category', title='3D Hotspot Map')

# 3. Range sliders
fig.update_xaxes(rangeslider_visible=True)

# 4. Custom hover templates
fig.update_traces(hovertemplate='<b>%{fullData.name}</b><br>' +
                                 'Step: %{x}<br>' +
                                 'Popularity: %{y:.3f}<br>' +
                                 '<extra></extra>')

# 5. Subplot synchronization
fig = make_subplots(rows=2, cols=2, 
                   shared_xaxes=True, shared_yaxes=True)

# 6. Custom buttons and dropdowns
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True, True]}]),
                dict(label="Popularity",
                     method="update", 
                     args=[{"visible": [True, False, False]}])
            ]),
            direction="down",
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        )
    ]
)
    """)


if __name__ == "__main__":
    run_interactive_visualization_demo()
    demonstrate_advanced_interactive_features()
