from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("PokemonDataResource")

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


@mcp.resource("pokemon://{name}")
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

if __name__ == "__main__":
    mcp.run()
