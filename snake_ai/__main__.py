# main.py
from snake_ai.constants import USE_LAST_MODEL
from snake_ai.game import SnakeGameAI
from snake_ai.agent import Agent
from snake_ai.helper import plot


def main():
    reward_all_steps = 0
    plot_reward = []
    plot_mean_rewards = []
    total_reward = 0
    record = 0
    agent = Agent()

    # load the last file if exists
    if USE_LAST_MODEL:
        agent.load_latest_model()

    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done, score)

        reward_all_steps += reward

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory(score)

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_reward.append(reward_all_steps)
            total_reward += reward_all_steps
            mean_rewards = total_reward / agent.n_games
            plot_mean_rewards.append(mean_rewards)
            plot(plot_reward, plot_mean_rewards)

            reward_all_steps = 0


if __name__ == '__main__':
    main()
