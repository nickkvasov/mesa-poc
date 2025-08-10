# Copy the JSON data files to the data directory
import shutil

# List of JSON files we created earlier
json_files = [
    "tourist_personas.json",
    "urban_hotspots.json", 
    "business_rules.json",
    "scenarios_events.json",
    "master_config.json"
]

# Copy each file to the data directory
for filename in json_files:
    try:
        source_path = filename
        dest_path = f"llm_tourism_sim/data/{filename}"
        shutil.copy(source_path, dest_path)
        print(f"✅ Copied {filename} to data directory")
    except FileNotFoundError:
        print(f"⚠️  Warning: {filename} not found in current directory")

print("\n📁 Data directory populated with LLM-generated JSON files!")
print("   - All configuration data ready for package use")