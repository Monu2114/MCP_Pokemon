# Pokémon MCP Server

## Project Overview

This project implements a Pokémon MCP (Model Context Protocol) server and client tools that provide:

- **Pokémon Data Resource:** Fetch detailed Pokémon information including stats, types, abilities, moves, and evolution chain from the public PokéAPI.
- **Battle Simulation Tool:** Simulates a simple battle between two Pokémon with status effects and type effectiveness.

The server exposes these features via the MCP protocol, and a client can call the resource and the tool.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher installed
- Internet connection (to fetch data from the PokéAPI)
- `requests` library for HTTP requests

### Install dependencies

Run this command to install necessary packages:

```bash
pip install -r requirements.txt
Running the Server
Open a terminal and navigate to the project directory.

Run the server script (pokemon_mcp.py) with TCP transport:

bash
Copy
Edit
python pokemon_mcp.py
This will start the MCP server on localhost at port 12345.

Running the Client
Open another terminal in the same directory.

Run your client script (pokemon_client.py) to call the server resources, for example:

bash
Copy
Edit
python pokemon_client.py
This client script connects to the server and fetches Pokémon info or simulates battles.

Features
Get Pokémon Info:
Request Pokémon details using the resource URL:
pokemon://info/{pokemon_name}
Example: pokemon://info/pikachu

Simulate Battle:
Use the battle tool to simulate a battle between two Pokémon:
pokemon://battle?pokemon1={name1}&pokemon2={name2}

Example Usage
In the client code:

python
Copy
Edit
from mcp.client.fastmcp import FastMCP

client = FastMCP("pokemon", transport="tcp", host="127.0.0.1", port=12345)

# Get info about Pikachu
result = client.call("pokemon://info/pikachu")
print(result)

# Simulate battle between Pikachu and Bulbasaur
battle_result = client.call("pokemon://battle", pokemon1="pikachu", pokemon2="bulbasaur")
print(battle_result)
Troubleshooting
Ensure the server is running before executing the client script.

Confirm that both server and client use the same host and port.

If you get connection errors, check firewall or network settings.

Check Python version and installed packages.

Project Files
pokemon_mcp.py — MCP server implementation

pokemon_client.py — Example client script to test server

requirements.txt — Python dependencies list

README.md — This documentation file

Final Notes
This project uses public PokéAPI endpoints for live data and simulates basic battle logic with type effectiveness and status effects.

yaml
Copy
Edit

---

### `requirements.txt`

requests
fastmcp

yaml
Copy
Edit

---

If you want, I can also help format the client script and server script or guide you on how to run them properly. Let me know!






You said:
even the last ones give in that readme format


ChatGPT said:
Got it! Here’s the full README with everything neatly formatted including the troubleshooting, project files, and final notes—all ready for your README.md:

markdown
Copy
Edit
# Pokémon MCP Server

## Project Overview

This project implements a Pokémon MCP (Model Context Protocol) server and client tools that provide:

- **Pokémon Data Resource:** Fetch detailed Pokémon information including stats, types, abilities, moves, and evolution chain from the public PokéAPI.
- **Battle Simulation Tool:** Simulates a simple battle between two Pokémon with status effects and type effectiveness.

The server exposes these features via the MCP protocol, and a client can call the resource and the tool.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher installed  
- Internet connection (to fetch data from the PokéAPI)  
- `requests` library for HTTP requests

### Install dependencies

Run this command to install necessary packages:

```bash
pip install -r requirements.txt
Running the Server
Open a terminal and navigate to the project directory.

Run the server script (pokemon_mcp.py) with TCP transport:

bash
Copy
Edit
python pokemon_mcp.py
This will start the MCP server on localhost at port 12345.

Running the Client
Open another terminal in the same directory.

Run your client script (pokemon_client.py) to call the server resources, for example:

bash
Copy
Edit
python pokemon_client.py
This client script connects to the server and fetches Pokémon info or simulates battles.

Features
Get Pokémon Info:
Request Pokémon details using the resource URL:
pokemon://info/{pokemon_name}
Example: pokemon://info/pikachu

Simulate Battle:
Use the battle tool to simulate a battle between two Pokémon:
pokemon://battle?pokemon1={name1}&pokemon2={name2}

Example Usage
In the client code:

python
Copy
Edit
from mcp.client.fastmcp import FastMCP

client = FastMCP("pokemon", transport="tcp", host="127.0.0.1", port=12345)

# Get info about Pikachu
result = client.call("pokemon://info/pikachu")
print(result)

# Simulate battle between Pikachu and Bulbasaur
battle_result = client.call("pokemon://battle", pokemon1="pikachu", pokemon2="bulbasaur")
print(battle_result)
Troubleshooting
Ensure the server is running before executing the client script.

Confirm that both server and client use the same host and port.

If you get connection errors, check firewall or network settings.

Check Python version and installed packages.

Project Files

pokemon_mcp.py — MCP server implementation

pokemon_client.py — Example client script to test server

requirements.txt — Python dependencies list

README.md — This documentation file