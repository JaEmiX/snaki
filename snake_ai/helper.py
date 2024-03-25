import matplotlib
import matplotlib.pyplot as plt

import os
from pathlib import Path

from snake_ai.json_manager import read_data, update_data_record_model
from snake_ai.record_model import RecordModel

plt.ion()
matplotlib.use('TkAgg')


def plot(rewards, mean_rewards):
    plt.clf()  # Clear the current figure
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Reward')
    plt.plot(rewards, label='Rewards')
    plt.plot(mean_rewards, label='Mean Rewards')
    plt.ylim(ymin=0)
    plt.text(len(rewards) - 1, rewards[-1], str(rewards[-1]))
    plt.text(len(mean_rewards) - 1, mean_rewards[-1], str(mean_rewards[-1]))
    plt.legend()
    plt.show(block=False)  # Show the plot without blocking the rest of the script
    plt.pause(0.02)  # Pause briefly to update the plot


def cleanup_models():
    list_of_best_models = read_data().record_models

    max_record = read_data().record

    files_to_delete = []

    for best_model in list_of_best_models:
        if best_model['record'] < max_record:
            files_to_delete.append(best_model['model_name'])

    max_reward = 0

    for best_model in list_of_best_models:
        if best_model['reward'] > max_reward and best_model['record'] == max_record:
            max_reward = best_model['reward']

    for best_model in list_of_best_models:
        if best_model['reward'] < max_reward and best_model['record'] == max_record:
            files_to_delete.append(best_model['model_name'])

    # Delete the files
    for file in files_to_delete:
        os.remove(file)
        print(f"Deleted {file}")

    best_model_list = [m for m in list_of_best_models if m['model_name'] not in files_to_delete]
    update_data_record_model(best_model_list)

    print(f"Preserved {list_of_best_models[0]} list with len {len(list_of_best_models)}")
