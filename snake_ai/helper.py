import matplotlib
import matplotlib.pyplot as plt
from IPython import display

plt.ion()
matplotlib.use('TkAgg')


def plot(rewards, mean_rewards):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Reward')
    plt.plot(rewards)
    plt.plot(mean_rewards)
    plt.ylim(ymin=0)
    plt.text(len(rewards) - 1, rewards[-1], str(rewards[-1]))
    plt.text(len(mean_rewards)-1, mean_rewards[-1], str(mean_rewards[-1]))
    plt.show(block=False)
    plt.pause(.1)
