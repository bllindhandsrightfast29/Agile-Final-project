#!/usr/bin/env python3
"""
Ninja Animal Character Manager
A 2D NES-style character management system with Naruto-themed combat and pentesting abilities
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class PentestPhase(Enum):
    """Pentesting phases mapped to Naruto mission phases"""
    RECONNAISSANCE = "reconnaissance"  # Information Gathering (Like scouting missions)
    SCANNING = "scanning"              # Active probing (Like sensory ninja detection)
    EXPLOITATION = "exploitation"      # Breaking in (Like infiltration jutsu)
    PRIVILEGE_ESCALATION = "privilege_escalation"  # Gaining higher access (Like power-ups)
    PERSISTENCE = "persistence"        # Maintaining access (Like summoning contracts)
    COVER_TRACKS = "cover_tracks"      # Hiding evidence (Like stealth techniques)


@dataclass
class NinjaAnimal:
    """Represents a Ninja Animal character with pentesting abilities"""
    name: str
    animal_type: str
    rank: str
    description: str
    appearance: Dict
    combat_style: str
    pentesting_abilities: Dict
    jutsu_list: List[Dict]
    stats: Dict

    def display_stats(self) -> str:
        """Display character stats in retro ASCII format"""
        stat_bar = "=" * 50
        output = f"\n{stat_bar}\n"
        output += f"  {self.name.upper()}\n"
        output += f"  {self.animal_type} - {self.rank}\n"
        output += f"{stat_bar}\n\n"

        output += f"Description: {self.description}\n\n"
        output += f"Combat Style: {self.combat_style}\n\n"

        output += "STATS:\n"
        for stat, value in self.stats.items():
            bar_length = value // 10
            bar = "█" * bar_length + "░" * (10 - bar_length)
            output += f"  {stat.upper():<12} [{bar}] {value}\n"

        return output

    def display_jutsu(self) -> str:
        """Display all jutsu techniques"""
        output = f"\n=== {self.name}'s Jutsu List ===\n\n"
        for i, jutsu in enumerate(self.jutsu_list, 1):
            output += f"{i}. {jutsu['name']} ({jutsu['type']})\n"
            output += f"   {jutsu['description']}\n"
            output += f"   Chakra Cost: {jutsu['chakra_cost']}\n"
            output += f"   Pentesting Technique: {jutsu['pentesting_equivalent']}\n\n"
        return output

    def display_pentesting_abilities(self) -> str:
        """Display pentesting abilities"""
        output = f"\n=== {self.name}'s Pentesting Arsenal ===\n\n"
        for ability_type, ability in self.pentesting_abilities.items():
            output += f"  {ability_type.upper()}: {ability}\n"
        return output


class CharacterManager:
    """Manages the ninja animal character roster"""

    def __init__(self, characters_file: str = "characters.json"):
        """Load characters from JSON file"""
        self.characters_file = characters_file
        self.characters: Dict[str, NinjaAnimal] = {}
        self.load_characters()

    def load_characters(self):
        """Load characters from JSON file into character objects"""
        try:
            with open(self.characters_file, 'r') as f:
                data = json.load(f)

            for char_id, char_data in data.get("ninja_animals", {}).items():
                self.characters[char_id] = NinjaAnimal(
                    name=char_data["name"],
                    animal_type=char_data["animal_type"],
                    rank=char_data["rank"],
                    description=char_data["description"],
                    appearance=char_data["appearance"],
                    combat_style=char_data["combat_style"],
                    pentesting_abilities=char_data["pentesting_abilities"],
                    jutsu_list=char_data["jutsu_list"],
                    stats=char_data["stats"]
                )

            print(f"✓ Loaded {len(self.characters)} ninja animal characters!")

        except FileNotFoundError:
            print(f"Error: {self.characters_file} not found!")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    def list_all_characters(self) -> str:
        """List all available characters"""
        output = "\n" + "="*60 + "\n"
        output += "  NINJA ANIMAL SUMMONING ROSTER\n"
        output += "  2D NES World - Pentesting Division\n"
        output += "="*60 + "\n\n"

        for char_id, char in self.characters.items():
            output += f"  [{char_id}]\n"
            output += f"    {char.name} - {char.animal_type}\n"
            output += f"    Rank: {char.rank}\n"
            output += f"    Specialty: {char.pentesting_abilities.get('primary', 'Unknown')}\n"
            output += "\n"

        return output

    def get_character(self, char_id: str) -> Optional[NinjaAnimal]:
        """Get a specific character by ID"""
        return self.characters.get(char_id)

    def filter_by_rank(self, rank: str) -> List[NinjaAnimal]:
        """Filter characters by rank"""
        return [char for char in self.characters.values() if char.rank == rank]

    def filter_by_pentest_ability(self, ability: str) -> List[NinjaAnimal]:
        """Filter characters by pentesting ability"""
        results = []
        for char in self.characters.values():
            if ability.lower() in str(char.pentesting_abilities).lower():
                results.append(char)
        return results

    def display_team_composition(self, char_ids: List[str]) -> str:
        """Display a team composition analysis"""
        output = "\n" + "="*60 + "\n"
        output += "  TEAM COMPOSITION ANALYSIS\n"
        output += "="*60 + "\n\n"

        team = [self.characters[cid] for cid in char_ids if cid in self.characters]

        if not team:
            return "No valid characters in team!\n"

        # Analyze team stats
        total_stats = {
            "health": 0,
            "chakra": 0,
            "attack": 0,
            "defense": 0,
            "speed": 0,
            "intelligence": 0
        }

        output += "Team Members:\n"
        for char in team:
            output += f"  • {char.name} ({char.animal_type}) - {char.rank}\n"
            for stat, value in char.stats.items():
                total_stats[stat] += value

        output += f"\nTeam Size: {len(team)}\n"
        output += "\nCombined Stats:\n"
        for stat, value in total_stats.items():
            output += f"  {stat.upper():<12}: {value}\n"

        output += "\nCombined Abilities:\n"
        abilities_set = set()
        for char in team:
            for ability in char.pentesting_abilities.values():
                abilities_set.add(ability)

        for ability in sorted(abilities_set):
            output += f"  • {ability}\n"

        return output


def main():
    """Main CLI interface"""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█  NINJA ANIMAL CHARACTER MANAGER - 2D NES EDITION  █".center(60))
    print("█  Pentesting Techniques x Naruto Combat Style     █".center(60))
    print("█" + " "*58 + "█")
    print("█"*60 + "\n")

    manager = CharacterManager()

    # Display all characters
    print(manager.list_all_characters())

    # Example: Display a specific character
    print("\n" + "="*60)
    print("  FEATURED CHARACTER")
    print("="*60)

    gambit = manager.get_character("toad_sage")
    if gambit:
        print(gambit.display_stats())
        print(gambit.display_pentesting_abilities())
        print(gambit.display_jutsu())

    # Example team composition
    print("\n" + "="*60)
    print("  SAMPLE PENTESTING TEAM")
    print("="*60)

    team = ["toad_sage", "snake_infiltrator", "hawk_scanner", "dog_tracker"]
    print(manager.display_team_composition(team))

    # Filter by rank
    print("\n" + "="*60)
    print("  S-RANK CHARACTERS")
    print("="*60 + "\n")

    s_rank = manager.filter_by_rank("S-Rank")
    for char in s_rank:
        print(f"  • {char.name} - {char.pentesting_abilities['ultimate']}")

    print("\n")


if __name__ == "__main__":
    main()
