import matplotlib
import matplotlib.pyplot as plt

import os
from pathlib import Path

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
    # The directory containing the files
    folder_path = './model'

    # Convert to Path object for easier manipulation
    folder = Path(folder_path)

    # Get a list of all files in the directory, sorted by modification time
    files = sorted(folder.glob('*'), key=os.path.getmtime)

    # Preserve the first and the newest files
    # First file (oldest by addition)
    first_file = files[0]

    # Newest file (latest by modification)
    newest_file = files[-1]

    # Remove first and newest from the list to delete
    files_to_delete = [f for f in files if f not in (first_file, newest_file)]

    # Delete the files
    for file in files_to_delete:
        os.remove(file)
        print(f"Deleted {file}")

    print(f"Preserved {first_file} and {newest_file}")
