# main.py
from snake_ai.game import SnakeGameAI
from snake_ai.agent import Agent
from snake_ai.helper import plot


def main():
    reward_all_steps = 0
    plot_scores = []
    plot_mean_scores = []
    plot_reward = []
    plot_mean_rewards = []
    total_reward = 0
    total_score = 0
    record = 0
    agent = Agent()

    # load the last file if exists
    # agent.load_latest_model()

    game = SnakeGameAI()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        reward_all_steps += reward

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            plot_reward.append(reward_all_steps)
            total_reward += reward_all_steps
            total_score += score
            mean_score = total_score / agent.n_games
            mean_rewards = total_reward / agent.n_games
            plot_mean_scores.append(mean_score)
            plot_mean_rewards.append(mean_rewards)
            plot(plot_reward, plot_mean_rewards)

            reward_all_steps = 0

if __name__ == '__main__':
    main()
