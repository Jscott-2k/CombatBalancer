#!/usr/bin/env python3
import argparse
import yaml
import sys

def load_config_file(path):
    """
    Loads a configuration file (YAML/JSON) from the given path.
    """
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration file {path}: {e}")

def run_simulation(config):
    """
    Stub simulation function.
    Replace this with your actual simulation logic.
    """
    print("Starting simulation with the following unified configuration:")
    print(config)
    
    # Dummy simulation results for now.
    simulation_results = {
        "win_rate": 0.75,            # e.g., 75% win rate for the party
        "average_rounds": 10,        # e.g., average of 10 rounds per simulation
        "character_survival": {
            "fighter": 0.9,
            "wizard": 0.6,
            "cleric": 0.8
        },
        "balance_rating": "Balanced"
    }
    
    return simulation_results

def main():
    parser = argparse.ArgumentParser(
        description="CombatBalancer CLI Runner - A D&D Encounter Simulation Tool"
    )
    parser.add_argument(
        "--encounter",
        required=True,
        help="Path to the encounter configuration file (YAML/JSON)."
    )
    parser.add_argument(
        "--party",
        required=True,
        help="Path to the party configuration file (YAML/JSON)."
    )
    parser.add_argument(
        "--terrain",
        help="Path to the terrain configuration file (YAML/JSON). Optional."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Increase output verbosity for debugging."
    )
    
    args = parser.parse_args()
    
    try:
        encounter_config = load_config_file(args.encounter)
        party_config = load_config_file(args.party)
        terrain_config = load_config_file(args.terrain) if args.terrain else None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Combine the separate configuration files into a unified configuration.
    unified_config = {
        "encounter": encounter_config,
        "party": party_config,
        "terrain": terrain_config,
    }
    
    if args.verbose:
        print("Encounter Config:")
        print(encounter_config)
        print("\nParty Config:")
        print(party_config)
        if terrain_config:
            print("\nTerrain Config:")
            print(terrain_config)
    
    results = run_simulation(unified_config)
    
    print("\nSimulation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()