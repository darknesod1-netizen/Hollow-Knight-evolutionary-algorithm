# Hollow Knight — Evolutionary Algorithm Agent

## About
This project was developed as part of the Nature Inspired Computing course at 
Innopolis University. The goal is to train an AI agent to autonomously complete 
King's Pass, the opening area of the game Hollow Knight, using a NEAT 
(NeuroEvolution of Augmenting Topologies) evolutionary algorithm.

## How It Works
The agent interacts with the game through a custom mod written in C#, which reads 
the Knight's game state every few frames — including position, velocity, and health 
— and broadcasts it over a local TCP socket to a Python process. The Python side 
runs a NEAT algorithm that evolves neural networks, where each network receives the 
game state as input and outputs a set of actions (move left, move right, jump, dash, 
attack). These actions are sent back to the game as simulated keypresses.

Fitness is evaluated using a multi-phase checkpoint system designed around King's 
Pass's layout. The level requires the agent to first move right, then climb upward, 
navigate a fork, and finally reach the exit door. Each phase rewards the most 
relevant movement — horizontal progress early on, then vertical progress during the 
climb, and a combination of both near the end. A speed bonus is also applied for 
agents that complete the level faster.

## Project Structure
- `mod/` — C# Hollow Knight mod that exports game state over TCP
- `evolutionary_algorithm/` — Python NEAT implementation and fitness logic
- `evolutionary_algorithm/config.txt` — NEAT hyperparameters
- `evolutionary_algorithm/bridge.py` — TCP communication with the mod
- `evolutionary_algorithm/actions.py` — Keyboard input simulation
- `evolutionary_algorithm/fitness.py` — Multi-phase fitness function
- `evolutionary_algorithm/main.py` — Main training loop

## Setup
1. Own Hollow Knight on Steam and install version `1.5.78.11833` via the Betas tab
2. Install Scarab mod manager and use it to install DebugMod and Benchwarp
3. Build the mod in `/mod` and copy the DLL to your HK mods folder
4. Install Python dependencies: `py -m pip install neat-python pyautogui`
5. Launch Hollow Knight, load a King's Pass save, then run `py main.py`

## Authors
- Daniil Ostrovskij
- Alisa Rabover
- Denis Bordiugov