# X position of the checkpoint we want to reach
# We'll update this once we find the actual coordinate in game
CHECKPOINT_X = 100.0

# Starting X position of the Knight in Forgotten Crossroads
START_X = 0.0

def compute_fitness(state_history):
    """
    Compute fitness for one genome based on its run history.
    
    Fitness is based on:
    - Max x position reached (primary goal)
    - Bonus for reaching the checkpoint
    - Penalty for dying
    """
    if not state_history:
        return 0.0

    max_x = max(s['x'] for s in state_history)
    final_state = state_history[-1]

    # Base fitness: how far right did we get?
    fitness = max_x - START_X

    # Big bonus for reaching checkpoint
    if max_x >= CHECKPOINT_X:
        fitness += 1000.0

    # Penalty for dying
    if final_state['health'] <= 0:
        fitness -= 50.0

    return fitness