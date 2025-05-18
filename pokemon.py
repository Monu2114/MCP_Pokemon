import random
from mcp.server.fastmcp import FastMCP
import requests
mcp = FastMCP("pokemon")

# Helper function to get evolution chain details



def get_evolution_chain(species_url):
    species_resp = requests.get(species_url)
    if species_resp.status_code != 200:
        return {}
    species_data = species_resp.json()
    evo_chain_url = species_data['evolution_chain']['url']

    evo_resp = requests.get(evo_chain_url)
    if evo_resp.status_code != 200:
        return {}

    evo_chain_data = evo_resp.json()
    evo_chain = []

    def extract_chain(chain):
        evo_chain.append(chain['species']['name'])
        for evo in chain.get('evolves_to', []):
            extract_chain(evo)
    
    extract_chain(evo_chain_data['chain'])
    return evo_chain


@mcp.resource("pokemon://info/{name}")
def get_pokemon(name: str):
    # Fetch main pokemon data
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    res = requests.get(url)
    if res.status_code != 200:
        return {"error": "Pokémon not found"}

    data = res.json()

    # Base stats
    base_stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    
    # Types
    types = [t['type']['name'] for t in data['types']]
    
    # Abilities
    abilities = [a['ability']['name'] for a in data['abilities']]
    
    # Moves with basic info (name and move effect URL)
    moves = []
    for m in data['moves']:
        move_name = m['move']['name']
        move_url = m['move']['url']
    # Fetch move details (optional, can slow down the response)
        move_resp = requests.get(move_url)
        if move_resp.status_code == 200:
            move_data = move_resp.json()
            effect_entries = move_data.get('effect_entries', [])
        # Get English effect description
            effect = next((e['effect'] for e in effect_entries if e['language']['name'] == 'en'), "")
        else:
            effect = ""
        moves.append({"name": move_name, "effect": effect})

    # Get evolution chain from species endpoint
    species_url = data['species']['url']
    evolution_chain = get_evolution_chain(species_url)

    return {
        "name": data['name'],
        "base_stats": base_stats,
        "types": types,
        "abilities": abilities,
        "moves": moves,
        "evolution_chain": evolution_chain
    }

# Type effectiveness (simplified)
type_chart = {
    ("fire", "grass"): 2.0,
    ("water", "fire"): 2.0,
    ("grass", "water"): 2.0,
    ("fire", "water"): 0.5,
    ("water", "grass"): 0.5,
    ("grass", "fire"): 0.5,
}


# Status effects impact
status_effects = ["paralysis", "burn", "poison", None]

# Get basic Pokémon stats and types
def get_pokemon_data(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()

    # We take first type only for simplicity
    poke_type = data['types'][0]['type']['name']

    stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
    return {
        "name": data['name'],
        "hp": stats['hp'],
        "attack": stats['attack'],
        "defense": stats['defense'],
        "speed": stats['speed'],
        "type": poke_type
    }

# Simple damage formula: ((2*Level/5 + 2)*Power*Attack/Defense)/50 + 2)*Modifier
# We'll fix Level=50, Power=50 (standard for moves)
def calculate_damage(attacker, defender, status_attacker):
    level = 50
    power = 50
    attack = attacker['attack']
    defense = defender['defense']
    base = ((2*level/5 + 2) * power * attack / defense) / 50 + 2

    # Type effectiveness
    modifier = type_chart.get((attacker['type'], defender['type']), 1.0)

    # Status effects modifying damage
    if status_attacker == "burn":
        base *= 0.5  # Burn halves attack damage

    damage = int(base * modifier)
    return max(1, damage)  # minimum 1 damage

# Apply status effect consequences at the end of defender's turn
def apply_status(status, hp):
    if status == "poison":
        hp -= 10  # poison damage per turn
    return hp

# Paralysis can cause skip turn; return True if can attack
def can_attack(status):
    if status == "paralysis" and random.random() < 0.25:
        return False
    return True

@mcp.tool("pokemon://battle")
def simulate_battle(pokemon1: str, pokemon2: str):
    p1 = get_pokemon_data(pokemon1)
    p2 = get_pokemon_data(pokemon2)

    if not p1 or not p2:
        return {"error": "One or both Pokémon not found."}

    # Randomly assign status effects (can be None)
    p1_status = random.choice(status_effects)
    p2_status = random.choice(status_effects)

    hp_map = {p1['name']: p1['hp'], p2['name']: p2['hp']}
    status_map = {p1['name']: p1_status, p2['name']: p2_status}

    log = [
        f"{p1['name']} status: {p1_status or 'none'}",
        f"{p2['name']} status: {p2_status or 'none'}"
    ]

    # Determine turn order based on speed
    if p1['speed'] >= p2['speed']:
        turn_order = [p1, p2]
    else:
        turn_order = [p2, p1]

    # Battle loop
    while hp_map[p1['name']] > 0 and hp_map[p2['name']] > 0:
        for attacker in turn_order:
            defender = p1 if attacker == p2 else p2
            att_name = attacker['name']
            def_name = defender['name']

            if hp_map[att_name] <= 0 or hp_map[def_name] <= 0:
                break  # battle over

            # Check if attacker can move (paralysis)
            if not can_attack(status_map[att_name]):
                log.append(f"{att_name} is paralyzed and couldn't move!")
                # Still apply poison damage to attacker at end of their turn
                hp_map[att_name] = apply_status(status_map[att_name], hp_map[att_name])
                if hp_map[att_name] <= 0:
                    log.append(f"{att_name} fainted from status effects!")
                    log.append(f"{def_name} wins!")
                    return {"log": log}
                continue

            # Calculate damage
            damage = calculate_damage(attacker, defender, status_map[att_name])
            hp_map[def_name] -= damage
            log.append(f"{att_name} attacks {def_name} for {damage} damage!")

            # Check if defender fainted
            if hp_map[def_name] <= 0:
                log.append(f"{def_name} fainted! {att_name} wins!")
                return {"log": log}

            # Apply status damage to defender at end of turn
            hp_map[def_name] = apply_status(status_map[def_name], hp_map[def_name])
            if status_map[def_name] == "poison":
                log.append(f"{def_name} is hurt by poison! -10 HP")

            if hp_map[def_name] <= 0:
                log.append(f"{def_name} fainted from status effects! {att_name} wins!")
                return {"log": log}

    return {"log": log}

if __name__ == "__main__":
    mcp.run(transport="tcp", host="127.0.0.1", port=12345)

