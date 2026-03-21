import neat
import os
import time
import pyautogui
from bridge import GameBridge
from actions import perform_action
from fitness import compute_fitness
from reset import reset_to_start

# How long each genome gets to run (in seconds)
RUN_DURATION = 500

def eval_genome(genome, config, bridge):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    state_history = []
    start_time = time.time()

    while time.time() - start_time < RUN_DURATION:
        state = bridge.get_state()
        if state is None:
            break

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
        perform_action(output)
        state_history.append(state)

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
    # Load NEAT config
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    # Create population
    population = neat.Population(config)

    # Add reporters so we can see progress
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Connect to the game
    bridge = GameBridge()
    print("Launch Hollow Knight and load your save, then press Enter...")
    input()
    bridge.connect()

    # Run NEAT
    winner = population.run(
        lambda genomes, config: eval_genomes(genomes, config, bridge),
        n=100  # number of generations
    )

    print(f"\nBest genome: {winner}")
    bridge.close()


if __name__ == '__main__':
    run()