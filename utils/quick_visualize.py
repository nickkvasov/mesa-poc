"""
Quick Visualization Utilities
============================

This module provides simple functions to quickly add visualization
to any tourism simulation without requiring complex setup.
"""

import os
import pandas as pd
from typing import Dict, List, Any, Optional
from .visualization import (
    create_popularity_chart,
    create_satisfaction_chart,
    create_time_series_dashboard,
    save_all_charts
)
import matplotlib.pyplot as plt


def quick_visualize_simulation(model_data: pd.DataFrame,
                              hotspot_stats: Optional[List[Dict]] = None,
                              persona_stats: Optional[Dict] = None,
                              output_dir: str = "quick_charts",
                              show_plots: bool = False) -> Dict[str, str]:
    """
    Quickly generate and save standard visualizations for a simulation.
    
    Args:
        model_data: DataFrame with simulation time series data
        hotspot_stats: Optional list of hotspot statistics
        persona_stats: Optional dictionary of persona statistics
        output_dir: Directory to save charts
        show_plots: Whether to display plots (in addition to saving)
        
    Returns:
        Dictionary with paths to saved chart files
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    saved_files = {}
    
    try:
        # 1. Popularity evolution chart
        print("📊 Creating popularity evolution chart...")
        fig1 = create_popularity_chart(
            model_data,
            title="Tourism Hotspot Popularity Evolution",
            save_path=f"{output_dir}/popularity_evolution.png"
        )
        saved_files["popularity"] = f"{output_dir}/popularity_evolution.png"
        
        if show_plots:
            plt.show()
        plt.close(fig1)
        
        # 2. Satisfaction by persona chart
        if persona_stats:
            print("📊 Creating satisfaction by persona chart...")
            fig2 = create_satisfaction_chart(
                persona_stats,
                title="Tourist Satisfaction by Persona",
                save_path=f"{output_dir}/satisfaction_by_persona.png"
            )
            saved_files["satisfaction"] = f"{output_dir}/satisfaction_by_persona.png"
            
            if show_plots:
                plt.show()
            plt.close(fig2)
        
        # 3. Time series dashboard
        print("📊 Creating time series dashboard...")
        fig3 = create_time_series_dashboard(
            model_data,
            title="Tourism Simulation Dashboard",
            save_path=f"{output_dir}/simulation_dashboard.png"
        )
        saved_files["dashboard"] = f"{output_dir}/simulation_dashboard.png"
        
        if show_plots:
            plt.show()
        plt.close(fig3)
        
        # 4. Save all charts automatically
        print("📊 Saving additional charts...")
        results = {
            'model_data': model_data,
            'hotspot_stats': hotspot_stats or [],
            'persona_stats': persona_stats or {}
        }
        save_all_charts(results, output_dir)
        
        print(f"✅ All charts saved to {output_dir}/")
        
    except Exception as e:
        print(f"❌ Error generating charts: {e}")
    
    return saved_files


def quick_compare_scenarios(scenario_results: List[Dict[str, Any]],
                           output_dir: str = "scenario_comparison",
                           show_plots: bool = False) -> Dict[str, str]:
    """
    Quickly compare multiple scenarios and generate comparison charts.
    
    Args:
        scenario_results: List of scenario result dictionaries
        output_dir: Directory to save comparison charts
        show_plots: Whether to display plots (in addition to saving)
        
    Returns:
        Dictionary with paths to saved chart files
    """
    from .visualization import create_scenario_comparison
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    saved_files = {}
    
    try:
        print("📊 Creating scenario comparison chart...")
        # Convert results to the format expected by create_scenario_comparison
        scenario_results_for_comparison = []
        for result in scenario_results:
            scenario_results_for_comparison.append({
                'scenario_name': result.get('name', 'Unknown'),
                'final_metrics': result.get('summary', {}).get('final_metrics', {})
            })
        
        fig = create_scenario_comparison(
            scenario_results_for_comparison,
            metrics=['avg_popularity', 'total_visitors', 'social_shares', 'avg_satisfaction'],
            title="Scenario Performance Comparison",
            save_path=f"{output_dir}/scenario_comparison.png"
        )
        saved_files["comparison"] = f"{output_dir}/scenario_comparison.png"
        
        if show_plots:
            plt.show()
        plt.close(fig)
        
        # Create comparison table
        comparison_data = []
        for result in scenario_results:
            metrics = result.get('summary', {}).get('final_metrics', {})
            comparison_data.append({
                'Scenario': result.get('name', 'Unknown'),
                'Avg_Popularity': metrics.get('avg_popularity', 0),
                'Total_Visitors': metrics.get('total_visitors', 0),
                'Social_Shares': metrics.get('social_shares', 0),
                'Avg_Satisfaction': metrics.get('avg_satisfaction', 0)
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df.to_csv(f"{output_dir}/scenario_comparison.csv", index=False)
        saved_files["comparison_table"] = f"{output_dir}/scenario_comparison.csv"
        
        print(f"✅ Scenario comparison saved to {output_dir}/")
        
    except Exception as e:
        print(f"❌ Error creating scenario comparison: {e}")
    
    return saved_files


def quick_summary_report(model_data: pd.DataFrame,
                        hotspot_stats: Optional[List[Dict]] = None,
                        persona_stats: Optional[Dict] = None,
                        output_file: str = "simulation_summary.txt") -> str:
    """
    Generate a quick text summary report of simulation results.
    
    Args:
        model_data: DataFrame with simulation time series data
        hotspot_stats: Optional list of hotspot statistics
        persona_stats: Optional dictionary of persona statistics
        output_file: Path to save the summary report
        
    Returns:
        Path to the saved summary file
    """
    try:
        with open(output_file, 'w') as f:
            f.write("TOURISM SIMULATION SUMMARY REPORT\n")
            f.write("=" * 40 + "\n\n")
            
            # Final metrics
            if not model_data.empty:
                final_metrics = model_data.iloc[-1]
                f.write("FINAL METRICS:\n")
                f.write("-" * 15 + "\n")
                f.write(f"Average Popularity: {final_metrics.get('Average_Popularity', 0):.3f}\n")
                f.write(f"Total Visitors: {int(final_metrics.get('Total_Visitors', 0))}\n")
                f.write(f"Social Shares: {int(final_metrics.get('Social_Shares', 0))}\n")
                f.write(f"Average Satisfaction: {final_metrics.get('Average_Satisfaction', 0):.3f}\n\n")
            
            # Top hotspots
            if hotspot_stats:
                f.write("TOP PERFORMING HOTSPOTS:\n")
                f.write("-" * 25 + "\n")
                sorted_hotspots = sorted(hotspot_stats, key=lambda x: x.get('current_popularity', 0), reverse=True)
                
                for i, hotspot in enumerate(sorted_hotspots[:5], 1):
                    f.write(f"{i}. {hotspot.get('name', 'Unknown')}\n")
                    f.write(f"   Popularity: {hotspot.get('current_popularity', 0):.3f}\n")
                    f.write(f"   Visitors: {hotspot.get('total_visitors', 0)}\n")
                    f.write(f"   Category: {hotspot.get('category', 'unknown')}\n\n")
            
            # Persona analysis
            if persona_stats:
                f.write("PERSONA ANALYSIS:\n")
                f.write("-" * 16 + "\n")
                for persona, stats in persona_stats.items():
                    f.write(f"{persona}:\n")
                    f.write(f"   Count: {stats.get('count', 0)}\n")
                    f.write(f"   Avg Satisfaction: {stats.get('avg_satisfaction', 0):.3f}\n")
                    f.write(f"   Avg Visits: {stats.get('avg_visits', 0):.1f}\n\n")
        
        print(f"✅ Summary report saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"❌ Error creating summary report: {e}")
        return ""


def add_visualization_to_existing_simulation(model_data: pd.DataFrame,
                                           hotspot_stats: Optional[List[Dict]] = None,
                                           persona_stats: Optional[Dict] = None,
                                           output_dir: str = "visualization_output") -> Dict[str, str]:
    """
    One-stop function to add comprehensive visualization to any existing simulation.
    
    Args:
        model_data: DataFrame with simulation time series data
        hotspot_stats: Optional list of hotspot statistics
        persona_stats: Optional dictionary of persona statistics
        output_dir: Directory to save all outputs
        
    Returns:
        Dictionary with paths to all generated files
    """
    print("🎨 Adding visualization to simulation...")
    
    # Create output directory structure
    charts_dir = f"{output_dir}/charts"
    data_dir = f"{output_dir}/data"
    reports_dir = f"{output_dir}/reports"
    
    os.makedirs(charts_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    all_files = {}
    
    # Generate charts
    chart_files = quick_visualize_simulation(
        model_data, hotspot_stats, persona_stats, charts_dir
    )
    all_files.update(chart_files)
    
    # Generate summary report
    summary_file = quick_summary_report(
        model_data, hotspot_stats, persona_stats, 
        f"{reports_dir}/simulation_summary.txt"
    )
    if summary_file:
        all_files["summary"] = summary_file
    
    # Save data files
    if not model_data.empty:
        model_data.to_csv(f"{data_dir}/model_data.csv", index=False)
        all_files["model_data"] = f"{data_dir}/model_data.csv"
    
    if hotspot_stats:
        import json
        with open(f"{data_dir}/hotspot_stats.json", 'w') as f:
            json.dump(hotspot_stats, f, indent=2)
        all_files["hotspot_stats"] = f"{data_dir}/hotspot_stats.json"
    
    if persona_stats:
        import json
        with open(f"{data_dir}/persona_stats.json", 'w') as f:
            json.dump(persona_stats, f, indent=2)
        all_files["persona_stats"] = f"{data_dir}/persona_stats.json"
    
    print(f"✅ All visualization outputs saved to {output_dir}/")
    print(f"📊 Generated {len(all_files)} files")
    
    return all_files
