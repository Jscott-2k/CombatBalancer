#!/usr/bin/env python3
import argparse
import yaml
import sys
import os

def load_yaml_file(path):
    """Loads a YAML configuration file."""
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(f"Failed to load YAML file '{path}': {e}")

def load_combatants(config_dir, combatant_ids):
    """Loads combatant configurations given the main config directory and list of IDs."""
    combatants = {}
    combatants_dir = os.path.join(config_dir, "parties", "combatants")
    for cid in combatant_ids:
        path = os.path.join(combatants_dir, f"{cid}.yaml")
        combatant_data = load_yaml_file(path)
        
        # Load abilities
        abilities_id = combatant_data['combatant']['ability_group']
        abilities_path = os.path.join(combatants_dir, "abilities", f"{abilities_id}.yaml")
        abilities_data = load_yaml_file(abilities_path)
        
        combatants[cid] = {
            "details": combatant_data["combatant"],
            "abilities": abilities_data["abilities"]
        }
    return combatants

def run_simulation(config):
    """Stub simulation function. Replace with your actual combat simulation logic."""
    print("Starting simulation with the following configuration:")
    print(config)

    # Dummy simulation results
    return {
        "win_rate": 0.75,
        "average_rounds": 10,
        "character_survival": {"fighter": 0.9, "wizard": 0.6, "cleric": 0.8},
        "balance_rating": "Balanced"
    }

def main():
    parser = argparse.ArgumentParser(
        description="CombatBalancer CLI Runner - D&D Encounter Simulation Tool"
    )

    parser.add_argument("--encounter", required=True, help="Path to encounter YAML file.")
    parser.add_argument("--friendly_party", required=True, help="Path to friendly party YAML file.")
    parser.add_argument("--enemy_party", required=True, help="Path to enemy party YAML file.")
    parser.add_argument("--terrain", help="Path to terrain YAML file.")
    parser.add_argument("--config_dir", default="config", help="Main configuration directory.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")

    args = parser.parse_args()

    try:
        encounter_config = load_yaml_file(args.encounter)
        friendly_party_config = load_yaml_file(args.friendly_party)
        enemy_party_config = load_yaml_file(args.enemy_party)
        terrain_config = load_yaml_file(args.terrain) if args.terrain else None

        # Load combatant details and abilities
        friendly_combatants = load_combatants(args.config_dir, friendly_party_config["party"]["members"])
        enemy_combatants = load_combatants(args.config_dir, enemy_party_config["party"]["members"])

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    unified_config = {
        "encounter": encounter_config,
        "friendly_party": friendly_combatants,
        "enemy_party": enemy_combatants,
        "terrain": terrain_config,
    }

    if args.verbose:
        print(yaml.dump(unified_config, sort_keys=False))

    results = run_simulation(unified_config)

    print("\nSimulation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
