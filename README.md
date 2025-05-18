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
