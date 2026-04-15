import neat
import os
import time
import pyautogui
import threading
from bridge import GameBridge
from actions import perform_action
from fitness import compute_fitness
from reset import reset_to_start

# How long each genome gets to run (in seconds)
RUN_DURATION = 10

def eval_genome(genome, config, bridge):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    state_history = []
    start_time = time.time()
    frame_count = 0

    while time.time() - start_time < RUN_DURATION:
        state = bridge.get_state()
        if state is None:
            continue  # Don't break, just skip this frame

        if frame_count % 5 == 0:
            inputs = (
                state['x'],
                state['y'],
                state['vx'],
                state['vy'],
                float(state['onGround']),
                float(state['jumping']),
                float(state['dashing']),
            )
            output = net.activate(inputs)

            t = threading.Thread(target=perform_action, args=(output,))
            t.daemon = True
            t.start()

        state_history.append(state)
        frame_count += 1

        if state['health'] <= 0:
            break

    elapsed_time = time.time() - start_time
    return compute_fitness(state_history, elapsed_time)


def eval_genomes(genomes, config, bridge):
    """Evaluate all genomes in the current generation."""
    for genome_id, genome in genomes:
        print(f"  Evaluating genome {genome_id}...")

        # Wait for user to reset the knight to start position
        reset_to_start()
        time.sleep(0.5)  # Give the game a moment to settle

        genome.fitness = eval_genome(genome, config, bridge)
        print(f"    Fitness: {genome.fitness:.2f}")


def run():
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    checkpoint_dir = os.path.join(os.path.dirname(__file__), 'checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_prefix = os.path.join(checkpoint_dir, 'neat-checkpoint-')

    # Restore from last checkpoint if one exists
    checkpoints = [f for f in os.listdir(checkpoint_dir) if f.startswith('neat-checkpoint-')]
    if checkpoints:
        latest = max(checkpoints, key=lambda f: int(f.split('-')[-1]))
        latest_path = os.path.join(checkpoint_dir, latest)
        print(f"Restoring from checkpoint: {latest_path}")
        population = neat.Checkpointer.restore_checkpoint(latest_path)
    else:
        print("No checkpoint found, starting fresh.")
        population = neat.Population(config)

    # Reporters
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Save a checkpoint every generation
    population.add_reporter(neat.Checkpointer(
        generation_interval=1,
        filename_prefix=checkpoint_prefix
    ))

    # Connect to game
    bridge = GameBridge()
    print("Launch Hollow Knight and load your save, then press Enter...")
    input()
    bridge.connect()

    # Run NEAT
    winner = population.run(
        lambda genomes, config: eval_genomes(genomes, config, bridge),
        n=100
    )

    print(f"\nBest genome: {winner}")
    bridge.close()


if __name__ == '__main__':
    run()