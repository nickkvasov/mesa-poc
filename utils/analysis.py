"""
Analysis Utilities
=================

This module provides functions for analyzing tourism simulation results,
calculating metrics, generating insights, and creating policy recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import statistics


def analyze_simulation_results(model_data: pd.DataFrame, 
                             hotspot_stats: List[Dict[str, Any]],
                             persona_stats: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Perform comprehensive analysis of simulation results.

    Args:
        model_data: Time series data from the model
        hotspot_stats: Statistics for each hotspot
        persona_stats: Statistics grouped by persona

    Returns:
        Dictionary with comprehensive analysis results
    """
    analysis = {
        "simulation_overview": {},
        "performance_metrics": {},
        "hotspot_analysis": {},
        "persona_analysis": {},
        "trend_analysis": {},
        "recommendations": []
    }

    # Simulation overview
    analysis["simulation_overview"] = {
        "total_steps": len(model_data) if not model_data.empty else 0,
        "total_hotspots": len(hotspot_stats),
        "total_personas": len(persona_stats),
        "data_quality": "complete" if not model_data.empty else "incomplete"
    }

    # Performance metrics
    if not model_data.empty:
        final_metrics = model_data.iloc[-1] if len(model_data) > 0 else {}
        initial_metrics = model_data.iloc[0] if len(model_data) > 0 else {}

        analysis["performance_metrics"] = {
            "final_popularity": float(final_metrics.get("Average_Popularity", 0)),
            "final_satisfaction": float(final_metrics.get("Average_Satisfaction", 0)),
            "total_visitors": int(final_metrics.get("Total_Visitors", 0)),
            "total_social_shares": int(final_metrics.get("Social_Shares", 0)),
            "popularity_growth": float(final_metrics.get("Average_Popularity", 0) - initial_metrics.get("Average_Popularity", 0)),
            "satisfaction_change": float(final_metrics.get("Average_Satisfaction", 0) - initial_metrics.get("Average_Satisfaction", 0))
        }

    # Hotspot analysis
    if hotspot_stats:
        hotspot_analysis = analyze_hotspots(hotspot_stats)
        analysis["hotspot_analysis"] = hotspot_analysis

    # Persona analysis  
    if persona_stats:
        persona_analysis = analyze_personas(persona_stats)
        analysis["persona_analysis"] = persona_analysis

    # Trend analysis
    if not model_data.empty:
        trend_analysis = analyze_trends(model_data)
        analysis["trend_analysis"] = trend_analysis

    # Generate recommendations
    recommendations = generate_policy_recommendations(analysis)
    analysis["recommendations"] = recommendations

    return analysis


def analyze_hotspots(hotspot_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze hotspot performance and characteristics.

    Args:
        hotspot_stats: List of hotspot statistics

    Returns:
        Dictionary with hotspot analysis results
    """
    if not hotspot_stats:
        return {"error": "No hotspot data provided"}

    # Calculate summary statistics
    popularity_scores = [h.get("Current_Popularity", 0) for h in hotspot_stats]
    visitor_counts = [h.get("Total_Visitors", 0) for h in hotspot_stats]
    social_shares = [h.get("Social_Shares", 0) for h in hotspot_stats]

    # Find top performers
    sorted_by_popularity = sorted(hotspot_stats, key=lambda x: x.get("Current_Popularity", 0), reverse=True)
    sorted_by_visitors = sorted(hotspot_stats, key=lambda x: x.get("Total_Visitors", 0), reverse=True)
    sorted_by_shares = sorted(hotspot_stats, key=lambda x: x.get("Social_Shares", 0), reverse=True)

    # Category analysis
    category_stats = defaultdict(lambda: {"count": 0, "avg_popularity": 0, "total_visitors": 0})

    for hotspot in hotspot_stats:
        category = hotspot.get("Category", "unknown")
        category_stats[category]["count"] += 1
        category_stats[category]["avg_popularity"] += hotspot.get("Current_Popularity", 0)
        category_stats[category]["total_visitors"] += hotspot.get("Total_Visitors", 0)

    # Calculate averages
    for category, stats in category_stats.items():
        if stats["count"] > 0:
            stats["avg_popularity"] /= stats["count"]

    return {
        "summary_statistics": {
            "total_hotspots": len(hotspot_stats),
            "avg_popularity": round(np.mean(popularity_scores), 3),
            "popularity_std": round(np.std(popularity_scores), 3),
            "total_visitors": sum(visitor_counts),
            "avg_visitors_per_hotspot": round(np.mean(visitor_counts), 1),
            "total_social_shares": sum(social_shares)
        },
        "top_performers": {
            "most_popular": {
                "name": sorted_by_popularity[0].get("Name", "Unknown"),
                "popularity": sorted_by_popularity[0].get("Current_Popularity", 0)
            } if sorted_by_popularity else None,
            "most_visited": {
                "name": sorted_by_visitors[0].get("Name", "Unknown"), 
                "visitors": sorted_by_visitors[0].get("Total_Visitors", 0)
            } if sorted_by_visitors else None,
            "most_shared": {
                "name": sorted_by_shares[0].get("Name", "Unknown"),
                "shares": sorted_by_shares[0].get("Social_Shares", 0)
            } if sorted_by_shares else None
        },
        "category_performance": dict(category_stats),
        "underperformers": [
            {
                "name": h.get("Name", "Unknown"),
                "popularity": h.get("Current_Popularity", 0),
                "visitors": h.get("Total_Visitors", 0)
            }
            for h in sorted_by_popularity[-2:] if h.get("Current_Popularity", 0) < np.mean(popularity_scores) * 0.7
        ]
    }


def analyze_personas(persona_stats: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze tourist persona performance and behavior patterns.

    Args:
        persona_stats: Dictionary with persona statistics

    Returns:
        Dictionary with persona analysis results
    """
    if not persona_stats:
        return {"error": "No persona data provided"}

    # Calculate summary statistics
    satisfaction_scores = [stats.get("avg_satisfaction", 0) for stats in persona_stats.values()]
    visit_counts = [stats.get("avg_visits", 0) for stats in persona_stats.values()]
    recommendation_counts = [stats.get("avg_recommendations", 0) for stats in persona_stats.values()]

    # Find top and bottom performers
    sorted_by_satisfaction = sorted(persona_stats.items(), 
                                  key=lambda x: x[1].get("avg_satisfaction", 0), reverse=True)

    # Analyze persona diversity
    satisfaction_range = max(satisfaction_scores) - min(satisfaction_scores) if satisfaction_scores else 0

    return {
        "summary_statistics": {
            "total_personas": len(persona_stats),
            "avg_satisfaction": round(np.mean(satisfaction_scores), 3) if satisfaction_scores else 0,
            "satisfaction_std": round(np.std(satisfaction_scores), 3) if satisfaction_scores else 0,
            "satisfaction_range": round(satisfaction_range, 3),
            "avg_visits_per_tourist": round(np.mean(visit_counts), 2) if visit_counts else 0,
            "total_recommendations": sum(recommendation_counts) if recommendation_counts else 0
        },
        "persona_rankings": {
            "highest_satisfaction": {
                "persona": sorted_by_satisfaction[0][0],
                "satisfaction": sorted_by_satisfaction[0][1].get("avg_satisfaction", 0)
            } if sorted_by_satisfaction else None,
            "lowest_satisfaction": {
                "persona": sorted_by_satisfaction[-1][0],
                "satisfaction": sorted_by_satisfaction[-1][1].get("avg_satisfaction", 0) 
            } if sorted_by_satisfaction else None
        },
        "behavioral_insights": _generate_persona_insights(persona_stats),
        "persona_distribution": {
            persona: stats.get("count", 0) 
            for persona, stats in persona_stats.items()
        }
    }


def analyze_trends(model_data: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze trends and patterns in time series data.

    Args:
        model_data: Time series data from model

    Returns:
        Dictionary with trend analysis results
    """
    if model_data.empty:
        return {"error": "No time series data provided"}

    trends = {}

    # Analyze each numeric column
    numeric_columns = model_data.select_dtypes(include=[np.number]).columns

    for column in numeric_columns:
        if len(model_data[column]) > 1:
            # Calculate trend
            x = np.arange(len(model_data))
            y = model_data[column].values

            # Linear regression for trend
            slope, intercept = np.polyfit(x, y, 1)

            # Calculate volatility
            volatility = np.std(np.diff(y)) if len(y) > 1 else 0

            # Determine trend direction
            if abs(slope) < 0.001:
                direction = "stable"
            elif slope > 0:
                direction = "increasing"
            else:
                direction = "decreasing"

            trends[column] = {
                "direction": direction,
                "slope": round(slope, 6),
                "volatility": round(volatility, 4),
                "initial_value": round(y[0], 3),
                "final_value": round(y[-1], 3),
                "total_change": round(y[-1] - y[0], 3),
                "percent_change": round(((y[-1] - y[0]) / max(abs(y[0]), 0.001)) * 100, 2)
            }

    return {
        "metric_trends": trends,
        "overall_assessment": _assess_overall_trends(trends),
        "stability_analysis": {
            "most_stable": min(trends.items(), key=lambda x: x[1]["volatility"])[0] if trends else None,
            "most_volatile": max(trends.items(), key=lambda x: x[1]["volatility"])[0] if trends else None
        }
    }


def compare_scenarios(baseline_results: Dict[str, Any], 
                     scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare multiple scenarios against a baseline.

    Args:
        baseline_results: Results from baseline simulation
        scenario_results: List of scenario result dictionaries

    Returns:
        Dictionary with comprehensive scenario comparison
    """
    if not baseline_results or not scenario_results:
        return {"error": "Insufficient data for comparison"}

    comparison = {
        "baseline_summary": baseline_results.get("performance_metrics", {}),
        "scenario_comparisons": [],
        "ranking_analysis": {},
        "impact_summary": {}
    }

    baseline_metrics = baseline_results.get("performance_metrics", {})

    # Compare each scenario to baseline
    for scenario_result in scenario_results:
        scenario_metrics = scenario_result.get("performance_metrics", {})
        scenario_name = scenario_result.get("scenario_name", "Unknown")

        scenario_comparison = {
            "scenario_name": scenario_name,
            "metric_changes": {},
            "overall_impact": "neutral"
        }

        positive_changes = 0
        negative_changes = 0

        for metric, baseline_value in baseline_metrics.items():
            scenario_value = scenario_metrics.get(metric, 0)

            if baseline_value != 0:
                change = scenario_value - baseline_value
                percent_change = (change / abs(baseline_value)) * 100
            else:
                change = scenario_value
                percent_change = 0 if scenario_value == 0 else 100

            scenario_comparison["metric_changes"][metric] = {
                "baseline": round(baseline_value, 3),
                "scenario": round(scenario_value, 3),
                "absolute_change": round(change, 3),
                "percent_change": round(percent_change, 2)
            }

            # Count positive/negative changes
            if percent_change > 1:  # More than 1% improvement
                positive_changes += 1
            elif percent_change < -1:  # More than 1% decline
                negative_changes += 1

        # Determine overall impact
        if positive_changes > negative_changes:
            scenario_comparison["overall_impact"] = "positive"
        elif negative_changes > positive_changes:
            scenario_comparison["overall_impact"] = "negative"

        comparison["scenario_comparisons"].append(scenario_comparison)

    # Ranking analysis
    comparison["ranking_analysis"] = _rank_scenarios(comparison["scenario_comparisons"])

    # Impact summary
    comparison["impact_summary"] = _summarize_scenario_impacts(comparison["scenario_comparisons"])

    return comparison


def calculate_satisfaction_metrics(satisfaction_data: List[float]) -> Dict[str, float]:
    """
    Calculate comprehensive satisfaction metrics.

    Args:
        satisfaction_data: List of satisfaction scores

    Returns:
        Dictionary with satisfaction metrics
    """
    if not satisfaction_data:
        return {"error": "No satisfaction data provided"}

    return {
        "mean": round(statistics.mean(satisfaction_data), 3),
        "median": round(statistics.median(satisfaction_data), 3),
        "std_dev": round(statistics.stdev(satisfaction_data) if len(satisfaction_data) > 1 else 0, 3),
        "min": round(min(satisfaction_data), 3),
        "max": round(max(satisfaction_data), 3),
        "range": round(max(satisfaction_data) - min(satisfaction_data), 3),
        "q25": round(np.percentile(satisfaction_data, 25), 3),
        "q75": round(np.percentile(satisfaction_data, 75), 3)
    }


def generate_policy_recommendations(analysis_results: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generate policy recommendations based on analysis results.

    Args:
        analysis_results: Comprehensive analysis results

    Returns:
        List of policy recommendation dictionaries
    """
    recommendations = []

    # Analyze performance metrics
    metrics = analysis_results.get("performance_metrics", {})
    hotspot_analysis = analysis_results.get("hotspot_analysis", {})
    persona_analysis = analysis_results.get("persona_analysis", {})

    # Satisfaction-based recommendations
    avg_satisfaction = metrics.get("final_satisfaction", 0)
    if avg_satisfaction < 0.6:
        recommendations.append({
            "category": "satisfaction",
            "priority": "high",
            "recommendation": "Implement visitor experience improvements to boost satisfaction",
            "rationale": f"Average satisfaction is {avg_satisfaction:.2f}, below optimal threshold of 0.6"
        })

    # Hotspot-based recommendations
    underperformers = hotspot_analysis.get("underperformers", [])
    if underperformers:
        recommendations.append({
            "category": "hotspots",
            "priority": "medium",
            "recommendation": f"Focus marketing and infrastructure investment on {len(underperformers)} underperforming hotspots",
            "rationale": f"Multiple hotspots showing below-average performance"
        })

    # Persona-based recommendations
    persona_rankings = persona_analysis.get("persona_rankings", {})
    lowest_satisfaction = persona_rankings.get("lowest_satisfaction")

    if lowest_satisfaction and lowest_satisfaction["satisfaction"] < 0.5:
        recommendations.append({
            "category": "personas",
            "priority": "medium",
            "recommendation": f"Develop targeted interventions for {lowest_satisfaction['persona']} segment",
            "rationale": f"This persona has lowest satisfaction at {lowest_satisfaction['satisfaction']:.2f}"
        })

    # Growth-based recommendations
    popularity_growth = metrics.get("popularity_growth", 0)
    if popularity_growth < 0:
        recommendations.append({
            "category": "marketing",
            "priority": "high",
            "recommendation": "Implement viral marketing campaign to reverse declining popularity",
            "rationale": f"Overall popularity declined by {abs(popularity_growth):.3f}"
        })

    return recommendations


# Helper functions
def _generate_persona_insights(persona_stats: Dict[str, Dict[str, Any]]) -> List[str]:
    """Generate behavioral insights from persona statistics."""
    insights = []

    # Find most/least satisfied personas
    if persona_stats:
        sorted_satisfaction = sorted(persona_stats.items(), 
                                   key=lambda x: x[1].get("avg_satisfaction", 0), reverse=True)

        highest = sorted_satisfaction[0]
        lowest = sorted_satisfaction[-1]

        insights.append(f"{highest[0]} shows highest satisfaction ({highest[1].get('avg_satisfaction', 0):.3f})")
        insights.append(f"{lowest[0]} shows lowest satisfaction ({lowest[1].get('avg_satisfaction', 0):.3f})")

        # Find most active persona
        sorted_visits = sorted(persona_stats.items(), 
                             key=lambda x: x[1].get("avg_visits", 0), reverse=True)
        if sorted_visits:
            most_active = sorted_visits[0]
            insights.append(f"{most_active[0]} is most active with {most_active[1].get('avg_visits', 0):.1f} average visits")

    return insights


def _assess_overall_trends(trends: Dict[str, Any]) -> str:
    """Assess the overall trend pattern across all metrics."""
    if not trends:
        return "insufficient_data"

    increasing_count = sum(1 for t in trends.values() if t["direction"] == "increasing")
    decreasing_count = sum(1 for t in trends.values() if t["direction"] == "decreasing")
    stable_count = sum(1 for t in trends.values() if t["direction"] == "stable")

    if increasing_count > decreasing_count + stable_count:
        return "generally_improving"
    elif decreasing_count > increasing_count + stable_count:
        return "generally_declining"
    else:
        return "mixed_trends"


def _rank_scenarios(scenario_comparisons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Rank scenarios by overall performance improvement."""
    if not scenario_comparisons:
        return {}

    # Calculate overall performance score for each scenario
    scenario_scores = []

    for comparison in scenario_comparisons:
        scenario_name = comparison["scenario_name"]
        metric_changes = comparison["metric_changes"]

        # Simple scoring: sum of positive percent changes
        total_score = sum(
            change_data["percent_change"] 
            for change_data in metric_changes.values()
            if change_data["percent_change"] > 0
        )

        scenario_scores.append({
            "scenario": scenario_name,
            "score": total_score,
            "positive_changes": sum(1 for c in metric_changes.values() if c["percent_change"] > 0)
        })

    # Sort by score
    scenario_scores.sort(key=lambda x: x["score"], reverse=True)

    return {
        "best_scenario": scenario_scores[0]["scenario"] if scenario_scores else None,
        "worst_scenario": scenario_scores[-1]["scenario"] if scenario_scores else None,
        "full_ranking": scenario_scores
    }


def _summarize_scenario_impacts(scenario_comparisons: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize the overall impact patterns across scenarios."""
    if not scenario_comparisons:
        return {}

    impact_counts = {"positive": 0, "negative": 0, "neutral": 0}

    for comparison in scenario_comparisons:
        impact = comparison.get("overall_impact", "neutral")
        impact_counts[impact] += 1

    return {
        "total_scenarios": len(scenario_comparisons),
        "impact_distribution": impact_counts,
        "success_rate": round(impact_counts["positive"] / len(scenario_comparisons) * 100, 1),
        "most_common_impact": max(impact_counts.items(), key=lambda x: x[1])[0]
    }
