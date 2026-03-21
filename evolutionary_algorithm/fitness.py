import time

# King's Pass coordinates
START_X = 35.46
START_Y = 11.41

CP1_X = 146.93  # End of first rightward section
CP2_Y = 60.41   # Top of climb 
EXIT_X = 189.40
EXIT_Y = 63.41

# How close the knight needs to be to trigger a checkpoint
CHECKPOINT_THRESHOLD = 1.0

MAX_RUN_TIME = 500.0

def compute_fitness(state_history, elapsed_time):
    """
    Compute fitness for one genome based on its run history.

    Segments:
    - Before CP1: reward max X progress
    - After CP1, before CP2: reward max Y progress
    - After CP2: reward max X + max Y*2 (Y weighted more since there is a fork and the player should take the way to the top)
    - Bonus for reaching the exit
    - Speed bonus: only applied if exit is reached
    """
    if not state_history:
        return 0.0

    max_x = max(s['x'] for s in state_history)
    max_y = max(s['y'] for s in state_history)
    final_state = state_history[-1]

    reached_cp1 = max_x >= CP1_X - CHECKPOINT_THRESHOLD
    reached_cp2 = max_y >= CP2_Y - CHECKPOINT_THRESHOLD
    reached_exit = max_x >= EXIT_X - CHECKPOINT_THRESHOLD

    fitness = 0.0

    if not reached_cp1:
        # Phase 1: just go right
        fitness = max_x - START_X

    elif not reached_cp2:
        # Phase 2: reached CP1, now climb
        fitness = (CP1_X - START_X)
        fitness += (max_y - START_Y) * 1.5

    else:
        # Phase 3: reached top, now X + Y*2
        fitness = (CP1_X - START_X)
        fitness += (CP2_Y - START_Y) * 1.5
        fitness += (max_x - START_X) + (max_y - START_Y) * 2.0

    # Big bonus for reaching the exit
    if reached_exit:
        fitness += 1000.0
        # Speed bonus: more reward for finishing faster
        speed_bonus = 500.0 * (1.0 - elapsed_time / MAX_RUN_TIME)
        fitness += max(0.0, speed_bonus)

    # Penalty for dying
    if final_state['health'] <= 0:
        fitness -= 50.0

    return fitness