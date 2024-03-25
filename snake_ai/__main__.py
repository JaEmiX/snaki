# main.py
import argparse
import json

import os
import sys

from snake_ai.game import SnakeGameAI
from snake_ai.agent import Agent
from snake_ai.helper import plot, cleanup_models
from snake_ai.json_manager import read_data, add_data_epoch, update_data_record

# Parsing the command-line arguments for the configuration file
parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, required=True, help='Path to the config file.')
args = parser.parse_args()

# Loading the config file
with open(args.config, 'r') as config_file:
    config = json.load(config_file)


def main():
    maxRecord = read_data().record
    epoch = read_data().epoch
    reward_all_steps_in_one_game = 0
    plot_reward = []
    plot_mean_rewards = []
    total_reward = 0
    highscore = 0
    agent = Agent()

    # load the last file if exists
    if config['use_last_model']:
        agent.load_latest_model()

    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done, score)
        agent.remember(state_old, final_move, reward, state_new, done, score)

        reward_all_steps_in_one_game += reward

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory(score)

            if score >= highscore:
                highscore = score
                agent.model.save(highscore, reward_all_steps_in_one_game)

            if score > 0:
                print('Game', agent.n_games, 'Score', score, 'Highscore:', highscore)

            plot_reward.append(reward_all_steps_in_one_game)
            total_reward += reward_all_steps_in_one_game
            mean_rewards = total_reward / agent.n_games
            plot_mean_rewards.append(mean_rewards)
            plot(plot_reward, plot_mean_rewards)

            reward_all_steps_in_one_game = 0

            if epoch > 5000:
                shutdown_program()

            if agent.n_games > 750 or highscore > maxRecord:
                if highscore > maxRecord:
                    update_data_record(highscore)

                add_data_epoch(1)
                restart_program()


def shutdown_program():
    sys.exit(0)


def restart_program():
    """Restarts the current program, with file objects and descriptors

    """
    cleanup_models()

    try:
        # This does not work within the PyCharm debugger, only when run normally
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print('Failed to restart:', e)


if __name__ == '__main__':
    main()
