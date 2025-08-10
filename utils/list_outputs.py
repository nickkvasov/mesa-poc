#!/usr/bin/env python3
"""
Output Directory Management Utility
==================================

This script provides utilities to list, explore, and manage simulation output directories.
"""

import sys
import os
from .results_storage import list_output_directories, get_latest_output_dir
from pathlib import Path


def list_all_outputs():
    """List all available output directories."""
    print("📁 Available Simulation Outputs")
    print("=" * 50)
    
    outputs = list_output_directories()
    
    if not outputs:
        print("❌ No output directories found.")
        print("   Run a simulation first to generate outputs.")
        return
    
    for i, output in enumerate(outputs, 1):
        print(f"\n{i}. 📂 {output['timestamp']}")
        print(f"   📅 Date: {output['simulation_date']}")
        print(f"   🎯 Steps: {output['model_steps']}")
        print(f"   👥 Agents: {output['total_agents']}")
        print(f"   📍 Path: {output['directory']}")


def show_latest_output():
    """Show information about the latest output directory."""
    print("🕐 Latest Simulation Output")
    print("=" * 30)
    
    latest_dir = get_latest_output_dir()
    
    if not latest_dir:
        print("❌ No output directories found.")
        return
    
    print(f"📂 Directory: {latest_dir}")
    
    # Check if README exists
    readme_path = Path(latest_dir) / "README.md"
    if readme_path.exists():
        print(f"📄 README: {readme_path}")
        print("\n📋 Contents:")
        with open(readme_path, 'r') as f:
            print(f.read())
    else:
        print("⚠️  No README file found.")


def explore_output(timestamp=None):
    """Explore a specific output directory."""
    if not timestamp:
        latest_dir = get_latest_output_dir()
        if not latest_dir:
            print("❌ No output directories found.")
            return
        output_dir = Path(latest_dir)
    else:
        output_dir = Path("outputs") / timestamp
    
    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    print(f"🔍 Exploring: {output_dir}")
    print("=" * 40)
    
    # List contents
    for item in output_dir.iterdir():
        if item.is_dir():
            print(f"📁 {item.name}/")
            # List subdirectory contents
            for subitem in item.iterdir():
                if subitem.is_file():
                    size = subitem.stat().st_size
                    print(f"   📄 {subitem.name} ({size} bytes)")
        else:
            size = item.stat().st_size
            print(f"📄 {item.name} ({size} bytes)")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python list_outputs.py list          # List all outputs")
        print("  python list_outputs.py latest        # Show latest output")
        print("  python list_outputs.py explore       # Explore latest output")
        print("  python list_outputs.py explore <timestamp>  # Explore specific output")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_all_outputs()
    elif command == "latest":
        show_latest_output()
    elif command == "explore":
        timestamp = sys.argv[2] if len(sys.argv) > 2 else None
        explore_output(timestamp)
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: list, latest, explore")


if __name__ == "__main__":
    main()
