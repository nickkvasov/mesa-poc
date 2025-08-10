# Create the visualization utility
visualization_utils = '''"""
Visualization Utilities
======================

This module provides functions for creating charts and visualizations of
tourism simulation results, including popularity trends, satisfaction metrics,
and scenario comparisons.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


def create_popularity_chart(model_data: pd.DataFrame, 
                          hotspot_data: Optional[pd.DataFrame] = None,
                          title: str = "Hotspot Popularity Evolution",
                          save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a line chart showing hotspot popularity evolution over time.
    
    Args:
        model_data: DataFrame with time series data from model
        hotspot_data: Optional DataFrame with hotspot-specific data  
        title: Chart title
        save_path: Optional path to save the chart
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if hotspot_data is not None and not hotspot_data.empty:
        # Plot individual hotspot popularity over time
        hotspots = hotspot_data.groupby(['Step', 'name'])['current_popularity'].first().unstack(fill_value=0)
        
        for hotspot in hotspots.columns:
            ax.plot(hotspots.index, hotspots[hotspot], marker='o', linewidth=2, label=hotspot)
        
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    else:
        # Plot average popularity from model data
        if 'Average_Popularity' in model_data.columns:
            ax.plot(model_data.index, model_data['Average_Popularity'], 
                   marker='o', linewidth=3, color='blue', label='Average Popularity')
            ax.legend()
    
    ax.set_xlabel('Simulation Step')
    ax.set_ylabel('Popularity Score')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_satisfaction_chart(persona_stats: Dict[str, Dict[str, Any]], 
                            title: str = "Tourist Satisfaction by Persona",
                            save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a bar chart showing satisfaction levels by tourist persona.
    
    Args:
        persona_stats: Dictionary with persona statistics
        title: Chart title
        save_path: Optional path to save the chart
        
    Returns:
        Matplotlib figure object
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Extract data
    personas = list(persona_stats.keys())
    satisfaction_scores = [stats.get('avg_satisfaction', 0) for stats in persona_stats.values()]
    visitor_counts = [stats.get('count', 0) for stats in persona_stats.values()]
    
    # Satisfaction bar chart
    bars1 = ax1.bar(personas, satisfaction_scores, color=sns.color_palette("viridis", len(personas)))
    ax1.set_ylabel('Average Satisfaction')
    ax1.set_title('Satisfaction by Persona')
    ax1.set_ylim(0, 1)
    
    # Add value labels on bars
    for bar, value in zip(bars1, satisfaction_scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    # Tourist count bar chart
    bars2 = ax2.bar(personas, visitor_counts, color=sns.color_palette("plasma", len(personas)))
    ax2.set_ylabel('Number of Tourists')
    ax2.set_title('Tourist Count by Persona')
    
    # Add value labels on bars
    for bar, value in zip(bars2, visitor_counts):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(value)}', ha='center', va='bottom')
    
    # Rotate x-axis labels for better readability
    for ax in [ax1, ax2]:
        ax.tick_params(axis='x', rotation=45)
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_scenario_comparison(scenario_results: List[Dict[str, Any]],
                             metrics: List[str] = None,
                             title: str = "Scenario Performance Comparison", 
                             save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a comparison chart showing multiple scenarios across key metrics.
    
    Args:
        scenario_results: List of scenario result dictionaries
        metrics: List of metrics to compare (default: all available)
        title: Chart title
        save_path: Optional path to save the chart
        
    Returns:
        Matplotlib figure object
    """
    if not scenario_results:
        raise ValueError("No scenario results provided")
    
    # Extract scenario names and metrics
    scenario_names = [result.get('scenario_name', 'Unknown') for result in scenario_results]
    
    # Default metrics if none specified
    if metrics is None:
        metrics = ['avg_popularity', 'total_visitors', 'social_shares', 'avg_satisfaction']
    
    # Filter available metrics
    available_metrics = []
    for metric in metrics:
        if any(metric in result.get('final_metrics', {}) for result in scenario_results):
            available_metrics.append(metric)
    
    if not available_metrics:
        raise ValueError("No common metrics found in scenario results")
    
    # Create subplots
    n_metrics = len(available_metrics)
    cols = 2
    rows = (n_metrics + 1) // 2
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    if rows == 1:
        axes = axes.reshape(1, -1)
    
    # Plot each metric
    for i, metric in enumerate(available_metrics):
        row, col = i // cols, i % cols
        ax = axes[row, col]
        
        values = []
        for result in scenario_results:
            final_metrics = result.get('final_metrics', {})
            values.append(final_metrics.get(metric, 0))
        
        bars = ax.bar(scenario_names, values, color=sns.color_palette("Set2", len(scenario_names)))
        
        # Format metric name for display
        metric_display = metric.replace('_', ' ').title()
        ax.set_title(f'{metric_display}', fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.3f}' if isinstance(value, float) else f'{value}',
                   ha='center', va='bottom', fontsize=10)
    
    # Hide empty subplots
    for i in range(n_metrics, rows * cols):
        row, col = i // cols, i % cols
        axes[row, col].set_visible(False)
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_hotspot_impact_heatmap(impact_data: pd.DataFrame,
                                title: str = "Hotspot Impact by Scenario",
                                save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a heatmap showing how different scenarios impact each hotspot.
    
    Args:
        impact_data: DataFrame with hotspot impact data
        title: Chart title
        save_path: Optional path to save the chart
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Pivot data for heatmap
    if 'Hotspot' in impact_data.columns and 'Scenario' in impact_data.columns:
        pivot_data = impact_data.pivot(index='Hotspot', columns='Scenario', values='Percent_Change')
    else:
        raise ValueError("Impact data must contain 'Hotspot', 'Scenario', and 'Percent_Change' columns")
    
    # Create heatmap
    sns.heatmap(pivot_data, 
                annot=True, 
                fmt='.1f',
                cmap='RdYlBu_r',
                center=0,
                cbar_kws={'label': 'Percent Change (%)'},
                ax=ax)
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Hotspot')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_hotspot_map(hotspots_data: List[Dict[str, Any]], 
                    popularity_data: Optional[Dict[str, float]] = None,
                    title: str = "Tourism Hotspots Map",
                    save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a scatter plot map of hotspots with optional popularity visualization.
    
    Args:
        hotspots_data: List of hotspot dictionaries with location data
        popularity_data: Optional dictionary mapping hotspot names to popularity scores
        title: Chart title
        save_path: Optional path to save the chart
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Extract coordinates and names
    x_coords = []
    y_coords = []
    names = []
    categories = []
    popularity_scores = []
    
    for hotspot in hotspots_data:
        location = hotspot.get('location', {})
        x_coords.append(location.get('x', 0))
        y_coords.append(location.get('y', 0))
        names.append(hotspot.get('name', 'Unknown'))
        categories.append(hotspot.get('category', 'unknown'))
        
        # Get popularity if provided
        hotspot_name = hotspot.get('name', 'Unknown')
        if popularity_data and hotspot_name in popularity_data:
            popularity_scores.append(popularity_data[hotspot_name])
        else:
            popularity_scores.append(0.5)  # Default
    
    # Create scatter plot
    if popularity_data:
        scatter = ax.scatter(x_coords, y_coords, 
                           s=[p * 500 for p in popularity_scores],  # Size based on popularity
                           c=popularity_scores,
                           cmap='viridis',
                           alpha=0.7,
                           edgecolors='black',
                           linewidth=1)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Popularity Score', rotation=270, labelpad=20)
    else:
        # Color by category
        unique_categories = list(set(categories))
        colors = sns.color_palette("Set3", len(unique_categories))
        category_colors = dict(zip(unique_categories, colors))
        
        for category in unique_categories:
            cat_indices = [i for i, cat in enumerate(categories) if cat == category]
            cat_x = [x_coords[i] for i in cat_indices]
            cat_y = [y_coords[i] for i in cat_indices]
            
            ax.scatter(cat_x, cat_y, 
                      label=category.title(),
                      s=100,
                      alpha=0.7,
                      edgecolors='black',
                      linewidth=1,
                      color=category_colors[category])
        
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add hotspot names as labels
    for i, name in enumerate(names):
        ax.annotate(name, (x_coords[i], y_coords[i]), 
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, alpha=0.8)
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def create_time_series_dashboard(model_data: pd.DataFrame,
                               agent_data: Optional[pd.DataFrame] = None,
                               title: str = "Tourism Simulation Dashboard",
                               save_path: Optional[str] = None) -> plt.Figure:
    """
    Create a comprehensive dashboard with multiple time series charts.
    
    Args:
        model_data: DataFrame with model-level time series data
        agent_data: Optional DataFrame with agent-level data
        title: Dashboard title
        save_path: Optional path to save the dashboard
        
    Returns:
        Matplotlib figure object
    """
    fig = plt.figure(figsize=(16, 12))
    
    # Create grid layout
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Plot 1: Popularity over time
    ax1 = fig.add_subplot(gs[0, 0])
    if 'Average_Popularity' in model_data.columns:
        ax1.plot(model_data.index, model_data['Average_Popularity'], 
                marker='o', linewidth=2, color='blue')
        ax1.set_title('Average Popularity')
        ax1.set_ylabel('Popularity Score')
        ax1.grid(True, alpha=0.3)
    
    # Plot 2: Visitor metrics
    ax2 = fig.add_subplot(gs[0, 1])
    if 'Total_Visitors' in model_data.columns:
        ax2.plot(model_data.index, model_data['Total_Visitors'], 
                marker='s', linewidth=2, color='green')
        ax2.set_title('Total Visitors')
        ax2.set_ylabel('Cumulative Visitors')
        ax2.grid(True, alpha=0.3)
    
    # Plot 3: Social shares
    ax3 = fig.add_subplot(gs[1, 0])
    if 'Social_Shares' in model_data.columns:
        ax3.plot(model_data.index, model_data['Social_Shares'], 
                marker='^', linewidth=2, color='orange')
        ax3.set_title('Social Media Shares')
        ax3.set_ylabel('Total Shares')
        ax3.grid(True, alpha=0.3)
    
    # Plot 4: Satisfaction
    ax4 = fig.add_subplot(gs[1, 1])
    if 'Average_Satisfaction' in model_data.columns:
        ax4.plot(model_data.index, model_data['Average_Satisfaction'], 
                marker='d', linewidth=2, color='red')
        ax4.set_title('Average Satisfaction')
        ax4.set_ylabel('Satisfaction Score')
        ax4.grid(True, alpha=0.3)
    
    # Plot 5-6: Combined metrics
    ax5 = fig.add_subplot(gs[2, :])
    
    # Normalize metrics for comparison
    metrics_to_plot = ['Average_Popularity', 'Average_Satisfaction']
    available_metrics = [m for m in metrics_to_plot if m in model_data.columns]
    
    for metric in available_metrics:
        normalized_values = (model_data[metric] - model_data[metric].min()) / (model_data[metric].max() - model_data[metric].min())
        ax5.plot(model_data.index, normalized_values, 
                marker='o', linewidth=2, label=metric.replace('_', ' '))
    
    ax5.set_title('Normalized Metrics Comparison')
    ax5.set_xlabel('Simulation Step')
    ax5.set_ylabel('Normalized Score')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def save_all_charts(results: Dict[str, Any], output_dir: str = "charts"):
    """
    Generate and save all standard charts for a simulation run.
    
    Args:
        results: Dictionary with simulation results
        output_dir: Directory to save charts
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    model_data = results.get('model_data')
    hotspot_stats = results.get('hotspot_stats', [])
    persona_stats = results.get('persona_stats', {})
    
    try:
        # Popularity chart
        if model_data is not None:
            fig1 = create_popularity_chart(model_data, save_path=f"{output_dir}/popularity_evolution.png")
            plt.close(fig1)
        
        # Satisfaction chart
        if persona_stats:
            fig2 = create_satisfaction_chart(persona_stats, save_path=f"{output_dir}/satisfaction_by_persona.png")
            plt.close(fig2)
        
        # Dashboard
        if model_data is not None:
            fig3 = create_time_series_dashboard(model_data, save_path=f"{output_dir}/simulation_dashboard.png")
            plt.close(fig3)
        
        # Hotspot map
        if hotspot_stats:
            popularity_dict = {h['Name']: h['Current_Popularity'] for h in hotspot_stats}
            # Would need hotspot location data for this chart
            
        print(f"Charts saved to {output_dir}/")
        
    except Exception as e:
        print(f"Error generating charts: {e}")
'''

# Write visualization.py
with open('llm_tourism_sim/utils/visualization.py', 'w') as f:
    f.write(visualization_utils)

print("✅ Visualization utilities created!")
print("   - Comprehensive charting functions for all simulation aspects")
print("   - Time series, comparison, heatmap, and dashboard visualizations")
print("   - Matplotlib and Seaborn integration with professional styling")