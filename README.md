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

## Structure
- `mod/` — C# Hollow Knight mod that exports game state over TCP
- `evolutionary_algorithm/` — Python NEAT implementation and fitness logic
- `evolutionary_algorithm/config.txt` — NEAT hyperparameters
- `evolutionary_algorithm/bridge.py` — TCP communication with the mod
- `evolutionary_algorithm/actions.py` — Keyboard input simulation
- `evolutionary_algorithm/fitness.py` — Multi-phase fitness function
- `evolutionary_algorithm/main.py` — Main training loop

## Setup
Step 1 — Install Hollow Knight
Buy and install Hollow Knight on Steam if not already done.

Step 2 — Switch to the correct game version
1. Right-click Hollow Knight in Steam → Properties
2. Go to Betas tab
3. Select "previous version 1.5.78.11833"
4. Let Steam download the downgrade

Step 3 — Install Scarab
1. Download Scarab from https://github.com/fifty-six/Scarab/releases
2. Run it and let it auto-detect your HK installation
3. Install DebugMod and Benchwarp
4. Launch the game and confirm you see the MOD string in the top left

Step 4 — Clone the repo

git clone https://github.com/darknessd1-netizen/Hollow-Knight-evolutionary-algorithm.git

cd Hollow-Knight-evolutionary-algorithm

Step 5 — Set up the mod
1. Create mod/HKPath.props with your PC's HK path:

<Project>
  <PropertyGroup>
    <HKPath>C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight</HKPath>
  </PropertyGroup>
</Project>

3. Build and install the mod:

cd mod

dotnet build

The post-build event will automatically copy the DLL to your HK mods folder.

Step 6 — Install Python dependencies

py -m pip install neat-python pyautogui

Step 7 — Set up Benchwarp
1. Launch Hollow Knight and load your King's Pass save
2. Enable hotkeys in Benchwarp settings
3. Test that WD while paused warps back to that spot

Step 8 - Set up DebugMod (optional)
1. Launch Hollow Knight and load your King's Pass save
2. In hotkeys for DebugMod set up hotkeys for increasing/decreasing tick rate
3. Enable Invincibility in "Cheats"
4. Increase/decrease tick rate (not faster than x25 than normal or else the algorithm may not send inputs fast enough)
5. Increase/decrease max run time in main.py

Step 8 — Run the algorithm
1. Launch Hollow Knight and load your King's Pass save
2. Open a terminal in the repo folder:
cd evolutionary_algorithm
py main.py
3. Press Enter when prompted and the algorithm will start

## Authors
- Daniil Ostrovskij
- Alisa Rabover
- Denis Bordiugov
